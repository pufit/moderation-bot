import aiohttp
import base64
import typing

from antigrisha.config import Config
from antigrisha.utils import TokenStorage

tokens = TokenStorage(token=Config.OAUTH_TOKEN)

URL = 'https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze'


class ModerationResult(typing.NamedTuple):
    adult: float
    gruesome: float
    text: float
    watermarks: float


async def run_moderation(photo_bytes: bytes) -> ModerationResult:
    iam = await tokens.fetch()

    data = base64.b64encode(photo_bytes)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            URL,
            json={
                'folderId': Config.FOLDER_ID,
                'analyze_specs': [{
                    'content': data.decode(),
                    'features': [{
                        'type': 'CLASSIFICATION',
                        'classificationConfig': {
                            'model': 'moderation'
                        }
                    }]
                }]
            },
            headers={
                'Authorization': f'Bearer {iam}'
            }
        ) as resp:
            results = (await resp.json())['results'][0]['results'][0]['classification']['properties']

            dict_results = {}
            for r in results:
                dict_results[r['name']] = r['probability']

            return ModerationResult(
                adult=dict_results['adult'],
                gruesome=dict_results['gruesome'],
                text=dict_results['text'],
                watermarks=dict_results['watermarks'],
            )
