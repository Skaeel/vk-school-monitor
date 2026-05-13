import asyncio
import time
import logging

import aiohttp
from typing import Optional

from src.config import settings
from src.client.scripts import wall_get_any


logger = logging.getLogger(__name__)


class VKCLient:
    def __init__(self):
        self.token = settings.token.token.get_secret_value()
        self.rps = 3
        
        self._session: Optional[aiohttp.ClientSession] = None
        self._semaphore = asyncio.Semaphore(self.rps)
        self._rate_lock = asyncio.Lock()
        self._last_call_time = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()
            self._session = None

    async def _execute(self, script: str) -> dict:
        async with self._rate_lock:
            now = time.monotonic()

            if self._last_call_time:
                delay = (1 / self.rps) - (now - self._last_call_time)
                if delay > 0:
                    await asyncio.sleep(delay)
            else:
                self._last_call_time = now

            if not self._session:
                raise RuntimeError("Session is not active. Use VKClient as async context manager.")
            
            try:
                async with self._session.get(
                    "https://api.vk.com/method/execute",
                    params={
                        "v": "5.199",
                        "access_token": self.token,
                        "code": script,
                    },
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

                    return data.get("response", "")
                    

            except aiohttp.ClientError as e:
                logger.error(f"HTTP Request failed: {str(e)}")
                raise


async def main():
    async with VKCLient() as vk:
        result = await vk._execute(script=wall_get_any([278844800]))
        print(result)


if __name__ == "__main__":
    asyncio.run(main())