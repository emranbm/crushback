from telethon.tl.custom import Conversation


async def add_crush(username: str, conv: Conversation):
    await conv.send_message('/addcrush')
    await conv.get_response()
    await conv.send_message(f'@{username}')
    await conv.get_response()
