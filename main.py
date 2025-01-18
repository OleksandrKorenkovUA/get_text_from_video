import yt_dlp
import whisper
import os
import re
from crews import TranslationCrew, SummarizationCrew, CorrectionCrew
from typing import Optional

def clean_filename(filename):
    cleaned = re.sub(r'[\\/*?:"<>|#]', "", filename)
    cleaned = re.sub(r'\s+', "_", cleaned)
    return cleaned.strip("_")

def save_text_to_file(text: str) -> bool:
    try:
        filename = input("Введіть ім'я файлу для збереження: ")
        if not filename.endswith('.txt'):
            filename += '.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Текст успішно збережено у файл: {filename}")
        return True
    except Exception as e:
        print(f"Помилка при збереженні файлу: {str(e)}")
        return False

def translate_text(text: Optional[str]) -> Optional[str]:
    if not text:
        print("Помилка: Текст для обробки відсутній")
        return None
    try:
        inputs = {
            'text_to_translate': text,
            'target_language': 'Ukrainian'
        }
        translated_text = TranslationCrew().crew().kickoff(inputs=inputs)
        return translated_text
    except Exception as e:
        print(f"Помилка при обробці тексту: {str(e)}")
        return None

def summarize_text(text: Optional[str]) -> Optional[str]:
    if not text:
        print("Помилка: Текст для обробки відсутній")
        return None
    try:
        inputs = {
            'text_for_summary': text,
            'language': 'Ukrainian'
        }
        summary = SummarizationCrew().crew().kickoff(inputs=inputs)
        if summary:
            print("\nКороткий зміст:")
            print(summary)
            return summary
        else:
            print("Помилка: Не вдалося створити короткий зміст")
            return None
    except Exception as e:
        print(f"Помилка при створенні короткого змісту: {str(e)}")
        return None
        
def correct_text(text: Optional[str]) -> Optional[str]:
    if not text:
        print("Помилка: Текст для обробки відсутній")
        return None
    try:
       
        inputs = {
            'text_to_correct': text,
            'language': 'Ukrainian'
        }
        corrected_text = CorrectionCrew().crew().kickoff(inputs=inputs)
        if corrected_text:
            print("\nВиправлений текст:")
            print(corrected_text)
            return corrected_text
        else:
            print("Помилка: Не вдалося виправити текст")
            return None
    except Exception as e:
        print(f"Помилка при виправленні тексту: {str(e)}")
        return None

def process_text(text: str) -> None:
    print("Оригінальний текст: ", text)
    current_text = text
    while True:
        print("\nОберіть дію:")
        print("1. Перекласти текст")
        print("2. Виправити текст") 
        print("3. Створити короткий зміст")
        print("4. Зберегти поточний текст")
        print("5. Завершити роботу")

        choice = input("Ваш вибір (1-6): ")

        if choice == "1":
            translated = translate_text(current_text)
            if translated:
                current_text = translated.raw
                print("\nТекст перекладено")
        elif choice == "2":
            corrected = correct_text(current_text)
            if corrected:
                current_text = corrected.raw
                print("\nТекст виправлено")
        elif choice == "3":
            summary = summarize_text(current_text)
            if summary:
                current_text = summary.raw
                print("\nСтворено короткий зміст")
        elif choice == "4":
            save_text_to_file(current_text)
            print("\nТекст збережено")
        elif choice == "5":
            print("\nЗавершення роботи")
            if input("Зберегти поточний текст перед виходом? (так/ні): ").lower() == 'так':
                save_text_to_file(current_text)
            break
        else:
            print("\nНекоректний вибір. Спробуйте ще раз")
            
        print("\nБажаєте продовжити роботу?")
        if input("Введіть 'так' або 'ні': ").lower() != 'так':
            break

def process_local_file(file_path: str) -> Optional[str]:
    try:
        file_path = file_path.strip("'\"")
        if not os.path.exists(file_path):
            print(f"Помилка: Файл {file_path} не знайдено")
            print("Перевірте, чи правильно вказано шлях до файлу")
            return None
        print(f"Обробка локального файлу: {file_path}")
        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        text = result["text"]
        process_text(text)
        return None
    except Exception as e:
        print(f"Сталася помилка при обробці локального файлу: {str(e)}")
        return None

def process_youtube_video(url: str) -> None:
    url = url.strip("'\"")
    print("\nВажлива інформація!")
    print("Для завантаження відео з YouTube потрібен доступ до ваших cookies з браузера Chrome.")
    print("Це необхідно для доступу до відео з обмеженим доступом або вікових обмежень.")
    print("Cookies будуть використані тільки для автентифікації з YouTube.\n")

    agreement = input("Ви згодні надати доступ до cookies? (так/ні): ").lower()
    
    if agreement != 'так':
        print("\nВи відмовились від надання доступу до cookies.")
        print("Бажаєте обробити локальний аудіо/відео файл замість цього?")
        choice = input("Введіть шлях до локального файлу або 'ні' для виходу: ")
        if choice.lower() != 'ні':
            process_local_file(choice)
        return
        
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'cookiesfrombrowser': ('chrome',),
            'outtmpl': '%(title)s.%(ext)s',
            'restrictfilenames': True,
            'windowsfilenames': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Завантаження аудіо починається...")
            info = ydl.extract_info(url, download=True)
            
            audio_file = None
            if 'requested_downloads' in info:
                for d in info['requested_downloads']:
                    if d['ext'] == 'mp3':
                        audio_file = d['filepath']
                        break
            
            if audio_file is None:
                clean_title = clean_filename(info['title'])
                audio_file = f"{clean_title}.mp3"
            
            if not os.path.exists(audio_file):
                print(f"Помилка: Файл {audio_file} не знайдено")
                return
                
            print(f"Назва: {info['title']}")
            print(f"Шлях до файлу: {audio_file}")
            
            try:
                model = whisper.load_model("base")
                result = model.transcribe(audio_file)
                text = result["text"]
                process_text(text)
            finally:
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                    
    except Exception as e:
        print(f"Сталася помилка: {str(e)}")

def run():
    print("Оберіть джерело для завантаження:")
    print("1. YouTube")
    print("2. Локальний файл")
    
    choice = input("Ваш вибір (1 або 2): ")
    
    if choice == "1":
        url = input("Введіть URL відео з YouTube: ")
        process_youtube_video(url)
    elif choice == "2":
        file_path = input("Введіть шлях до локального файлу: ")
        process_local_file(file_path)
    else:
        print("Невірний вибір. Будь ласка, оберіть 1 або 2.")

if __name__ == "__main__":
    run()
