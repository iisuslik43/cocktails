import os

import telebot

from dm import Action, apply_action, State
from nlu import parse_action

TOKEN = os.environ['TOKEN']


bot = telebot.TeleBot(TOKEN)
is_running = False


@bot.message_handler(commands=['start'])
def start_handler(message):
    global is_running
    if not is_running:
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Hello mate')
        bot.register_next_step_handler(msg, communicate, State.START, [])
        is_running = True


def communicate(message, state, ingredients):
    global is_running
    chat_id = message.chat.id
    text = message.text
    action_with_ingredient = parse_action(text)
    action = action_with_ingredient.action
    answer_message, next_state = apply_action(state, action_with_ingredient, ingredients)
    print(state, next_state, action, action_with_ingredient.ingredient, ingredients)
    if action != Action.SAY_GOODBYE:
        msg = bot.send_message(chat_id, answer_message)
        bot.register_next_step_handler(msg, communicate, next_state, ingredients)
        return
    bot.send_message(chat_id, answer_message)
    is_running = False


@bot.message_handler(content_types=['text'])
def text_handler(message):
    global is_running
    if not is_running:
        communicate(message, State.START, [])


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
