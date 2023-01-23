from aiogram import Dispatcher, Bot, types, executor
import random
import config as cfg
import logging
from db import Database
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# import bs4
# import sys
# import requests
# import os
# import time
# from threading import Thread

logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


# start command
@dp.message_handler(commands=["start"], commands_prefix="/")
async def welcome(message: types.Message):
    mark_up_menu = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="Entertainment😃", callback_data="entertainment_functions")
    button2 = types.InlineKeyboardButton(text="Technical⚙️", callback_data="technical_functions")
    mark_up_menu.add(button1, button2)
    await bot.send_sticker(message.chat.id,
                           sticker="CAACAgIAAxkBAAEHTzZjxsgF7CFUHnbM3-bMqUySqPJYowAC8AgAAo0D-EoDLJ8XHORyoC0E")
    await bot.send_message(message.chat.id,
                           f"<b>Hi there, <em>{message.from_user.first_name}</em> , my name 'Your bot name'!)</b>\nPlease, choose the types of function to start working😊",
                           parse_mode="html", reply_markup=mark_up_menu)


# ban user
@dp.message_handler(commands=['ban'], commands_prefix="!/", is_chat_admin=True)
async def ban(message: types.Message):
    if not message.reply_to_message:
        await message.answer("The command needs to be a reply to message!")
        return
    await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.answer(f"✅ User@{message.reply_to_message.from_user.username} was baned!")
    await message.delete()


# unban user
@dp.message_handler(commands=['unban'], commands_prefix="!/", is_chat_admin=True)
async def unban(message: types.Message):
    if not message.reply_to_message:
        await message.answer("The command needs to be a reply to message!")
        return
    await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.answer(f"✅ User @{message.reply_to_message.from_user.username} was forgiven and unbanned!")
    await message.delete()


# kick user
@dp.message_handler(commands=['kick'], commands_prefix="!/", is_chat_admin=True)
async def kick(message: types.Message):
    if not message.reply_to_message:
        await message.answer("The command needs to be a reply to message!")
        return
    await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.answer(f"✅ User @{message.reply_to_message.from_user.username} was kicked from chat!")
    await message.delete()


# mute user
@dp.message_handler(commands=['mute'], commands_prefix="!/", is_chat_admin=True)
async def mute(message: types.Message):
    if not message.reply_to_message:
        await message.answer("The command needs to be a reply to message!")
        return
    if len(message.text) < 6:
        await message.answer("❓ In order to mash up a user it is necessary to enter the time in seconds, example: /mute 60")
        return
    mute_time = int(message.text[6:])
    db.add_mute(user_id=message.reply_to_message.from_user.id, mute_time=mute_time)
    await message.delete()
    await message.reply_to_message.reply(f"🤐 User @{message.reply_to_message.from_user.username} was muted for {mute_time} секунд!")


# entertainment functions
@dp.callback_query_handler(text="entertainment_functions")
async def callback_function_type_entertainment(callback: types.CallbackQuery):
    markup_funcs = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton(text="object of bulling❤", callback_data="loser")
    button2 = types.InlineKeyboardButton(text="compliment victim🤩", callback_data="compliments")
    button3 = types.InlineKeyboardButton(text="what shall me to do?🤔", callback_data="random_action")
    button4 = types.InlineKeyboardButton(text="compliment from bot😏", callback_data="compliment_bot")
    button5 = types.InlineKeyboardButton(text="chat with admin", callback_data="admin_chat")
    markup_funcs.add(button1, button2, button3, button4, button5)
    if callback.message:
        if callback.data == "entertainment_functions":
            await bot.send_message(callback.message.chat.id, "Choose, how to entertain)", parse_mode="html",
                                   reply_markup=markup_funcs)


# technical functions
@dp.callback_query_handler(text="technical_functions")
async def callback_function_type_technical(callback: types.CallbackQuery):
    if callback.data == "technical_functions":
        await bot.send_message(callback.message.chat.id,
                               'To perform one of the technical functions, you must reply to the users message and...\n/ban - ban the user\n/unban - unban the user\n/kick - kick the user out of the chat\n/mute - mute the user', parse_mode="html")


@dp.callback_query_handler(text="loser")
async def callback_functions(callback: types.CallbackQuery):
    losers_list = ["list of losers)"]
    finish_list = str(random.choice(losers_list))
    if callback.message:
        if callback.data == "loser":
            await bot.send_message(callback.message.chat.id, f"Bulling object👉 {finish_list}")


@dp.callback_query_handler(text="compliments")
async def compliment_victim(callback: types.CallbackQuery):
    compliments_to_person_list = ["list of people"]
    final_compliments_to_person_list = str(random.choice(compliments_to_person_list))
    if callback.message:
        if callback.data == "compliments":
            await bot.send_message(callback.message.chat.id,
                                   f"And 2day our victim of compliments!👉 {final_compliments_to_person_list}")


@dp.callback_query_handler(text="random_action")
async def random_action(callback: types.CallbackQuery):
    actions_list = ["list of actons"]
    finish_actions_list = str(random.choice(actions_list))
    if callback.message:
        if callback.data == "random_action":
            await bot.send_message(callback.message.chat.id,
                                   f"Хэй, <em>{callback.from_user.first_name}</em>, may you wanna...{finish_actions_list} ",
                                   parse_mode="html")


@dp.callback_query_handler(text="compliment_bot")
async def compliment_from_bot(callback: types.CallbackQuery):
    compliments_from_bot_list = ["compliments list"]
    final_compliments_from_bot_list = str(random.choice(compliments_from_bot_list))
    if callback.message:
        if callback.data == "compliment_bot":
            await bot.send_message(callback.message.chat.id,
                                   f"<em>{callback.from_user.first_name}</em>!{final_compliments_from_bot_list}❤❤❤",
                                   parse_mode="html")


@dp.callback_query_handler(text="admin_chat")
async def chat_with_admin(callback: types.CallbackQuery):
    if callback.message:
        if callback.data == "admin_chat":
            await bot.send_message(callback.message.chat.id,
                                   f"<b>{callback.from_user.first_name}</b>Here you write a message to bot admin--> 'your bot or profile link'",
                                   parse_mode="html")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
