from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Term(Base):
    __tablename__ = "term"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())

    set_id: Mapped[int] = mapped_column(ForeignKey("set.id"))
    set_: Mapped["Set"] = relationship(
        back_populates="terms",
        cascade="all, delete-orphan",  # ??
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, " + \
            f"description={self.description!r})"


class Set(Base):
    __tablename__ = "set"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(), unique=True)

    folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(
        back_populates="sets",
        cascade="all, delete-orphan",  # ??
    )

    def __repr__(self) -> str:
        return f"Set(id={self.id!r}, email_address={self.name!r})"


class Folder(Base):
    __tablename__ = "folder"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(), unique=True)

    folder_id: Mapped[int] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(
        back_populates="folders",
        cascade="all, delete-orphan",  # ??
    )

    def __repr__(self) -> str:
        return f"Folder(id={self.id!r}, name={self.name!r})"
