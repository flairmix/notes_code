class IFCAnalyzer:
    def __init__(self, dataset):
        self.dataset = dataset

    def print_summary(self, category=None):
        if category:
            if category not in self.dataset:
                print(f"⚠️ Категория '{category}' не найдена.")
                return
            print(f"\n📂 Сводка по категории '{category.upper()}':")
            for key, items in self.dataset[category].items():
                print(f"• {key.capitalize()}: {len(items)} шт.")
        else:
            print("\n📊 Общая сводка по всем категориям:")
            for cat_name, cat_data in self.dataset.items():
                total = sum(len(items) for items in cat_data.values())
                print(f"{cat_name.capitalize()}: {total} элементов")

    def print_elements(self, category, element_type):
        if category not in self.dataset:
            print(f"⚠️ Категория '{category}' не найдена.")
            return

        if element_type not in self.dataset[category]:
            print(f"⚠️ Элемент '{element_type}' не найден в категории '{category}'.")
            return

        elements = self.dataset[category][element_type]
        print(f"\n🔍 Элементы '{element_type}' из категории '{category}':")

        for el in elements:
            guid = getattr(el, "GlobalId", "Без GUID")

            if element_type == "spaces":
                name = getattr(el, "Name", "Без имени")
                number = getattr(el, "LongName", "Без номера")
                desc = getattr(el, "Description", "")
                print(f"- [{number}] {name} | {desc} [GUID: {guid}]")
            else:
                name = getattr(el, "Name", "Без имени")
                print(f"- {name} [GUID: {guid}]")

    def print_element_properties(self, category, element_type):
        if category not in self.dataset or element_type not in self.dataset[category]:
            print(f"⚠️ Раздел '{category}' или тип элемента '{element_type}' не найден.")
            return

        elements = self.dataset[category][element_type]
        if not elements:
            print("⚠️ Нет элементов данного типа.")
            return

        element = elements[0]
        print(f"\n🔍 Свойства элемента типа '{element_type}' (первый из {len(elements)}):\n")

        # 📄 Основные атрибуты IFC
        print("📄 Основные поля IFC:")
        base_attrs = ["Name", "LongName", "Description", "ObjectType", "GlobalId", "PredefinedType"]
        for attr in base_attrs:
            val = getattr(element, attr, None)
            if val is not None:
                print(f"• {attr}: {val}")

        # 🧩 Свойства из PropertySet-ов
        print("\n🧩 Свойства из PropertySet-ов:")
        for rel in getattr(element, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_set = rel.RelatingPropertyDefinition
                if prop_set.is_a("IfcPropertySet"):
                    print(f"\n📦 {prop_set.Name}")
                    for prop in prop_set.HasProperties:
                        name = prop.Name
                        value = getattr(prop, "NominalValue", None)
                        if hasattr(value, "wrappedValue"):
                            value = value.wrappedValue
                        print(f"• {name}: {value}")

    def get_property_value(self, category, element_type, property_name):
        if category not in self.dataset or element_type not in self.dataset[category]:
            print(f"⚠️ Раздел '{category}' или тип элемента '{element_type}' не найден.")
            return

        elements = self.dataset[category][element_type]
        if not elements:
            print("⚠️ Нет элементов данного типа.")
            return

        results = []

        print(f"\n🔍 Значения параметра '{property_name}' для элементов типа '{element_type}':\n")
        for el in elements:
            # Попробуем сначала взять как стандартное поле IFC
            if hasattr(el, property_name):
                val = getattr(el, property_name)
            else:
                val = self._get_property_from_sets(el, property_name)

            # Обработка обёртки ifcopenshell
            if hasattr(val, "wrappedValue"):
                val = val.wrappedValue

            name = getattr(el, "Name", "Без имени")
            print(f"• {name}: {val}")
            results.append((name, val))

        return results

    def _get_property_from_sets(self, element, target_name):
        for rel in getattr(element, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_set = rel.RelatingPropertyDefinition
                if prop_set.is_a("IfcPropertySet"):
                    for prop in prop_set.HasProperties:
                        if prop.Name == target_name:
                            return getattr(prop, "NominalValue", None)
        return None

    def list_available(self):
        print("📚 Доступные категории и типы элементов:")
        for cat_name, elements in self.dataset.items():
            print(f"\n{cat_name.upper()}:")
            for key in elements.keys():
                print(f"  - {key}")
