import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

# КНОПКИ
keyboardMainMenu = types.InlineKeyboardMarkup(row_width=2)
kb_do_order = types.InlineKeyboardButton(text='Сделать заказ', callback_data='kb_do_order')
kb_price = types.InlineKeyboardButton(text='Прайс', callback_data='kb_price')
kb_actions = types.InlineKeyboardButton(text='Акции', callback_data='kb_actions')
kb_works = types.InlineKeyboardButton(text='Наши работы', callback_data='kb_works')
kb_about = types.InlineKeyboardButton(text='О нашей компании', callback_data='kb_about')
kb_info = types.InlineKeyboardButton(text='Инфо', callback_data='kb_info')
keyboardMainMenu.row(kb_do_order).add(kb_price, kb_actions, kb_works, kb_about).row(kb_info)

# КЛАВИАТУРА в ожидании обработки
keyboard_finish = types.InlineKeyboardMarkup(row_width=3)
kb_complete = types.InlineKeyboardButton(text='☑', callback_data='kb_complete')
kb_process = types.InlineKeyboardButton(text='⌛', callback_data='kb_process')
kb_denied = types.InlineKeyboardButton(text='❌', callback_data='kb_denied')
keyboard_finish.add(kb_complete, kb_process, kb_denied)

# КЛАВИАТУРА В ОБРАБОТКЕ


# Delete keyboard
keyboardDel = types.ReplyKeyboardRemove()

total_input = {
        'phone': None,
        'location': None,
        'problem': None,
        'username': None
    }

# Start message
@bot.message_handler(['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Приветственное сообщение: Бла-Бла-Бла", reply_markup=keyboardMainMenu)

# Secret command for delete keyboard
@bot.message_handler(['del_keyboard'])
def del_keyboard(message):
    bot.send_message(message.chat.id, 'Deleted', reply_markup=keyboardDel)


@bot.callback_query_handler(func=lambda callback: callback.data)
def answer_callback(callback):
    if callback.data == 'kb_do_order':
        # Start Other
        keyboardSendPhone = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb_send_phone = types.KeyboardButton(text='Отправить свой телефон', request_contact=True)
        kb_back = types.KeyboardButton('Отмена')
        keyboardSendPhone.add(kb_send_phone, kb_back)

        bot.send_message(callback.message.chat.id, 'В разработке')
        send = bot.send_message(callback.message.chat.id, 'Отправьте свой телефон, нажав соответствующую кнопку ниже.',
                                reply_markup=keyboardSendPhone)
        bot.register_next_step_handler(send, input_phone)

    # Button Price
    elif callback.data == 'kb_price':
        bot.send_message(callback.message.chat.id, 'Здесь будет прайс')

    # Button actions
    elif callback.data == 'kb_actions':
        bot.send_message(callback.message.chat.id, 'Здесь будут акции')

    # Button our works
    elif callback.data == 'kb_works':
        bot.send_message(callback.message.chat.id, 'Здесь будут работы с фото')

    # Button about
    elif callback.data == 'kb_about':
        bot.send_message(callback.message.chat.id, 'Здесь будет информация о компании')

    # Button info
    elif callback.data == 'kb_info':
        bot.send_message(callback.message.chat.id, 'Здесь будет "инфа"')

    # Button in report for set processed
    elif callback.data == 'kb_process':
        keyboard_processed = types.InlineKeyboardMarkup(row_width=2)
        keyboard_processed.add(kb_complete, kb_denied)
        bot.edit_message_text(     f'Пришла новая заявка!\n'
                                   f'ID: {callback.message.id}\n\n'
                                   f'Имя: {callback.message.from_user.first_name}\n'
                                   f"Username: @{total_input['username']}\n"
                                   f"Телефон: +{total_input['phone']}\n"
                                   f"Адрес: {total_input['location']}\n\n"
                                   f"Суть проблемы:\n{total_input['problem']}\n\n"
                                   f"Статус: в обработке ⌛\n"
                                   f"@{callback.from_user.username}", callback.message.chat.id, callback.message.id,
                                   reply_markup=keyboard_processed)

    # Button in report for set completed
    elif callback.data == 'kb_complete':

        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=(f'Пришла новая заявка!\n'
                                    f'ID: {callback.message.id}\n\n'
                                    f'Имя: {callback.message.from_user.first_name}\n'
                                    f"Username: @{total_input['username']}\n"
                                    f"Телефон: +{total_input['phone']}\n"
                                    f"Адрес: {total_input['location']}\n\n"
                                    f"Суть проблемы:\n{total_input['problem']}\n\n"
                                    f"Статус: выполнен ☑\n"
                                    f"@{callback.from_user.username}"))

    # Button in report for set denied
    elif callback.data == 'kb_denied':
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
                              text=f'Пришла новая заявка!\n'
                                   f'ID: {callback.message.id}\n\n'
                                   f'Имя: {callback.message.from_user.first_name}\n'
                                   f"Username: @{total_input['username']}\n"
                                   f"Телефон: +{total_input['phone']}\n"
                                   f"Адрес: {total_input['location']}\n\n"
                                   f"Суть проблемы:\n{total_input['problem']}\n\n"
                                   f"Статус: отказан ❌\n"
                                   f"@{callback.from_user.username}")

# Other past 2
def input_phone(message):

    if message.text == 'Отмена':
        bot.send_message(message.chat.id, 'Отменено', reply_markup=keyboardDel)
    else:
        total_input['phone'] = message.contact.phone_number
        bot.send_message(message.chat.id, 'Номер принят!', reply_markup=keyboardDel)
        send = bot.send_message(message.chat.id, 'Напишите свой адрес:')
        bot.register_next_step_handler(send, input_location, total_input)

# Other past 3
def input_location(message, total_input):
    total_input['location'] = message.text
    bot.send_message(message.chat.id, 'Адрес принят!')
    send = bot.send_message(message.chat.id, 'Опишите вашу проблему:')
    bot.register_next_step_handler(send, input_problem, total_input)

# Other past 4
def input_problem(message, total_input):

    total_input['problem'] = message.text
    bot.send_message(message.chat.id, 'Ваша заявка передана менеджеру. В скором времени с вами свяжутся.')

    bot.send_message(config.admin_chat, f'Пришла новая заявка!\n'
                                        f'ID: {message.id}\n\n'
                                        f'Имя: {message.from_user.first_name}\n'
                                        f'Username: @{message.from_user.username}\n'
                                        f"Телефон: +{total_input['phone']}\n"
                                        f"Адрес: {total_input['location']}\n\n"
                                        f"Суть проблемы:\n{total_input['problem']}\n\n"
                                        f"Статус: в ожидании обработки ⭕", reply_markup=keyboard_finish)
    total_input['username'] = message.from_user.username


print('Bot started!')
bot.infinity_polling()
