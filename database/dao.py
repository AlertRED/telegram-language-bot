from typing import List
from sqlalchemy import (
    desc,
    func,
    select,
)

import database.models as models
from database.access import Session


_None = object()


class NotEnoughTermsException(Exception):
    pass


def register_user(telegram_user_id: int) -> None:
    with Session() as session:
        query = select(models.User).where(
            models.User.telegram_id == telegram_user_id,
        ).exists()
        is_exist = session.query(query).scalar()
        if not is_exist:
            user_info = models.UserInfo()
            user = models.User(
                telegram_id=telegram_user_id,
                user_info=user_info,
            )
            session.add(user, user_info)
            session.commit()


def get_user(telegram_id: int) -> models.Folder:
    with Session() as session:
        query = select(
            models.User,
        ).where(
            models.User.telegram_id == telegram_id,
        )
        return session.scalars(query).first()


def get_folder(folder_id: int) -> models.Folder:
    with Session() as session:
        query = select(models.Folder).where(
            models.Folder.id == folder_id,
        )
        return session.scalars(query).first()


def get_collection(
    collection_id: int = _None,
    collection_name: str = _None,
    folder_id: int = _None,
) -> models.Collection:
    with Session() as session:
        query = select(models.Collection)
        if collection_id != _None:
            query = query.where(
                models.Collection.id == collection_id,
            )
        if collection_name != _None:
            query = query.where(
                models.Collection.name == collection_name,
            )
        if folder_id != _None:
            query = query.where(
                models.Collection.folder_id == folder_id,
            )
        return session.scalars(query).first()


def get_term(
    term_id: int = _None,
    term_name: str = _None,
    collection_id: int = _None,
) -> models.Term:
    with Session() as session:
        query = select(
            models.Term
        )
        if term_id != _None:
            query = query.where(
                models.Term.id == term_id,
            )
        if term_name != _None:
            query = query.where(
                models.Term.name == term_name,
            )
        if collection_id != _None:
            query = query.where(
                models.Term.collection_id == collection_id,
            )
        return session.scalars(query).first()


def get_folders_count(
    telegram_user_id: int,
    folder_id: int = None,
    exclude_folder_ids: list = None,
) -> int:
    if exclude_folder_ids is None:
        exclude_folder_ids = []
    with Session() as session:
        query = select(func.count()).select_from(
            select(
                models.Folder,
            ).join(
                models.User,
                models.User.id == models.Folder.owner_id,
            ).where(
                models.User.telegram_id == telegram_user_id,
                models.Folder.parent_folder_id == folder_id,
                models.Folder.id.not_in(exclude_folder_ids),
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_terms_count(telegram_user_id: int, collection_id: int = None) -> int:
    with Session() as session:
        query = select(func.count()).select_from(
            select(
                models.Term,
            ).join(
                models.User,
                models.User.id == models.Term.owner_id,
            ).where(
                models.User.telegram_id == telegram_user_id,
                models.Term.collection_id == collection_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_collections_count(
    telegram_user_id: int,
    folder_id: int = None,
    exclude_collection_ids: list = None,
) -> int:
    if exclude_collection_ids is None:
        exclude_collection_ids = []
    with Session() as session:
        query = select(func.count()).select_from(
            select(
                models.Collection
            ).join(
                models.User,
                models.User.telegram_id == telegram_user_id,
            ).where(
                models.Collection.folder_id == folder_id,
                models.Collection.id.not_in(exclude_collection_ids),
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_folders(
    telegram_user_id: int,
    parent_folder_id: int = _None,
    offset: int = 0,
    limit: int = None,
    exclude_folders_ids: list = None,
) -> List[models.Folder]:
    if exclude_folders_ids is None:
        exclude_folders_ids = []
    with Session() as session:
        query = select(
            models.Folder,
        ).join(
            models.User,
            models.User.telegram_id == telegram_user_id,
        ).where(
            models.Folder.owner_id == models.User.id,
            models.Folder.id.not_in(exclude_folders_ids),
        )
        if parent_folder_id != _None:
            query = query.where(
                models.Folder.parent_folder_id == parent_folder_id,
            )
        query = query.offset(
            offset=offset,
        ).limit(
            limit=limit,
        ).order_by(
            desc(models.Folder.updated_datetime),
        )
        return session.scalars(query).all()


def get_collections(
    telegram_user_id: int,
    folder_id: int = None,
    offset: int = 0,
    limit: int = None,
    exclude_collection_ids: list = None,
) -> List[models.Collection]:
    with Session() as session:
        query = select(
            models.Collection,
        ).join(
            models.User,
            models.User.telegram_id == telegram_user_id,
        ).where(
            models.Collection.owner_id == models.User.id,
            models.Collection.folder_id == folder_id,
            models.Collection.id.not_in(exclude_collection_ids),
        ).offset(
            offset=offset,
        ).limit(
            limit=limit,
        )
        collections = session.scalars(query).all()
        return collections


def get_terms(
    telegram_user_id: int,
    collection_id: int = None,
    offset: int = 0,
    limit: int = None,
) -> List[models.Term]:
    with Session() as session:
        query = select(
            models.Term,
        ).join(
            models.User,
            models.User.telegram_id == telegram_user_id,
        ).where(
            models.Term.owner_id == models.User.id,
            models.Term.collection_id == collection_id,
        ).offset(
            offset=offset,
        ).limit(
            limit=limit,
        )
        return session.scalars(query).all()


def create_collection(
    telegram_user_id: int,
    collection_name: str,
    folder_id: int = None,
) -> models.Collection:
    with Session() as session:
        user = get_user(telegram_id=telegram_user_id)
        if user:
            collection = models.Collection(
                name=collection_name,
                owner_id=user.id,
                folder_id=folder_id,
            )
            session.add(collection)
            session.commit()
            session.refresh(collection)
            return collection


def update_collection(
    collection_id: int,
    collection_name: str = _None,
    folder_id: int = _None,
) -> None:
    with Session() as session:
        collection = get_collection(collection_id)
        if collection:
            if collection_name != _None:
                collection.name = collection_name
            if folder_id != _None:
                collection.folder_id = folder_id
            session.add(collection)
            session.commit()


def update_term(
    term_id: int,
    term_name: str = _None,
    term_description: str = _None,
    collection_id: int = _None,
) -> None:
    with Session() as session:
        term = get_term(term_id)
        if term:
            if term_name != _None:
                term.name = term_name
            if term_description != _None:
                term.description = term_description
            if collection_id != _None:
                term.collection_id = collection_id
            session.add(term)
            session.commit()


def delete_collection(
    collection_id: int,
) -> None:
    with Session() as session:
        collection = get_collection(collection_id)
        if collection:
            session.delete(collection)
            session.commit()


def delete_term(
    term_id: int,
) -> None:
    with Session() as session:
        term = get_term(term_id)
        if term:
            session.delete(term)
            session.commit()


def create_term(
    telegram_user_id: int,
    collection_id: int,
    term_name: str,
    term_description: str,
) -> models.Term:
    with Session() as session:
        user = get_user(telegram_id=telegram_user_id)
        if user:
            term = models.Term(
                name=term_name,
                description=term_description,
                collection_id=collection_id,
                owner_id=user.id,
            )
            session.add(term)
            session.commit()
            session.refresh(term)
            return term


def create_folder(
    telegram_user_id: int,
    folder_name: str,
    folder_id: int = None,
) -> models.Folder:
    with Session() as session:
        user = get_user(telegram_id=telegram_user_id)
        if user:
            folder = models.Folder(
                name=folder_name,
                owner_id=user.id,
                parent_folder_id=folder_id,
            )
            session.add(folder)
            session.commit()
            session.refresh(folder)
            return folder


def update_folder(
    folder_id: int,
    folder_name: str = _None,
    parent_folder_id: int = _None,
) -> None:
    with Session() as session:
        folder = get_folder(folder_id)
        if folder:
            if folder_name != _None:
                folder.name = folder_name
            if parent_folder_id != _None:
                folder.parent_folder_id = parent_folder_id
            session.add(folder)
            session.commit()


def delete_folder(
    folder_id: int,
) -> None:
    with Session() as session:
        folder = get_folder(folder_id)
        if folder:
            session.delete(folder)
            session.commit()


def get_find_definition_terms(
    collection_id: int,
    limit: int,
    excluded_ids: list = None,
) -> List[models.Term]:
    with Session() as session:
        query = select(models.Term).where(
            models.Term.collection_id == collection_id,
            models.Term.id.not_in(excluded_ids),
        ).order_by(func.random())
        term = session.scalars(query).first()
        if not term:
            raise NotEnoughTermsException
        query = select(models.Term).where(
            models.Term.collection_id == collection_id,
            models.Term.id != term.id,
        ).order_by(func.random()).limit(limit - 1)
        terms = session.scalars(query).all()
        return [term] + terms


def get_simple_train_terms(
    collection_id: int,
) -> List[models.Term]:
    with Session() as session:
        query = select(
            models.Term.id, models.Term.name, models.Term.description,
        ).where(
            models.Term.collection_id == collection_id,
        ).order_by(func.random())
        terms = session.execute(query).fetchall()
        return terms
