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
    
    def get_pattern_text(self, text: str, pattern: str) -> list[str]:
        """Проверяет, содержит ли текст заданный паттерн (регулярное выражение)."""
        if not isinstance(text, str):
            return None
        match = re.findall(pattern, text, flags=re.IGNORECASE) #TODO искать все и возвращать
        return match if len(match)>0 else None
    
    # patterns for classifying 
    def check_conditions(self):
        """Проверяет условия для каждой строки и обновляет DataFrame."""
        pattern_design_assignment = [
             r"задан\w*\s+на\s+проектирован\w*",
             r"техническ\w*\s+задани\w*",
             r"\bтехнологич\w*\s+требован\w*\b",
            #  r'\bпо технологическим требованиям\b',
        ]
        pattern_link_external = [
            r"СП\s*\d+",
            r"СП\d+",
            r"ГОСТ \d+",
            r"СанПиН \d+",
            r"\[\d+\]",

        ]
        
        table_pattern = r"<table "
        
        pattern_link_internal = [
            r'\bуказан\w*\sв\s\d+\.\d+\b',
            r'\bв\sсоответствии\sс\sтребованиями\sраздела\s\d+(\.\d+)?\b',
            r'\bв\sсоответствии\sс\s(?:требованиями\s)?раздел[а-я]*\s\d+(?:\.\d+)?(?:\s*(?:и|,)\s*\d+(?:\.\d+)?)*\b',
            r'\bв\sсоответствии\sс\sприложен\w*\s[А-Я]\b',
        ]

        calculation_list_pattern = [
            r"определя\w*\s*расчет\w*",
            r"рассчитанн\w*\s*в\s*соответст\w*\s*c",
            r"\b(определя[ею]т(?:ся)?|рассчитыва[ею]т(?:ся)?)\s+(на\s+основани[иея]|по\s+результат[уыам]|из|в\s+ходе)?\s*расчет[аоуы]?\b",
            r"\bпринима[ею]т(?:ся)?\s+(по|из)?\s*расчет[ауо]?\b",
            r"\bс\s+результат[ауыами]?\s+расчет[ауо]?\b",
            r"\bрасчет[аеоуы]?\b",
            r"\bследует\s+рассчитыва[тьй]\b",
            r"\bПДК\b",
            r"\bпо\s+расчет[ауо]?\b",
            r"\bдолж(?:н(?:а|о|ы|ен)?)?\s+соответствова[тьй]?\s+расчетн(?:ой|ому|ым|ых)?\b",
            r"\bпо\s+аэродинамическ(?:ому|им|ой)?\s+расчет[ауо]?\b",
            r"\bобосновыва[ею]т(?:ся)?\s+расчет[аоуы]?\b",
            r"\bдолжн(?:а|о|ы)?\s+быть\s+дополнительно\s+рассчитан[аоы]?ы?\b",
            r"\bрассчитанн(?:ую|ый|ое|ые|ым|ом)\s+на\b",
            r'\bопредел\w*\b(?:\s+\w+)?\s+\bрасчет\w*\b',
        ]

        not_ordinary_patterns = [
            r"рекомендуе\w*",
            r'(?<!\bне )\bдопускает\w*\b',
            r"примерно\w*",
            r"разумн\w*",
            r" должн\w*\s*соответство\w*\s*требовани\w*\s*норматив\w*\s* докумен\w*",
            r'\b(?:др\.|т\.п\.|т\.д\.)',
            r'\bВ случае отсутствия информации\b', r'\bпри отсутствии информации\b',
            r"\bследует\s*предусматривать\s*мероприятия \b",
            r"\bс\s*учетом\s*возможнос\w*\b",
            r"\bПри\s*невозможности\b",
            r'\bдоступ\w*\s*(?:для обслуживающего персонала|персонала)?\b',
            r'\bпри\s*необходимости\b',
            r'\bпри\s*возможности\b',
            r"\bвозможно\b",
            r"\bпо усмотрению\b",
            r"\bв отдельных случаях\b",
            r"\bпри определенных условиях\b",
            r"\bв зависимости от обстоятельств\b",
            r"\bпри желании\b",
            r"\bв ряде случаев\b",
            r"\bпри условии\b",
            r"\bв случае необходимости\b",
            r"\bпо мере необходимости\b",
            r"\bв случае потребности\b",
            r"\bпри соответствующих условиях\b",
            r"\bвозможное отклонение\b",
            r"\bвозможные варианты\b",
            r"\bпри наличии возможности\b",
            r"\bв случае целесообразности\b",
            # r"\bминимальн\w*\b",
            # r"\bмаксимальн\w*\b",
            r"\bкак\sправило\b",
            r"\bбывш\w*\sв\sупотреблении",
            r"\bрациональн\w*\b",
            r"\bоптимальн\w*\b",
            r"\bв\s*непосредственной\s*близости\b",
            
        ]
        
        for i, row in self.df.iterrows():

            for pattern in pattern_design_assignment:
                match = self.has_pattern(row["Содержание"], pattern=pattern)
                if match:
                    self.df.at[i, "Наличие ссылок на Задание на проектирование"] = 1
                    self.df.at[i, "Комментарии"] += "Наличие ссылок на Задание на проектирование\n"

            for pattern in pattern_link_external:
                match = self.get_pattern_text(row["Содержание"], pattern=pattern)
                if match:
                    self.df.at[i, "Наличие ссылок на другие НД, в которых содержатся требования"] = 1
                    self.df.at[i, "Комментарии"] += f"Наличие ссылок на другие НД, в которых содержатся требования {match}\n"

            for pattern in pattern_link_internal:
                match = self.get_pattern_text(row["Содержание"], pattern=pattern)
                if match:
                    self.df.at[i, "Наличие ссылок на другие пункы этого СП"] = 1
                    self.df.at[i, "Комментарии"] += f"Наличие ссылок на другие пункы этого СП {match}\n"
                    
            if self.has_pattern(row["Содержание"], table_pattern):
                self.df.at[i, "Наличие таблиц"] = 1
                self.df.at[i, "Комментарии"] += "Наличие таблиц\n"

            for pattern in calculation_list_pattern:
                match = self.get_pattern_text(row["Содержание"], pattern=pattern)
                if match:
                    self.df.at[i, "Упоминание расчетов"] = 1
                    self.df.at[i, "Комментарии"] += f"Упоминание расчетов {match} \n"
                    break

            for pattern in not_ordinary_patterns:

                match = self.get_pattern_text(row["Содержание"], pattern=pattern)
                
                if match:
                    if ("Неоднозначная формулировка" not in self.df.at[i, "Комментарии"]):
                        self.df.at[i, "Комментарии"] += f"Неоднозначная формулировка {match}\n"
                    else:
                        self.df.at[i, "Комментарии"] +=  f"{match}"

                


    
    def save_csv(self):
        """Сохраняет обновленный DataFrame в CSV."""
        self.df[self.final_columns].to_csv(self.output_csv_path, index=False, encoding="utf-8-sig")
    
    def process_data(self):
        """Основной метод обработки данных."""
        self.check_conditions()
        self.save_csv()
