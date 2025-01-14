@echo off
REM MySQLのインストールディレクトリ（C:\mysql\bin）に移動
cd /d C:\mysql\bin

REM MySQLサーバーを起動（--consoleオプション付き）
start mysqld --console

REM サーバー起動後に少し待機（例えば5秒間）
timeout /t 5 /nobreak > nul

REM MySQLにログイン（rootユーザーとして、パスワードの入力を促す）
mysql -u root -p

REM 終了後、バッチ処理を終了
exit
