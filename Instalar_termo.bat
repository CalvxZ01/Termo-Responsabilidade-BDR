@echo off
chcp 65001 >nul
title Instalar Termo BDR

:: Verifica se está rodando como Administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ========================================================
    echo  ERRO: Este script precisa ser executado como ADMIN.
    echo  Clique com o botão direito e escolha "Executar como Administrador".
    echo ========================================================
    echo.
    pause
    exit
)

echo.
echo ========================================================
echo  Instalando Termo BDR...
echo ========================================================
echo.

:: Define caminhos
set "SOURCE_DIR=%~dp0"
set "INSTALL_DIR=%ProgramFiles%\TermoBDR"
set "STARTUP_DIR=%ProgramData%\Microsoft\Windows\Start Menu\Programs\StartUp"
set "EXE_NAME=TermoBDR.exe"

:: 1. Criar pasta de instalação
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 2. Copiar arquivos para a pasta de instalação (não para o Startup)
echo Copiando arquivos para: "%INSTALL_DIR%"
copy /Y "%SOURCE_DIR%%EXE_NAME%" "%INSTALL_DIR%"
if exist "%SOURCE_DIR%logo_bdr.png" copy /Y "%SOURCE_DIR%logo_bdr.png" "%INSTALL_DIR%" >nul
if exist "%SOURCE_DIR%TAHOMA.TTF" copy /Y "%SOURCE_DIR%TAHOMA.TTF" "%INSTALL_DIR%" >nul
if exist "%SOURCE_DIR%TAHOMABD.TTF" copy /Y "%SOURCE_DIR%TAHOMABD.TTF" "%INSTALL_DIR%" >nul

:: 3. Criar Atalho na pasta de Inicialização
echo Criando atalho na Inicialização...
set "TARGET=%INSTALL_DIR%\%EXE_NAME%"
set "SHORTCUT=%STARTUP_DIR%\TermoBDR.lnk"
set "PWS=powershell.exe -ExecutionPolicy Bypass -NoProfile -NonInteractive -Command"

%PWS% "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%TARGET%'; $s.WorkingDirectory = '%INSTALL_DIR%'; $s.Save()"

:: 4. Limpar bagunça anterior (se houver arquivos soltos no Startup)
echo Limpando arquivos antigos do Startup...
del "%STARTUP_DIR%\TermoBDR.exe" 2>nul
del "%STARTUP_DIR%\logo_bdr.png" 2>nul
del "%STARTUP_DIR%\TAHOMA.TTF" 2>nul
del "%STARTUP_DIR%\TAHOMABD.TTF" 2>nul

echo.
echo ========================================================
echo  SUCESSO! Instalação corrigida.
echo  O programa foi movido para Arquivos de Programas e
echo  apenas um atalho foi criado na inicialização.
echo ========================================================
echo.
pause
