import asyncio
import time
import logging

import aiohttp
from typing import Optional

from src.config import settings
from src.client.scripts import wall_get_script


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

    async def wall_get(self, domains_last_post_date_map: dict):
        if not domains_last_post_date_map:
            return []
        
        domains = domains_last_post_date_map.keys()
        chunks = [domains[i:i+25] for i in range(0, len(domains), 25)]
        all_new_posts = []

        async def _process_chunk(domains: list[int]):
            script = wall_get_script(domains)
            return await self._execute(script)
        
        async def _limited_process(domains: list[int]):
            async with self._semaphore:
                return await _process_chunk(domains)
            
        results = await asyncio.gather(*[_limited_process(c) for c in chunks])

        for posts in results:
            for post in posts:
                format_post = {
                    "date": post["date"],
                    "id": post["id"],
                    "owner_id": post["owner_id"],
                    "text": post["text"]
                }
                last_post_date = domains_last_post_date_map[format_post["owner_id"]]
                if last_post_date is None or format_post["date"] > last_post_date: # last_post_date в другом формате!
                    all_new_posts.append(format_post)
                else:
                    break

        return all_new_posts
            