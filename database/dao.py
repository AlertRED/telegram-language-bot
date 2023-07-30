from typing import List
from sqlalchemy import (
    asc,
    desc,
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


_None = object()


class NotEnoughTermsException(Exception):
    pass


def register_user(telegram_user_id: int) -> None:
    with Session() as session:
        query = select(User).exists().where(
            User.telegram_id == telegram_user_id,
        )
        is_exist = session.query(query).scalar()
        if not is_exist:
            session.add(User(telegram_id=telegram_user_id))
            session.commit()


def get_folder(folder_id: int) -> Folder:
    with Session() as session:
        query = select(Folder).where(
            Folder.id == folder_id,
        )
        return session.scalars(query).first()


def get_collection(collection_id: int) -> Collection:
    with Session() as session:
        query = select(Collection).where(
            Collection.id == collection_id,
        )
        return session.scalars(query).first()


def get_folders_count(telegram_user_id: int, folder_id: int = None) -> int:
    with Session() as session:
        query = select(func.count()).select_from(
            select(Folder).where(
                Folder.owner_id == telegram_user_id,
                Folder.parent_folder_id == folder_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_terms_count(collection_id: int = None) -> int:
    with Session() as session:
        query = select(func.count()).select_from(
            select(Term).where(
                Term.collection_id == collection_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_collections_count(telegram_user_id: int, folder_id: int = None) -> int:
    with Session() as session:
        query = select(func.count()).select_from(
            select(Collection).where(
                Collection.owner_id == telegram_user_id,
                Collection.folder_id == folder_id,
            ).subquery(),
        )
        return session.execute(query).scalar_one()


def get_folders(
    telegram_user_id: int,
    parent_folder_id: int = _None,
    offset: int = 0,
    limit: int = None,
) -> List[Folder]:
    with Session() as session:
        query = select(Folder).where(
            Folder.owner_id == telegram_user_id,
        )
        if parent_folder_id != _None:
            query = query.where(Folder.parent_folder_id == parent_folder_id)
        query = query.offset(offset=offset).limit(limit=limit).order_by(
            desc(Folder.updated_datetime),
        )
        return session.scalars(query).all()


def get_collections(
    telegram_user_id: int,
    folder_id: int = None,
    offset: int = 0,
    limit: int = None,
) -> List[Collection]:
    with Session() as session:
        query = select(Collection).where(
            Collection.owner_id == telegram_user_id,
            Collection.folder_id == folder_id,
        ).offset(offset=offset).limit(limit=limit)
        collections = session.scalars(query).all()
        return collections


def get_terms(
    telegram_user_id: int,
    collection_id: int = None,
    offset: int = 0,
    limit: int = None,
) -> List[Term]:
    with Session() as session:
        query = select(Term).where(
            Term.owner_id == telegram_user_id,
            Term.collection_id == collection_id,
        ).offset(offset=offset).limit(limit=limit)
        return session.scalars(query).all()


def get_term(term_id: int) -> Term:
    with Session() as session:
        query = select(Term).where(
            Term.id == term_id,
        )
        return session.scalars(query).first()


def create_collection(
    telegram_user_id: int,
    collection_name: str,
    folder_id: int = None,
) -> Collection:
    with Session() as session:
        query = select(Collection).exists().where(
            Collection.owner_id == telegram_user_id,
            Collection.name == collection_name,
            Collection.folder_id == folder_id,
        )
        is_exist = session.query(query).scalar()
        if not is_exist:
            collection = Collection(
                name=collection_name,
                owner_id=telegram_user_id,
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
) -> Term:
    with Session() as session:
        query = select(Collection).where(
            Collection.id == collection_id,
        )
        collection = session.scalars(query).first()
        if collection:
            term = Term(
                name=term_name,
                description=term_description,
                collection=collection,
                owner_id=telegram_user_id,
            )
            session.add(term)
            session.commit()
            session.refresh(term)
            return term


def create_folder(
    telegram_user_id: int,
    folder_name: str,
    folder_id: int = None,
) -> Folder:
    with Session() as session:
        query = select(Folder).exists().where(
            Folder.owner_id == telegram_user_id,
            Folder.name == folder_name,
            Folder.parent_folder_id == folder_id,
        )
        is_exist = session.query(query).scalar()
        if not is_exist:
            folder = Folder(
                name=folder_name,
                owner_id=telegram_user_id,
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
) -> List[Term]:
    with Session() as session:
        query = select(Term).where(
            Term.collection_id == collection_id,
            Term.id.not_in(excluded_ids),
        ).order_by(func.random())
        term = session.scalars(query).first()
        if not term:
            raise NotEnoughTermsException
        query = select(Term).where(
            Term.collection_id == collection_id,
            Term.id != term.id,
        ).order_by(func.random()).limit(limit - 1)
        terms = session.scalars(query).all()
        return [term] + terms


def get_simple_train_terms(
    collection_id: int,
) -> List[Term]:
    with Session() as session:
        query = select(
            Term.id, Term.name, Term.description,
        ).where(
            Term.collection_id == collection_id,
        ).order_by(func.random())
        terms = session.execute(query).fetchall()
        return terms
