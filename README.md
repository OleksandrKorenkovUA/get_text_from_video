# Додаток для обробки тексту за допомогою Whisper та Ollama

## Огляд
Цей додаток використовує **Whisper** для перетворення мовлення в текст і **Ollama** для аналізу тексту, включаючи переклад, створення короткого змісту та виправлення тексту. Він дозволяє обробляти аудіофайли (локальні або з YouTube) і надає інструменти для роботи з текстом українською мовою.

### Функції
- **Розпізнавання мовлення**: Транскрибує аудіофайли у текст за допомогою Whisper.
- **Переклад**: Перекладає розпізнаний текст українською мовою.
- **Створення короткого змісту**: Витягує ключові моменти з тексту.
- **Виправлення тексту**: Автоматично виправляє граматичні та стилістичні помилки.

## Встановлення

### Попередні вимоги
- Python 3.8 або новіша версія
- Встановлений `ffmpeg` для обробки аудіо:
  - **MacOS**: `brew install ffmpeg`
  - **Windows**: `choco install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg`

### Встановлення Whisper
1. Встановіть Whisper за допомогою pip:
   ```bash
   pip install -U openai-whisper
   ```
   
   Або встановіть найновішу версію з GitHub:
   ```bash
   pip install git+https://github.com/openai/whisper.git
   ```

2. Якщо виникають помилки при встановленні tiktoken, встановіть Rust:
   ```bash
   pip install setuptools-rust
   ```

### Встановлення Ollama
1. Встановіть Ollama відповідно до вашої операційної системи:
   - **MacOS і Linux**:
     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```
   - **Windows**: Завантажте та встановіть інсталятор з [офіційного сайту](https://ollama.com/download)

### Інструкція зі встановлення додатку
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/OleksandrKorenkovUA/get_text_from_video
   cd get_text_from_video
   ```

## Використання додатку
Встановіть залежності 
pip install -r requirements.txt

### Запуск програми
1. Запустіть програму командою:
   ```bash
   python main.py
   ```

2. Оберіть джерело для обробки:
   - YouTube відео (опція 1)
   - Локальний аудіо/відео файл (опція 2)

### Обробка YouTube відео
1. Виберіть опцію 1
2. Вставте URL відео з YouTube
3. Надайте дозвіл на використання cookies з Chrome

#### Важлива інформація про використання cookies
При завантаженні відео з YouTube, програма запитує доступ до cookies браузера Chrome. Це необхідно з наступних причин:
- Доступ до відео з віковими обмеженнями
- Завантаження відео, доступних тільки для авторизованих користувачів
- Доступ до приватних плейлистів
- Обхід регіональних обмежень

Cookies використовуються виключно для автентифікації з YouTube та безпечно обробляються за допомогою бібліотеки yt-dlp. Програма:
- Зчитує cookies з браузера Chrome
- Використовує їх тільки для одного сеансу завантаження
- Не зберігає cookies локально
- Не передає cookies третім сторонам

Якщо ви відмовляєтесь надати доступ до cookies, програма запропонує альтернативний варіант - обробку локального файлу.

4. Дочекайтесь завершення завантаження та обробки

### Обробка локального файлу
1. Виберіть опцію 2
2. Вкажіть повний шлях до аудіо/відео файлу
3. Дочекайтесь завершення обробки

### Робота з текстом
Після обробки аудіо ви можете:
1. Перекласти текст українською (опція 1)
2. Виправити граматику та стиль (опція 2)
3. Створити короткий зміст (опція 3)
4. Зберегти поточний текст у файл (опція 4)
5. Завершити роботу (опція 5)

### Збереження результатів
- Для збереження тексту виберіть опцію 4
- Введіть бажане ім'я файлу (розширення .txt буде додано автоматично)
- При виході з програми вам також буде запропоновано зберегти останню версію тексту
