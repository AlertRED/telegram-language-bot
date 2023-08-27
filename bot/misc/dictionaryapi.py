"""File for working with dictionaryapi
"""

import aiohttp
from typing import List
from http import HTTPStatus


async def get_definitions(term: str, maximum=4) -> List[str]:
    """Get list of definitions

    :param term: word for searching definitions
    :type term: str
    :param maximum: limit of returning definitions, defaults to 4
    :type maximum: int, optional
    :return: List of definitions
    :rtype: List[str]
    """
    definitions = []
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://api.dictionaryapi.dev/api/v2/entries/en/{term}',
        ) as resp:
            if resp.status == HTTPStatus.OK:
                count = 0
                words = await resp.json()
                for word in words:
                    for definition in word.get('meanings'):
                        count += 1
                        if maximum <= count:
                            return definitions
                        definitions.append(
                            definition.get('definitions')[0].get('definition'),
                        )
    return definitions
