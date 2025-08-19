import logging

import httpx
import asyncio

logger = logging.getLogger(__name__)


class TelegramBot:

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.uri = f"https://api.telegram.org/bot{token}/"

    def _send_message(self, text: str) -> None:
        payload = {"chat_id": self.chat_id, "text": text}
        with httpx.Client() as client:
            res = client.post(self.uri + "sendMessage", data=payload)
        if res.status_code != 200:
            logger.error(res.text)
        return

    def new_borrowing(self, borrowing):
        user = borrowing.user
        book = borrowing.book.name
        borrow = borrowing.borrow_date.strftime("%d.%m.%Y")
        expected_return = borrowing.expected_return_date.strftime("%d.%m.%Y")
        message = (
            f"📚 New Book Borrowing!\n\n"
            f"User: {user.full_name}, {user.email}\n"
            f"Book: {book}\n"
            f"Borrow Date: {borrow}\n"
            f"Expected Return Date: {expected_return}\n"
        )
        return self._send_message(message)

    def expired_borrowing(self, borrowing):
        user = borrowing.user
        book = borrowing.book.name
        borrow = borrowing.borrow_date.strftime("%d.%m.%Y")
        expected_return = borrowing.expected_return_date.strftime("%d.%m.%Y")
        message = (
            f"⚠️ Overdue Borrowing!"
            f"User: {user.full_name}, {user.email}\n"
            f"Book: {book}\n"
            f"Borrow Date: {borrow}\n"
            f"Expected Return Date: {expected_return}\n"
            f"The book has not been returned on time. Please take action as soon as possible."
        )
        self._send_message(message)

    def no_expired_borrowings(self):
        message = "No borrowings overdue today!✅"
        self._send_message(message)

    async def listen_and_reply(self):
        offset = None
        print("Bot started...")
        async with httpx.AsyncClient(timeout=None) as client:
            while True:
                params = {"timeout": 10}
                if offset:
                    params["offset"] = offset
                resp = await client.get(self.uri + "getUpdates", params=params)
                data = resp.json()
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message")
                    if message:
                        chat_id = message["chat"]["id"]
                        text = f"Your chat id is: {chat_id}"
                        self._send_message(chat_id, text)


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN", None)
    bot = TelegramBot(TOKEN)
    asyncio.run(bot.listen_and_reply())
