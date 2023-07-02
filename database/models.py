import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class Base(DeclarativeBase):
    pass


class TimeStamp:
    created_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    updated_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), default=func.now(),
    )


class User(Base, TimeStamp):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(Integer())

    terms: Mapped["Term"] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",  # ??
    )
    collections: Mapped[List["Collection"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",  # ??
    )
    folders: Mapped[List["Folder"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",  # ??
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, telegram_id={self.telegram_id!r})"


class Term(Base):
    __tablename__ = "term"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="terms")

    collection_id: Mapped[int] = mapped_column(ForeignKey("collection.id"))
    collection: Mapped["Collection"] = relationship(back_populates="terms")

    def __repr__(self) -> str:
        return f"Term(id={self.id!r}, name={self.name!r}, " + \
            f"description={self.description!r})"


class Collection(Base):
    __tablename__ = "collection"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(), unique=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="collections")

    terms: Mapped[List["Term"]] = relationship(
        back_populates="collection",
        cascade="all, delete-orphan",  # ??
    )

    folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(back_populates="collections")

    def __repr__(self) -> str:
        return f"Collection(id={self.id!r}, email_address={self.name!r})"


class Folder(Base):
    __tablename__ = "folder"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(), unique=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="folders")

    collections: Mapped[List["Collection"]] = relationship(
        back_populates="folder",
        cascade="all, delete-orphan",
    )

    parent_folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"))
    parent_folder: Mapped[Optional["Folder"]] = relationship(back_populates="folders")

    folders: Mapped[List["Folder"]] = relationship(
        remote_side='folder.id',
        backref=backref('parent_folder'),
    )
    parent_folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey("folder.id"))
    folders: Mapped[List["Folder"]] = relationship("Folder", cascade="all, delete-orphan")
    # folders: Mapped[List["Folder"]] = relationship(
    #     back_populates="parent_folder",
    #     cascade="all, delete-orphan",  # ??
    # )

    def __repr__(self) -> str:
        return f"Folder(id={self.id!r}, name={self.name!r})"
