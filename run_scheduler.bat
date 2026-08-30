@echo off
REM Windows 用のニュース配信スケジューラー実行ファイル
REM このファイルをダブルクリックして実行します

echo.
echo ====================================
echo    NEWS DAILY - ニュース要約配信
echo ====================================
echo.

REM Python が存在するか確認
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo エラー: Python がインストールされていません
    echo https://www.python.org から Python をインストールしてください
    pause
    exit /b 1
)

REM 必要なライブラリをチェック
python -c "import anthropic, requests, schedule" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 必要なライブラリをインストール中...
    pip install -r requirements.txt
    if %ERRORLEVEL% NEQ 0 (
        echo エラー: ライブラリのインストールに失敗しました
        pause
        exit /b 1
    )
)

REM .env ファイルが存在するか確認
if not exist ".env" (
    echo エラー: .env ファイルが見つかりません
    echo .env.example をコピーして .env を作成してください
    echo.
    echo コマンド: copy .env.example .env
    pause
    exit /b 1
)

REM メイン実行
echo システムを起動中...
echo.
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo エラーが発生しました
    pause
    exit /b 1
)

pause
