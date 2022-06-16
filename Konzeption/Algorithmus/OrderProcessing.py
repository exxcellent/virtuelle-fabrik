from scipy.optimize import minimize
import math
import numpy as np
import Product
import MaterialRessources

class Batch(object):

    def __init__(self, product_ID, productCount, produced, finished, priority):
        self.product_ID = product_ID
        self.productCount = productCount
        self.produced = produced
        self.finished = finished
        self.priority = priority

class Scheduling(object):

    def __init__(self, batch_ID, station_ID, employee_ID):
        self.batch_ID = batch_ID
        self.station_ID = station_ID
        self.employee_ID = employee_ID

b1 = Batch(product_ID=1, productCount=100, produced=0, finished='false', priority=10)

def materialPlanning(batch):
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

#https://www.microtech.de/blog/optimale-bestellmenge
def getStorageCosts(matID):
    for ms in MaterialRessources.materialStorages:
        if ms.material_ID == matID:
            storageCosts = ms.costsPerUnit
            return storageCosts

def getMaterialCosts(matID):
    for ms in MaterialRessources.materials:
        if ms.material_ID == matID:
            materialCosts = ms.pricePerUnit
            return materialCosts

def getBaseOrderCosts(matID):
    for ms in MaterialRessources.materials:
        if ms.material_ID == matID:
            orderCosts = ms.orderCosts
            return orderCosts

def optimizedOrderAmount(x, orderAmount, storageCosts, orderCosts):
    return storageCosts*x + (orderCosts(x) * orderAmount/x)

def createOrderCostsFunction(order_base_price, price_per_unit, max_rebate, rebate_const = 1.0):
    def orderCosts(x):
        return order_base_price + (price_per_unit * (1 - max_rebate * (1 - math.exp(- rebate_const * x)))) * x
    return orderCosts

def calloptOrderAmount(narr):
    i = 0
    while i < narr.size/2:
        orderCostFunc = createOrderCostsFunction(getBaseOrderCosts(narr[0][i]), getMaterialCosts(narr[0][i]), 0.2, 0.01)
        opt = minimize(optimizedOrderAmount, 20, args=(narr[1][i], getStorageCosts(narr[0][i]), orderCostFunc), bounds=[(1, 1000)])
        x = math.ceil(opt.x)
        frequency = narr[1][i]/x
        #frequency = math.ceil(frequency)
        print("Optimized Order Amount for Material with ID", narr[0][i], "is:", x,"with the order frequency:", frequency)
        i += 1



#opt = minimize(optimizedOrder, x0)
#print(opt)

calloptOrderAmount(materialPlanning(b1))