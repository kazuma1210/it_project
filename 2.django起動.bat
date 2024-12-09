@echo off
REM 作業ディレクトリ（D:\sotuken\it_project）に移動
cd /d D:\sotuken\it_project

REM 必要なパッケージのインストール
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM マイグレーションの実行
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM 開発用サーバーを起動
echo Starting the development server...
python manage.py runserver

REM 完了メッセージ
echo Django development server is running.

REM バッチ処理終了
exit
