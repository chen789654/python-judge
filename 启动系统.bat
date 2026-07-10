@echo off
chcp 65001 >nul
title Python Judge - 在线评测系统

echo ============================================
echo    Python Judge 在线评测系统 - 启动中...
echo ============================================
echo.

:: 切换到项目目录
cd /d "%~dp0"

:: 检测 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    pause
    exit /b
)

:: 检测依赖是否已安装
pip list 2>nul | findstr "Flask" >nul
if %errorlevel% neq 0 (
    echo [提示] 首次启动，正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b
    )
    echo [完成] 依赖安装成功
)

:: 获取本机局域网 IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*192\.168\."') do set IP=%%a
if "%IP%"=="" (
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*10\."') do set IP=%%a
)
if "%IP%"=="" (
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*172\."') do set IP=%%a
)
:: 去掉前面的空格
set IP=%IP: =%

echo ============================================
echo    系统启动成功！
echo.
echo    本地访问：  http://localhost:5000
echo    局域网访问：http://%IP%:5000
echo.
echo    教师账号：  admin
echo    登录密码：  123456
echo.
echo    请把局域网地址发给学生
echo    关闭此窗口 = 关闭系统
echo ============================================
echo.

:: 启动 Flask
python run.py

pause
