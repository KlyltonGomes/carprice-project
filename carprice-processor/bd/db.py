import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

BR_TZ = pytz.timezone("America/Sao_Paulo")

# Listener para converter datetime antes de persistir
@event.listens_for(SessionLocal, "before_flush")
def convert_datetime_to_brt(session, flush_context, instances):
    for obj in session.new:
        for attr in dir(obj):
            value = getattr(obj, attr, None)
            if isinstance(value, datetime):
                # Converte UTC para BRT
                br_value = value.replace(tzinfo=pytz.utc).astimezone(BR_TZ).replace(tzinfo=None)
                setattr(obj, attr, br_value)

