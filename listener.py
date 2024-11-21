from pynput import keyboard
from repository import KeyRepository
from config import settings
from logger_config import get_logger

logger = get_logger(__name__, settings.LOGGING_FILE)
repository = KeyRepository(settings.DATABASE_URL)


def on_press(key):
    logger.debug("Key '%s' pressed.", key)
    repository.add_key_press(str(key))


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
