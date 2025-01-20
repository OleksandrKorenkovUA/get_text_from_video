import yt_dlp
import whisper
import os
import re
from crews import TranslationCrew, SummarizationCrew, CorrectionCrew
from typing import Optional
import requests
from bs4 import BeautifulSoup


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
    try:
        # Extract video metadata and clean title
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = clean_filename(info.get("title", "video"))
        
        # Download and convert video
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': f'video/{title}.mp4',
            'postprocessors': [
                {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}
            ],
            'merge_output_format': 'mp4',
            'keepvideo': False
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Process the final output
        model = whisper.load_model("base")
        file_path = f'video/{title}.mp4'
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не знайдено")
        
        # Transcribe using Whisper
        result = model.transcribe(file_path)
        text = result["text"]
        process_text(text)
    
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
