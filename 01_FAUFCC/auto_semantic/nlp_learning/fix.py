import spacy
from spacy.training import offsets_to_biluo_tags, biluo_tags_to_spans
import json

nlp = spacy.load("ru_core_news_sm")

def fix_alignment(item):
    doc = nlp(item["text"])
    original_entities = [(ent["start"], ent["end"], ent["label"]) for ent in item["entities"]]
    biluo_tags = offsets_to_biluo_tags(doc, original_entities)

    # Если нет проблемы, вернуть исходный пример
    if "-" not in biluo_tags:
        return item

    # Иначе исправляем сущности
    corrected_spans = biluo_tags_to_spans(doc, biluo_tags)
    corrected_entities = []
    for span in corrected_spans:
        corrected_entities.append({
            "start": span.start_char,
            "end": span.end_char,
            "label": span.label_
        })

    return {"text": item["text"], "entities": corrected_entities}

# Загрузите ваш текущий датасет
with open("01_FAUFCC\\auto_semantic\\nlp_learning\\train_dataset.json", "r", encoding="utf-8") as f:
    data_json = json.load(f)

# Исправьте весь датасет
data_fixed = [fix_alignment(item) for item in data_json]

# Сохраните исправленный датасет
with open("01_FAUFCC\\auto_semantic\\nlp_learning\\train_dataset_fixed.json", "w", encoding="utf-8") as f:
    json.dump(data_fixed, f, ensure_ascii=False, indent=4)

print("✅ Разметка успешно исправлена и сохранена в train_dataset_fixed.json")
