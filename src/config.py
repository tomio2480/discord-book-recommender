"""環境変数を管理するモジュール。"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    """アプリケーション設定を保持するデータクラス。"""

    discord_token: str
    anthropic_api_key: str
    google_sheets_id: str
    google_credentials_json: str


def load_config() -> Config:
    """環境変数から設定を読み込む。

    Returns:
        Config オブジェクト

    Raises:
        ValueError: 必須の環境変数が設定されていない場合
    """
    load_dotenv()

    required_vars = [
        "DISCORD_TOKEN",
        "ANTHROPIC_API_KEY",
        "GOOGLE_SHEETS_ID",
        "GOOGLE_CREDENTIALS_JSON",
    ]

    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"必須の環境変数が設定されていません: {', '.join(missing)}")

    return Config(
        discord_token=os.environ["DISCORD_TOKEN"],
        anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
        google_sheets_id=os.environ["GOOGLE_SHEETS_ID"],
        google_credentials_json=os.environ["GOOGLE_CREDENTIALS_JSON"],
    )
