# Advent of Code Leaderboard Stats Telegram Bot

A Telegram bot written in Python to interact with the Advent of Code (AoC) website's private leaderboard.

## Commands

- `/start`: Start the bot and receive a welcome message.
- `/help`: Display available commands and their descriptions.
- `/stats`: Retrieve private leaderboard statistics.
- `/top`: Rank the top 10 players based on stars.

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies: `pip install -r requirements.txt`

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `AOC_SESSION_COOKIE`: Your Advent of Code session cookie.
- `AOC_LEADERBOARD_ID`: Your Advent of Code private leaderboard ID.
