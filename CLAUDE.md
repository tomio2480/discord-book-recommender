# Claude Code 向け指示書

このファイルは Claude Code がこのプロジェクトを理解するための指示書である。

## プロジェクト概要

Google Sheets に登録された本のリストから、ユーザーの気分や要望に合わせて本を選書する Discord Bot。

## 技術スタック

- Python 3.11+
- discord.py（Bot フレームワーク）
- gspread（Google Sheets 連携）
- Anthropic Claude API（選書 AI）
- Northflank（ホスティング）

## ディレクトリ構成

```
discord-book-recommender/
├── src/
│   ├── main.py       # エントリーポイント
│   ├── bot.py        # Discord Bot 本体
│   ├── sheets.py     # Google Sheets 読み込み
│   ├── selector.py   # Claude API 選書
│   └── config.py     # 環境変数管理
├── Dockerfile        # コンテナビルド用
├── northflank.json   # Northflank IaC
└── requirements.txt  # 依存パッケージ
```

## 開発時の注意

- テストファースト TDD で開発を進める
- セキュリティを担保すること（環境変数の扱い等）
- 短いソースコードで最低限の機能を実装する
- 不要なコードは削除する
