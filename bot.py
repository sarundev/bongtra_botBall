import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Local file path or an https:// image URL
BANNER = os.getenv("BANNER", str(Path(__file__).parent / "banner.jpg"))

WELCOME_TEXT = (
    "⚽️ <b>FOOTBALL HUB</b>\n"
    "<i>Your daily football destination</i> 🌍\n\n"
    "🔴 Live Matches\n"
    "📊 Latest Scores\n"
    "📅 Upcoming Fixtures\n"
    "📰 Football News\n"
    "🏆 League Tables\n\n"
    "👇 <b>Choose an option below</b>"
)

SECTIONS = {
    "live": "🔴 <b>Live Matches</b>\n\nNo live matches right now. Check back soon!",
    "scores": "📊 <b>Latest Scores</b>\n\nRecent results will appear here.",
    "fixtures": "📅 <b>Upcoming Fixtures</b>\n\nUpcoming matches will appear here.",
    "news": "📰 <b>Football News</b>\n\nThe latest headlines will appear here.",
    "tables": "🏆 <b>League Tables</b>\n\nLeague standings will appear here.",
}


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 Live Matches", callback_data="live")],
        [
            InlineKeyboardButton("📊 Latest Scores", callback_data="scores"),
            InlineKeyboardButton("📅 Fixtures", callback_data="fixtures"),
        ],
        [
            InlineKeyboardButton("📰 News", callback_data="news"),
            InlineKeyboardButton("🏆 League Tables", callback_data="tables"),
        ],
    ])


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back to Menu", callback_data="menu")]])


def banner_photo():
    if BANNER.startswith("http"):
        return BANNER
    return open(BANNER, "rb")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_photo(
        photo=banner_photo(),
        caption=WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu(),
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "menu":
        await query.edit_message_caption(
            caption=WELCOME_TEXT, parse_mode=ParseMode.HTML, reply_markup=main_menu()
        )
        return

    text = SECTIONS.get(query.data)
    if text:
        await query.edit_message_caption(
            caption=text, parse_mode=ParseMode.HTML, reply_markup=back_menu()
        )


def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("Missing BOT_TOKEN. Put it in a .env file (see .env.example).")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler(["start", "menu"], start))
    app.add_handler(CallbackQueryHandler(on_button))

    print("⚽️ Football Hub bot is running... (Ctrl+C to stop)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
