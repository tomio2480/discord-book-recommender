"""Claude API を使って本を選書するモジュール。"""

import anthropic

from .sheets import Book


class BookSelector:
    """Claude API を使って本を選書するクラス。"""

    MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 1024

    def __init__(self, api_key: str) -> None:
        """クライアントを初期化する。

        Args:
            api_key: Anthropic API キー
        """
        self._client = anthropic.Anthropic(api_key=api_key)

    def select(self, books: list[Book], request: str) -> str:
        """ユーザーの要望に基づいて本を選書する。

        Args:
            books: 本のリスト
            request: ユーザーの要望

        Returns:
            選書結果のテキスト
        """
        books_text = self._format_books(books)
        prompt = self._build_prompt(books_text, request)

        message = self._client.messages.create(
            model=self.MODEL,
            max_tokens=self.MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text

    def _format_books(self, books: list[Book]) -> str:
        """本のリストをテキストに整形する。"""
        lines = []
        for book in books:
            parts = [f"『{book.title}』{book.author}"]
            if book.genre:
                parts.append(f"[{book.genre}]")
            if book.pages:
                parts.append(f"{book.pages}p")
            if book.memo:
                parts.append(f"({book.memo})")
            lines.append(" ".join(parts))
        return "\n".join(lines)

    def _build_prompt(self, books_text: str, request: str) -> str:
        """選書用のプロンプトを構築する。"""
        return f"""あなたは読書アドバイザーです。
以下の本リストから、ユーザーの要望に合った本を5冊程度選んでください。

## 本リスト
{books_text}

## ユーザーの要望
{request}

## 回答形式
以下の形式で回答してください。絵文字は最初の見出しにのみ使用し、本文中では使わないでください。

📚 [要望に応じた一言コメント]

1. 『タイトル』著者
   → おすすめ理由（2-3行）

2. 『タイトル』著者
   → おすすめ理由（2-3行）

（以下同様）

## 注意事項
- 本リストに存在する本のみを選んでください
- ユーザーの気分、読書時間、好みを考慮してください
- 各本の推薦理由は具体的かつ簡潔に記載してください
- 本文中に絵文字は使わないでください"""
