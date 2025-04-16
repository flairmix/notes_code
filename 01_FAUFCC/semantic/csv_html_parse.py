import pandas as pd
import re
from bs4 import BeautifulSoup

def clean_html(text):
    """Удаляет все HTML-теги из текста."""
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=" ").strip()
    cleaned_text = re.sub(r'""', '', cleaned_text)  # Удаляем последовательность ""
    return cleaned_text

def process_txt_to_csv(input_txt, output_csv):
    """
    Загружает TXT-файл, удаляет HTML-разметку и сохраняет данные в CSV-файл с одной колонкой.
    """
    with open(input_txt, "r", encoding="utf-8") as file:
        text = file.read()
    
    cleaned_text = clean_html(text)
    
    df = pd.DataFrame({"Text": [cleaned_text]})
    df.to_csv(output_csv, index=False)
    print(f'Файл успешно сохранен как {output_csv}')


# Пример использования
process_txt_to_csv('semantic\Выгрузка.txt', 'output.csv')
