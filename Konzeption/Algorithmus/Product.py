
class Product(object):
    """This constructor defines the product attributes

    :param product_ID: primary Key
    :type product_ID: int
    :param name: name of the product
    :type name: str
    :param sellPrice: selling price of product
    :type sellPrice: float
    :param recipe_ID: points to the recipe of the product
    :type recipe_ID: int
    """
    def __init__(self, product_ID: int, name: str, sellPrice: float, recipe_ID: int):
        self.product_ID = product_ID
        self.name = name
        self.sellPrice = sellPrice
        self.recipe_ID = recipe_ID


class ProductStorage(object):
    """This constructor represents how much of each product is currently stored in the warehouse
        :param stock: stock count
        :type stock: int
        :param capacity: maximum capacity, which can be stored
        :type capacity: int
        :param output: product output per time unit due to shipping
        :type output: int
        :param product_ID: product ID which is stored
        :type product_ID: int
        :param costsPerUnit: storage costs of the product per time unit
        :type costsPerUnit: float
        """
    def __init__(self, stock: int, capacity: int, output: int, product_ID: int, costsPerUnit: float):

        self.stock = stock
        self.capacity = capacity
        self.output = output
        self.product_ID = product_ID
        self.costsPerUnit = costsPerUnit

# This constructor defines the recipe attributes, for example the steps, which are required to execute
class Recipe(object):
    def __init__(self, recipe_ID: int, name: str, steps, product_ID: int):
        self.recipe_ID = recipe_ID
        self.name = name
        self.steps = steps
        self.product_ID = product_ID

# defines the ID and name of steps
class Step(object):

    def __init__(self, step_ID: int, name: str):
        self.step_ID = step_ID
        self.name = name


step1 = Step(step_ID=1, name="Producing bottle")
step2 = Step(2, "Fill bottle with water")

recipes = [
    Recipe(recipe_ID=1, name="Wasserflasche", steps=[step1,step2], product_ID=1)
    ]

product1 = Product(product_ID=1, name="Wasserflasche", sellPrice=2.0, recipe_ID=1)

