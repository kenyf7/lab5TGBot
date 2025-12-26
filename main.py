import telebot
import requests
import jsons
from environs import Env

from Class_ModelResponse import ModelResponse


# --- config ---
env = Env()
env.read_env()

TG_TOKEN = env("API_TOKEN")
bot = telebot.TeleBot(TG_TOKEN)

LM_BASE = "http://localhost:1234"
LM_CHAT = f"{LM_BASE}/v1/chat/completions"
LM_MODELS = f"{LM_BASE}/v1/models"

# контекст по пользователю
ctx_store: dict[int, str] = {}


# --- helpers ---
def get_ctx(user_id: int) -> str:
    return ctx_store.get(user_id, "")


def set_ctx(user_id: int, value: str) -> None:
    ctx_store[user_id] = value


def drop_ctx(user_id: int) -> None:
    ctx_store.pop(user_id, None)


def lm_current_model() -> str | None:
    r = requests.get(LM_MODELS, timeout=10)
    if r.status_code != 200:
        return None
    data = r.json()
    if not data.get("data"):
        return None
    return data["data"][0].get("id")


def build_prompt(history: str) -> str:
    return (
        "Ты — дружелюбный ассистент. Тебе передают историю диалога в формате:\n"
        "user: <сообщение пользователя>\n"
        "assistant: <ответ ассистента>\n"
        "Продолжи диалог и ответь за assistant.\n\n"
        "История диалога:\n"
        f"{history}\n"
        "assistant:"
    )


def lm_answer(prompt: str) -> str:
    payload = {"messages": [{"role": "user", "content": prompt}]}
    r = requests.post(LM_CHAT, json=payload, timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"LM Studio вернул код {r.status_code}")
    parsed: ModelResponse = jsons.loads(r.text, ModelResponse)
    return parsed.choices[0].message.content.strip()


# --- commands ---
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    text = (
        "Привет! Я Telegram-бот, подключённый к локальной модели через LM Studio.\n\n"
        "Команды:\n"
        "/start  - помощь\n"
        "/model  - показать модель\n"
        "/clear  - очистить контекст\n\n"
        "Напиши сообщение — отвечу с учётом истории диалога."
    )
    bot.reply_to(msg, text)


@bot.message_handler(commands=["model"])
def cmd_model(msg):
    try:
        name = lm_current_model()
    except Exception as e:
        bot.reply_to(msg, f"Не удалось подключиться к LM Studio: {e}")
        return

    if name:
        bot.reply_to(msg, f"Используемая модель: {name}")
    else:
        bot.reply_to(msg, "Не удалось получить информацию о модели.")


@bot.message_handler(commands=["clear"])
def cmd_clear(msg):
    uid = msg.from_user.id
    drop_ctx(uid)
    bot.reply_to(msg, "🧹 Контекст диалога очищен. Начинаем заново!")


# --- main chat ---
@bot.message_handler(func=lambda m: True)
def on_text(msg):
    uid = msg.from_user.id
    q = msg.text

    history = get_ctx(uid)
    history = f"{history}user: {q}\n"

    prompt = build_prompt(history)

    try:
        reply = lm_answer(prompt)
    except Exception as e:
        bot.reply_to(msg, f"Ошибка при обращении к модели: {e}")
        return

    history = f"{history}assistant: {reply}\n"
    set_ctx(uid, history)

    bot.reply_to(msg, reply)


if __name__ == "__main__":
    bot.polling(none_stop=True)






