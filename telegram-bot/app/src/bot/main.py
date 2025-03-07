from pathlib import Path
from redis import Redis
from telebot import TeleBot
from telebot.types import Message
from telebot import types
from telebot.apihelper import ApiException

import sys
import signal
import time

from core.cache import get_cache
from core.config import config
from src.api.api_service import APIService

bot = TeleBot(token=config.TELEGRAM_TOKEN)
api_service = APIService()

BASE_PATH = Path("src/bot/resources")

user_search_results = {}
user_current_position = {}

@bot.message_handler(commands=["start"])
def start(message: Message):
    image = open(BASE_PATH / Path("PRODLOGO.jpg"), "rb")

    bot.send_photo(
        message.chat.id, 
        caption=(
            f"Здравствуйте! \n"
            f"Это бот, который умеет выдавать поисковые результаты по менторам. \n\n"
            f"Для начала вам необходимо оставить поисковый запрос:\n"
            f"/search"
        ),
        photo=image
    )

@bot.message_handler(commands=["search"])
def search(message: Message):
    bot.send_message(message.chat.id, "Пожалуйста, введите поисковый запрос для поиска менторов:")
    bot.register_next_step_handler(message, process_search_query)

def process_search_query(message: Message):
    query = message.text
    user_id = message.from_user.id
    
    bot.send_message(message.chat.id, f"Ищем менторов по запросу: {query}...")
    
    try:
        mentors = api_service.get_search_result(query=query)
        if not mentors:
            bot.send_message(message.chat.id, "По вашему запросу ничего не найдено. Попробуйте другой запрос: /search")
            return
        
        user_search_results[user_id] = mentors
        user_current_position[user_id] = 0
        
        show_mentor_card(message.chat.id, user_id)
        
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при выполнении поиска: {str(e)}")

def show_mentor_card(chat_id, user_id):
    mentors = user_search_results.get(user_id, [])
    position = user_current_position.get(user_id, 0)
    
    if not mentors:
        bot.send_message(chat_id, "Нет данных для отображения. Начните новый поиск: /search")
        return
    
    mentor = mentors[position].get("mentor", {})
    
    text = f"Ментор #{position + 1} из {len(mentors)}\n\n"
    text += f"Имя: {mentor.get('name', 'Не указано')}\n"
    text += f"Почта: {mentor.get("email")}\n"
    text += f"Телеграм: {mentor.get("telegram")}\n"
    text += f"Релевантный опыт ментора: {mentor.get("expertise")}\n"
    text += f"Био: {mentor.get("bio")}\n"
    text += f"Рейтинг ментора: {mentor.get("score")} очков."

    markup = types.InlineKeyboardMarkup(row_width=2)
    prev_button = types.InlineKeyboardButton("<<", callback_data="prev")
    next_button = types.InlineKeyboardButton(">>", callback_data="next")
    
    buttons = []
    if position > 0:
        buttons.append(prev_button)
    if position < len(mentors) - 1:
        buttons.append(next_button)
    
    markup.add(*buttons)
    
    bot.send_message(chat_id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["prev", "next"])
def handle_navigation(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if user_id not in user_search_results or user_id not in user_current_position:
        bot.answer_callback_query(call.id, "Данные не найдены. Начните новый поиск.")
        return
    
    mentors = user_search_results[user_id]
    position = user_current_position[user_id]
    
    if call.data == "prev" and position > 0:
        user_current_position[user_id] = position - 1
    elif call.data == "next" and position < len(mentors) - 1:
        user_current_position[user_id] = position + 1
    
    bot.delete_message(chat_id, call.message.message_id)
    show_mentor_card(chat_id, user_id)
    
    bot.answer_callback_query(call.id)

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
