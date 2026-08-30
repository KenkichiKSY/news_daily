#!/bin/bash
# Linux/Mac 用のニュース配信スケジューラー実行スクリプト

echo ""
echo "======================================"
echo "  NEWS DAILY - ニュース要約配信"
echo "======================================"
echo ""

# Python が存在するか確認
if ! command -v python3 &> /dev/null; then
    echo "❌ エラー: Python3 がインストールされていません"
    echo "インストール: brew install python3 (Mac) または sudo apt install python3 (Ubuntu)"
    exit 1
fi

# 必要なライブラリをチェック
python3 -c "import anthropic, requests, schedule" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 必要なライブラリをインストール中..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ エラー: ライブラリのインストールに失敗しました"
        exit 1
    fi
fi

# .env ファイルが存在するか確認
if [ ! -f ".env" ]; then
    echo "❌ エラー: .env ファイルが見つかりません"
    echo "実行: cp .env.example .env"
    exit 1
fi

# メイン実行
echo "🚀 システムを起動中..."
echo ""
python3 main.py

exit $?
