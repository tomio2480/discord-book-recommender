"""Google Sheets から本のリストを取得するモジュール。"""

import json
from dataclasses import dataclass

import gspread
from google.oauth2.service_account import Credentials


@dataclass
class Book:
    """本の情報を表すデータクラス。"""

    title: str
    author: str
    publisher: str = ""
    description: str = ""
    is_read: bool = False
    memo: str = ""


class SheetsClient:
    """Google Sheets からデータを取得するクライアント。"""

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
    ]

    def __init__(self, credentials_json: str, sheets_id: str) -> None:
        """クライアントを初期化する。

        Args:
            credentials_json: サービスアカウントの認証情報 (JSON 文字列)
            sheets_id: スプレッドシートの ID
        """
        self._sheets_id = sheets_id
        self._client = self._create_client(credentials_json)

    def _create_client(self, credentials_json: str) -> gspread.Client:
        """gspread クライアントを作成する。"""
        credentials_dict = json.loads(credentials_json)
        credentials = Credentials.from_service_account_info(
            credentials_dict, scopes=self.SCOPES
        )
        return gspread.authorize(credentials)

    def get_books(self) -> list[Book]:
        """本のリストを取得する。

        Returns:
            本のリスト

        Raises:
            gspread.exceptions.SpreadsheetNotFound: スプレッドシートが見つからない場合
            gspread.exceptions.APIError: API エラーが発生した場合
        """
        spreadsheet = self._client.open_by_key(self._sheets_id)
        worksheet = spreadsheet.sheet1
        records = worksheet.get_all_records()

        books = []
        for record in records:
            # 削除フラグがあるものはスキップ
            delete_flag = record.get("削除フラグ")
            if delete_flag and str(delete_flag).upper() == "TRUE":
                continue

            title = record.get("タイトル", "")
            author = record.get("著者名", "")
            if not title or not author:
                continue

            is_read_raw = record.get("既読フラグ", "")
            is_read = bool(is_read_raw)

            book = Book(
                title=title,
                author=author,
                publisher=record.get("出版社", ""),
                description=record.get("商品説明", ""),
                is_read=is_read,
                memo=record.get("メモ", ""),
            )
            books.append(book)

        return books
