import asyncio

from src.client import VKCLient
from src.client.scripts import wall_get_script
from src.db.methods.user import add_user, add_users, get_tracked_users_last_post_dates


async def main():
    # async with VKCLient() as vk:
    #     all_posts = []
    #     result = await vk._execute(script=wall_get_script([278844800, 418648413]))
    #     for posts in result:
    #         for post in posts:
    #             all_posts.append({
    #                 "date": post["date"],
    #                 "id": post["id"],
    #                 "owner_id": post["owner_id"],
    #                 "text": post["text"]
    #             })
    #     print(all_posts)

    # await add_user(1, "123", "name", "surname", "922")

    # print(await get_id_last_post_date_map())

    async with VKCLient() as vk:
        print(await vk.wall_get(await get_tracked_users_last_post_dates()))

if __name__ == "__main__":
    asyncio.run(main())