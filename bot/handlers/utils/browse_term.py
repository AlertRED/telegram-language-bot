import math
from aiogram import (
    Router,
    types,
)
from aiogram.utils.i18n import gettext as _

from .calbacks import (
    ChangeCollectionCallback,
    TermSelectedCallback,
)
import database.dao as dao


router = Router()


class CollectionIsEmptyException(Exception):
    pass


async def start_browse(
    callback: types.CallbackQuery,
    collection_id: int,
    page: int = 0,
) -> None:
    TERMS_PER_PAGE = 10
    terms_count = dao.get_terms_count(collection_id)
    if terms_count == 0:
        raise CollectionIsEmptyException

    terms = dao.get_terms(
        callback.from_user.id,
        collection_id=collection_id,
        limit=TERMS_PER_PAGE,
        offset=page * TERMS_PER_PAGE,
    )
    total_pages = math.ceil(terms_count / TERMS_PER_PAGE)

    text = ''
    for i, term in enumerate(terms):
        text += _(
            '\n\n{i+1}. <u><b>{name}</b></u> - '
            '{description}'
        ).format(
            name=term.name,
            description=term.description,
        )

    await callback.message.edit_text(
        text=text,
        parse_mode='html',
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=str(i + 1),
                        callback_data=TermSelectedCallback(
                            term_id=term.id,
                        ).pack(),
                    ) for i, term in enumerate(terms)
                ],
                [
                    types.InlineKeyboardButton(
                        text='<',
                        callback_data=ChangeCollectionCallback(
                            collection_id=collection_id,
                            page=max(page - 1, 0),
                        ).pack(),
                    ),
                    types.InlineKeyboardButton(
                        text='>',
                        callback_data=ChangeCollectionCallback(
                            collection_id=collection_id,
                            page=min(page + 1, total_pages),
                        ).pack(),
                    ),
                ],
            ],
        ),
    )


@router.callback_query(ChangeCollectionCallback.filter())
async def change_page(
    callback: types.CallbackQuery,
    callback_data: ChangeCollectionCallback,
) -> None:
    await start_browse(
        callback,
        callback_data.collection_id,
        callback_data.page,
    )
