import pandas as pd
import re

class CSVProcessor:
    def __init__(self, input_csv_path, output_csv_path):
        """
        :param input_csv_path: путь к входному CSV-файлу (с заголовком).
        :param output_csv_path: путь к выходному CSV-файлу.
        """
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path
        
        self.base_cols = [
            "l",
            "Содержание",
            "Дата ввода требования в действие",
            "Реестр НТД",
            "Требование безопасности",
            "ЮИН"
        ]

        self.extra_cols = [
            "Обрабатывается в ЦИМ",
            "Подлежит переводу в МПФ",
            "Передано подрядчику",
            "Комментарии",
            "Наличие ссылок на другие НД, в которых содержатся требования",
            "Наличие ссылок на Задание на проектирование",
            "Наличие ссылок на другие пункы этого СП",
            "Наличие формул",
            "Наличие таблиц",
            "Наличие рисунков/диаграмм",
            "Требование носит рекомендательный характер"
        ]
        
        self.final_columns = self.base_cols + self.extra_cols
        
        self.df = self.load_csv()
        self.initialize_extra_columns()
        
    def load_csv(self):
        """Загружает CSV и выбирает необходимые столбцы."""
        return pd.read_csv(
            self.input_csv_path,
            usecols=self.base_cols,
            dtype=str,
            sep=";",
        )
    
    def initialize_extra_columns(self):
        """Добавляет дополнительные столбцы в DataFrame."""
        for col in self.extra_cols:
            self.df[col] = 0
        self.df["Комментарии"] = ""
    
    def has_pattern(self, text: str, pattern: str) -> bool:
        """Проверяет, содержит ли текст заданный паттерн (регулярное выражение)."""
        if not isinstance(text, str):
            return False
        return bool(re.search(pattern, text, flags=re.IGNORECASE))
    
    def check_conditions(self):
        """Проверяет условия для каждой строки и обновляет DataFrame."""
        zadanie_pattern = r"задан\w*\s+на\s+проектирован\w*"
        
        for i, row in self.df.iterrows():
            if self.has_pattern(row["Содержание"], zadanie_pattern):
                self.df.at[i, "Наличие ссылок на Задание на проектирование"] = 1
    
    def save_csv(self):
        """Сохраняет обновленный DataFrame в CSV."""
        self.df[self.final_columns].to_csv(self.output_csv_path, index=False, encoding="utf-8-sig")
    
    def process_data(self):
        """Основной метод обработки данных."""
        self.check_conditions()
        self.save_csv()
