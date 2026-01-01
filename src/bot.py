"""Discord Bot の基本機能を提供するモジュール。"""

import discord
from discord import app_commands

from .selector import BookSelector
from .sheets import SheetsClient


class BookRecommenderBot(discord.Client):
    """本を選書する Discord Bot。"""

    def __init__(
        self,
        sheets_client: SheetsClient,
        selector: BookSelector,
    ) -> None:
        """Bot を初期化する。

        Args:
            sheets_client: Google Sheets クライアント
            selector: 選書ロジック
        """
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self._sheets_client = sheets_client
        self._selector = selector

    async def setup_hook(self) -> None:
        """Bot 起動時にスラッシュコマンドを同期する。"""
        self._register_commands()
        await self.tree.sync()

    def _register_commands(self) -> None:
        """スラッシュコマンドを登録する。"""

        @self.tree.command(name="選書", description="気分や要望に合わせて本をおすすめします")
        @app_commands.describe(要望="どんな本が読みたいか教えてください")
        async def sensho(interaction: discord.Interaction, 要望: str) -> None:
            await self._handle_sensho(interaction, 要望)

    async def _handle_sensho(
        self, interaction: discord.Interaction, request: str
    ) -> None:
        """選書コマンドを処理する。"""
        await interaction.response.defer(thinking=True)

        try:
            books = self._sheets_client.get_books()
            if not books:
                await interaction.followup.send("本のリストが空です。")
                return

            result = self._selector.select(books, request)
            await self._send_result(interaction, result)

        except Exception as e:
            await interaction.followup.send(f"エラーが発生しました: {e}")

    async def _send_result(
        self, interaction: discord.Interaction, result: str
    ) -> None:
        """結果を送信する。Discord の 2000 文字制限に対応。"""
        if len(result) <= 2000:
            await interaction.followup.send(result)
            return

        chunks = self._split_message(result, 2000)
        for i, chunk in enumerate(chunks):
            if i == 0:
                await interaction.followup.send(chunk)
            else:
                await interaction.channel.send(chunk)

    def _split_message(self, text: str, max_length: int) -> list[str]:
        """テキストを指定した長さで分割する。"""
        chunks = []
        while text:
            if len(text) <= max_length:
                chunks.append(text)
                break
            split_pos = text.rfind("\n", 0, max_length)
            if split_pos == -1:
                split_pos = max_length
            chunks.append(text[:split_pos])
            text = text[split_pos:].lstrip("\n")
        return chunks
