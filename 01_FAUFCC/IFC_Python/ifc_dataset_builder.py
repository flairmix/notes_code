
class IFCDatasetBuilder:
    def __init__(self, ifc_model):
        self.model = ifc_model
        self.dataset = {
            "architecture": {},
            "structure": {},
            "metal": {}
        }

    def build(self):
        self.dataset["architecture"] = {
            "spaces": self.model.by_type("IfcSpace"),
            "walls": self.model.by_type("IfcWall") + self.model.by_type("IfcWallStandardCase"),
            "doors": self.model.by_type("IfcDoor"),
            "windows": self.model.by_type("IfcWindow"),
            "slabs": self.model.by_type("IfcSlab"),
            "stairs": self.model.by_type("IfcStair"),
            "railings": self.model.by_type("IfcRailing"),
            "coverings": self.model.by_type("IfcCovering"),
            "facades": self.model.by_type("IfcCurtainWall"), 
        }

        self.dataset["structure"] = {
            "columns": self.model.by_type("IfcColumn"),
            "beams": self.model.by_type("IfcBeam"),
            "slabs": self.model.by_type("IfcSlab"),
            "footings": self.model.by_type("IfcFooting"),
        }

        self.dataset["metal"] = {
            "members": self.model.by_type("IfcMember"),
            "plates": self.model.by_type("IfcPlate"),
            "columns": self.model.by_type("IfcColumn"),
            "beams": self.model.by_type("IfcBeam"),
        }

        return self.dataset