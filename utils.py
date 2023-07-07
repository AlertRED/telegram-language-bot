from typing import List
from sqlalchemy import (
    func,
    select,
)

from database.models import (
    Term,
    User,
    Collection,
    Folder,
)
from database.access import (
    Session,
)


def register_user(telegram_user_id: int) -> None:
    with Session() as session:
        query = select(User).exists().where(
            User.telegram_id == telegram_user_id,
        )
        is_exist = session.query(query).scalar()
        if not is_exist:
            with session.begin():
                session.add(User(telegram_id=telegram_user_id))


def get_folder(telegram_user_id: int, folder_id: int = None) -> Folder:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(Folder).where(
            Folder.owner == user,
            Folder.id == folder_id,
        )
        return session.scalars(query).first()


def get_folders_count(telegram_user_id: int, folder_id: int = None) -> int:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(func.count()).select_from(
            select(Folder).where(
                Folder.owner == user,
                Folder.parent_folder_id == folder_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_collections_count(telegram_user_id: int, folder_id: int = None) -> int:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(func.count()).select_from(
            select(Collection).where(
                Collection.owner == user,
                Collection.folder_id == folder_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_folders(
        telegram_user_id: int,
        folder_id: int = None,
        offset: int = 0,
        limit: int = None,
) -> List[Folder]:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(Folder).where(
            Folder.owner == user,
            Folder.parent_folder_id == folder_id,
        ).offset(offset=offset).limit(limit=limit)
        return session.scalars(query).all()


def get_collections(
        telegram_user_id: int,
        folder_id: int = None,
        offset: int = 0,
        limit: int = None,
) -> List[Collection]:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(Collection).where(
            Collection.owner == user,
            Collection.folder_id == folder_id,
        ).offset(offset=offset).limit(limit=limit)
        collections = session.scalars(query).all()
        return collections


def create_collection(
        telegram_user_id: int,
        collection_name: str,
        folder_id: int = None,
) -> None:
    with Session() as session:
        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()
        query = select(Collection).exists().where(
            Collection.owner == user,
            Collection.name == collection_name,
        )
        is_exist = session.query(query).scalar()
        if not is_exist:
            session.add(
                Collection(
                    name=collection_name,
                    owner=user,
                    folder_id=folder_id,
                ),
            )
            session.commit()


def create_term(
        telegram_user_id: int,
        collection_id: int,
        term_name: str,
        term_description: str,
) -> None:
    with Session() as session:

        query = select(User).where(
            User.telegram_id == telegram_user_id,
        )
        user: User = session.scalars(query).first()

        query = select(Collection).where(
            Collection.id == collection_id,
        )
        collection = session.scalars(query).first()
        if collection:
            session.add(
                Term(
                    name=term_name,
                    description=term_description,
                    collection=collection,
                    owner=user,
                ),
            )
            session.commit()
