import tkinter as tk
from tkinter import ttk
import csv
import unicodedata
import platform
import subprocess
import datetime
import re
import os
import json
import urllib.request
import urllib.parse
import threading
import time
import sys

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader


# ===================================================================
# CONFIG — agora seguro para GitHub
# ===================================================================

# Tudo sensível agora é variável de ambiente!
# No Windows você configura com:
# setx M365_CLIENT_SECRET "valor"
# setx M365_CLIENT_ID "valor"
# setx M365_TENANT_ID "valor"
# setx TEAMS_WEBHOOK "url"
# setx SP_SITE_HOST "xxx.sharepoint.com"
# setx SP_SITE_PATH "sites/Exemplo"
# setx SP_LIBRARY "Documentos Compartilhados/Termos"

CLIENT_SECRET = os.getenv("M365_CLIENT_SECRET")
CLIENT_ID     = os.getenv("M365_CLIENT_ID")
TENANT_ID     = os.getenv("M365_TENANT_ID")
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

SITE_HOSTNAME = os.getenv("SP_SITE_HOST")
SITE_PATH     = os.getenv("SP_SITE_PATH")
LIB_CAMINHO   = os.getenv("SP_LIBRARY", "TermosAceitos")

APP_DIR = r"C:\TermoBDR"
LOGFILE = os.path.join(APP_DIR, "termo_log.txt")
os.makedirs(APP_DIR, exist_ok=True)

ACEITES_DIR = r"C:\ProgramData\TermoBDR"
ACEITES_FILE = os.path.join(ACEITES_DIR, "aceites.json")
os.makedirs(ACEITES_DIR, exist_ok=True)


# ===================================================================
# LOG
# ===================================================================
def log(msg):
    try:
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}\n")
    except:
        pass


# ===================================================================
# CONTROLE DE ACEITES
# ===================================================================
def carregar_aceites():
    return json.load(open(ACEITES_FILE, "r", encoding="utf-8")) if os.path.exists(ACEITES_FILE) else {}

def salvar_aceites(aceites):
    json.dump(aceites, open(ACEITES_FILE,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

def ja_aceitou_nesta_maquina(email):
    maquina = platform.node()
    aceites = carregar_aceites()
    return email.lower() in aceites.get(maquina, {})

def registrar_aceite(email):
    maquina = platform.node()
    aceites = carregar_aceites()
    aceites.setdefault(maquina,{})[email.lower()] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_aceites(aceites)


# ===================================================================
# PDF
# ===================================================================
try:
    pdfmetrics.registerFont(TTFont("Tahoma","TAHOMA.TTF"))
    FONT="Tahoma"; FBOLD="Tahoma-Bold"
except:
    FONT="Helvetica"; FBOLD="Helvetica-Bold"

def gerar_pdf(path,payload,termo):
    c = canvas.Canvas(path,pagesize=A4)
    w,h = A4

    try:
        img = ImageReader("logo.png")                  # <<< somente usar imagem se quiser
        c.drawImage(img,40,h-120,width=130,height=50)
    except:
        pass

    c.setFont(FBOLD,15)
    c.drawCentredString(w/2,h-50,"TERMO DE RESPONSABILIDADE - EMPRESA")

    c.setFont(FONT,9)
    c.drawString(40,h-100,f"Nome: {payload['nome']}")
    c.drawString(40,h-115,f"CPF:  {payload['cpf_formatado']}")
    c.drawString(40,h-130,f"E-mail: {payload['email']}")
    c.drawString(40,h-145,f"Data/Hora: {payload['data']}")

    y=h-180
    for linha in termo.split("\n"):
        if y<80: c.showPage(); y=h-60; c.setFont(FONT,9)
        c.drawString(40,y,linha); y-=12

    c.save()


def salvar_pdf_local(payload, termo_texto):
    pasta = os.path.join(os.path.expanduser("~"),"Documents","TermosAceitos")
    os.makedirs(pasta,exist_ok=True)

    nome = payload["nome"].replace("/","-")
    pdf_name = f"Termo BDR - {nome} - {payload['cpf_formatado']}.pdf"
    path = os.path.join(pasta,pdf_name)

    gerar_pdf(path,payload,termo_texto)
    return path


# ===================================================================
# OBTÉM NOME & E-MAIL MICROSOFT 365
# ===================================================================
def obter_usuario_m365():
    try:
        upn=subprocess.check_output(["whoami","/upn"],text=True).strip()
    except: return None

    if "@" not in upn: return None

    prefixo=upn.split("@")[0]
    nome = " ".join([x.capitalize() for x in prefixo.split(".")])
    return {"nome":nome,"email":upn}


# ===================================================================
# UI
# ===================================================================
def mostrar(nome,email,termo):
    root=tk.Tk()
    root.title("Termo")
    root.geometry("1150x720")
    root.attributes("-topmost",True)

    ttk.Label(root,text="TERMO DE RESPONSABILIDADE",font=("Segoe UI",18,"bold")).pack(pady=10)

    caixa=tk.Text(root,wrap="word",font=("Segoe UI",11),height=22)
    caixa.insert("1.0",termo); caixa.configure(state="disabled"); caixa.pack(fill="both",expand=True,padx=10,pady=5)

    ttk.Label(root,text="Nome:").pack(anchor="w",padx=20)
    nome_var=tk.StringVar(value=nome)
    ttk.Entry(root,textvariable=nome_var,width=45,state="readonly").pack(anchor="w",padx=20)

    ttk.Label(root,text="CPF:").pack(anchor="w",padx=20,pady=2)
    cpf_var=tk.StringVar()
    ttk.Entry(root,textvariable=cpf_var,width=20).pack(anchor="w",padx=20)

    ok = tk.BooleanVar()
    ttk.Checkbutton(root,text="Declaro ter lido e concordo.",variable=ok).pack(anchor="w",padx=20,pady=8)

    def aceitar():
        cpf=re.sub(r"\D","",cpf_var.get())
        if len(cpf)!=11: return

        payload={
            "nome":nome,
            "email":email,
            "cpf_formatado":f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
            "data":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        pdf=salvar_pdf_local(payload,termo)
        registrar_aceite(email)
        log(f"Aceito por {email} — PDF salvo em {pdf}")
        root.destroy()

    ttk.Button(root,text="ACEITAR",command=aceitar).pack(pady=15)
    root.mainloop()


# ===================================================================
# MAIN EXECUÇÃO
# ===================================================================
if __name__=="__main__":
    usr=obter_usuario_m365()
    if not usr: sys.exit()

    if ja_aceitou_nesta_maquina(usr["email"]):
        log("Usuário já aceitou — encerrando.")
        sys.exit()

    texto = """
    Termo de responsabilidade...
    (coloque aqui o seu texto real)
    """

    mostrar(usr["nome"],usr["email"],texto)
