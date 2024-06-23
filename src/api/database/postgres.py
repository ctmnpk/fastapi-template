from datetime import datetime
from typing import List

from decouple import config
from pytz import timezone
from sqlalchemy import create_engine, ForeignKey, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from models.enums import Gender, Priority, Role


user = config("POSTGRES_USER")
password = config("POSTGRES_PASSWORD")
host = config("POSTGRES_HOST")
port = config("POSTGRES_PORT", cast=int)
database = config("POSTGRES_DATABASE")
connection_string = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)

local_timezone = timezone("America/Sao_Paulo")
metadata = MetaData()
engine = create_engine(
    url=connection_string, pool_size=5, pool_pre_ping=True, pool_recycle=3600
)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    metadata

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(16))
    password: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str]
    age: Mapped[int]
    gender: Mapped[Gender]
    todos: Mapped[List["Todos"]] = relationship(
                                        "Todos",
                                        back_populates="user",
                                        cascade="all, delete"
                                    )
    role: Mapped[Role] = mapped_column(default=Role.COMMONER)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now(tz=local_timezone)
    )


class Todos(Base):
    __tablename__ = "todos"
    metadata

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    dead_line: Mapped[datetime]
    priority: Mapped[Priority] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["Users"] = relationship("Users", back_populates="todos")
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now(tz=local_timezone)
    )

metadata.create_all(bind=engine, tables=[Todos.__table__, Users.__table__])

connection = engine.connect()
