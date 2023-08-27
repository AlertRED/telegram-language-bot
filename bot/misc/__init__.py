from .instances import (
    __,
    bot,
    i18n,
    redis,
    dispatcher,
    arq_scheduler,
)

from .configure import setup
from .dictionaryapi import get_definitions


__all__ = (
    '__',
    'bot',
    'i18n',
    'redis',
    'dispatcher',
    'arq_scheduler',
    'setup',
    'get_commands',
    'get_definitions',
)
