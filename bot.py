import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

import os
TOKEN = os.getenv("TOKEN")

загаданное_число = {}
язык_пользователя = {}

тексты = {
    "ru": {
        "старт": "Прииииееет! 😄 Я Бот Веселуха! Выбирай кнопку!",
        "привет": "Прииииееет! 😂 Рад тебя видеть!!!",
        "как дела": "Отлично! Я же бот, у меня всегда хорошо 😄",
        "пока": "Пока-пока! 👋 Не скучай без меня!",
        "угадай": "Я загадал число от 1 до 10! Угадай! 🎲",
        "больше": "Больше! ⬆️",
        "меньше": "Меньше! ⬇️",
        "угадал": "Правильно! 🎉 Ты угадал!",
        "число": "Напиши число! 😄",
        "else": "Ха-ха! Ты написал: {} 😂",
        "язык": "Выбери язык / Choose language / Оберіть мову:",
        "язык_выбран": "Язык изменён на Русский! 🇷🇺",
        "кнопки": [
            ["Анекдот", "Привет"],
            ["Как дела", "Угадай число"],
            ["Предсказание", "Совет дня"],
            ["Камень ножницы бумага"],
            ["Пока"]
        ],
        "анекдоты": [
            "Почему программисты носят очки? Потому что не С# 😂",
            "Чебурашка говорит: Гена, давай вызовем сантехника!\nГена: Зачем? У нас всё хорошо!\nЧебурашка: Да вот кран высоко, и в туалете вода быстро течёт — умываться не успеваю! 😂",
            "Учительница спрашивает на уроке Окружающий мир:\n— Чего больше всего боятся звери в лесу?\nДети почти хором:\n— МАШУ!!! 😂",
            "— Не подскажете, каким успокоительным пользуется медведь после общения с Машей из мультика? 😂"
        ],
        "предсказания": [
            "🔮 Сегодня тебя ждёт что-то вкусное!",
            "🔮 Звёзды говорят — сегодня отличный день для отдыха!",
            "🔮 Скоро тебя ждёт приятный сюрприз!",
            "🔮 Сегодня ты будешь самым весёлым человеком в комнате 😄",
            "🔮 Удача на твоей стороне — используй это!"
        ],
        "советы": [
            "💪 Выпей стакан воды — это всегда полезно!",
            "💪 Улыбнись! Это заразно и бесплатно 😄",
            "💪 Сделай 10 приседаний прямо сейчас!",
            "💪 Позвони кому-нибудь близкому сегодня!",
            "💪 Отдохни 5 минут от телефона... хотя потом 😄"
        ],
        "кнп": {
            "камень": "🪨 Камень",
            "ножницы": "✂️ Ножницы",
            "бумага": "📄 Бумага",
            "выиграл": "Ты выиграл! 🎉а я проиграл эххххх....",
            "проиграл": "Я выиграл! 😈 ураааааааааа!!!!!!!!!!",
            "ничья": "Ничья! 🤝жаль жаль жаль ну это лучше чем порожения поздравляем друг друга урааааааа!!!",
            "выбор": "Выбери:",
            "я_выбрал": "Я выбрал"
        }
    },
    "uk": {
        "старт": "Привіііііт! 😄 Я Бот Веселуха! Обирай кнопку!",
        "привет": "Привіііііт! 😂 Радий тебе бачити!!!",
        "как дела": "Чудово! Я ж бот, у мене завжди добре 😄",
        "пока": "Бувай! 👋 Не сумуй без мене!",
        "угадай": "Я загадав число від 1 до 10! Вгадай! 🎲",
        "больше": "Більше! ⬆️",
        "меньше": "Менше! ⬇️",
        "угадал": "Правильно! 🎉 Ти вгадав!",
        "число": "Напиши число! 😄",
        "else": "Ха-ха! Ти написав: {} 😂",
        "язык": "Виберіть мову / Choose language / Выберите язык:",
        "язык_выбран": "Мову змінено на Українську! 🇺🇦",
        "кнопки": [
            ["Анекдот", "Привіт"],
            ["Як справи", "Вгадай число"],
            ["Передбачення", "Порада дня"],
            ["Камінь ножиці папір"],
            ["Бувай"]
        ],
        "анекдоты": [
            "Чому програмісти носять окуляри? Бо не С# 😂",
            "Чебурашка каже: Гено, давай викличемо сантехніка!\nГена: Навіщо? У нас все добре!\nЧебурашка: Та от кран високо, і у туалеті вода швидко тече — вмитися не встигаю! 😂",
            "Вчителька запитує на уроці Навколишній світ:\n— Чого найбільше бояться звірі у лісі?\nДіти майже хором:\n— МАШУ!!! 😂",
            "— Чи не підкажете, яким заспокійливим користується ведмідь після спілкування з Машею з мультика? 😂"
        ],
        "предсказания": [
            "🔮 Сьогодні на тебе чекає щось смачне!",
            "🔮 Зірки кажуть — сьогодні чудовий день для відпочинку!",
            "🔮 Скоро на тебе чекає приємний сюрприз!",
            "🔮 Сьогодні ти будеш найвеселішою людиною в кімнаті 😄",
            "🔮 Удача на твоєму боці — використай це!"
        ],
        "советы": [
            "💪 Випий склянку води — це завжди корисно!",
            "💪 Посміхнись! Це заразно і безкоштовно 😄",
            "💪 Зроби 10 присідань прямо зараз!",
            "💪 Подзвони комусь близькому сьогодні!",
            "💪 Відпочинь 5 хвилин від телефону... хоча потім 😄"
        ],
        "кнп": {
            "камень": "🪨 Камінь",
            "ножницы": "✂️ Ножиці",
            "бумага": "📄 Папір",
            "выиграл": "Ти виграв! 🎉",
            "проиграл": "Я виграв! 😈",
            "ничья": "Нічия! 🤝",
            "выбор": "Обирай:",
            "я_выбрал": "Я обрав"
        }
    },
    "en": {
        "старт": "Heeello! 😄 I'm Bot Veselukha! Choose a button!",
        "привет": "Heeello! 😂 Glad to see you!!!",
        "как дела": "Great! I'm a bot, I'm always fine 😄",
        "пока": "Bye-bye! 👋 Don't miss me!",
        "угадай": "I guessed a number from 1 to 10! Guess! 🎲",
        "больше": "Higher! ⬆️",
        "меньше": "Lower! ⬇️",
        "угадал": "Correct! 🎉 You guessed it!",
        "число": "Write a number! 😄",
        "else": "Ha-ha! You wrote: {} 😂",
        "язык": "Choose language / Выберите язык / Оберіть мову:",
        "язык_выбран": "Language changed to English! 🇬🇧",
        "кнопки": [
            ["Joke", "Hello"],
            ["How are you", "Guess number"],
            ["Prediction", "Tip of the day"],
            ["Rock Paper Scissors"],
            ["Bye"]
        ],
        "анекдоты": [
            "Why do programmers wear glasses? Because they can't C# 😂",
            "Cheburashka: Gena, let's call a plumber!\nGena: Why? We're fine.\nCheburashka: The faucet is too high, and the toilet is running too fast — I don't have time to wash up! 😂",
            "A teacher in a world around us class:\n— What are forest animals most afraid of?\nAlmost everyone in unison:\n— MASHA!!! 😂",
            "— What kind of sedative does the bear use after dealing with Masha from the cartoon? 😂"
        ],
        "предсказания": [
            "🔮 Something delicious awaits you today!",
            "🔮 Stars say — today is a great day to rest!",
            "🔮 A pleasant surprise is coming your way!",
            "🔮 Today you will be the funniest person in the room 😄",
            "🔮 Luck is on your side — use it!"
        ],
        "советы": [
            "💪 Drink a glass of water — always helpful!",
            "💪 Smile! It's contagious and free 😄",
            "💪 Do 10 squats right now!",
            "💪 Call someone close to you today!",
            "💪 Take a 5 minute break from your phone... well, later 😄"
        ],
        "кнп": {
            "камень": "🪨 Rock",
            "ножницы": "✂️ Scissors",
            "бумага": "📄 Paper",
            "выиграл": "You win! 🎉",
            "проиграл": "I win! 😈",
            "ничья": "Draw! 🤝",
            "выбор": "Choose:",
            "я_выбрал": "I chose"
        }
    }
}

def get_lang(user_id):
    return язык_пользователя.get(user_id, "ru")

def get_keyboard(user_id):
    lang = get_lang(user_id)
    return ReplyKeyboardMarkup(тексты[lang]["кнопки"], resize_keyboard=True)

def кнп_клавиатура(user_id):
    lang = get_lang(user_id)
    к = тексты[lang]["кнп"]
    return ReplyKeyboardMarkup([
        [к["камень"], к["ножницы"], к["бумага"]]
    ], resize_keyboard=True)

игра_кнп = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = get_lang(user_id)
    await update.message.reply_text(тексты[lang]["старт"], reply_markup=get_keyboard(user_id))

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = get_lang(user_id)
    клавиатура = ReplyKeyboardMarkup([
        ["🇷🇺 Русский", "🇺🇦 Українська", "🇬🇧 English"]
    ], resize_keyboard=True)
    await update.message.reply_text(тексты[lang]["язык"], reply_markup=клавиатура)

async def ответ(update: Update, context: ContextTypes.DEFAULT_TYPE):
    текст = update.message.text.lower()
    user_id = update.message.from_user.id

    if "русский" in текст:
        язык_пользователя[user_id] = "ru"
        игра_кнп.pop(user_id, None)
        await update.message.reply_text(тексты["ru"]["язык_выбран"], reply_markup=get_keyboard(user_id))
        return
    elif "українська" in текст:
        язык_пользователя[user_id] = "uk"
        игра_кнп.pop(user_id, None)
        await update.message.reply_text(тексты["uk"]["язык_выбран"], reply_markup=get_keyboard(user_id))
        return
    elif "english" in текст:
        язык_пользователя[user_id] = "en"
        игра_кнп.pop(user_id, None)
        await update.message.reply_text(тексты["en"]["язык_выбран"], reply_markup=get_keyboard(user_id))
        return

    lang = get_lang(user_id)
    т = тексты[lang]
    kb = get_keyboard(user_id)
    к = т["кнп"]

    if any(x in текст for x in ["камень ножницы", "камінь ножиці", "rock paper"]):
        игра_кнп[user_id] = True
        await update.message.reply_text(к["выбор"], reply_markup=кнп_клавиатура(user_id))

    elif user_id in игра_кнп:
        if any(x in текст for x in ["🪨", "камень", "камінь", "rock"]):
            мой = "камень"
        elif any(x in текст for x in ["✂️", "ножниц", "ножиц", "scissors"]):
            мой = "ножницы"
        elif any(x in текст for x in ["📄", "бумаг", "папір", "paper"]):
            мой = "бумага"
        else:
            await update.message.reply_text(к["выбор"], reply_markup=кнп_клавиатура(user_id))
            return

        бот = random.choice(["камень", "ножницы", "бумага"])
        победы = [("камень", "ножницы"), ("ножницы", "бумага"), ("бумага", "камень")]

        if мой == бот:
            результат = к["ничья"]
        elif (мой, бот) in победы:
            результат = к["выиграл"]
        else:
            результат = к["проиграл"]

        бот_текст = к[бот]
        мой_текст = к[мой]
        del игра_кнп[user_id]
        await update.message.reply_text(
            f"Ты: {мой_текст}\n{к['я_выбрал']}: {бот_текст}\n{результат}",
            reply_markup=kb
        )

    elif any(x in текст for x in ["привет", "привіт", "hello"]):
        await update.message.reply_text(т["привет"], reply_markup=kb)
    elif any(x in текст for x in ["как дела", "як справи", "how are you"]):
        await update.message.reply_text(т["как дела"], reply_markup=kb)
    elif any(x in текст for x in ["пока", "бувай", "bye"]):
        await update.message.reply_text(т["пока"], reply_markup=kb)
    elif any(x in текст for x in ["анекдот", "joke"]):
        await update.message.reply_text(random.choice(т["анекдоты"]), reply_markup=kb)
    elif any(x in текст for x in ["предсказание", "передбачення", "prediction"]):
        await update.message.reply_text(random.choice(т["предсказания"]), reply_markup=kb)
    elif any(x in текст for x in ["совет", "порада", "tip"]):
        await update.message.reply_text(random.choice(т["советы"]), reply_markup=kb)
    elif any(x in текст for x in ["угадай число", "вгадай число", "guess number"]):
        загаданное_число[user_id] = random.randint(1, 10)
        await update.message.reply_text(т["угадай"], reply_markup=kb)
    elif user_id in загаданное_число:
        try:
            число = int(текст)
            if число == загаданное_число[user_id]:
                await update.message.reply_text(т["угадал"], reply_markup=kb)
                del загаданное_число[user_id]
            elif число < загаданное_число[user_id]:
                await update.message.reply_text(т["больше"], reply_markup=kb)
            else:
                await update.message.reply_text(т["меньше"], reply_markup=kb)
        except:
            await update.message.reply_text(т["число"], reply_markup=kb)
    else:
        await update.message.reply_text(т["else"].format(текст), reply_markup=kb)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("language", language))
app.add_handler(MessageHandler(filters.TEXT, ответ))
#app.run_polling()
