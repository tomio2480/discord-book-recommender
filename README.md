# discord-book-recommender

Google Sheets に登録された本のリストから、ユーザーの気分や要望に合わせて本を選書してくれる Discord Bot。

## 📖 目次

- [概要](#-概要)
- [使用イメージ](#-使用イメージ)
- [技術スタック](#-技術スタック)
- [対応する本リスト](#-対応する本リスト)
- [セットアップ](#-セットアップ)
- [環境変数](#-環境変数)
- [開発](#-開発)
- [デプロイ](#-デプロイ)
- [ライセンス](#-ライセンス)

## 🎯 概要

自然言語で要望を伝えると、Google Sheets に登録された本の中から 5 冊程度の本をおすすめしてくれる。

## 💬 使用イメージ

```
ユーザー: /選書 今日は雨で憂鬱。でも2時間くらい読書できる。
         現実逃避できて、読後感が良いものがいいな

Bot:     📚 雨の日にぴったりの5冊、選んでみました！

         1. 『かもめ食堂』群ようこ
            → 静かな北欧の空気感が、雨音と合いそう。
              心がほっこりする読後感も◎

         2. 『夜は短し歩けよ乙女』森見登美彦
            → 現実離れした京都の夜の冒険。2時間で
              ちょうど読み切れるボリューム感。
         ...
```

## 🛠 技術スタック

| 要素 | 技術 |
|------|------|
| 言語 | Python 3.11+ |
| Bot フレームワーク | discord.py |
| Sheets 連携 | gspread |
| AI | Google Gemini API |
| ホスティング | Northflank |

## 📚 対応する本リスト

このBotは [Libra Mate](https://play.google.com/store/apps/details?id=com.apps.hal.libramate&hl=ja) からエクスポートした Google Sheets に対応している。

Libra Mate は書籍管理アプリで、蔵書を Google Sheets に出力できる。このアプリを利用している人であれば、同じ仕組みを構築できる。

### 必要なカラム

| カラム名 | 説明 | 必須 |
|----------|------|------|
| タイトル | 本のタイトル | 必須 |
| 著者名 | 著者 | 必須 |
| 出版社 | 出版社名 | 任意 |
| 商品説明 | 本の説明文 | 任意 |
| 既読フラグ | 読了済みかどうか | 任意 |
| 削除フラグ | TRUE の場合は除外 | 任意 |
| メモ | 自由記述 | 任意 |

## 🚀 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/tomio2480/discord-book-recommender.git
cd discord-book-recommender
```

### 2. 依存パッケージをインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

```bash
cp .env.example .env
# .env を編集して各種トークン・認証情報を設定
```

### 4. Google Sheets のサービスアカウント設定

1. [Google Cloud Console](https://console.cloud.google.com/) でプロジェクトを作成
2. Google Sheets API を有効化
3. サービスアカウントを作成し、JSON キーをダウンロード
4. JSON キーの内容を 1 行にして `GOOGLE_CREDENTIALS_JSON` に設定
5. サービスアカウントのメールアドレスをスプレッドシートに共有

### 5. Bot を起動

```bash
python src/main.py
```

## 🔑 環境変数

| 変数名 | 説明 |
|--------|------|
| `DISCORD_TOKEN` | Discord Bot トークン（[Discord Developer Portal](https://discord.com/developers/applications) で取得） |
| `GEMINI_API_KEY` | Gemini API キー（[Google AI Studio](https://aistudio.google.com/) で取得） |
| `GOOGLE_SHEETS_ID` | スプレッドシートの ID（URL の `/d/` と `/edit` の間の文字列） |
| `GOOGLE_CREDENTIALS_JSON` | サービスアカウント認証情報（JSON を 1 行にしたもの） |

## 🧑‍💻 開発

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 📦 デプロイ

Northflank を使用してデプロイする。GitHub 連携を設定すると push 時に自動デプロイされる。

### 手順

1. Northflank でプロジェクトを作成
2. Combined Service を追加し、GitHub リポジトリを連携
3. Environment タブで環境変数を設定
4. デプロイ実行

### Northflank Template

`northflank.json` を使用した GitOps デプロイにも対応している。

## 📄 ライセンス

MIT License
