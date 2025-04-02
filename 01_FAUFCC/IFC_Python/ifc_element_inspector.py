import ifcopenshell.geom

class IFCElementInspector:
    def __init__(self, dataset):
        self.dataset = dataset

    def unwrap(self, value):
        return value.wrappedValue if hasattr(value, "wrappedValue") else value

    def get_elements_by_category(self, category, element_type=None) -> list:
        if category not in self.dataset or element_type not in self.dataset[category]:
            print(f"⚠️ Раздел '{category}' или тип элемента '{element_type}' не найден.")
            return None

        return self.dataset[category][element_type]


    def get_element(self, category, element_type, index):
        if category not in self.dataset or element_type not in self.dataset[category]:
            print(f"⚠️ Раздел '{category}' или тип элемента '{element_type}' не найден.")
            return None

        elements = self.dataset[category][element_type]
        if index >= len(elements):
            print(f"⚠️ Индекс {index} вне диапазона.")
            return None

        return elements[index]

    def get_coordinates(self, element):
        def extract_coords(placement):
            if (
                hasattr(placement, "RelativePlacement")
                and hasattr(placement.RelativePlacement, "Location")
            ):
                coords = placement.RelativePlacement.Location.Coordinates
                return [self.unwrap(c) for c in coords]
            return [0.0, 0.0, 0.0]

        coords = [0.0, 0.0, 0.0]
        placement = getattr(element, "ObjectPlacement", None)

        while placement:
            step = extract_coords(placement)
            coords = [sum(x) for x in zip(coords, step)]
            placement = getattr(placement, "PlacementRelTo", None)

        return tuple(coords)

    def get_coordinates_geom(self, element):
        try:
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)

            shape = ifcopenshell.geom.create_shape(settings, element)
            verts = shape.geometry.verts

            x = verts[0::3]
            y = verts[1::3]
            z = verts[2::3]

            center = (
                sum(x) / len(x) if x else 0.0,
                sum(y) / len(y) if y else 0.0,
                sum(z) / len(z) if z else 0.0
            )
            return center

        except Exception as e:
            print(f"⚠️ Не удалось построить геометрию: {e}")
            return None

    def get_bounding_box(self, element):
        try:
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)

            shape = ifcopenshell.geom.create_shape(settings, element)
            verts = shape.geometry.verts

            x = verts[0::3]
            y = verts[1::3]
            z = verts[2::3]

            min_point = (min(x), min(y), min(z))
            max_point = (max(x), max(y), max(z))

            return {
                "min": min_point,
                "max": max_point,
                "size": (
                    max_point[0] - min_point[0],
                    max_point[1] - min_point[1],
                    max_point[2] - min_point[2],
                )
            }

        except Exception as e:
            print(f"⚠️ Не удалось получить bounding box: {e}")
            return None

    def get_hierarchy(self, element):
        print(f"\n📂 Иерархия для элемента: {getattr(element, 'Name', 'Без имени')}")
        current = element

        while current:
            name = getattr(current, "Name", "")
            guid = getattr(current, "GlobalId", "")
            print(f"• {current.is_a()} — {name} [GUID: {guid}]")

            if hasattr(current, "ContainedInStructure"):
                rels = current.ContainedInStructure
                if rels:
                    current = rels[0].RelatingStructure
                    continue

            if hasattr(current, "Decomposes") and current.Decomposes:
                current = current.Decomposes[0].RelatingObject
            else:
                break

    def get_field_value(self, element, field_name):
        # 1. Пробуем встроенное поле
        if hasattr(element, field_name):
            val = getattr(element, field_name)
            return self.unwrap(val)

        # 2. Пробуем найти в PropertySets
        for rel in getattr(element, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_set = rel.RelatingPropertyDefinition
                if prop_set.is_a("IfcPropertySet"):
                    for prop in prop_set.HasProperties:
                        if prop.Name == field_name:
                            return self.unwrap(getattr(prop, "NominalValue", None))

        return None
