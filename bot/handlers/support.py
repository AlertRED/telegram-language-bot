from aiogram.fsm.context import FSMContext

from bot.constants import PERMANENT_SAVED_KEYS_IN_STATE


async def state_safe_clear(
    state: FSMContext,
    is_state: bool = True,
    is_data: bool = True,
    excluded_keys: list = None,
) -> None:
    if is_state:
        await state.set_state(None)
    if is_data:
        state_data = await state.get_data()
        _excluded_keys = excluded_keys or [] + PERMANENT_SAVED_KEYS_IN_STATE
        save_data = {
            k: v
            for k, v in state_data.items()
            if k in _excluded_keys
        }
        await state.set_data(save_data)
