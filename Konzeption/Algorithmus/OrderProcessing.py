from scipy.optimize import minimize
import math
import numpy as np
import Product
import MaterialRessources

class Batch(object):
    """This constructor describes all needed details about an order

    :param product_ID: primary Key
    :type product_ID: int
    :param productCount: amount of the product, which is desired
    :type productCount: int
    :param produced: already produced products
    :type produced: int
    :param finished: decides if the batch is either finished or in progress
    :type finished: int
    :param priority: priority of the order
    :type priority: int
    """
    def __init__(self, product_ID, productCount, produced, finished, priority):
        self.product_ID = product_ID
        self.productCount = productCount
        self.produced = produced
        self.finished = finished
        self.priority = priority

class Scheduling(object):
    """This constructor describes how the batch is scheduled

    :param batch_ID: primary Key
    :type batch_ID: int
    :param station_ID: foreign Key
    :type station_ID: int
    :param employee_ID: foreign Key
    :type employee_ID: int
    """
    def __init__(self, batch_ID, station_ID, employee_ID):
        self.batch_ID = batch_ID
        self.station_ID = station_ID
        self.employee_ID = employee_ID

b1 = Batch(product_ID=1, productCount=100, produced=0, finished='false', priority=10)

def materialPlanning(batch):
    """This function calculates the total material needs of an order and takes the storage stock into account

    :param batch: Inputs a Object of batch, which has all informations about a specific order
    :type batch: object
    :return: Returns a numpy array with 2 dimensions (material IDs and material amounts)
    :rtype: numpy
    """
    counter = 0
    recipeID = 0
    matList = []
    matAmountList = []
    for rec in Product.recipes:
        if batch.product_ID == rec.product_ID:
            recipeID = rec.recipe_ID
    for mat in MaterialRessources.matRequirements:
        if mat.recipe_ID == recipeID:
            matList.append(mat.material_ID)
            matAmountList.append(mat.requiredQuantities*batch.productCount)
    for mat in matList:             # for Loop for reqMaterial-stock
        counter +=1
        for s in MaterialRessources.materialStorages:
            if mat == s.material_ID:
                matAmountList[counter-1] -= s.stock
    narr = np.array([matList, matAmountList])
    return narr

print("Product ID and Amount:", "\n",materialPlanning(b1))

def getStorageCosts(matID):
    """This is a getter function for the storage costs per material

    :param matID: Material ID, which is needed to get the fitting storage costs
    :type matID: int
    :return: Returns the storage costs per material
    :rtype: float
    """
    for ms in MaterialRessources.materialStorages:
        if ms.material_ID == matID:
            storageCosts = ms.costsPerUnit
            return storageCosts

def getMaterialCosts(matID):
    """This is a getter function for the material costs

    :param matID: Material ID, which is needed to get the fitting material costs
    :type matID: int
    :return: Returns the material costs
    :rtype: float
    """
    for ms in MaterialRessources.materials:
        if ms.material_ID == matID:
            materialCosts = ms.pricePerUnit
            return materialCosts

def getBaseOrderCosts(matID):
    """This is a getter function for the base order costs for a specific material ID

    :param matID: Material ID, which is needed to get the fitting base order costs
    :type matID: int
    :return: Returns the order costs
    :rtype: float
    """
    for ms in MaterialRessources.materials:
        if ms.material_ID == matID:
            orderCosts = ms.orderCosts
            return orderCosts

def optimizedOrderAmount(x, orderAmount, storageCosts, orderCosts):
    """This function calculates the order costs with a quantity discount

    :param x: Inputs a starting value for material amount
    :type x: int
    :param orderAmount: Inputs the needed material amount
    :type orderAmount: int
    :param storageCosts: Inputs the storage costs for the specific material
    :type storageCosts: float
    :param orderCosts: Inputs the orderCosts
    :type orderCosts: float
    :return: Returns optimized order amount
    :rtype: float
    """
    return storageCosts*x + (orderCosts(x) * orderAmount/x)

def createOrderCostsFunction(order_base_price, price_per_unit, max_rebate, rebate_const = 1.0):
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the order costs

    :param order_base_price: Inputs the base price for an order, without any discount
    :type order_base_price: float
    :param price_per_unit: Inputs the material price per unit
    :type price_per_unit: float
    :param max_rebate: Inputs the maximum discount for an order
    :type max_rebate: float
    :param rebate_const: Inputs the rebate constant
    :type rebate_const: float

    :return: Returns the order costs
    :rtype: float
    """
    def orderCosts(x):
        """This function calculates the order costs with a quantity discount

        :param x: Inputs a starting value for material amount
        :type x: int
        :return: Returns the order costs
        :rtype: float
        """
        return order_base_price + (price_per_unit * (1 - max_rebate * (1 - math.exp(- rebate_const * x)))) * x
    return orderCosts

def calloptOrderAmount(narr):
    """This function is starting the optimization of the order amount

    :param narr: Inputs a numpy array with the material IDs and their needed amount
    :type narr: list
    """
    i = 0
    while i < narr.size/2:
        orderCostFunc = createOrderCostsFunction(getBaseOrderCosts(narr[0][i]), getMaterialCosts(narr[0][i]), 0.2, 0.01)
        opt = minimize(optimizedOrderAmount, 20, args=(narr[1][i], getStorageCosts(narr[0][i]), orderCostFunc), bounds=[(1, 1000)])
        x = math.ceil(opt.x)
        frequency = narr[1][i]/x
        print("Optimized Order Amount for Material with ID", narr[0][i], "is:", x,"with the order frequency:", round(frequency,0))
        i += 1
