
class Material(object):
    """This constructor shows the important attributes of each material

        :param material_ID: primary Key
        :type material_ID: int
        :param materialName: name of the material
        :type materialName: str
        :param pricePerUnit: prices of each material
        :type pricePerUnit: float
        :param orderCosts: costs of the order
        :type orderCosts: float
    """
    def __init__(self, material_ID: int, materialName: str, pricePerUnit: float, orderCosts: float):
        self.material_ID = material_ID
        self.materialName = materialName
        self.pricePerUnit = pricePerUnit
        self.orderCosts = orderCosts


class MaterialRequirements(object):
    """ This constructor defines how many units of material the respective recipe requires to produce a product

        :param recipe_ID: primary Key
        :type recipe_ID: int
        :param material_ID: foreign Key
        :type material_ID: int
        :param requiredQuantities: requirements of each material
        :type requiredQuantities: int
    """
    def __init__(self, recipe_ID: int, material_ID: int, requiredQuantities: int):
        self.recipe_ID = recipe_ID
        self.material_ID = material_ID
        self.requiredQuantities = requiredQuantities


class MaterialStorage(object):
    """This constructor represents how much of each material is currently stored in the warehouse

        :param material_ID: primary Key
        :type material_ID: int
        :param stock: currently in the warehouse
        :type stock: int
        :param stockReserved: products which are already in a production queue
        :type stockReserved: int
        :param stockUp: increase of materials per time unit
        :type stockUp: int
        :param costsPerUnit: costs of the production
        :type costsPerUnit: float
    """
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