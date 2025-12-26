# Telegram-бот с локальной LLM (LM Studio) и поддержкой контекста

Этот проект — Telegram-бот на Python, который отвечает пользователю с помощью **локальной языковой модели**, запущенной через **LM Studio (OpenAI-compatible API)**.  
Бот хранит контекст диалога отдельно для каждого пользователя и умеет очищать его командой **/clear**. Также можно узнать, какая модель используется, командой **/model**.

## Возможности

- Ответы через локальную LLM (LM Studio Local Server)
- Контекст диалога для каждого пользователя (в памяти приложения)
- Команды:
  - **/start** — краткая справка
  - **/model** — показать текущую модель из LM Studio
  - **/clear** — очистить контекст диалога

## Требования

- **Python 3.10+**
- Telegram Bot API Token (BotFather)
- **LM Studio** с включённым Local Server (обычно `http://localhost:1234`)
- Установленные библиотеки Python:
  - `pyTelegramBotAPI`
  - `requests`
  - `jsons`
  - `environs`

## Установка и запуск

### 1) Клонирование репозитория

```bash
git clone <repo_url>
cd <repo_folder>
```

### 2) (Рекомендуется) Виртуальное окружение

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3) Установка зависимостей

```bash
pip install pyTelegramBotAPI requests jsons environs
```

### 4) Создание `.env`

В корне проекта создай файл **.env**:

```env
API_TOKEN=ВАШ_TELEGRAM_BOT_TOKEN
```

### 5) Настройка и запуск LM Studio

1. Установи **LM Studio**
2. Скачай модель (например: `Qwen2.5-1.5B-Instruct-Q6_K.gguf` или более качественную `Q8_K`, если позволяет ПК)
3. Перейди в **Developer / Local Server**
4. Запусти Local Server (должен быть доступен `http://localhost:1234`)

Проверка (опционально): открой в браузере  
`http://localhost:1234/v1/models` — должен вернуться JSON со списком моделей.

### 6) Запуск бота

```bash
python main.py
```

Открой Telegram и напиши своему боту.

## Как работает контекст

- Контекст хранится **в оперативной памяти** (словарь в коде).
- При перезапуске программы контекст **сбрасывается**.
- Для ручной очистки используй **/clear**.

## Настройка адреса LM Studio

Если LM Studio работает на другом адресе/порту — поменяй URL в `main.py`:

- `LM_STUDIO_CHAT_URL`
- `LM_STUDIO_MODELS_URL`

## Возможные проблемы

**Бот не отвечает / ошибка подключения**  
- Убедись, что Local Server в LM Studio запущен  
- Проверь `http://localhost:1234/v1/models`

**Слишком долгий ответ / таймаут**  
- В коде можно увеличить `timeout` у `requests.post(...)`  
- Попробуй более лёгкую модель

---
