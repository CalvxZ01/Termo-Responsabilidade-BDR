# 📄 Termo de Responsabilidade Automático

> Sistema automatizado para coleta de aceite de termo de responsabilidade de equipamentos.
> Simples, seguro e integrado ao ambiente Windows.

---

## 🎯 O que ele faz?
Este programa exibe uma tela de **Termo de Responsabilidade** assim que o colaborador faz login no computador.

- ✅ **Bloqueia a tela** até o aceite.
- ✅ **Captura dados automaticamente** (Nome, E-mail, Máquina, Serial).
- ✅ **Gera um PDF assinado** digitalmente com os dados.
- ✅ **Envia para a nuvem** (SharePoint) e notifica no **Teams**.
- ✅ **Inteligente:** Se o usuário já aceitou nesta máquina, o termo não aparece de novo.

---

## � Como Instalar (Via Pen Drive)

Para instalar em um novo computador, você não precisa saber programação. Basta ter o Pen Drive preparado.

### 1. Prepare o Pen Drive
Coloque os seguintes arquivos na raiz do Pen Drive:
- `TermoBDR.exe` (O programa principal)
- `instalar_termo.bat` (O instalador automático)
- `logo_bdr.png` (A logo da empresa)
- `TAHOMA.TTF` (Fonte opcional, se tiver)

### 2. Instale no Computador
1. Conecte o Pen Drive no computador de destino.
2. Clique com o botão direito no arquivo **`instalar_termo.bat`**.
3. Escolha a opção **"Executar como Administrador"**.
4. Aguarde a mensagem de "SUCESSO".

Pronto! Na próxima vez que qualquer pessoa entrar nessa máquina, o termo aparecerá.

---

## 🛠️ Como Atualizar o Código (Para TI)

Se você alterou o código Python (`TERMO BDR.py`) e precisa gerar uma nova versão do executável:

1. Abra a pasta do projeto.
2. Dê dois cliques no arquivo **`compilar.bat`**.
3. Aguarde o processo terminar.
4. O novo `TermoBDR.exe` será criado na pasta principal, pronto para ser copiado para o Pen Drive.

---

## 📂 Onde ficam os arquivos?

### No computador do usuário:
- **Instalação:** `C:\Arquivos de Programas\TermoBDR\`
- **Registro de Aceite:** `C:\ProgramData\TermoBDR\aceites.json`
- **PDF Gerado (Backup Local):** `Documentos\TermosAceitos\`

### Na Nuvem (SharePoint):
- O PDF é enviado automaticamente para a pasta configurada no script.

---

## ⚠️ Solução de Problemas Comuns

| Problema | Solução |
|---|---|
| **O termo não abre** | Verifique se o usuário já aceitou antes (apague o arquivo `aceites.json` para testar de novo). |
| **Antivírus bloqueou** | Adicione uma exceção para a pasta `C:\Arquivos de Programas\TermoBDR`. |
| **Erro de "canvasd"** | Use a versão atualizada do `.exe`. |
| **Logo não aparece** | Certifique-se de que o arquivo `logo_bdr.png` estava no Pen Drive na hora da instalação. |

---

### 📞 Suporte
Em caso de dúvidas ou erros, entre em contato com o setor de TI ou mande mensagem para o numero 55+ (65) 9-9979-0737.
**Desenvolvido internamente para BDR.**
