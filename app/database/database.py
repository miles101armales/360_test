from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.settings import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

async def init_db():
	async with engine.begin() as connection:
		await connection.run_sync(Base.metadata.create_all)

async def close_db():
	await engine.dispose()