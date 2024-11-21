import time
from datetime import datetime
from telebot import TeleBot
from config import settings
from bot import generate_statistics
from logger_config import get_logger

bot = TeleBot(settings.BOT_TOKEN)
logger = get_logger("notifications", settings.LOGGING_FILE)
hour, minute = map(int, settings.NOTIFICATION_TIME.split(":"))


def main():
    while True:
        try:
            now = datetime.now()
            if now.hour == hour and now.minute == minute:
                for admin in settings.ADMINS:
                    stats = generate_statistics(1, "Today", "get_average_all_presses_per_day", 1)
                    bot.send_message(admin, stats, parse_mode="Markdown")
                    logger.debug(f"Sent statistics to admin {admin}")

            else:
                logger.debug("Waiting for the notification time")

            time.sleep(30)

        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main()
