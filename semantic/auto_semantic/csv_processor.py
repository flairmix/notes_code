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
            "Упоминание расчетов",
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
    
    def get_pattern_text(self, text: str, pattern: str) -> str:
        """Проверяет, содержит ли текст заданный паттерн (регулярное выражение)."""
        if not isinstance(text, str):
            return None
        match = re.search(pattern, text, flags=re.IGNORECASE)
        return match.group(0) if match else None
    
    # patterns for classifying 
    def check_conditions(self):
        """Проверяет условия для каждой строки и обновляет DataFrame."""
        zadanie_pattern = r"задан\w*\s+на\s+проектирован\w*"
        SP_pattern = r"СП \d*+."
        GOST_pattern = r"ГОСТ \d*+."
        SanPin_pattern = r"СанПиН \d*+."
        bibliografy_pattern = r"\[\d+\]"
        table_pattern = r"<table "
        calculation_pattern = r"<определяется расчетом "

        calculation_list_pattern = [
            r"\b(определя[ею]т(?:ся)?|рассчитыва[ею]т(?:ся)?)\s+(на\s+основани[иея]|по\s+результат[уыам]|из|в\s+ходе)?\s*расчет[аоуы]?\b",
            r"\bпринима[ею]т(?:ся)?\s+(по|из)?\s*расчет[ауо]?\b",
            r"\bс\s+результат[ауыами]?\s+расчет[ауо]?\b",
            r"\bрасчет[аеоуы]?\b",
            r"\bследует\s+рассчитыва[тьй]\b",
            r"\bПДК\b",
            r"\bпо\s+расчет[ауо]?\b",
            r"\bдолжн(?:а|о|ы)?\s+соответствова[тьй]?\s+расчетн(?:ой|ому|ым|ых)?\b",
            r"\bпо\s+аэродинамическ(?:ому|им|ой)?\s+расчет[ауо]?\b",
            r"\bобосновыва[ею]т(?:ся)?\s+расчет[аоуы]?\b",
            r"\bдолжн(?:а|о|ы)?\s+быть\s+дополнительно\s+рассчитан[аоы]?ы?\b",
            r"\bрассчитанн(?:ую|ый|ое|ые|ым|ом)\s+на\b",
        ]

        not_ordinary_patterns = [r"\b(должн(?:а|о|ы)?|следует|рекомендуется|допускается|может)\s+(быть\s+)?(использован(?:о|а|ы)?|применен(?:о|а|ы)?|учт(?:ен|ена|ено|ены)?|рассмотрен(?:о|а|ы)?|выбран(?:о|а|ы)?)\b",
            r"\b(достаточн(?:о|ая|ые|ым|ых|ого)|адекватн(?:о|ая|ые|ым|ых|ого)|целесообразн(?:о|ая|ые|ым|ых|ого)|эффективн(?:о|ая|ые|ым|ых|ого))\b",
            r"\b(примерно|в\s+пределах|не\s+менее|не\s+более|до\s+\d+%?|от\s+\d+%?|в\s+диапазоне|может\s+составлять)\b",
            r"\b(должны\s+быть|могут\s+быть|могут\s+использоваться|следует\s+предусматривать|может\s+приниматься|рекомендуется\s+применение)\b",
            r"\b(разумн(?:ый|ая|ое|ые)|достаточн(?:ый|ая|ое|ые)|следует\s+учитывать|допускается\s+изменение|может\s+быть\s+принято)\b",
        ]
        
        for i, row in self.df.iterrows():
            if self.has_pattern(row["Содержание"], zadanie_pattern):
                self.df.at[i, "Наличие ссылок на Задание на проектирование"] = 1

            if (self.has_pattern(row["Содержание"], SP_pattern) or
                self.has_pattern(row["Содержание"], GOST_pattern) or
                self.has_pattern(row["Содержание"], SanPin_pattern) or
                self.has_pattern(row["Содержание"], bibliografy_pattern)):
                
                self.df.at[i, "Наличие ссылок на другие НД, в которых содержатся требования"] = 1

            if self.has_pattern(row["Содержание"], table_pattern):
                self.df.at[i, "Наличие таблиц"] = 1

            for pattern in calculation_list_pattern:
                if self.has_pattern(row["Содержание"], pattern=pattern):
                    self.df.at[i, "Упоминание расчетов"] = 1
                    break

            for pattern in not_ordinary_patterns:
                if self.get_pattern_text(row["Содержание"], pattern=pattern):
                    self.df.at[i, "Комментарии"] = 1
                    break


    
    def save_csv(self):
        """Сохраняет обновленный DataFrame в CSV."""
        self.df[self.final_columns].to_csv(self.output_csv_path, index=False, encoding="utf-8-sig")
    
    def process_data(self):
        """Основной метод обработки данных."""
        self.check_conditions()
        self.save_csv()
