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
kb_info = types.InlineKeyboardButton(text='Инфо', callback_data='kb_info')
keyboardMainMenu.row(kb_do_order).add(kb_price, kb_actions, kb_works, kb_info)

# АДМИН ЧАТ
# КЛАВИАТУРА в ожидании обработки
keyboard_finish = types.InlineKeyboardMarkup(row_width=3)
kb_complete = types.InlineKeyboardButton(text='✔', callback_data='kb_complete')
kb_process = types.InlineKeyboardButton(text='⚙', callback_data='kb_process')
kb_denied = types.InlineKeyboardButton(text='❌', callback_data='kb_denied')
keyboard_finish.add(kb_complete, kb_process, kb_denied)

# КЛАВИАТУРА ДЛЯ ИЗМЕНЕНИЯ РЕЗУЛЬТАТА
keyboard_setresult = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
edit_kb_complete = types.KeyboardButton(text='✔')
edit_kb_process = types.KeyboardButton(text='⚙')
edit_kb_denied = types.KeyboardButton(text='❌')
keyboard_setresult.add(edit_kb_complete, edit_kb_process, edit_kb_denied)

# Other Message
keyboard_other_message = types.InlineKeyboardMarkup(row_width=1)
kb_main_menu = types.InlineKeyboardButton(text='Главное меню', callback_data='kb_main_menu')
keyboard_other_message.add(kb_do_order, kb_main_menu)

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
    bot.send_message(message.chat.id, '💯 Быстро и выгодно вернём жизнь вашему кондиционеру.\n\n'
                                      '❗ Компания "Холод ДВ"\n\n'
                                      '📌 Работаем с 2010 года!\n\n'
                                      '📌 Гарантия на выполненные работы!\n\n'
                                      '📌 Только обученные специалисты!\n\n'
                                      '📌 Работаем с профессиональным оборудованием и '
                                      'антибактериальными растворами!\n\n', reply_markup=keyboardMainMenu)


@bot.message_handler(['send_chat_id'])
def send_chat_id(message):
    bot.send_message(message.chat.id, message.chat.id)

# Secret command for delete keyboard
@bot.message_handler(['del_keyboard'])
def del_keyboard(message):
    bot.send_message(message.chat.id, 'Deleted', reply_markup=keyboardDel)


# @bot.message_handler(['set_result'])
# def set_result(message):
#     if message.chat.id == config.admin_chat:
#         send = bot.send_message(message.chat.id, 'Напишите ID заявки')
#         bot.register_next_step_handler(send, edit_report)
# def edit_report(message):
#     ID = message.text
#     try:
#         bot.edit_message_text(ID, '')

@bot.callback_query_handler(func=lambda callback: callback.data)
def answer_callback(callback):
    if callback.data == 'kb_do_order':
        # Start Other
        keyboardSendPhone = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb_send_phone = types.KeyboardButton(text='Отправить свой телефон', request_contact=True)
        kb_back = types.KeyboardButton('Отмена')
        keyboardSendPhone.add(kb_send_phone, kb_back)

        send = bot.send_message(callback.message.chat.id, 'Отправьте свой телефон, нажав соответствующую кнопку ниже.',
                                reply_markup=keyboardSendPhone)
        bot.register_next_step_handler(send, input_phone)

    # Button Price
    elif callback.data == 'kb_price':
        bot.send_message(callback.message.chat.id, '✔ Диагностика - 500р. / бесплатная '
                                                   '(если ремонт производит наша компания)\n\n'
                                                   '✔ Дозаправка - от 500р. (При необходимости)\n\n'
                                                   '✔ Чистка внутреннего блока - 1000р.\n\n'
                                                   '✔ Чистка внешнего блока - 1000р.\n\n'
                                                   '✔ Ремонт дренажной системы - 500р. / с полным разбором - 1000р.)\n\n'
                                                   '✔ Замена электро-деталей - цена обговаривается после осмотра',
                         reply_markup=keyboard_other_message)

    # Button actions
    elif callback.data == 'kb_actions':
        bot.send_message(callback.message.chat.id,
                         '''
Компания Холод ДВ 🤗\n
Запускает предсезонную АКЦИЮ по ОБСЛУЖИВАНИЮ  КОНДИЦИОНЕРОВ😊\n\n
 
❓Что включает техобслуживание кондиционера:\n
✅1. чистка внутреннего блока: фильтров, корпуса, теплообменника, вентилятора;\n
✅2. чистка внешнего блока;\n
✅3. проверка межблочных соединений электропитания;\n
✅4. очистку и дезинфекцию испарителя кондиционера;\n
✅5. проверка давления в системе;\n
✅6. прочистка дренажной системы: дренажного поддона, сливного шланга;\n
✅7. ➕ бонусом ПОЛНАЯ дозаправка кондиционера\n
 Стоимость комплексного ТО домашнего кондиционера ВСЕГО 2️⃣5️⃣0️⃣0️⃣ рублей💣💥! \n\n
 
 Акция продлится до 31 мая 2022 года. \n\n
 
Успейте записаться сейчас, количество мест ограничено.
                                                   ''',
                         parse_mode='Markdown')
        bot.send_message(callback.message.chat.id,
                         '''
В ТО кондиционеров входит:

*Профилактика внутреннего блока кондиционера:*

📌Диагностика и проверка правильности эксплуатации оборудования,
по параметрам, заявленным производителем;

📌Проверка работы кондиционера во всех режимах;

📌Очистка корпуса лицевой панели;

📌Чистка фильтров;

📌Чистка испарителя;

📌Проверка работы дренажных каналов для слива конденсата;

📌Чистка лопаток вентилятора;

📌Обработка дезинфицирующим составом.

Профилактика наружного блока кондиционера:

📌Внешний осмотр оборудования, проверка креплений, ограждений и
конструкций установки;

📌Измерение напряжения питающей сети, пусковых и рабочих токов
компрессора и электродвигателей вентиляторов (при необходимости);

📌Измерение давления всасывания и нагнетания в процессе работы,
при необходимости, дозаправка системы хладагентом

📌Гидравлическая и механическая чистка теплообменной
поверхности конденсатора, 

📌очистка корпуса наружного блока от
пыли и грязи;

📌Протяжка клемм электрических соединений;

📌Проверка режимов, устранение выявленных недостатков
оборудования;

💣После тех.обслуживания все характеристики по
производительности приближены к заводским.
                         ''', parse_mode='Markdown', reply_markup=keyboard_other_message)

    # Button our works
    elif callback.data == 'kb_works':
        bot.send_message(callback.message.chat.id, 'Мы работаем над этим разделом :)',
                         reply_markup=keyboard_other_message)

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
                                   f"Статус: в обработке ⚙\n"
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
                                    f"Статус: выполнен ✔\n"
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

    # Button Main Menu
    elif callback.data == 'kb_main_menu':
        bot.send_message(callback.message.chat.id, '💯 Быстро и выгодно вернём жизнь вашему кондиционеру.\n\n'
                                          '❗ Компания "Холод ДВ"\n\n'
                                          '📌 Работаем с 2010 года!\n\n'
                                          '📌 Гарантия на выполненные работы!\n\n'
                                          '📌 Только обученные специалисты!\n\n'
                                          '📌 Работаем с профессиональным оборудованием и '
                                          'антибактериальными растворами!\n\n', reply_markup=keyboardMainMenu)

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
    bot.send_message(message.chat.id, 'Ваша заявка передана менеджеру. В скором времени с вами свяжутся.',
                     reply_markup=keyboard_other_message)

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
