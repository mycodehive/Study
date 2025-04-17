@echo off
goto menu

:: ========== �ܰ� �Լ��� ==========

:step1
echo [1] Python ��ġ ���� �ٿ�ε� ��...
curl -o python-3.10.0-amd64.exe https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe
echo [�Ϸ�] ��ġ ���� �ٿ�ε��.
pause
goto menu

:step2
echo [2] Python ��ġ ��...
start /wait python-3.10.0-amd64.exe /quiet InstallAllUsers=1 TargetDir=C:\Python310 Include_launcher=0 Include_test=0 PrependPath=0
if not exist C:\Python310\python.exe (
    echo [����] Python ��ġ ����!
) else (
    echo [�Ϸ�] Python ��ġ��: C:\Python310
)
pause
goto menu

:step3
echo [3] pip ��ġ �� ���׷��̵� ��...
C:\Python310\python.exe -m ensurepip
C:\Python310\python.exe -m pip install --upgrade pip
echo [�Ϸ�] pip ��ġ��.
pause
goto menu

:step4
echo [4] ����ȯ�� ���� ��...
cd /d %~dp0
C:\Python310\python.exe -m venv guardfall_env
echo [�Ϸ�] ����ȯ�� ������.
pause
goto menu

:step5
echo [5] ����ȯ�� Ȱ��ȭ �� pip upgrade ��ġ ��...
call guardfall_env\Scripts\activate
pip install --upgrade pip
echo [�Ϸ�] Ȱ��ȭ �Ϸ�.
pause
goto menu

:step6
echo [6] ����ȯ�� ��Ȱ��ȭ
call guardfall_env\Scripts\activate
deactivate
pause
goto menu

:: ========== �޴� ==========

:menu
cls
echo =====================================================
echo  GuardFall ȯ�漳�� ������(�����ڸ��� �����ϼ���)
echo =====================================================
echo [1] Python(3.10) ��ġ ���� �ٿ�ε�
echo [2] Python(3.10) ��ġ
echo [3] pip ��ġ �� ���׷��̵�
echo [4] ����ȯ�� ����
echo [5] ����ȯ�� Ȱ��ȭ
echo [6] ����ȯ�� ��Ȱ��ȭ
echo [0] ����
echo ----------------------------------------
set /p choice="������ �ܰ� ��ȣ�� �Է��ϼ��� (0~6): "

if "%choice%"=="1" goto step1
if "%choice%"=="2" goto step2
if "%choice%"=="3" goto step3
if "%choice%"=="4" goto step4
if "%choice%"=="5" goto step5
if "%choice%"=="6" goto step6
if "%choice%"=="0" exit

echo [!] �߸��� �Է��Դϴ�. �ٽ� �����ϼ���.
pause
goto menu
