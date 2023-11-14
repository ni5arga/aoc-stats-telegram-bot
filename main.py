import os
import requests
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
AOC_COOKIE = os.environ.get('AOC_SESSION_COOKIE')
LEADERBOARD_ID = os.environ.get('AOC_LEADERBOARD_ID')

if not BOT_TOKEN or not AOC_COOKIE or not LEADERBOARD_ID:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN, AOC_SESSION_COOKIE, and AOC_LEADERBOARD_ID environment variables.")

AOC_API_URL = f'https://adventofcode.com/2023/leaderboard/private/view/{LEADERBOARD_ID}.json'

def get_aoc_leaderboard_stats():
    headers = {'Cookie': f'session={AOC_COOKIE}'}
    response = requests.get(AOC_API_URL, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your AoC Leaderboard Bot. Use the /help command to see available commands.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Available commands:\n'
        '/start - Start the bot\n'
        '/help - Show this help message\n'
        '/stats - Get private leaderboard stats\n'
        '/top - Rank top 10 players based on stars'
    )

def stats(update: Update, context: CallbackContext) -> None:
    leaderboard_stats = get_aoc_leaderboard_stats()

    if leaderboard_stats:
        message = f"Leaderboard Stats:\n\n"
        for member_id, member in leaderboard_stats['members'].items():
            message += f"{member['name']}: {member['local_score']} points\n"

        update.message.reply_text(message)
    else:
        update.message.reply_text("Failed to fetch AoC Leaderboard stats.")

def top(update: Update, context: CallbackContext) -> None:
    leaderboard_stats = get_aoc_leaderboard_stats()

    if leaderboard_stats:
        sorted_members = sorted(leaderboard_stats['members'].values(), key=lambda x: (x['stars'], x['local_score']), reverse=True)

        message = "Top 10 Players Based on Stars:\n\n"
        for idx, member in enumerate(sorted_members[:10], start=1):
            message += f"{idx}. {member['name']} - Stars: {member['stars']}, Points: {member['local_score']}\n"

        update.message.reply_text(message)
    else:
        update.message.reply_text("Failed to fetch AoC Leaderboard stats.")

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("top", top))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
