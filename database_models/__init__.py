# This file can be left empty.```

<br>

**FILE: `database_models/models.py`**
```python
import os
import datetime
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey, JSON, create_engine
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Use os.environ.get for Render compatibility
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/yeab_game_db")

engine = create_async_engine(DATABASE_URL)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String)
    balance = Column(Numeric(10, 2), default=0.0, nullable=False)

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.telegram_id"))
    opponent_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    stake = Column(Numeric(10, 2), nullable=False)
    pot = Column(Numeric(10, 2), nullable=False)
    win_condition = Column(Integer, nullable=False)  # 1, 2, or 4 tokens
    status = Column(String, default="lobby", index=True) # lobby, active, finished, forfeited
    current_turn_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    board_state = Column(JSON, nullable=True)
    last_action_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    winner_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    game_message_id = Column(Integer, nullable=True) # To edit the board message

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"), nullable=False)
    tx_ref = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(String, nullable=False)  # deposit, withdrawal
    status = Column(String, default="pending", index=True) # pending, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    account_details = Column(String, nullable=True) # For withdrawals

async def init_db():
    """Initializes the database and creates tables."""
    async with engine.begin() as conn:
        print("Creating all database tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Database tables created.")