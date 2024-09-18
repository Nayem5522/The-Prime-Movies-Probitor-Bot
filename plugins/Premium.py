# SPECIAL THANKS TO [Rishikesh Sharma] @Rk_botowner FOR THESE AMAZING CODES
# SPECIAL THANKS TO @DeletedFromEarth FOR MODIFYING THESE AMAZING CODES

from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, PREMIUM_LOGS
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("User removed successfully!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>Hey {user.mention},\n\nYour premium access has been removed. Thank you for using our service!</b>"
            )
        else:
            await message.reply_text("Unable to remove user. Was it a premium user ID?")
    else:
        await message.reply_text("Usage: /remove_premium user_id") 

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(user_id)  
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")            
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"Premium User Data:\n\nUser: {user}\nUser ID: <code>{user_id}</code>\nTime Left: {time_left_str}\nExpiry Date: {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"Hey {user},\n\nYou do not have any active premium plans. To purchase one, click below:",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Checkout Premium Plans", callback_data='seeplans')]]))			 

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Joining Time: %I:%M:%S %p") 
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        time = message.command[2] + " " + message.command[3]
        seconds = await get_seconds(time)
        
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  
            await db.update_user(user_data)  
            expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")         
            await message.reply_text(f"Premium added successfully!\n\nUser: {user.mention}\nUser ID: <code>{user_id}</code>\nPremium Access: {time}\nJoining Date: {current_time}\nExpiry Date: {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"Hey {user.mention},\nThank you for purchasing premium.\n\nPremium Access: {time}\nJoining Date: {current_time}\nExpiry Date: {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\nUser: {user.mention}\nUser ID: <code>{user_id}</code>\nPremium Access: {time}\nJoining Date: {current_time}\nExpiry Date: {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("Invalid time format. Please use '1 day', '1 hour', '1 min', '1 month', or '1 year'")
    else:
        await message.reply_text("Usage: /add_premium user_id time")

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"Premium User Data:\n\nUser: {user.mention}\nUser ID: <code>{user_id}</code>\nTime Left: {time_left_str}\nExpiry Date: {expiry_str_in_ist}")
        else:
            await message.reply_text("No premium data found in the database!")
    else:
        await message.reply_text("Usage: /get_premium user_id")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>Fetching...</i>")
    new = f"Premium Users List:\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ Expiry Time: %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"	 
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\nUser ID: {user['id']}\nExpiry Date: {expiry_str_in_ist}\nTime Left: {time_left_str}\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")



@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [[
	
        InlineKeyboardButton("📲 ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜᴇʀᴇ", url='https://t.me/Prime_Admin_Support_BOT')],[InlineKeyboardButton("❌ ᴄʟᴏꜱᴇ ❌", callback_data="close_data")
    ]]
    await message.reply_photo(photo="https://envs.sh/w6R.jpg", caption=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    
# SPECIAL THANKS TO [Rishikesh Sharma] @Rk_botowner FOR THESE AMAZING CODES
# SPECIAL THANKS TO @DeletedFromEarth FOR MODIFYING THESE AMAZING CODES 
