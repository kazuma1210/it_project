@echo off
REM --- VSCターミナルを使って MySQL サーバーの起動 ---
REM Visual Studio Code のターミナルを開いて MySQL サーバーを起動

cd /d C:\mysql\bin
start "" "C:\Users\student\AppData\Local\Programs\Microsoft VS Code\Code.exe" --new-window --command "workbench.action.terminal.new" --file-write --args "mysqld --console"

REM --- VSCターミナルを使って Django サーバーの起動 ---
REM プロジェクトディレクトリに移動して Django サーバーを起動

cd /d D:\sotuken\it_project
start "" "C:\Users\student\AppData\Local\Programs\Microsoft VS Code\Code.exe" --new-window --command "workbench.action.terminal.new" --file-write --args "python manage.py runserver"

REM --- VSCターミナルを使って MySQL に自動ログイン ---
REM MySQL に root ユーザーでログイン

cd /d C:\mysql\bin
start "" "C:\Users\student\AppData\Local\Programs\Microsoft VS Code\Code.exe" --new-window --command "workbench.action.terminal.new" --file-write --args "mysql -u root"
