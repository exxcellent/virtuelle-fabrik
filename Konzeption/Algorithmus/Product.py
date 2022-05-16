class Product(object):

    def __init__(self, product_ID, sellPrice, recipe_ID):
        self.product_ID = product_ID
        self.sellPrice = sellPrice
        self.recipe_ID = recipe_ID

class ProductStorage(object):

    def __init__(self, stock, capacity, output, product_ID, costsPerUnit):
        self.stock = stock
        self.capacity = capacity
        self.output = output
        self.product_ID = product_ID
        self.costsPerUnit = costsPerUnit

class Recipe(object):

    def __init__(self, recipe_ID, steps, product_ID):
        self.recipe_ID = recipe_ID
        self.steps = steps
        self.product_ID = product_ID

class Step(object):

    def __init__(self, step_ID, name):
        self.step_ID = step_ID
        self.name = name


step1 = Step(step_ID=1, name="Producing bottle")
step2 = Step(2, "Fill bottle with water")

recipes = [
    Recipe(recipe_ID=1, steps=[step1,step2], product_ID=1)
    ]

product1 = Product(1, 2.0, 1)

