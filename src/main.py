"""アプリケーションのエントリーポイント。"""

import logging

from .bot import BookRecommenderBot
from .config import load_config
from .selector import BookSelector
from .sheets import SheetsClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Bot を起動する。"""
    logger.info("設定を読み込んでいます...")
    config = load_config()

    logger.info("クライアントを初期化しています...")
    sheets_client = SheetsClient(
        credentials_json=config.google_credentials_json,
        sheets_id=config.google_sheets_id,
    )
    selector = BookSelector(api_key=config.gemini_api_key)

    logger.info("Bot を起動しています...")
    bot = BookRecommenderBot(sheets_client=sheets_client, selector=selector)
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()
