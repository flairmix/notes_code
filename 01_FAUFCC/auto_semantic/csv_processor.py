import pandas as pd
import re
import json

class CSVProcessor:
    """
    A class for processing and analyzing technical requirement data from a CSV file.

    Main functionalities:
    - Loads a CSV file containing regulatory or technical requirements.
    - Initializes additional columns for classification and commentary.
    - Uses regular expressions to detect the presence of references, formulas, calculations,
    tables, diagrams, and other key indicators in the text.
    - Flags rows based on detected patterns (e.g., links to other documents, internal references, recommendations).
    - Appends detailed comments describing findings for each row.
    - Saves the processed data into a new CSV file for further use.

    This class is useful for preprocessing regulatory documents, extracting key features,
    and preparing the dataset for downstream analysis or machine learning tasks.

    Args:
        input_csv_path (str): Path to the input CSV file (with headers).
        output_csv_path (str): Path where the output CSV will be saved.
    """

    def __init__(self, input_csv_path, output_csv_path, pattern_json_path):
        self.input_csv_path = input_csv_path
        self.output_csv_path = output_csv_path
        self.pattern_json_path = pattern_json_path
        
        self.base_cols = [
            "ID",
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
            "Упоминание расчетов",
            "Наличие таблиц",
            "Наличие рисунков/диаграмм",
            "Требование носит рекомендательный характер"
        ]
        
        self.final_columns = self.base_cols + self.extra_cols
        
        self.df = self.load_csv()
        self.initialize_extra_columns()
        self.patterns = self.load_patterns()
        
    def load_csv(self):
        """Загружает CSV и выбирает необходимые столбцы."""
        return pd.read_csv(
            self.input_csv_path,
            usecols=self.base_cols,
            dtype=str,
            sep=";",
        )
    
    def load_patterns(self):
        """Загружает регулярные выражения из JSON-файла."""
        with open(self.pattern_json_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
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
    
    def get_pattern_text(self, text: str, pattern: str) -> list[str]:
        """Проверяет, содержит ли текст заданный паттерн (регулярное выражение)."""
        if not isinstance(text, str):
            return None
        match = re.findall(pattern, text, flags=re.IGNORECASE) #TODO искать все и возвращать
        return match if len(match)>0 else None
    
    def check_conditions(self):
        for i, row in self.df.iterrows():
            for category, pattern_list in self.patterns.items():
                for pattern in pattern_list:
                    match = self.get_pattern_text(row["Содержание"], pattern=pattern)
                    if match:
                        if category in self.df.columns:
                            self.df.at[i, category] = 1
                        if category == "Наличие таблиц":
                            self.df.at[i, "Комментарии"] += f"{category}\n"
                        elif category == "Упоминание расчетов":
                            self.df.at[i, "Комментарии"] += f"{category} {match} \n"
                            break
                        elif category == "Требование носит рекомендательный характер":
                            if "Неоднозначная формулировка" not in self.df.at[i, "Комментарии"]:
                                self.df.at[i, "Комментарии"] += f"Неоднозначная формулировка {match}\n"
                            else:
                                self.df.at[i, "Комментарии"] += f"{match}"
                        else:
                            self.df.at[i, "Комментарии"] += f"{category} {match}\n"
    
    def save_csv(self):
        """Сохраняет обновленный DataFrame в CSV."""
        self.df[self.final_columns].to_csv(self.output_csv_path, index=False, encoding="utf-8-sig")
    
    def process_data(self):
        """Основной метод обработки данных."""
        self.check_conditions()
        self.save_csv()
