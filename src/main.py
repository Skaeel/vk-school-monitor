import asyncio

from src.client import VKCLient
from src.client.scripts import wall_get_any


async def main():
    async with VKCLient() as vk:
        result = await vk._execute(script=wall_get_any([278844800]))
        print(result)


if __name__ == "__main__":
    asyncio.run(main())