from typing import List
from http import HTTPStatus
import aiohttp


async def get_definitions(term: str, maximum=4) -> List[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://api.dictionaryapi.dev/api/v2/entries/en/{term}',
        ) as resp:
            if resp.status == HTTPStatus.OK:
                count = 0
                definitions = []
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
            return []
