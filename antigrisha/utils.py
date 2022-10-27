import aiohttp
import io

from PIL import Image

from datetime import datetime


class TokenStorage:
    URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    def __init__(self, token):
        self._token = token

        self._iam = None
        self._last_updated = 0

    async def _update_iam(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.URL, json={'yandexPassportOauthToken': self._token}) as resp:
                self._iam = (await resp.json())['iamToken']
                self._last_updated = datetime.now().timestamp()

    async def fetch(self):
        if self._last_updated + 60 * 60 < datetime.now().timestamp():
            await self._update_iam()

        return self._iam


def img_to_png(data: bytes) -> bytes:
    img = Image.open(io.BytesIO(data)).convert('RGB')

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='png')

    return img_bytes.getvalue()


def tgs_to_png(data: bytes) -> bytes:
    raise NotImplementedError()
