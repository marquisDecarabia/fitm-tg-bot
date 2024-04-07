#!/usr/bin/env python
# pylint: disable=unused-argument, line-too-long, fixme

import logging
from typing import Final, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

TOKEN: Final = "6643073236:AAECmdhJo505_GWi5UuoutUH3XbY_bAGQZ4"
BOT_USERNAME: Final = "@bgkmupractice_bot"
DEPARTMENT_LINK_BASE: Final = "https://fitm.kubg.edu.ua/struktura1/kafedry"

DEPARTMENT_INFO_TEXT = {
    "computer-science": "«Кафедра комп’ютерних наук (КН)» – здійснює навчання студентів в області Інформаційних технологій за спеціальністю 122 «Комп’ютерні науки» (Computer Science, CS) і є потужним навчально-науковим структурним підрозділом Факультету інформаційних технологій та математики. На кафедрі здійснюється підготовка здобувачів вищої освіти з галузі знань 12 «Інформаційні технології»  за спеціальністю 122 «Комп’ютерні науки» першого (бакалаврського)  і другого (магістерського)  освітніх рівнів.",
    "math-and-physics": "«Кафедра математики і фізики» (завідувачка Семеняка Світлана Олексіївна, кандидат фізико-математичних наук, доцент і просто найкраща) є випусковою для здобувачів вищої освіти першого (бакалаврського) і другого (магістерського) освітніх рівнів з галузі знань 11 «Математика та статистика» за спеціальністю 111 «Математика».",
    "cybersecurity": "«Кафедра інформаційної та кібернетичної безпеки» – готує фахівців вищої кваліфікації в галузі знань 12 – «Інформаційні технології» спеціальностей  123 «Комп’ютерна інженерія» та 125 «Кібербезпека та захист інформації» з метою забезпечення потреб виробничої, освітньої, наукової та інших сфер діяльності людини, суспільства та держави в цілому."
}
DEPARTMENT_INFO_LINKS = {
    "computer-science": f"{DEPARTMENT_LINK_BASE}/kafedra-kompiuternykh-nauk/pro-kafedru.html",
    "math-and-physics": f"{DEPARTMENT_LINK_BASE}/kafedra-matematyky-i-fizyky/pro-kafedru.html",
    "cybersecurity": f"{DEPARTMENT_LINK_BASE}/kafedra-informatsiinoi-ta-kibernetychnoi-bezpeky/pro-kafedru.html",
}
DEPARTMENT_EDU_LINKS = {
    "computer-science": f"{DEPARTMENT_LINK_BASE}/kafedra-kompiuternykh-nauk/navchalno-metodychna-robota-kknm.html",
    "math-and-physics": f"{DEPARTMENT_LINK_BASE}/kafedra-matematyky-i-fizyky/navchalno-metodychna-robota.html#osvitnii-riven-pershyi-bakalavrskyi",
    "cybersecurity": f"{DEPARTMENT_LINK_BASE}/kafedra-informatsiinoi-ta-kibernetychnoi-bezpeky-im-profesora-volodymyra-buriachka/navchalno-metodychna-robota.html",
}
DEPARTMENT_CONTACT_LINKS = {
    "computer-science": f"{DEPARTMENT_LINK_BASE}/kafedra-kompiuternykh-nauk/kontakti.html",
    "math-and-physics": f"{DEPARTMENT_LINK_BASE}/kafedra-matematyky-i-fizyky/kontakti.html",
    "cybersecurity": f"{DEPARTMENT_LINK_BASE}/kafedra-informatsiinoi-ta-kibernetychnoi-bezpeky-im-profesora-volodymyra-buriachka/kontakti.html",
}
APPLICANTS_INFO_LINK: Final = "https://fitm.kubg.edu.ua/struktura1/vstupnykam.html"
FACULTY_INFO_LINK: Final = "https://fitm.kubg.edu.ua/pro-fakultet/vizytivka.html"
FACULTY_INFO = f"""
<a href="{FACULTY_INFO_LINK}">✨<strong>«Факультет інформаційних технологій та математики»</strong>✨</a> створено у вересні 2022 року шляхом реорганізації Факультету інформаційних технологій та управління.

На факультеті працює понад 40 штатних співробітників, серед яких член-кореспондент НАПН України, 6 докторів наук, професорів, 28 кандидатів наук і доцентів.

До структури Факультету входять три кафедри:
<a href="{DEPARTMENT_INFO_LINKS['cybersecurity']}">🔐 Кафедра інформаційної та кібернетичної безпеки</a>
<a href="{DEPARTMENT_INFO_LINKS['computer-science']}">💾 Кафедра комп’ютерних наук</a>
<a href="{DEPARTMENT_INFO_LINKS['math-and-physics']}">🚀 Кафедра математики і фізики</a>

Факультет налагодив і розвиває тісні зв’язки з міжнародними фондами та інституціями: Erasmus+, Eurasia, Міжнародний фонд «Відродження», Міжнародний Вишеградський фонд та ін. Така співпраця передбачає як спільні наукові дослідження, так і академічну мобільність викладачів і студентів.

Викладачі факультету активні учасники міжнародних проектів:
- Модернізація педагогічної вищої освіти інноваційними засобами навчання (МОПЕД), 2017-2020 рр.;
- Партнерство для навчання та викладання університетської математики (PLATINUM), 2018-2021;
- Розвиток математичних компетентностей учнів шляхом цифрового математичного моделювання (DeDiMaMo), 2019-2022 рр.;
- Цифрова трансформація в освіті: найкращі дослідження ЄС (DigTriES), 2022 та ін."""

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_main_menu(update.message.chat_id, context)

async def send_main_menu(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("📌 Дізнатися більше про факультет", callback_data="more-info"),
         InlineKeyboardButton("📋 Кафедри факультету", callback_data="departments")],
        [InlineKeyboardButton("🎓 Вступникам", callback_data="applicants")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="Привіт! Цей бот допоможе вам отримати інформацію про Факультет інформаційних технологій та математики Київського столичного університету імені Бориса Грінченка.", reply_markup=reply_markup)

async def send_departments_menu(chat_id, context):
    keyboard = [
        [InlineKeyboardButton("💾 Кафедра комп’ютерних наук", callback_data="computer-science")],
        [InlineKeyboardButton("🚀 Кафедра математики і фізики", callback_data="math-and-physics")],
        [InlineKeyboardButton("🔐 Кафедра інформаційної та кібернетичної безпеки", callback_data="cybersecurity")],
        [InlineKeyboardButton("↩️ Назад", callback_data="back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="👉 Виберіть кафедру:", reply_markup=reply_markup)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

async def send_department_info(update, context, department):
    chat_id = update.effective_chat.id

    text = DEPARTMENT_INFO_TEXT[department]
    url = DEPARTMENT_INFO_LINKS[department]

    keyboard = [
            [InlineKeyboardButton("📚 Освітня програма", callback_data=f"education_{department}"),
             InlineKeyboardButton("📩 Контакти", callback_data=f"contacts_{department}")],
            [InlineKeyboardButton("↩️ Назад", callback_data="departments")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text=f"{text}\nДетальна інформація: {url}", reply_markup=reply_markup)

async def button(update: Update, context:  ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    if data in ["cybersecurity", "computer-science", "math-and-physics"]:
        await send_department_info(update, context, data)
    elif data == "more-info":
        await query.edit_message_text(text=FACULTY_INFO, parse_mode='HTML')
        await send_main_menu(chat_id, context)
    elif data == "departments":
        await send_departments_menu(chat_id, context)
    elif data == "applicants":
        url = APPLICANTS_INFO_LINK
        await context.bot.send_message(update.effective_chat.id, text=f"Детальна інформація для вступникiв доступна за посиланням: {url}")
    elif data == "back":
        await send_main_menu(chat_id, context)
    elif "education" in data:
        department = data.split("_")[1]
        url = DEPARTMENT_EDU_LINKS[department]
        await context.bot.send_message(chat_id=chat_id, text=f"🔎 Детальна інформація про освітню програму кафедри: {url}")
    elif "contacts" in data:
        department = data.split("_")[1]
        url = DEPARTMENT_CONTACT_LINKS[department]
        await context.bot.send_message(chat_id=chat_id, text=f"📩Контакти кафедри: {url}")
    else:
        await query.edit_message_text(text=f"⚠️ Щось пiшло не так. \nВибрана опція: {data}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button))

    # Polling
    app.run_polling()

if __name__ == "__main__":
    print("@bgkmupractice_bot was made for educational purposes by D. Kriukova and O. Kozlov")
    print("© 2024 Borys Grinchenko Kyiv Metropolitan University")
    main()
