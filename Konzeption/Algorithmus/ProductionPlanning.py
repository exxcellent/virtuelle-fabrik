from scipy.optimize import minimize
import math
import numpy as np
import Product
import MaterialRessources
import WorkingRessources

def getStepList(recipe):
    counter = None
    sl = []
    for s in recipe.steps:
        if counter is not None:
            sl.append(counter)
        counter = 0
        for m in WorkingRessources.machineCapabilities:
            if s.step_ID == m.step_ID:
                counter += 1
    sl.append(counter)
    return sl

def getMachineList(recipe):
    ml = []
    for s in recipe.steps:
        for m in WorkingRessources.machineCapabilities:
            if s.step_ID == m.step_ID:
                ml.append(m)
    return ml

def stepAmount(recipe):
    return len(recipe.steps)

def getFrequency(mID):
    for m in WorkingRessources.machineCapabilities:
        if mID == m.machine_ID:
            return m.clockRate

def getStebAbility(mID):
    for m in WorkingRessources.machineCapabilities:
        if mID == m.machine_ID:
            return m.step_ID

def getCostsPerMinute(mID):
    for m in WorkingRessources.machines:
        if mID == m.machine_ID:
            return m.costsPerTimeUnit

def optimizeFrequency(recipe):
    machineList = getMachineList(recipe)
    stepList = getStepList(recipe)
    i = 0
    for s in stepList:
        x = 0
        while(x < s):
            print("Machine ID:",machineList[i].machine_ID,", Step Ability:", machineList[i].step_ID,
            ", Frequency:",machineList[i].clockRate,", Costs per time unit:", getCostsPerMinute(machineList[i].machine_ID))
            i+=1
            x+=1

optimizeFrequency(Product.recipes[0])
print(getStepList(Product.recipes[0]))