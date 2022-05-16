class Material(object):

    def __init__(self, material_ID, materialName, pricePerUnit):
        self.material_ID = material_ID
        self.materialName = materialName
        self.pricePerUnit = pricePerUnit

class MaterialRequirements(object):

    def __init__(self, recipe_ID, material_ID, requiredQuantities):
        self.recipe_ID = recipe_ID
        self.material_ID = material_ID
        self.requiredQuantities = requiredQuantities

class MaterialStorage(object):

    def __init__(self, material_ID, stock, stockReserved, stockUp, costsPerUnit):
        self.material_ID = material_ID
        self.stock = stock
        self.stockReserved = stockReserved
        self.stockUp = stockUp
        self.costsPerUnit = costsPerUnit

materials =[
    Material(material_ID=1, materialName="glass", pricePerUnit=0.2),
    Material(2, "water", 0.1),
]

materialStorages = [
    MaterialStorage(material_ID=1, stock=30, stockReserved=45, stockUp=0, costsPerUnit=1.5),
    MaterialStorage(2, 10, 100, 0, 100)
]

matRequirements = [
    MaterialRequirements(recipe_ID=1, material_ID=1, requiredQuantities=2),
    MaterialRequirements(1, 2, 1),
]