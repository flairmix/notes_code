import spacy
from spacy.training.example import Example
from spacy.scorer import Scorer
import json

# Загрузка модели
nlp = spacy.load("custom_ner_model_ru")
ner = nlp.get_pipe("ner")

# Добавляем кастомные лейблы
custom_labels = [
    "PARAMETER", "TEMP", "COMPONENT", "EQUIPMENT", "ACTION", "STANDARD", "FLOWRATE",
    "CONDITION", "SYSTEM", "VALUE", "UNIT", "LOCATION", "HEIGHT", "DISTANCE",
    "MODALITY", "REFERENCE", "REQUIREMENT", "PURPOSE", "REGULATION", "SUBSTANCE"
]
for label in custom_labels:
    ner.add_label(label)

# Загрузка тренировочных данных
with open("01_FAUFCC\\auto_semantic\\nlp_learning\\train_dataset_fixed.json", "r", encoding="utf-8") as f:
    train_data_json = json.load(f)

train_data = []
for item in train_data_json:
    entities = [(ent['start'], ent['end'], ent['label']) for ent in item['entities']]
    train_data.append((item['text'], {"entities": entities}))

# Загрузка тестовых данных
with open("01_FAUFCC\\auto_semantic\\nlp_learning\\test_dataset_fixed.json", "r", encoding="utf-8") as f:
    test_data_json = json.load(f)

test_data = []
for item in test_data_json:
    entities = [(ent['start'], ent['end'], ent['label']) for ent in item['entities']]
    test_data.append((item['text'], {"entities": entities}))

# # Обучение модели
# optimizer = nlp.resume_training()
# for epoch in range(30):
#     losses = {}
#     for text, ann in train_data:
#         example = Example.from_dict(nlp.make_doc(text), ann)
#         nlp.update([example], drop=0.25, losses=losses)
#     print(f"Epoch {epoch+1} - Loss: {losses['ner']:.4f}")

# # Сохранение обученной модели
# nlp.to_disk("custom_ner_model_ru")
# print("✅ Модель сохранена в 'custom_ner_model_ru'")

examples = []
for item in test_data_json:
    doc = nlp.make_doc(item['text'])
    entities = [(ent['start'], ent['end'], ent['label']) for ent in item['entities']]
    examples.append(Example.from_dict(doc, {"entities": entities}))

# Оценка на тестовом наборе
scorer = Scorer()
scores = scorer.score(examples)

print("\n--- Evaluation on test set ---")
print(f"Precision: {scores['ents_p']:.2f}%")
print(f"Recall:    {scores['ents_r']:.2f}%")
print(f"F1-score:  {scores['ents_f']:.2f}%")