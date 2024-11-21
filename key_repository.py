from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from logger_config import get_logger

logger = get_logger(__name__, settings.LOGGING_FILE)
Base = declarative_base()


class Keys(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pressedAt = Column(DateTime, nullable=False, default=datetime.now)


class KeyRepository:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.debug("KeyRepository initialized with database URL: %s", database_url)

    def add_key_press(self, key_name):
        session = self.Session()
        try:
            new_key = Keys(name=key_name)
            session.add(new_key)
            session.commit()
            logger.debug("Key '%s' added successfully.", key_name)
        except Exception as e:
            session.rollback()
            logger.error("Error adding key '%s': %s", key_name, e)
        finally:
            session.close()

    def get_total_presses(self):
        session = self.Session()
        try:
            count = session.query(func.count(Keys.id)).scalar()
            logger.debug("Total presses retrieved: %d", count)
            return count
        finally:
            session.close()

    def get_presses_by_name(self, key_name):
        session = self.Session()
        try:
            count = session.query(func.count(Keys.id)).filter(Keys.name == key_name).scalar()
            logger.debug("Presses for key '%s': %d", key_name, count)
            return count
        finally:
            session.close()

    def get_presses_in_timeframe(self, start_time, end_time):
        session = self.Session()
        try:
            count = session.query(func.count(Keys.id)).filter(
                Keys.pressedAt >= start_time,
                Keys.pressedAt <= end_time
            ).scalar()
            logger.debug("Presses in timeframe (%s - %s): %d", start_time, end_time, count)
            return count
        finally:
            session.close()

    def get_key_presses_in_timeframe(self, key_name, start_time, end_time):
        session = self.Session()
        try:
            count = session.query(func.count(Keys.id)).filter(
                Keys.name == key_name,
                Keys.pressedAt >= start_time,
                Keys.pressedAt <= end_time
            ).scalar()
            logger.debug("Presses for key '%s' in timeframe (%s - %s): %d", key_name, start_time, end_time, count)
            return count
        finally:
            session.close()

    def get_all_keys(self):
        session = self.Session()
        try:
            keys = session.query(Keys).all()
            logger.debug("Retrieved all keys, count: %d", len(keys))
            return keys
        finally:
            session.close()
