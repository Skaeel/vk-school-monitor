import asyncio

from src.client import VKCLient
from src.client.scripts import wall_get_script


async def main():
    async with VKCLient() as vk:
        all_posts = []
        result = await vk._execute(script=wall_get_script([278844800, 418648413]))
        for posts in result:
            for post in posts:
                all_posts.append({
                    "date": post["date"],
                    "id": post["id"],
                    "owner_id": post["owner_id"],
                    "text": post["text"]
                })
        print(all_posts)


if __name__ == "__main__":
    asyncio.run(main())