import telebot
from trello import TrelloApi

import time

import config

TEMPORARY_LISTS = {
    "wait_to_feedback": [],
    "wait_to_sharenew": [],
    "isadmin_debounce": False,
    "feedback_debounce": False,
    "sharenew_debounce": False,
    "change_news_subscription": False,
    "admission_management_debounce": False,
    "open_doors_registration": [],
    "courses_registration": []
}

bot = telebot.TeleBot(config.BOT_TOKEN)

trello = TrelloApi(config.TRELLO_KEY)
trello.set_token(config.TRELLO_TOKEN)


def start_actions(user: telebot.types.User, pseudo_action, method, Args):
    print(user.username, "action", pseudo_action)
    if pseudo_action == "start_message":
        buttons = {}
        buttons["🎓 Спеціальності 🎓"] = {"callback_data": "specialities"}
        buttons["↗️ Вступ до коледжу ↗️"] = {"callback_data": "enter_college"}
        buttons["🙇🏻‍♂️ Підготовчі курси 🙇🏻‍♂️"] = {"callback_data": "courses"}
        buttons["🗺️ Як добратись 🗺️"] = {"callback_data": "college_location"}
        buttons["📰 Останні новини 📰"] = {"callback_data": "news_list"}
        buttons["🔰 Студентська рада 🔰"] = {"callback_data": "stud_rada"}
        buttons["🛂 Приймальна комісія 🛂"] = {"callback_data": "admission_info"}
        buttons["🚪 День відкритих дверей 🚪"] = {"callback_data": "open_doors_days"}
        buttons["📥 Зворотній зв'язок 📥"] = {"callback_data": "feedback"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        # bot.send_message(chat_id=method.from_user.id, text=config.MESSAGES["start"], parse_mode="HTML")
        bot.send_message(chat_id=method.from_user.id, text="Я можу вам допомогти у таких напрямках:", parse_mode="HTML", reply_markup=markup)

    elif pseudo_action == "college_location":
        buttons = {}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        message_info = bot.send_message(chat_id=method.from_user.id, text=config.MESSAGES["location"], parse_mode="HTML")
        bot.send_location(chat_id=method.from_user.id, latitude=48.465542998205095, longitude=35.01998831756344, reply_markup=markup)

    elif pseudo_action == "admission_info":
        buttons = {}
        buttons["🗓 Графік роботи 🗓"] = {"callback_data": "enter_college_shedule"}
        buttons["☎️ Зв'язатись ☎️"] = {"callback_data": "admission_contact"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=method.from_user.id, text=config.MESSAGES["admission_info"], parse_mode="HTML", reply_markup=markup)
    
    elif pseudo_action == "specialities":
        buttons = {}
        buttons["171 Електроніка"] = {"callback_data": "specialities_info_171"}
        buttons["123 Комп’ютерна інженерія"] = {"callback_data": "specialities_info_123"}
        buttons["172 Електронні комунікації та радіотехніка"] = {"callback_data": "specialities_info_172"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        bot.send_message(chat_id=method.from_user.id, text="<b>В нас представлені такі спеціальності:</b>", reply_markup=telebot.util.quick_markup(buttons, row_width=1), parse_mode="HTML")

    elif "specialities_info" in pseudo_action:
        spec_num = str(pseudo_action).split("_")[2]

        buttons = {}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "delete_it"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=method.from_user.id, text=config.MESSAGES[f"spec_{spec_num}"], parse_mode="HTML", reply_markup=markup)

    elif pseudo_action == "enter_college":
        buttons = {}
        buttons["Правила прийому"] = {"callback_data": "enter_college_rules"}
        buttons["Перелік конкурсних предметів"] = {"callback_data": "enter_college_predmets"}
        buttons["Перелік документів для вступу"] = {"callback_data": "enter_college_documents"}
        buttons["Ліцензійний обсяг місць для навчання"] = {"callback_data": "enter_college_seats"}
        buttons["Розмір плати за навчання"] = {"callback_data": "enter_college_money"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=method.from_user.id, text="Для вступу до коледжу...", parse_mode="HTML", reply_markup=markup)

    elif pseudo_action == "enter_rules":
        pass
    elif pseudo_action == "entry_steps":
        pass
    elif pseudo_action == "open_doors_days":
        buttons = {}
        buttons["📝 Записатись на участь 📝"] = {"callback_data": "open_doors_register"}
        buttons["🛂 Приймальна комісія 🛂"] = {"callback_data": "admission_info"}
        buttons["🗺️ Як добратись 🗺️"] = {"callback_data": "college_location"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        dates_formate = ""
        for d in config.OPEN_DOORS_DAYS_DATES:
            dates_formate += f"\n{d[0]} - {d[1]}"

        # bot.send_message(chat_id=method.from_user.id, text=config.MESSAGES["pk_landing_sites"], parse_mode="HTML")
        bot.send_message(chat_id=method.from_user.id, text=f"{config.MESSAGES['pk_landing_sites']}\n\n<b>Наступні дати відкритих дверей:</b>{dates_formate}\n\nВи можете записатись прямо зараз!", parse_mode="HTML",
                         reply_markup=markup)

    elif pseudo_action == "preparation_courses":
        pass
    elif pseudo_action == "news_list":
        news_count = 0
        news_cards = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["News"])

        bot.send_message(chat_id=method.from_user.id, text="<b>Останні новини коледжу:</b>", parse_mode="HTML")

        for card in news_cards:
            news_count += 1
            new_card = trello.cards.get(card_id_or_shortlink=card["id"])

            split_name = str.split(new_card["name"], "/")
            date, title = split_name[0], split_name[1]
            telebot.util.antiflood(bot.send_message, chat_id=method.from_user.id,
                                   text=f"{telebot.formatting.hlink(content=title, url=new_card['cover']['scaled'][5]['url'])} [{telebot.formatting.hitalic(date)}]\n\n{str(new_card['desc'])}",
                                   parse_mode="HTML")

            if news_count > config.SEND_LAST_NEWS:
                break

        buttons = {}
        buttons["🔔 Підписатись на розсилку 🔔"] = {"callback_data": "subscribe"}
        buttons["🛑 Відписатись від розсилки 🛑"] = {"callback_data": "unsubscribe"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=method.from_user.id, text="<b>Доступні такі дії:</b>", parse_mode="HTML", reply_markup=markup)

    elif "request_info" in pseudo_action:
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.answer_callback_query(method.id, "Не так швидко...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        try:
            if check_on_admission(user.id)[0]:
                card_id = str.split(pseudo_action, '_')[2]

                bot.answer_callback_query(method.id, f"Запрос {card_id}.")

                request_card = trello.cards.get(card_id_or_shortlink=card_id)
                request_actions = list(trello.cards.get_action(card_id_or_shortlink=card_id))

                actions_amount = request_card['badges']['comments']

                request_actions.reverse()

                buttons = {}
                text_result = ""

                buttons["🕐 Поставити на очікування 🕐"] = {"callback_data": f"wait_admission_request_{request_card['id']}"}
                buttons["✅ Відкрити питання ✅"] = {"callback_data": f"open_admission_request_{request_card['id']}"}
                buttons["🚫 Закрити питання 🚫"] = {"callback_data": f"close_admission_request_{request_card['id']}"}
                buttons["🔄️ Оновити дані 🔄️"] = {"callback_data": f"update_admission_request_{request_card['id']}"}

                actions_result = ""
                if actions_amount <= 0:
                    actions_result = telebot.formatting.hitalic("Історія подій відсутня.")
                else:
                    actions_result = f"            <b>Історія подій ({actions_amount} дій):</b>"
                    for com in request_actions:
                        if com['type'] == "commentCard":
                            com_text = com['data']['text']
                            if ":" in com_text:
                                split_com = str.split(com_text, ": ")
                                actions_result += f"\n<b>{split_com[0]}:</b> <code>{split_com[1]}</code>"
                            else:
                                actions_result += f"\n        {telebot.formatting.hitalic(com_text)}"

                text_result += f"<b>Запит: <code>{request_card['name']}</code> (<code>{request_card['id']}</code>)</b>\n\n"

                text_result += f"<b>Статус:</b> {config.REQUESTS_EMOJIS[request_card['labels'][0]['id']]}\n\n"

                q_user, a_user = bot.get_chat_member(chat_id=int(request_card['name']), user_id=int(request_card['name'])), None
                if request_card['desc'] != "":
                   a_user = bot.get_chat_member(chat_id=int(request_card['desc']), user_id=int(request_card['desc']))

                text_result += f"<b>Запитуючий:</b> <code>{q_user.user.last_name} {q_user.user.first_name}</code> (<code>@{q_user.user.username}</code>, <code>{q_user.user.id}</code>)"
                text_result += "\n"

                if (request_card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Waiting"]) or not a_user:
                    text_result += f"<b>Відповідач:</b> <i>Відсутній</i>"
                else:
                    text_result += f"<b>Відповідач:</b> <code>{a_user.user.last_name} {a_user.user.first_name}</code> (<code>@{a_user.user.username}</code>, <code>{a_user.user.id}</code>)"

                text_result += f"\n\n{actions_result}"

                if Args["update_message"]:
                        bot.edit_message_text(chat_id=method.from_user.id, message_id=Args["update_message"], text=text_result, reply_markup=telebot.util.quick_markup(buttons, row_width=1), parse_mode="HTML")
                else:
                    bot.send_message(chat_id=method.from_user.id, text=text_result, reply_markup=telebot.util.quick_markup(buttons, row_width=1), parse_mode="HTML")
            else:
                bot.answer_callback_query(method.id, "🚫")
        except:
            bot.answer_callback_query(method.id, "Схоже ніяких змін не було.")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif "open_admission_request" in pseudo_action:
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.answer_callback_query(method.id, "Не так швидко...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        card_id = str.split(pseudo_action, "_")[3]
        request_card = trello.cards.get(card_id_or_shortlink=card_id)

        if check_on_admission(method.from_user.id)[1] == True:
            if request_card['labels'][0]['id'] != config.TRELLO_CONFIG["Labels"]["Request_Waiting"]:
                bot.answer_callback_query(method.id, "Ви не можете перевідкрити питання.")
            else:
                if request_card['desc'] == "":
                    trello.cards.delete_idLabel_idLabel(card_id_or_shortlink=card_id, idLabel=config.TRELLO_CONFIG["Labels"]["Request_Waiting"])
                    trello.cards.update(card_id_or_shortlink=card_id, desc=str(method.from_user.id), idLabels=[config.TRELLO_CONFIG["Labels"]["Request_Conversation"]])
                    trello.cards.new_action_comment(card_id_or_shortlink=card_id, text="Питання було відкрито.")

                    bot.send_message(chat_id=int(request_card['name']), text="<i>Питання було відкрито. Можете спілкуватись.</i>", parse_mode="HTML")
                    bot.send_message(chat_id=method.from_user.id, text="<i>Питання було відкрито. Можете спілкуватись.</i>", parse_mode="HTML")

                    bot.answer_callback_query(method.id, "Питання відкрито.")
                else:
                    bot.answer_callback_query(method.id, "На це питання вже хтось відповідає.")
        else:
            bot.answer_callback_query(method.id, "/start_admission_job")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif "wait_admission_request" in pseudo_action:
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.answer_callback_query(method.id, "Не так швидко...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        card_id = str.split(pseudo_action, "_")[3]
        request_card = trello.cards.get(card_id_or_shortlink=card_id)

        if check_on_admission(method.from_user.id)[1] == True:
            if request_card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Waiting"]:
                bot.answer_callback_query(method.id, "Питання вже на очікуванні.")
            else:
                if request_card['desc'] == str(method.from_user.id):
                    trello.cards.delete_idLabel_idLabel(card_id_or_shortlink=card_id, idLabel=config.TRELLO_CONFIG["Labels"]["Request_Conversation"])
                    trello.cards.update(card_id_or_shortlink=card_id, desc="", idLabels=[config.TRELLO_CONFIG["Labels"]["Request_Waiting"]])
                    trello.cards.new_action_comment(card_id_or_shortlink=card_id, text="Питання було поставлено на очікування.")

                    bot.send_message(chat_id=int(request_card['name']), text="<i>Питання було поставлено на очікування.</i>", parse_mode="HTML")
                    bot.send_message(chat_id=method.from_user.id, text="<i>Питання було поставлено на очікування.</i>", parse_mode="HTML")

                    bot.answer_callback_query(method.id, "Питання відкрито.")
                else:
                    bot.answer_callback_query(method.id, "На це питання вже хтось відповідає.")
        else:
            bot.answer_callback_query(method.id, "/start_admission_job")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif "close_admission_request" in pseudo_action:
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.answer_callback_query(method.id, "Не так швидко...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        card_id = str.split(pseudo_action, "_")[3]
        request_card = trello.cards.get(card_id_or_shortlink=card_id)
        is_admission_user = check_on_admission(user.id)[0]

        def process():
            trello.cards.delete_idLabel_idLabel(card_id_or_shortlink=card_id,
                                                idLabel=config.TRELLO_CONFIG["Labels"]["Request_Conversation"])
            trello.cards.update(card_id_or_shortlink=card_id,
                                idLabels=[config.TRELLO_CONFIG["Labels"]["Request_Closed"]])
            trello.cards.new_action_comment(card_id_or_shortlink=card_id, text="Питання було закрито.")
            bot.send_message(chat_id=int(request_card['name']), text="<i>Питання було закрито.</i>", parse_mode="HTML")
            if request_card['desc'] != "":
                bot.send_message(chat_id=int(request_card['desc']), text="<i>Питання було закрито.</i>",
                                 parse_mode="HTML")
            bot.answer_callback_query(method.id, "Питання закрито.")

        if request_card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Closed"]:
            bot.answer_callback_query(method.id, "Питання вже закрито.")
        else:
            if (int(request_card['name']) == user.id):
                process()
            elif ((request_card['desc'] == str(user.id)) and is_admission_user):
                if check_on_admission(method.from_user.id)[1] == True:
                    process()
                else:
                    bot.answer_callback_query(method.id, "/start_admission_job")
            else:
                bot.answer_callback_query(method.id, "Ви не маєте можливості зробити цю дію.")


        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif "admission_requests" in pseudo_action:
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.reply_to(message=method, text="Зачекайте будь ласка...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        if check_on_admission(user.id)[0]:
            includes_closed_requests = "+closed" in method.text
            list_buttons = {}

            requests_history = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["AdmissionRequests"])
            for request_card in requests_history:
                status_label = request_card['labels'][0]
                emoji = config.REQUESTS_EMOJIS[status_label['id']]
                label_id = status_label['id']
                actions_amount = request_card['badges']['comments']
                if label_id == config.TRELLO_CONFIG["Labels"]["Request_Closed"]:
                    if includes_closed_requests:
                        list_buttons[f"[{emoji}] {request_card['name']} ({actions_amount} дій)"] = {"callback_data": f"request_info_{request_card['id']}"}
                else:
                    list_buttons[f"[{emoji}] {request_card['name']} ({actions_amount} дій)"] = {
                        "callback_data": f"request_info_{request_card['id']}"}

            markup = telebot.util.quick_markup(list_buttons, row_width=1)
            bot.send_message(chat_id=method.from_user.id, text="<b>Ось список запросів:</b>", reply_markup=markup,
                             parse_mode="HTML")
        else:
            bot.reply_to(message=method, text="🚫")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif pseudo_action == "start_admission_job":
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.reply_to(message=method, text="Зачекайте будь ласка...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        user_card = check_on_admission(user.id)[0]

        if user_card:
            is_already_active = False

            for l in user_card["labels"]:
                if l["id"] == config.TRELLO_CONFIG["Labels"]["Admission_Active"]:
                    is_already_active = True

            if is_already_active:
                bot.reply_to(message=method, text="Ви вже активні для відповідей.")
            else:
                new_name = user_card['desc']
                if new_name == None or new_name == "":
                    new_name = f"{user.last_name} {user.first_name}"
                trello.cards.update(card_id_or_shortlink=user_card["id"], desc=new_name, idLabels=[config.TRELLO_CONFIG["Labels"]["Admission_Active"]])
                bot.send_message(chat_id=user.id, text=f"Ви тепер активні для відповідей як <code>{new_name}</code>.\nВведіть /admission_requests для перегляду запросів.\nВведіть /end_admission_job для завершення роботи.", parse_mode="HTML")

        else:
            bot.reply_to(message=method, text="🚫")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif pseudo_action == "end_admission_job":
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.reply_to(message=method, text="Зачекайте будь ласка...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        user_card = check_on_admission(user.id)[0]

        if user_card:
            is_already_active = False

            for l in user_card["labels"]:
                if l["id"] == config.TRELLO_CONFIG["Labels"]["Admission_Active"]:
                    is_already_active = True

            if is_already_active:
                # trello.cards.update(card_id_or_shortlink=user_card["id"], idLabels=[])
                trello.cards.delete_idLabel_idLabel(card_id_or_shortlink=user_card["id"], idLabel=config.TRELLO_CONFIG["Labels"]["Admission_Active"])
                bot.reply_to(message=method, text="Ви тепер неактивні для відповідей.")
            else:
                bot.reply_to(message=method, text="Ви й так неактивні для відповідей.")

        else:
            bot.reply_to(message=method, text="🚫")

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif pseudo_action == "subscribe":
        if TEMPORARY_LISTS["change_news_subscription"] == True:
            bot.answer_callback_query(method.id, "Зачекайте будь ласка...")
            return
        TEMPORARY_LISTS["change_news_subscription"] = True

        have_subscription = None

        users = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["NewsSubscribers"])
        for user_card in users:
            user_id = int(user_card["name"])
            if user_id == method.from_user.id:
                have_subscription = user_card["id"]

        if have_subscription:
            bot.answer_callback_query(method.id, "Ви вже підписані на розсилку")
        else:
            trello.cards.new(name=str(method.from_user.id), idList=config.TRELLO_CONFIG["Lists"]["NewsSubscribers"])
            bot.answer_callback_query(method.id, "Підписано на розсилку новин")

        time.sleep(5)
        TEMPORARY_LISTS["change_news_subscription"] = False

    elif pseudo_action == "unsubscribe":
        if TEMPORARY_LISTS["change_news_subscription"] == True:
            bot.answer_callback_query(method.id, "Зачекайте будь ласка...")
            return
        TEMPORARY_LISTS["change_news_subscription"] = True

        is_have_changes = False

        users = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["NewsSubscribers"])
        for user_card in users:
            user_id = int(user_card["name"])
            if user_id == method.from_user.id:
                trello.cards.delete(card_id_or_shortlink=user_card["id"])
                is_have_changes = True

        if is_have_changes:
            bot.answer_callback_query(method.id, "Розсилка новин призупинена")
        else:
            bot.answer_callback_query(method.id, "Ви не підписані на розсилку")

        time.sleep(5)
        TEMPORARY_LISTS["change_news_subscription"] = False

    elif pseudo_action == "feedback":
        if TEMPORARY_LISTS["feedback_debounce"] == True:
            bot.reply_to(message=method, text=telebot.formatting.hitalic("Не так швидко..."), parse_mode="HTML")
            return
        TEMPORARY_LISTS["feedback_debounce"] = True

        if check_on_feedback(method.from_user.id):
            bot.reply_to(message=method,
                         text=telebot.formatting.hitalic("Ви вже маєте активний запит на зворотній зв'язок."),
                         parse_mode="HTML")

        else:
            inline_buttons, button_index = {}, 0

            for info in config.FEEDBACK_VARIANTS:
                inline_buttons[info[1]] = {"callback_data": f"feedback_type_{info[0]}_{button_index}"}
                button_index += 1

            inline_buttons["❌ Скасувати ❌"] = {"callback_data": "cancel_feedback"}

            feedback_markup = telebot.util.quick_markup(inline_buttons, row_width=1)
            new_message = bot.send_message(chat_id=method.from_user.id,
                                           text="Спочатку оберіть тему, на яку хочете написати зворотній зв'язок.\nНатисніть 'скасувати' щоб скасувати дію.",
                                           reply_markup=feedback_markup)
            TEMPORARY_LISTS["wait_to_feedback"].append([method.from_user.id, new_message.message_id, None, None])

        time.sleep(1)
        TEMPORARY_LISTS["feedback_debounce"] = False

    elif pseudo_action == "permissions":
        if TEMPORARY_LISTS["isadmin_debounce"]:
            bot.reply_to(message=method, text=telebot.formatting.hitalic("Не так швидко..."), parse_mode="HTML")
            return
        TEMPORARY_LISTS["isadmin_debounce"] = True

        result_text = ""

        result_text += "<b>Адміністратор:</b> "
        if check_on_admin(method.from_user.id):
            result_text += "✅\n/share_new"
        else:
            result_text += "❌"

        result_text += "\n<b>Приймальна комісія:</b> "
        if check_on_admission(method.from_user.id)[0]:
            result_text += "✅\n/admission_requests (+closed)\n/start_admission_job\n/end_admission_job"
        else:
            result_text += "❌"

        bot.reply_to(message=method, text=result_text, parse_mode="HTML")

        time.sleep(2)
        TEMPORARY_LISTS["isadmin_debounce"] = False

    elif pseudo_action == "sharenew":
        if TEMPORARY_LISTS["sharenew_debounce"] == True:
            bot.reply_to(message=method, text=telebot.formatting.hitalic("Не так швидко..."), parse_mode="HTML")
            return
        TEMPORARY_LISTS["sharenew_debounce"] = True

        if check_on_admin(method.from_user.id):
            articles_for_share, inline_buttons = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["News"]), {}

            for new_card in articles_for_share:
                split_name = str.split(new_card["name"], "/")
                date, title = split_name[0], split_name[1]

                inline_buttons[f"[{date}] {title}"] = {"callback_data": f"share_new_{new_card['id']}"}

            inline_buttons["❌ Скасувати ❌"] = {"callback_data": "cancel_sharenew"}

            share_markup = telebot.util.quick_markup(inline_buttons, row_width=1)
            new_message = bot.send_message(chat_id=method.from_user.id, text="Оберіть статью яку ви хочете поширити:",
                                           reply_markup=share_markup)

            TEMPORARY_LISTS["wait_to_sharenew"].append([method.from_user.id, new_message.message_id, None, None, None])

        else:
            bot.reply_to(message=method, text="🚫")

        time.sleep(1)
        TEMPORARY_LISTS["sharenew_debounce"] = False


def share_new(card_id):
    new_card = trello.cards.get(card_id_or_shortlink=card_id)
    users = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["NewsSubscribers"])

    split_name = str.split(new_card["name"], "/")
    date, title = split_name[0], split_name[1]

    markup = share_markup = telebot.util.quick_markup({"🛑 Зупинити розсилку 🛑": {"callback_data": "unsubscribe"}}, row_width=1)

    for user_card in users:
        user_id = int(user_card["name"])
        telebot.util.antiflood(bot.send_message, chat_id=user_id, text=f"{telebot.formatting.hlink(content=title, url=new_card['cover']['scaled'][5]['url'])} [{telebot.formatting.hitalic(date)}]\n\n{str(new_card['desc'])}", parse_mode="HTML", reply_markup=markup)


def check_on_active_request(user_id, include_waiting):
    requests = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["AdmissionRequests"])
    for card in requests:
        card_user_id = int(card['name'])
        if card_user_id == user_id:
            if include_waiting:
                if (card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Conversation"]) or (card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Waiting"]):
                    return card
            else:
                if card['labels'][0]['id'] == config.TRELLO_CONFIG["Labels"]["Request_Conversation"]:
                    return card

def check_on_sharenew(user_id):
    for info in TEMPORARY_LISTS["wait_to_sharenew"]:
        if info[0] == user_id:
            return info


def check_on_feedback(user_id):
    for info in TEMPORARY_LISTS["wait_to_feedback"]:
        if info[0] == user_id:
            return info


def check_on_admin(user_id):
    admin_users = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["Admins"])

    for card in admin_users:
        if int(card["name"]) == user_id:
            return card

    return False


def check_on_admission(user_id):
    admin_users = trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["Admission"])

    for card in admin_users:
        if int(card["name"]) == user_id:
            is_active = False
            if len(card['labels']) > 0:
                is_active = True
            return card, is_active

    return False, False


def check_on_opendoors_reg(user_id):
    for info in TEMPORARY_LISTS["open_doors_registration"]:
            if info[0] == user_id:
                return info
    return False

def check_on_courses_reg(user_id):
    for info in TEMPORARY_LISTS["courses_registration"]:
            if info[0] == user_id:
                return info
    return False


@bot.message_handler(commands=["perms", "check_permissions", "permissions"])
def check_permissions(message: telebot.types.Message):
    start_actions(message.from_user, "permissions", message, {})


@bot.message_handler(commands=["start"])
def send_help(message: telebot.types.Message):
    if message.message_id <= 1:
        bot.send_message(chat_id=message.chat.id, text=config.MESSAGES["start"], parse_mode="HTML")
    start_actions(message.from_user, "start_message", message, {})


@bot.message_handler(commands=["admission_requests", "admission_requests+closed"])
def send_help(message: telebot.types.Message):
    start_actions(message.from_user, "admission_requests", message, {})


@bot.message_handler(commands=["start_admission_job"])
def send_help(message: telebot.types.Message):
    start_actions(message.from_user, "start_admission_job", message, {})


@bot.message_handler(commands=["end_admission_job"])
def send_help(message: telebot.types.Message):
    start_actions(message.from_user, "end_admission_job", message, {})


@bot.message_handler(commands=["site"])
def send_dev_name(message):
    bot.reply_to(message=message, text=config.COLLEGE_SITE)


@bot.message_handler(commands=["news", "news_list"])
def send_dev_name(message):
    start_actions(message.from_user, "news_list", message, {})


@bot.message_handler(commands=["feedback", "report"])
def feedback(message: telebot.types.Message):
    start_actions(message.from_user, "feedback", message, {})


@bot.message_handler(commands=["share_new"])
def send_news(message: telebot.types.Message):
    start_actions(message.from_user, "sharenew", message, {})


@bot.message_handler(func=lambda message: True)
def every_message(message: telebot.types.Message):
    print(message.from_user.username, "message", message.text)

    checked_on_admission = check_on_admission(message.from_user.id)[0]
    checked_on_feedback = check_on_feedback(message.from_user.id)
    checked_on_active_request = check_on_active_request(message.from_user.id, False)
    checked_on_opendoors_reg = check_on_opendoors_reg(message.from_user.id)
    checked_on_courses_reg = check_on_courses_reg(message.from_user.id)

    if checked_on_courses_reg:
        if checked_on_courses_reg[1] == True:
            if checked_on_courses_reg[2] == None:
                new_text = str(message.text).replace(" ", "")

                if len(new_text) <= 15:
                    checked_on_courses_reg[2] = new_text
                    bot.send_message(chat_id=message.chat.id, text=f"Напишіть своє прізвище та ім'я:")

                else: bot.reply_to(message=message, text="Номер не може бути більше 10 символів.")

            elif checked_on_courses_reg[3] == None:
                splitted = str(message.text).split(" ")

                if len(message.text) <= 35:
                    if len(splitted) == 2:
                        checked_on_courses_reg[3] = message.text

                        markup = telebot.util.quick_markup({ "✅ Підтвердити ✅": {"callback_data": "courses_register_accept2"}, "🚫 Скасувати 🚫": {"callback_data": "courses_register_decline"} }, row_width=2)
                        bot.send_message(chat_id=message.chat.id, text=f"Ви дійсно хочете забронювати місце на підготовчих курсах? <code>{checked_on_courses_reg[2]}</code>, <code>{checked_on_courses_reg[3]}</code>", reply_markup=markup, parse_mode="HTML")

                    else: bot.reply_to(message=message, text="В повідомлені має бути тільки ім'я і фамілія через пробіл.")
                    

                else: bot.reply_to(message=message, text="Повідомлення не може бути більше 35 символів.")

    if checked_on_opendoors_reg:
        if checked_on_opendoors_reg[1] == True:
            if checked_on_opendoors_reg[2] == None:
                new_text = str(message.text).replace(" ", "")

                if len(new_text) <= 15:
                    checked_on_opendoors_reg[2] = new_text
                    bot.send_message(chat_id=message.chat.id, text=f"Напишіть своє прізвище та ім'я:")

                else: bot.reply_to(message=message, text="Номер не може бути більше 10 символів.")

            elif checked_on_opendoors_reg[3] == None:
                splitted = str(message.text).split(" ")

                if len(message.text) <= 35:
                    if len(splitted) == 2:
                        checked_on_opendoors_reg[3] = message.text

                        day_info = config.OPEN_DOORS_DAYS_DATES[config.ACTUAL_OPEN_DOORS_DAY-1]

                        markup = telebot.util.quick_markup({ "✅ Підтвердити ✅": {"callback_data": "open_doors_register_accept2"}, "🚫 Скасувати 🚫": {"callback_data": "open_doors_register_decline"} }, row_width=2)
                        bot.send_message(chat_id=message.chat.id, text=f"Ви дійсно хочете зареєструватись на найближчий День відкритих дверей? <code>{day_info[0]} - {day_info[1]}</code>, <code>{checked_on_opendoors_reg[2]}</code>, <code>{checked_on_opendoors_reg[3]}</code>", reply_markup=markup, parse_mode="HTML")

                    else: bot.reply_to(message=message, text="В повідомлені має бути тільки ім'я і фамілія через пробіл.")
                    

                else: bot.reply_to(message=message, text="Повідомлення не може бути більше 35 символів.")

    if checked_on_active_request:
        admission_reply_markup = telebot.util.quick_markup({"🚫 Закрити питання 🚫": {"callback_data": f"close_admission_request_{checked_on_active_request['id']}"}})
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id, reaction=[telebot.types.ReactionTypeEmoji("👍")], is_big=False)
        bot.send_message(chat_id=int(checked_on_active_request['desc']), text=f"<b>{message.from_user.first_name}:</b> <code>{message.text}</code>", reply_markup=admission_reply_markup, parse_mode="HTML")
        trello.cards.new_action_comment(card_id_or_shortlink=checked_on_active_request['id'], text=f"{message.from_user.first_name}: {message.text}")

    if checked_on_admission:
        for card in trello.lists.get_card(idList=config.TRELLO_CONFIG['Lists']['AdmissionRequests']):
            if card["labels"][0]['id'] == config.TRELLO_CONFIG['Labels']['Request_Conversation'] and card['desc'] == checked_on_admission['name']:
                admission_reply_markup = telebot.util.quick_markup({"✅ Питання вирішено ✅": {"callback_data": f"close_admission_request_{card['id']}"}})
                bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,
                                         reaction=[telebot.types.ReactionTypeEmoji("👍")], is_big=False)
                bot.send_message(chat_id=int(card['name']), text=f"<b>{checked_on_admission['desc']}:</b> <code>{message.text}</code>", reply_markup=admission_reply_markup, parse_mode="HTML")
                trello.cards.new_action_comment(card_id_or_shortlink=card['id'], text=f"{checked_on_admission['desc']}: {message.text}")
                break

    if checked_on_feedback and checked_on_feedback[2] != None:
        user = message.from_user
        chat_id = checked_on_feedback[0]
        message_id = checked_on_feedback[1]
        feedback_type = checked_on_feedback[2]
        str_feedback_type = checked_on_feedback[3]

        user_link = f"https://t.me/{user.username}"
        user_info = f"@{user.username} ({user.id}) | {user.last_name} {user.first_name}"
        feedback_text = message.text


        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"Зворотній зв'язок надіслано.\nТип повідомлення: `{str_feedback_type}`\nПовідомлення: `{feedback_text}`", parse_mode="Markdown")
        bot.send_message(chat_id=config.DEVELOPER_USER_ID, text=f"❗**Надіслано зворотній зв'язок:**\n**Користувач:** `{user_info}` | {user_link}\nТип повідомлення: `{str_feedback_type}`\nПовідомлення: `{feedback_text}`", parse_mode="Markdown")

        trello.cards.new(name=user_info, desc=feedback_text, idList=config.TRELLO_CONFIG["Lists"]["Feedbacks"], urlSource=user_link, pos=0, idLabels=[config.TRELLO_CONFIG["Labels"][f"Feedback_Type_{feedback_type}"]])

        for waiting in TEMPORARY_LISTS["wait_to_feedback"]:
            if waiting[0] == message.from_user.id:
                TEMPORARY_LISTS["wait_to_feedback"].remove(waiting)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call: telebot.types.CallbackQuery):
    print(call.from_user.username, "call", call.data)

    if call.data == "feedback":
        start_actions(call.from_user, "feedback", call, {})
        bot.answer_callback_query(call.id, "Зворотній зв'язок.")

    elif call.data == "admission_info":
        start_actions(call.from_user, "admission_info", call, {})
        bot.answer_callback_query(call.id, "Приймальна комісія.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == "open_doors_days":
        start_actions(call.from_user, "open_doors_days", call, {})
        bot.answer_callback_query(call.id, "День відкритих дверей.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == "subscribe":
        start_actions(call.from_user, "subscribe", call, {})

    elif call.data == "unsubscribe":
        start_actions(call.from_user, "unsubscribe", call, {})

    elif call.data == "enter_college":
        start_actions(call.from_user, call.data, call, {})
        bot.answer_callback_query(call.id, "День відкритих дверей.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == "to_start":
        start_actions(call.from_user, "start_message", call, {})
        bot.answer_callback_query(call.id, "Повернутись.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    elif call.data == "delete_it":
        bot.answer_callback_query(call.id, "Повернутись.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


    elif call.data == "stud_rada":
        bot.answer_callback_query(call.id, "Студентська рада.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        buttons = {}
        buttons["Склад студентської ради"] = {"callback_data": "stud_rada_sklad"}
        buttons["Новинний канал студентської ради"] = {"callback_data": "stud_rada_channel"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=call.from_user.id, text=config.MESSAGES["stud_rada"], reply_markup=markup, parse_mode="HTML")

    elif "stud_rada_" in call.data:
        bot.answer_callback_query(call.id, "Студентська рада.")
        
        buttons = {}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "delete_it"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        text_lol = ""
        version = str(call.data).split("_")[2]
        if version == "sklad": text_lol = "<i><b>26 жовтня 2023 року</b> відбулися збори Студентської Ради нашого коледжу, де було прийнято важливі рішення та обрано представників, які будуть сприяти розвитку студентського життя.</i>\n\n<b>Голова:</b>\n<code>Камлук Артем</code>\n\n<b>Заступник голови:</b>\n<code>Кочарян Карен</code>\n\n<b>Секретар:</b>\n<code>Сошенков Микита</code>\n\n<b>Комітет освіти і науки:</b>\n<code>Дрогуль Владислав</code>\n\n<b>Комітет прес-центру, соціально-правових питань та внутрішніх справ:</b>\n<code>Коваленко Максим</code>, <code>Лета Тимур</code>\n\n<b>Комітет спорту та здоров'я:</b>\n<code>Рубанов Богдан</code>, <code>Єфімов Олександр</code>, <code>Власенко Олексій</code>\n\n<b>Комітет туристичного та художньо-естетичного напрямів:</b>\n<code>Кочарян Карен</code>, <code>Скарлош Данило</code>, <code>Коваленко Дмитро</code>"
        elif version == "channel": text_lol = "https://t.me/+XQwI9xC5rucwMjQy"

        bot.send_message(chat_id=call.from_user.id, text=text_lol, reply_markup=markup, parse_mode="HTML")


    elif "request_info" in call.data:
        start_actions(call.from_user, call.data, call, {"update_message": False})

    elif "close_admission_request" in call.data:
        start_actions(call.from_user, call.data, call, {})

    elif "open_admission_request" in call.data:
        start_actions(call.from_user, call.data, call, {})

    elif "wait_admission_request" in call.data:
        start_actions(call.from_user, call.data, call, {})

    elif "update_admission_request" in call.data:
        card_id = str.split(call.data, '_')[3]
        start_actions(call.from_user, f"request_info_{card_id}", call, {"update_message": call.message.message_id})

    elif "enter_college_" in call.data:
        bot.answer_callback_query(call.id, "Інформація про вступ.")

        version = str(call.data).split("_")[2]
        text_lol = ""
        if version == "predmets": text_lol = "Перелік конкурсних предметів: \n<b>База 9 класів(БСО):</b> \nіндивідуальна усна співбесіда з математики та української мови \n<b>База 11 класів(ПЗСО, КР):</b> \nіндивідуальна усна співбесіда з математики та української мови. \nЗамість проходження співбесіди для вступу на основі ПЗСО, КР вступник може подати результати: \n - Зовнішнього незалежного оцінювання 2020-2021 років у будь-яких комбінаціях \n - Національного мультипредметного теста 2022 року; \n - Національного мультипредметного теста 2023 року."
        elif version == "rules": text_lol = "https://pk.kre.dp.ua/порядок-та-правила-прийому"
        elif version == "documents": text_lol = "<b>Перелік документів для подачі (у випадку зарахування на навчання):</b> \n - 6 кольорових фотокарток розміром 3×4 см; \n - пільгові документи (документи, щодо підтвердження пільг); \n - характеристика; \n - медична довідка (форма 086-О); \n - довідка про щеплення форма 063 (копія); \n - епікриз на підлітка."
        elif version == "seats": text_lol = "Перелік акредитованих освітньо-професійних програм та конкурсних пропозицій, за якими здійснюється прийом на навчання, і їх ліцензійний обсяг: \n - обслуговування комп’ютерних систем і мереж: 50 осіб (на базі БСО); \n - конструювання, виробництво та технічне обслуговування радіотехнічних пристроїв: 65 осіб (на базі БСО) \n - конструювання, виготовлення та технічне обслуговування виробів електронної техніки: 25 осіб (на базі БСО); \n - монтаж, технічне обслуговування і ремонт обладнання радіозв’язку, радіомовлення та телебачення: 25 осіб (на базі БСО)."
        elif version == "money": text_lol = "9800 грн / рік навчання + поправки на інфляцію"
        elif version == "shedule": text_lol = "Графік роботи \nпонеділок – п’ятниця: 09:00 – 16:00"

        buttons = {}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "delete_it"}
        markup = telebot.util.quick_markup(buttons, row_width=1)

        bot.send_message(chat_id=call.from_user.id, text=text_lol, reply_markup=markup, parse_mode="HTML")

    elif call.data == "specialities":
        bot.answer_callback_query(call.id, "Спеціальності.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start_actions(call.from_user, call.data, call, {})

    elif "specialities_info" in call.data:
        bot.answer_callback_query(call.id, "Інформація про спеціальність.")
        start_actions(call.from_user, call.data, call, {})



    elif call.data == "courses":
        bot.answer_callback_query(call.id, "Підготовчі курси.")
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        buttons = {}
        buttons["📝 Забронювати місце в групі 📝"] = {"callback_data": "courses_register"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)
        
        bot.send_message(chat_id=call.from_user.id, text=f"Готуємо до успішного складання вступних випробувань до коледжу радіоелектроніки та інших навчальних закладів\n<b>Термін навчання:</b> <code>6 місяців</code>\nhttps://landing.kre.dp.ua/courses", reply_markup=markup, parse_mode="HTML")

    elif call.data == "courses_register":
        for info in TEMPORARY_LISTS["courses_registration"]:
            if info[0] == call.from_user.id:
                bot.answer_callback_query(call.id, "Ви вже реєструєтесь.")
                return

        for card in trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["Registrations"]):
            if card["labels"][0]["id"] == config.TRELLO_CONFIG["Labels"]["Register_Courses"]:
                if str(call.from_user.id) in card["name"]:
                    bot.answer_callback_query(call.id, "Ви вже зареєстровані.")
                    return
                
        TEMPORARY_LISTS["courses_registration"].append([call.from_user.id, False, None, None])

        bot.answer_callback_query(call.id, "Підтвердіть або скасуйте.")

        markup = telebot.util.quick_markup({ "✅ Підтвердити ✅": {"callback_data": "courses_register_accept"}, "🚫 Скасувати 🚫": {"callback_data": "courses_register_decline"} }, row_width=2)
        bot.send_message(chat_id=call.from_user.id, text=f"Ви дійсно хочете забронювати місце на підготовчих курсах?", reply_markup=markup, parse_mode="HTML")

    elif call.data == "courses_register_accept":
        for info in TEMPORARY_LISTS["courses_registration"]:
            if info[0] == call.from_user.id:
                if info[1] == True:
                    bot.answer_callback_query(call.id, "Ви вже підтвердили.")
                    return
                else: info[1] = True
            
        bot.answer_callback_query(call.id, "Підтверджено.")

        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id, text=f"Напишіть свій номер телефону:")

    elif call.data == "courses_register_decline":
        bot.answer_callback_query(call.id, "Скасовано.")

        for info in TEMPORARY_LISTS["courses_registration"]:
            if info[0] == call.from_user.id:
                TEMPORARY_LISTS["courses_registration"].remove(info)
            

    elif call.data == "courses_register_accept2":
        bot.answer_callback_query(call.id, "Зареєстровано.")

        for info in TEMPORARY_LISTS["courses_registration"]:
            if info[0] == call.from_user.id:
                trello.cards.new(name=f"@{call.from_user.username} ({call.from_user.id}) | {info[2]} | {info[3]}", idList=config.TRELLO_CONFIG["Lists"]["Registrations"], idLabels=[config.TRELLO_CONFIG["Labels"]["Register_Courses"]])
                TEMPORARY_LISTS["courses_registration"].remove(info)

        buttons = {}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)
        bot.send_message(chat_id=call.from_user.id, text=f"Вас було зареєстровано.\nВам зателефонують по вказаному номеру для уточнення інформації.", reply_markup=markup)

        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)








    elif call.data == "open_doors_register":
        for info in TEMPORARY_LISTS["open_doors_registration"]:
            if info[0] == call.from_user.id:
                bot.answer_callback_query(call.id, "Ви вже реєструєтесь.")
                return

        for card in trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["Registrations"]):
            if card["labels"][0]["id"] == config.TRELLO_CONFIG["Labels"]["Register_OpenDoors"]:
                if str(call.from_user.id) in card["name"]:
                    bot.answer_callback_query(call.id, "Ви вже зареєстровані.")
                    return
                
        TEMPORARY_LISTS["open_doors_registration"].append([call.from_user.id, False, None, None])

        bot.answer_callback_query(call.id, "Підтвердіть або скасуйте.")

        day_info = config.OPEN_DOORS_DAYS_DATES[config.ACTUAL_OPEN_DOORS_DAY-1]

        markup = telebot.util.quick_markup({ "✅ Підтвердити ✅": {"callback_data": "open_doors_register_accept"}, "🚫 Скасувати 🚫": {"callback_data": "open_doors_register_decline"} }, row_width=2)
        bot.send_message(chat_id=call.from_user.id, text=f"Ви дійсно хочете зареєструватись на найближчий День відкритих дверей? <code>{day_info[0]} - {day_info[1]}</code>", reply_markup=markup, parse_mode="HTML")

    elif call.data == "open_doors_register_accept":
        for info in TEMPORARY_LISTS["open_doors_registration"]:
            if info[0] == call.from_user.id:
                if info[1] == True:
                    bot.answer_callback_query(call.id, "Ви вже підтвердили.")
                    return
                else: info[1] = True
            
        bot.answer_callback_query(call.id, "Підтверджено.")

        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.from_user.id, text=f"Напишіть свій номер телефону:")

    elif call.data == "open_doors_register_decline":
        bot.answer_callback_query(call.id, "Скасовано.")

        for info in TEMPORARY_LISTS["open_doors_registration"]:
            if info[0] == call.from_user.id:
                TEMPORARY_LISTS["open_doors_registration"].remove(info)
            

    elif call.data == "open_doors_register_accept2":
        bot.answer_callback_query(call.id, "Зареєстровано.")

        for info in TEMPORARY_LISTS["open_doors_registration"]:
            if info[0] == call.from_user.id:
                trello.cards.new(name=f"@{call.from_user.username} ({call.from_user.id}) | {info[2]} | {info[3]}", idList=config.TRELLO_CONFIG["Lists"]["Registrations"], idLabels=[config.TRELLO_CONFIG["Labels"]["Register_OpenDoors"]])
                TEMPORARY_LISTS["open_doors_registration"].remove(info)

        buttons = {}
        buttons["🗺️ Як добратись 🗺️"] = {"callback_data": "college_location"}
        buttons["↩️ Повернутись ↩️"] = {"callback_data": "to_start"}
        markup = telebot.util.quick_markup(buttons, row_width=1)
        bot.send_message(chat_id=call.from_user.id, text=f"Вас було зареєстровано.", reply_markup=markup)

        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)



    elif call.data == "news_list":
        bot.answer_callback_query(call.id, "Останні новини.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start_actions(call.from_user, call.data, call, {})

    elif call.data == "college_location":
        bot.answer_callback_query(call.id, "Локація.")
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start_actions(call.from_user, call.data, call, {})

    elif call.data == "admission_contact_accept":
        if TEMPORARY_LISTS["admission_management_debounce"] == True:
            bot.answer_callback_query(call.id, "Зачекайте, будь ласка...")
            return
        TEMPORARY_LISTS["admission_management_debounce"] = True

        if check_on_active_request(call.from_user.id, True):
            bot.answer_callback_query(call.id, "Запит вже створено. Чекайте відповіді.")
            return

        card = trello.cards.new(name=str(call.from_user.id), idLabels=[config.TRELLO_CONFIG["Labels"]["Request_Waiting"]], idList=config.TRELLO_CONFIG["Lists"]["AdmissionRequests"])

        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text="Дякуємо за звернення. Зачекайте на відповідь фахівця.", reply_markup=telebot.util.quick_markup({"🚫 Закрити питання 🚫": {"callback_data": f"close_admission_request_{card['id']}"}}))
        bot.answer_callback_query(call.id, "Запит створено. Чекайте відповіді.")

        for admission_user in trello.lists.get_card(idList=config.TRELLO_CONFIG["Lists"]["Admission"]):
            if len(admission_user['labels']) > 0:
                bot.send_message(chat_id=int(admission_user['name']), text=f"Поступив новий запит від <code>{call.from_user.last_name} {call.from_user.first_name}</code>.", parse_mode="HTML", reply_markup=telebot.util.quick_markup({"↗️ Перейти до інформації ↗️": {"callback_data": f"request_info_{card['id']}"}}, row_width=1))

        time.sleep(2)
        TEMPORARY_LISTS["admission_management_debounce"] = False

    elif call.data == "admission_contact_decline":
        bot.answer_callback_query(call.id, "Скасовано.")
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    elif call.data == "admission_contact_onlinechat":
        bot.answer_callback_query(call.id, "Підтвердіть або скасуйте.")

        markup = telebot.util.quick_markup({ "✅ Підтвердити ✅": {"callback_data": "admission_contact_accept"}, "🚫 Скасувати 🚫": {"callback_data": "admission_contact_decline"} }, row_width=2)
        bot.send_message(chat_id=call.from_user.id, text="Ви дійсно хочете почати онлайн-чат із членом приймальної комісії?", reply_markup=markup, parse_mode="HTML")

    elif call.data == "admission_contact_phone":
        bot.answer_callback_query(call.id, "Зв'язок.")
        markup = telebot.util.quick_markup({ "↩️ Повернутись ↩️": {"callback_data": "delete_it"} }, row_width=1)
        bot.send_message(chat_id=call.from_user.id, text="<b>Відповідальний секретар ПК:</b>\n<code>+38 (097) 501 92 77</code> <i>(Viber, Telegram, WhatsApp)</i>\n\n<b>Підготовчі курси:</b>\n<code>+38 (096) 819 52 29</code> <i>(Viber, Telegram)</i>", reply_markup=markup, parse_mode="HTML")

    elif call.data == "admission_contact":
        bot.answer_callback_query(call.id, "Зв'язок.")
        markup = telebot.util.quick_markup({ "📞 Зателефонувати 📞": {"callback_data": "admission_contact_phone"}, "🤖 Он-лайн чат 🤖": {"callback_data": "admission_contact_onlinechat"}, "↩️ Повернутись ↩️": {"callback_data": "delete_it"} }, row_width=2)
        bot.send_message(chat_id=call.from_user.id, text="Оберіть зручний способ зв'язку:", reply_markup=markup, parse_mode="HTML")

    elif call.data == "cancel_feedback":
        for waiting in TEMPORARY_LISTS["wait_to_feedback"]:
            if waiting[0] == call.from_user.id:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1], text="Надсилання зворотнього зв'язку скасовано.")
                bot.answer_callback_query(call.id, "Зворотній зв'язок скасовано.")
                TEMPORARY_LISTS["wait_to_feedback"].remove(waiting)
                break
        bot.answer_callback_query(call.id, "Такого запиту вже не існує. Створіть новий.")

    elif call.data == "cancel_sharenew":
        for waiting in TEMPORARY_LISTS["wait_to_sharenew"]:
            if waiting[0] == call.from_user.id:
                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1], text="Поширення новини скасовано")
                bot.answer_callback_query(call.id, "Поширення новини скасовано.")
                TEMPORARY_LISTS["wait_to_sharenew"].remove(waiting)
                break
        bot.answer_callback_query(call.id, "Такого запиту вже не існує. Створіть новий.")

    elif call.data == "confirm_sharenew":
        for waiting in TEMPORARY_LISTS["wait_to_sharenew"]:
            if waiting[0] == call.from_user.id:
                w0, w1, w2, w3 = waiting[0], waiting[1], waiting[2], waiting[3]

                TEMPORARY_LISTS["wait_to_sharenew"].remove(waiting)

                bot.answer_callback_query(call.id, "Процес розсилки розпочато.")
                trello.cards.new_action_comment(card_id_or_shortlink=waiting[2], text=f"Новину було поширено користувачем @{call.from_user.username}.")

                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1],
                                      text=f"🕐 Розсилку новини `{waiting[3]}` було розпочато.", parse_mode="Markdown")
                share_new(waiting[2])
                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1],
                                      text=f"✅ Розсилку новини `{waiting[3]}` було **завершено**.", parse_mode="Markdown")

                break
        bot.answer_callback_query(call.id, "Такого запиту вже не існує. Створіть новий.")

    elif "share_new" in call.data:
        for waiting in TEMPORARY_LISTS["wait_to_sharenew"]:
            if waiting[0] == call.from_user.id:
                sharenew_cardid = str.split(call.data, "_")[2]

                waiting[2] = sharenew_cardid # id
                waiting[3] = trello.cards.get(card_id_or_shortlink=sharenew_cardid)["name"]

                share_markup = telebot.util.quick_markup({"✅ Відправити ✅": {"callback_data": "confirm_sharenew"}, "❌ Скасувати ❌": {"callback_data": "cancel_sharenew"}}, row_width=1)
                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1], text=f"Ви впевнені, що хочете відправити новину `{waiting[3]}`?", reply_markup=share_markup, parse_mode="Markdown")

                bot.answer_callback_query(call.id, "Новину обрано.")
                break
        bot.answer_callback_query(call.id, "Такого запиту вже не існує. Створіть новий.")

    elif "feedback_type" in call.data:
        feedback_type = str.split(call.data, "_")[2]
        str_feedback_type = feedback_type
        feedback_type_index = int(str.split(call.data, "_")[3])

        for info in config.FEEDBACK_VARIANTS:
            if info[0] == feedback_type:
                str_feedback_type = info[1]

        for waiting in TEMPORARY_LISTS["wait_to_feedback"]:
            if waiting[0] == call.from_user.id:
                feedback_markup = telebot.util.quick_markup({"❌ Скасувати ❌": {"callback_data": "cancel_feedback"}}, row_width=1)

                bot.edit_message_text(chat_id=call.from_user.id, message_id=waiting[1], text=f"Тип звертання: `{str_feedback_type}`.\nОпишіть суть звертання.\nНатисніть 'скасувати' щоб скасувати дію.", reply_markup=feedback_markup)

                bot.answer_callback_query(call.id, "Тип звертання обрано.")
                waiting[2] = feedback_type
                waiting[3] = str_feedback_type

                break
        bot.answer_callback_query(call.id, "Такого запиту вже не існує. Створіть новий.")


if __name__ == "__main__":
    bot.infinity_polling()