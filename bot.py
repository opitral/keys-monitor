import datetime

from telebot import TeleBot, types
from telebot.custom_filters import SimpleCustomFilter
from config import settings
from formatter import Row, RowDiff, Table
from repository import KeyRepository

bot = TeleBot(settings.BOT_TOKEN)
repository = KeyRepository(settings.DATABASE_URL)


class AdminFilter(SimpleCustomFilter):
    key = 'is_admin'

    def check(self, message: types.Message):
        return message.from_user.id in settings.ADMINS


bot.add_custom_filter(AdminFilter())


def setup_bot_commands():
    commands = [
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("today", "Show today's statistics"),
        types.BotCommand("week", "Show weekly statistics"),
        types.BotCommand("month", "Show monthly statistics"),
    ]
    bot.set_my_commands(commands)


def generate_statistics(period_days, label, average_method, comparison_days):
    start_time = datetime.datetime.now() - datetime.timedelta(days=period_days)
    end_time = datetime.datetime.now()

    statistic_table = Table(f"*📊 {label} statistic*")
    average_table = Table(f"*🔀 Average {label.lower()}*")
    comparison_table = Table(f"*📅 Comparison with the previous {label.lower()}*")

    for field in settings.SHOW_FIELDS:
        if field == "total":
            total = repository.get_total_presses()
            avg = getattr(repository, average_method)()  # Використовуємо переданий метод для total
            prev = repository.get_key_presses_in_timeframe(
                field,
                start_time - datetime.timedelta(days=comparison_days),
                end_time - datetime.timedelta(days=comparison_days),
            )
            statistic_table.add_row(Row(field, total))
            average_table.add_row(Row(field, avg))
            comparison_table.add_row(RowDiff(field, total, prev))
        else:
            count = repository.get_key_presses_in_timeframe(field, start_time, end_time)

            if period_days == 1:
                avg = repository.get_average_presses_per_day(field)
            elif period_days == 7:
                avg = repository.get_average_presses_per_week(field)
            elif period_days == 30:
                avg = repository.get_average_presses_per_month(field)
            else:
                raise ValueError("Unsupported period_days value!")

            prev_count = repository.get_key_presses_in_timeframe(
                field,
                start_time - datetime.timedelta(days=comparison_days),
                end_time - datetime.timedelta(days=comparison_days),
            )
            statistic_table.add_row(Row(field, count))
            average_table.add_row(Row(field, avg))
            comparison_table.add_row(RowDiff(field, count, prev_count))

    return f'{statistic_table}\n\n{average_table}\n\n{comparison_table}'


@bot.message_handler(commands=["start"], is_admin=True)
def start(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name or 'admin'}!")


@bot.message_handler(commands=["today"], is_admin=True)
def today(message):
    stats = generate_statistics(1, "Today", "get_average_all_presses_per_day", 1)
    bot.send_message(message.chat.id, stats, parse_mode="Markdown")


@bot.message_handler(commands=["week"], is_admin=True)
def week(message):
    stats = generate_statistics(7, "Week", "get_average_all_presses_per_week", 7)
    bot.send_message(message.chat.id, stats, parse_mode="Markdown")


@bot.message_handler(commands=["month"], is_admin=True)
def month(message):
    stats = generate_statistics(30, "Month", "get_average_all_presses_per_month", 30)
    bot.send_message(message.chat.id, stats, parse_mode="Markdown")


if __name__ == "__main__":
    setup_bot_commands()
    bot.polling()
