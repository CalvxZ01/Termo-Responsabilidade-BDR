# Termo de Responsabilidade – Automação de Aceite 📄

Aplicação em Python que exibe um termo de responsabilidade para o usuário no primeiro login da máquina.  
Após o aceite, um PDF é gerado automaticamente com os dados preenchidos e armazenado em **Documentos → TermosAceitos**.

Este projeto foi preparado para uso empresarial, com segurança adequada para publicação pública no GitHub — **nenhuma credencial sensível é armazenada no código.**

---

## 🚀 Funcionalidades

| Função | Status |
|---|---|
| Exibe termo no login do usuário | ✔ |
| Captura nome do colaborador automaticamente (UPN) | ✔ |
| Usuário informa CPF manualmente | ✔ |
| Gera PDF com nome + CPF no formato correto | ✔ |
| Salva localmente com histórico por usuário | ✔ |
| Armazena aceite por máquina (não repete o termo) | ✔ |
| Código seguro para repositório público | ✔ |

---

## 📁 Estrutura de armazenamento

Após aceite, o sistema cria:

C:/
├─ ProgramData/TermoBDR/aceites.json ← controla quem já aceitou
└─ Users/<Usuario>/Documents/TermosAceitos/
└─ Termo BDR - NOME - CPF.pdf ← PDF gerado

yaml
Copiar código

Se o usuário já aceitou, o termo **não aparece novamente**, evitando repetição.

---

## 🔧 Requisitos

| Recurso | Necessário |
|---|---|
| Python 3.10+ | ✔ |
| Bibliotecas externas | reportlab |
| Windows + Microsoft 365 corporativo | ✔ recomendado |

Instalação das dependências:

```bash
pip install reportlab
🔐 Variáveis de Ambiente (opcional)
Se futuramente quiser integrar SharePoint / Teams, basta definir:

bash
Copiar código
setx M365_CLIENT_SECRET "secreto"
setx M365_CLIENT_ID "seu-id"
setx M365_TENANT_ID "tenant"
setx TEAMS_WEBHOOK "webhook"
setx SP_SITE_HOST "empresa.sharepoint.com"
setx SP_SITE_PATH "sites/Setor"
setx SP_LIBRARY "Documentos/TermosAceitos"
Sem isso, o sistema continuará funcionando localmente.

▶ Como executar
bash
Copiar código
python termo.py
Para transformar em .EXE:

bash
Copiar código
pyinstaller --noconsole --onefile "termo.py"
O executável pode ser colocado na pasta:

makefile
Copiar código
C:\TermoBDR\
e configurado para rodar no logon via Política de Grupo / Registro / Agendador.

🏢 Uso corporativo
Pode ser distribuído via GPO, Intune, script PowerShell ou MSI

Executa apenas na primeira vez em cada máquina

Garante rastreabilidade do aceite do colaborador

📄 Licença
Este projeto é aberto para empresas que desejam utilizar ou evoluir internamente.
Credenciais e integrações devem ser configuradas no ambiente da organização.

Mantenedor
Desenvolvido internamente para controle de responsabilidade digital de equipamentos.