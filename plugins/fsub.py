import logging
from database.fsub_db import Fsub_DB
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from info import CHANNELS, ADMINS, AUTH_CHANNEL, HOW_TO_VERIFY, CHNL_LNK, GRP_LNK, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, REQST_CHANNEL, SUPPORT_CHAT_ID, MAX_B_TN, IS_VERIFY, HOW_TO_VERIFY, FSUB_CHANNEL_1, FSUB_CHANNEL_2
from utils import temp, get_size, check_verification, get_token
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, Message

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
LINKS = None  # Store invite links for both channels
FSUB_TEMP = {}


@Client.on_chat_join_request(filters.chat(FSUB_CHANNEL_1) | filters.chat(FSUB_CHANNEL_2))
async def fetch_requests(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    date = message.date
    await Fsub_DB().add_user(id=user_id, name=name, username=username, date=date)
    file_id = FSUB_TEMP.get(user_id)

    if file_id:
        if IS_VERIFY and not await check_verification(bot, user_id):
            btn = [
                [
                    InlineKeyboardButton("Vᴇʀɪғʏ", url=await get_token(bot, user_id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)),
                    InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ]
            ]
            return await bot.send_message(
                chat_id=user_id,
                text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ! Kɪɴᴅʟʏ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</b>",
                protect_content=PROTECT_CONTENT,
                reply_markup=InlineKeyboardMarkup(btn)
            )

        files_ = await get_file_details(file_id)
        if not files_:
            return await bot.send_message(user_id, 'No such file exists.')

        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        caption = files.caption or title

        if CUSTOM_FILE_CAPTION:
            try:
                caption = CUSTOM_FILE_CAPTION.format(
                    file_name=title or '', file_size=size or '', file_caption=caption or ''
                )
            except Exception as e:
                logger.exception(e)

        dm = await bot.send_cached_media(
            chat_id=user_id,
            file_id=file_id,
            caption=caption,
            protect_content=False
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                ],
                [
                    InlineKeyboardButton("Bᴏᴛ Uᴩᴅᴀᴛᴇꜱ", url="https://t.me/+ixCkCbBsG6hkMzU1")
                ]
            ]
        )
        await dm.edit_reply_markup(buttons)
        FSUB_TEMP[user_id] = None


async def Force_Sub(bot: Client, message: Message, fileid=None):
    global LINKS
    if not (FSUB_CHANNEL_1 and FSUB_CHANNEL_2):
        return True

    try:
        user = await Fsub_DB().get_user(message.from_user.id)
        if user and str(user['id']) == str(message.from_user.id):
            return True
    except Exception as e:
        logger.exception(e)
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Error: {e}"
        )

    try:
        if not LINKS:
            link_1 = await bot.create_chat_invite_link(chat_id=FSUB_CHANNEL_1, creates_join_request=True)
            link_2 = await bot.create_chat_invite_link(chat_id=FSUB_CHANNEL_2, creates_join_request=True)
            LINKS = (link_1.invite_link, link_2.invite_link)

        user_channel_1 = await bot.get_chat_member(chat_id=FSUB_CHANNEL_1, user_id=message.from_user.id)
        user_channel_2 = await bot.get_chat_member(chat_id=FSUB_CHANNEL_2, user_id=message.from_user.id)

        if user_channel_1.status == "member" and user_channel_2.status == "member":
            return True
    except UserNotParticipant:
        buttons = [
            [InlineKeyboardButton("📢 Join Channel 1", url=LINKS[0])],
            [InlineKeyboardButton("📢 Join Channel 2", url=LINKS[1])],
            [InlineKeyboardButton("🔄 Retry", callback_data=f"retry#{fileid}")]
        ]
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You need to join both channels to access the content.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
          
import logging
from database.fsub_db import Fsub_DB
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id, get_bad_files
from info import (
    CHANNELS, ADMINS, AUTH_CHANNEL, HOW_TO_VERIFY, CHNL_LNK, GRP_LNK, LOG_CHANNEL, PICS, 
    BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, 
    SUPPORT_CHAT_ID, MAX_B_TN, IS_VERIFY, HOW_TO_VERIFY, FSUB_CHANNEL_1, FSUB_CHANNEL_2
)
from utils import temp, get_size, check_verification, get_token
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, Message

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
LINKS = None  # Global storage for invite links for both channels
FSUB_TEMP = {}

@Client.on_chat_join_request(filters.chat(FSUB_CHANNEL_1) | filters.chat(FSUB_CHANNEL_2))
async def fetch_requests(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    date = message.date
    await Fsub_DB().add_user(id=user_id, name=name, username=username, date=date)

    file_id = FSUB_TEMP.get(user_id)
    if file_id:
        # Verify the user if needed
        if IS_VERIFY and not await check_verification(bot, user_id):
            btn = [
                [
                    InlineKeyboardButton(
                        "Vᴇʀɪғʏ", url=await get_token(bot, user_id, f"https://telegram.me/{temp.U_NAME}?start=", file_id)
                    ),
                    InlineKeyboardButton("Hᴏᴡ Tᴏ Vᴇʀɪғʏ", url=HOW_TO_VERIFY)
                ]
            ]
            return await bot.send_message(
                chat_id=user_id,
                text="<b>Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ! Pʟᴇᴀsᴇ ᴠᴇʀɪғʏ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</b>",
                protect_content=PROTECT_CONTENT,
                reply_markup=InlineKeyboardMarkup(btn)
            )

        # Fetch and send file
        files_ = await get_file_details(file_id)
        if not files_:
            return await bot.send_message(user_id, 'No such file exists.')

        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        caption = files.caption or title

        if CUSTOM_FILE_CAPTION:
            try:
                caption = CUSTOM_FILE_CAPTION.format(
                    file_name=title or '', file_size=size or '', file_caption=caption or ''
                )
            except Exception as e:
                logger.exception(e)

        dm = await bot.send_cached_media(
            chat_id=user_id,
            file_id=file_id,
            caption=caption,
            protect_content=False
        )

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url=GRP_LNK),
                    InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url=CHNL_LNK)
                ],
                [
                    InlineKeyboardButton("Bᴏᴛ Uᴩᴅᴀᴛᴇꜱ", url="https://t.me/+ixCkCbBsG6hkMzU1")
                ]
            ]
        )
        await dm.edit_reply_markup(buttons)
        FSUB_TEMP[user_id] = None

@Client.on_message(filters.command("total_reqs") & filters.user(ADMINS))
async def total_reqs_num(bot, message):
    num = await Fsub_DB().total_users()
    return await message.reply_text(f"Total Requests: {num}")

@Client.on_message(filters.command("get_reqs") & filters.user(ADMINS))
async def get_all_reqs(bot, message):
    users = await Fsub_DB().get_all_users()
    out = "Users who sent requests are:\n\n"
    msg = await message.reply_text(f"{out}")
    if users is None:
        await msg.edit_text("No users found!")
        return

    async for user in users:
        out += f"ID: {user['id']}\nName: {user['name']}\nUserName: @{user['username']}\nDate Request Sent: {user['date']}\n\n"
    try:
        await msg.edit_text(f"{out}")
    except MessageTooLong:
        with open('requests.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('requests.txt', caption="List of requests")

@Client.on_message(filters.command("delete_reqs") & filters.user(ADMINS))
async def delete_reqs(bot, message):
    await Fsub_DB().purge_all_users()
    return await message.reply_text("Successfully deleted all requests from DB.")

@Client.on_message(filters.command("delete_req") & filters.user(ADMINS))
async def delete_req(bot, message):
    try:
        userid = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("Provide a user ID.\nExample: /delete_req 123456")
    user = await Fsub_DB().get_user(userid)
    name = user['name']
    await Fsub_DB().purge_user(userid)
    return await message.reply_text(f"Successfully deleted {name} from DB.")

@Client.on_message(filters.command("get_req") & filters.user(ADMINS))
async def get_req(bot, message):
    try:
        userid = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("Provide a user ID.\nExample: /get_req 123456")
    user = await Fsub_DB().get_user(userid)
    return await message.reply_text(f"Request Details:\nID: {user['id']}\nName: {user['name']}\nUserName: @{user['username']}\nDate of Request: {user['date']}")

async def Force_Sub(bot: Client, message: Message, fileid=None):
    global LINKS
    if not (FSUB_CHANNEL_1 and FSUB_CHANNEL_2):
        return True

    try:
        user = await Fsub_DB().get_user(message.from_user.id)
        if user and str(user['id']) == str(message.from_user.id):
            return True
    except Exception as e:
        logger.exception(e)

    try:
        user_channel_1 = await bot.get_chat_member(chat_id=FSUB_CHANNEL_1, user_id=message.from_user.id)
        user_channel_2 = await bot.get_chat_member(chat_id=FSUB_CHANNEL_2, user_id=message.from_user.id)

        if user_channel_1.status == "member" and user_channel_2.status == "member":
            return True
    except UserNotParticipant:
        if LINKS is None:
            invite_1 = await bot.create_chat_invite_link(FSUB_CHANNEL_1, creates_join_request=True)
            invite_2 = await bot.create_chat_invite_link(FSUB_CHANNEL_2, creates_join_request=True)
            LINKS = (invite_1.invite_link, invite_2)

        buttons = [
            [InlineKeyboardButton("Join Channel 1", url=LINKS[0])],
            [InlineKeyboardButton("Join Channel 2", url=LINKS[1])],
        ]

        if fileid:
            FSUB_TEMP[message.from_user.id] = fileid

        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Please join both channels to proceed.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
    
