import aiohttp

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
