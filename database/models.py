import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


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
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer(), unique=True)
    user_info_id: Mapped[int] = mapped_column(ForeignKey('user_info.id', ondelete="CASCADE"))

    user_info: Mapped['UserInfo'] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )
    terms: Mapped[List['Term']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
    collections: Mapped[List['Collection']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )
    folders: Mapped[List['Folder']] = relationship(
        back_populates='owner',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'User(id={self.id!r}, telegram_id={self.telegram_id!r})'


class UserInfo(Base):
    __tablename__ = 'user_info'

    id: Mapped[int] = mapped_column(primary_key=True)
    total_requests: Mapped[int] = mapped_column(Integer(),)
    language: Mapped[str] = mapped_column(String(),)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id',))


class FindDefinitonStatistic(Base, TimeStamp):
    __tablename__ = 'find_definition_statistic'

    id: Mapped[int] = mapped_column(primary_key=True)
    win_guesses: Mapped[int] = mapped_column(Integer(), default=0)
    lose_guesses: Mapped[int] = mapped_column(Integer(), default=0)
    player_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    player = relationship("User")


class Term(Base, TimeStamp):
    __tablename__ = 'term'
    __table_args__ = (
        UniqueConstraint('name', 'collection_id', name='unique_term_in_collection'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    collection_id: Mapped[int] = mapped_column(ForeignKey('collection.id', ondelete="CASCADE"))

    owner: Mapped['User'] = relationship(back_populates='terms')
    collection: Mapped['Collection'] = relationship(back_populates='terms')

    def __repr__(self) -> str:
        return f'Term(id={self.id!r}, name={self.name!r}, ' + \
            f'description={self.description!r})'


class Collection(Base, TimeStamp):
    __tablename__ = 'collection'
    __table_args__ = (
        UniqueConstraint('name', 'folder_id', name='unique_collection_in_folder'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey('folder.id', ondelete="CASCADE"))

    owner: Mapped['User'] = relationship(back_populates='collections')
    terms: Mapped[List['Term']] = relationship(
        back_populates='collection',
        cascade='all, delete-orphan',
    )
    folder: Mapped['Folder'] = relationship(back_populates='collections')

    def __repr__(self) -> str:
        return f'Collection(id={self.id!r}, email_address={self.name!r})'


class Folder(Base, TimeStamp):
    __tablename__ = 'folder'
    __table_args__ = (
        UniqueConstraint('name', 'parent_folder_id', name='unique_folder_in_folder'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"))
    parent_folder_id: Mapped[Optional[int]] = mapped_column(ForeignKey('folder.id', ondelete="CASCADE"))

    owner: Mapped['User'] = relationship(back_populates='folders')
    collections: Mapped[List['Collection']] = relationship(
        back_populates='folder',
        cascade='all, delete-orphan',
    )
    folders: Mapped[List['Folder']] = relationship(
        back_populates='parent_folder',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'Folder(id={self.id!r}, name={self.name!r})'
