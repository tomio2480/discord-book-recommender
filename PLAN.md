# discord-book-recommender 実装計画書

## 概要

Google Sheets に登録された本のリストから、ユーザーの気分や要望に合わせて本を選書してくれる Discord Bot。

### 機能

- 自然言語で要望を伝えると、5冊程度の本をおすすめしてくれる
- 例: 「今日は雨で憂鬱。2時間くらい読書できる。現実逃避できて読後感が良いものがいい」

### 使用イメージ

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

---

## 技術スタック

| 要素 | 技術 | 理由 |
|------|------|------|
| 言語 | Python 3.11+ | discord.py, gspread が充実 |
| Bot フレームワーク | discord.py | 日本語ドキュメント豊富、軽量 |
| Sheets 連携 | gspread + サービスアカウント | シンプルな API |
| AI | Anthropic Claude API | 自然言語理解に強い |
| ホスティング | Northflank (Free プラン) | 既存 Bot 運用中、GitOps 対応 |
| IaC | Northflank Template (JSON) | 初回セットアップ自動化 |

---

## システム構成

```
┌─────────────┐    メッセージ     ┌─────────────┐
│   Discord   │ ◄──────────────► │  Bot Server │
│   ユーザー   │    選書結果      │  (Python)   │
└─────────────┘                  └──────┬──────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   │
             ┌─────────────┐     ┌─────────────┐           │
             │   Google    │     │  Claude API │           │
             │   Sheets    │     │  (選書AI)   │           │
             │  (本リスト)  │     └─────────────┘           │
             └─────────────┘                               │
```

---

## ディレクトリ構成

```
discord-book-recommender/
├── CLAUDE.md                 # Claude Code 向け指示書
├── PLAN.md                   # この計画書
├── README.md                 # プロジェクト説明
├── requirements.txt          # Python 依存パッケージ
├── Dockerfile                # コンテナビルド用
├── northflank.json           # Northflank Template (IaC)
├── .env.example              # 環境変数テンプレート
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py               # エントリーポイント
│   ├── bot.py                # Discord Bot 本体
│   ├── sheets.py             # Google Sheets 読み込み
│   ├── selector.py           # Claude API で選書
│   └── config.py             # 設定・環境変数管理
└── credentials/
    └── .gitkeep              # サービスアカウント鍵の配置場所（Git管理外）
```

---

## 環境変数・シークレット

| 変数名 | 説明 | 取得元 |
|--------|------|--------|
| `DISCORD_TOKEN` | Discord Bot トークン | Discord Developer Portal |
| `ANTHROPIC_API_KEY` | Claude API キー | Anthropic Console |
| `GOOGLE_SHEETS_ID` | 本リストのスプレッドシート ID | Google Sheets URL から |
| `GOOGLE_CREDENTIALS_JSON` | サービスアカウント認証情報 (JSON) | Google Cloud Console |

---

## 実装フェーズ

### Phase 1: 環境構築・基盤

1. GitHub リポジトリ作成
2. 基本ファイル群の作成 (README, .gitignore, requirements.txt, Dockerfile)
3. CLAUDE.md 作成（Claude Code 向け指示書）

### Phase 2: コア機能実装

4. Google Sheets 読み込み機能 (`sheets.py`)
5. Claude API 選書機能 (`selector.py`)
6. Discord Bot 基本機能 (`bot.py`)
7. エントリーポイント統合 (`main.py`)

### Phase 3: デプロイ準備

8. Northflank Template 作成 (`northflank.json`)
9. Dockerfile 最適化
10. 動作確認・デバッグ

### Phase 4: 改善

11. エラーハンドリング強化
12. キャッシュ機能（Sheets データ）
13. Discord 2000 文字制限対応

---

## GitHub Issues（作成すべき項目）

以下の Issue を機能単位で作成し、順番に解決していく。

### Phase 1: 環境構築・基盤

```markdown
## Issue #1: プロジェクト基盤ファイルの作成
### 概要
プロジェクトの基盤となるファイル群を作成する

### タスク
- [ ] README.md 作成
- [ ] .gitignore 作成
- [ ] requirements.txt 作成
- [ ] .env.example 作成
- [ ] src/ ディレクトリ構成作成

### 完了条件
- 上記ファイルが全て作成されている
- requirements.txt に必要なパッケージが記載されている
```

```markdown
## Issue #2: Dockerfile 作成
### 概要
Northflank でのデプロイ用 Dockerfile を作成する

### タスク
- [ ] マルチステージビルドの Dockerfile 作成
- [ ] 非 root ユーザーでの実行
- [ ] ヘルスチェック対応

### 完了条件
- ローカルで docker build が成功する
- コンテナが正常に起動する
```

### Phase 2: コア機能実装

```markdown
## Issue #3: Google Sheets 読み込み機能
### 概要
gspread を使って Google Sheets から本のリストを取得する

### タスク
- [ ] src/sheets.py 作成
- [ ] サービスアカウント認証の実装
- [ ] 本リスト取得関数の実装
- [ ] エラーハンドリング

### 完了条件
- Google Sheets から本のリストを取得できる
- 認証エラー時に適切なエラーメッセージが出る
```

```markdown
## Issue #4: Claude API 選書機能
### 概要
Anthropic Claude API を使って本を選書するロジックを実装する

### タスク
- [ ] src/selector.py 作成
- [ ] Claude API クライアント初期化
- [ ] 選書用プロンプト設計
- [ ] レスポンスのパース・整形

### 完了条件
- 本リストと要望を渡すと、5冊程度の選書結果が返る
- 各本に推薦理由が付いている
```

```markdown
## Issue #5: Discord Bot 基本機能
### 概要
discord.py を使って Bot の基本機能を実装する

### タスク
- [ ] src/bot.py 作成
- [ ] Bot 初期化・接続処理
- [ ] /選書 スラッシュコマンド実装
- [ ] ローディング表示（「考え中...」）
- [ ] 結果送信

### 完了条件
- Discord でコマンドを実行すると選書結果が返る
- ローディング中の表示がある
```

```markdown
## Issue #6: エントリーポイント統合
### 概要
各モジュールを統合して Bot を起動可能にする

### タスク
- [ ] src/main.py 作成
- [ ] src/config.py 作成（環境変数管理）
- [ ] 各モジュールの統合
- [ ] ローカル動作確認

### 完了条件
- python src/main.py で Bot が起動する
- Discord 上で /選書 コマンドが動作する
```

### Phase 3: デプロイ準備

```markdown
## Issue #7: Northflank Template 作成
### 概要
Northflank の IaC (Infrastructure as Code) テンプレートを作成する

### タスク
- [ ] northflank.json 作成
- [ ] プロジェクト・サービス定義
- [ ] シークレットグループ定義
- [ ] 環境変数のマッピング

### 完了条件
- northflank.json が正しい JSON 形式である
- 必要な環境変数が arguments として定義されている

### 参考
Northflank Template ドキュメント: https://northflank.com/docs/v1/application/infrastructure-as-code/
```

```markdown
## Issue #8: デプロイ・動作確認
### 概要
Northflank へデプロイして本番動作を確認する

### タスク
- [ ] Northflank で Template を GitOps 連携
- [ ] シークレット設定 (Argument overrides)
- [ ] デプロイ実行
- [ ] 本番動作確認

### 完了条件
- Northflank 上で Bot が稼働している
- Discord 上で /選書 コマンドが正常に動作する
```

---

## Northflank Template 設計

`northflank.json` の基本構造:

```json
{
  "apiVersion": "v1.2",
  "name": "discord-book-recommender",
  "description": "選書AI Discord Bot",
  "arguments": {
    "DISCORD_TOKEN": "",
    "ANTHROPIC_API_KEY": "",
    "GOOGLE_SHEETS_ID": "",
    "GOOGLE_CREDENTIALS_JSON": ""
  },
  "spec": {
    "kind": "Workflow",
    "spec": {
      "type": "sequential",
      "steps": [
        {
          "kind": "Project",
          "ref": "project",
          "spec": {
            "name": "discord-book-recommender",
            "description": "選書AI Discord Bot",
            "region": "europe-west"
          }
        },
        {
          "kind": "Workflow",
          "spec": {
            "type": "sequential",
            "context": {
              "projectId": "${refs.project.id}"
            },
            "steps": [
              {
                "kind": "SecretGroup",
                "ref": "secrets",
                "spec": {
                  "name": "bot-secrets",
                  "secretType": "environment-arguments",
                  "secrets": {
                    "variables": {
                      "DISCORD_TOKEN": "${args.DISCORD_TOKEN}",
                      "ANTHROPIC_API_KEY": "${args.ANTHROPIC_API_KEY}",
                      "GOOGLE_SHEETS_ID": "${args.GOOGLE_SHEETS_ID}",
                      "GOOGLE_CREDENTIALS_JSON": "${args.GOOGLE_CREDENTIALS_JSON}"
                    }
                  }
                }
              },
              {
                "kind": "CombinedService",
                "ref": "bot-service",
                "spec": {
                  "name": "book-recommender-bot",
                  "billing": {
                    "deploymentPlan": "nf-compute-10"
                  },
                  "deployment": {
                    "instances": 1
                  },
                  "buildConfiguration": {
                    "dockerfile": {
                      "dockerFilePath": "/Dockerfile",
                      "dockerWorkDir": "/"
                    }
                  },
                  "vcsData": {
                    "projectUrl": "https://github.com/<GITHUB_USER>/discord-book-recommender",
                    "projectType": "github",
                    "projectBranch": "main"
                  },
                  "runtimeEnvironment": {
                    "inheritSecretGroups": [
                      "${refs.secrets.id}"
                    ]
                  }
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

※ `<GITHUB_USER>` は実際の GitHub ユーザー名に置き換える

---

## Google Sheets の想定構成

Bot が読み取る本リストの想定カラム:

| カラム名 | 説明 | 例 |
|----------|------|-----|
| タイトル | 本のタイトル | かもめ食堂 |
| 著者 | 著者名 | 群ようこ |
| ジャンル | ジャンル（任意） | 小説 |
| ページ数 | ページ数（任意） | 200 |
| 読了 | 読了フラグ（任意） | TRUE/FALSE |
| メモ | 自由メモ（任意） | 北欧が舞台 |

※ 最低限「タイトル」「著者」があれば動作可能

---

## 次のアクション

Claude Code で以下を実行:

1. **リポジトリ作成**: `gh repo create discord-book-recommender --public`
2. **Issue 作成**: 上記の Issue テンプレートに従って #1〜#8 を作成
3. **Issue #1 から順に実装開始**

---

## 備考

- Northflank Free プランの制限: 2 services, 2 databases, 2 cron jobs
- 現在 1 service を既存 Bot で使用中 → 残り 1 枠でこの Bot をデプロイ
- Template + GitOps で初回セットアップを簡略化
- 以降は GitHub push で自動デプロイ