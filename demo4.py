from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest, DeleteMessagesRequest
from telethon.tl.types import PeerChannel
import re

api_id = '25504149'
api_hash = '5cdd1680c1a4f7f49da84b7f6eed0ebb'
phone_number = '+998909044143'
channel_username = 'Nocommenttesting'

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    
    channel = await client.get_entity(channel_username)
    
    full_channel = await client.get_entity(PeerChannel(channel.id))
    if not full_channel.admin_rights or not full_channel.admin_rights.delete_messages:
        print("The account does not have permission to delete messages in this channel.")
        return
    
    history = await client(GetHistoryRequest(
        peer=channel,
        limit=1000,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))
    
    message_ids = [msg.id for msg in history.messages if msg.message and '#Day' in msg.message]
    
    print(f"Message IDs to be deleted: {message_ids}")
    
    if message_ids:
        try:
            chunk_size = 100
            for i in range(0, len(message_ids), chunk_size):
                chunk = message_ids[i:i + chunk_size]
                await client(DeleteMessagesRequest(id=chunk))
                print(f"Deleted message IDs: {chunk}")
        except Exception as e:
            print(f"An error occurred while deleting messages: {e}")
    else:
        print("No messages containing '#Day' found.")

with client:
    client.loop.run_until_complete(main())