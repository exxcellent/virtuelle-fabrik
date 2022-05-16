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
def optimizedOrderAmount(x,matID,m,orderCosts):
    storageCosts = 0
    for ms in MaterialRessources.materialStorages:
        if ms.material_ID == matID:
            storageCosts = ms.costsPerUnit
    return orderCosts/(storageCosts*(m+x))

def calloptOrderAmount(narr):
    i = 0
    while i < narr.size/2:
        opt = minimize(optimizedOrderAmount, 200, args=(narr[0][i],narr[1][i], 5000))
        res = math.ceil(opt.fun)
        if res < narr[1][i]:        # if optimum smaller than needed amount, res = needed amount
            res = narr[1][i]
        print("Optimized Order Amount for Material with ID", narr[0][i], "is:", res)
        i += 1

calloptOrderAmount(materialPlanning(b1))