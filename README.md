# TODOリストアプリケーション

Flaskで作成されたシンプルなTODOリストアプリケーションです。

## 機能

- タスクの追加、編集、削除
- 日付と時間でタスクを管理
- タスクの完了状態の切り替え
- 日付でグループ化された表示

## インストール方法

1. リポジトリをクローン:
```bash
git clone https://github.com/mitsufujiryoh/todo-app.git
cd todo-app
```

2. 仮想環境を作成して有効化:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. 依存パッケージをインストール:
```bash
pip install -r requirements.txt
```

## 実行方法

```bash
python app.py
```

ブラウザで http://127.0.0.1:5000 にアクセスしてください。

## 使用技術

- バックエンド: Flask, SQLAlchemy
- フロントエンド: Bootstrap 5, JavaScript
- データベース: SQLite