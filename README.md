# discord-book-recommender

Google Sheets に登録された本のリストから、ユーザーの気分や要望に合わせて本を選書してくれる Discord Bot。

## 📖 目次

- [概要](#-概要)
- [使用イメージ](#-使用イメージ)
- [技術スタック](#-技術スタック)
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
| AI | Anthropic Claude API |
| ホスティング | Northflank |

## 🚀 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/your-username/discord-book-recommender.git
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

### 4. Bot を起動

```bash
python src/main.py
```

## 🔑 環境変数

| 変数名 | 説明 |
|--------|------|
| `DISCORD_TOKEN` | Discord Bot トークン |
| `ANTHROPIC_API_KEY` | Claude API キー |
| `GOOGLE_SHEETS_ID` | 本リストのスプレッドシート ID |
| `GOOGLE_CREDENTIALS_JSON` | サービスアカウント認証情報 (JSON 文字列) |

## 🧑‍💻 開発

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 📦 デプロイ

Northflank Template (`northflank.json`) を使用して GitOps デプロイが可能。

1. Northflank で Template を作成
2. リポジトリを連携
3. Argument overrides でシークレットを設定
4. デプロイ実行

## 📄 ライセンス

MIT License
