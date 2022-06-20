#Each material has an ID, a name and a purchase price per unit.
# In addition, order costs are incurred differently for each material
class Material(object):
    def __init__(self, material_ID: int, materialName: str, pricePerUnit: float, orderCosts: float):
        self.material_ID = material_ID
        self.materialName = materialName
        self.pricePerUnit = pricePerUnit
        self.orderCosts = orderCosts

# This is an intermediate class that defines how many units of material
# the respective recipe requires to produce a product.
class MaterialRequirements(object):
    def __init__(self, recipe_ID: int, material_ID: int, requiredQuantities: int):
        self.recipe_ID = recipe_ID
        self.material_ID = material_ID
        self.requiredQuantities = requiredQuantities

# This class represents how much of each material is currently stored in the warehouse
# The reservedStock stands for materials which are already in a production queue
class MaterialStorage(object):
    def __init__(self, material_ID: int, stock: int, stockReserved: int, stockUp: int, costsPerUnit: float):
        self.material_ID = material_ID
        self.stock = stock
        self.stockReserved = stockReserved
        self.stockUp = stockUp
        self.costsPerUnit = costsPerUnit


#in the following arrays, you can add new materials, with their storage and their requirements for specific recipes
materials =[
    Material(material_ID=1, materialName="glass", pricePerUnit=0.2, orderCosts=500.0),
    Material(2, "water", 0.1, 300.0),
]

materialStorages = [
    MaterialStorage(material_ID=1, stock=30, stockReserved=45, stockUp=0, costsPerUnit=2.0),
    MaterialStorage(2, 10, 100, 0, 1.0)
]

matRequirements = [
    MaterialRequirements(recipe_ID=1, material_ID=1, requiredQuantities=2),
    MaterialRequirements(1, 2, 1),
]