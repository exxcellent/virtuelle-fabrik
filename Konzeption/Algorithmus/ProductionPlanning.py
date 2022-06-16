import scipy
from scipy.optimize import minimize
import numpy as np
import Product
import MaterialRessources
import WorkingRessources
from typing import List, Dict
from WorkingRessources import Machine

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

# 1 -> [machine1, machine3]
# 2 -> [machine2, machine4]
def getRecipeStepToMachineListMapping(recipe) -> Dict[int, List[Machine]]:
    # {'1': Machine1, Machine3, Machine4; '2': Machine2, Machine5}
    ml = dict()
    for s in recipe.steps:
        for m in WorkingRessources.machineCapabilities:
            if s.step_ID == m.step_ID:
                ml.setdefault(s.step_ID, [])
                try:
                    ml[m.step_ID].append(m)
                except KeyError:
                    ml[s.step_ID] = [m]
    return ml

def stepAmount(recipe):
    return len(recipe.steps)

def getFrequency(mID):
    for m in WorkingRessources.machineCapabilities:
        if mID == m.machine_ID:
            return m.clockRate

def getStepAbility(mID):
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
    lowfreq = 1000
    freq = None
    for s in stepList:
        x = 0
        while (x < s):
            if freq is None:
                freq = 0
            freq += machineList[i].clockRate
            print("Machine ID:", machineList[i].machine_ID, ", Step Ability:", machineList[i].step_ID,
                  ", Frequency:", machineList[i].clockRate, ", Costs per time unit:",
                  getCostsPerMinute(machineList[i].machine_ID))
            i += 1
            x += 1
        if freq is not None:
            if freq < lowfreq:
                lowfreq = freq
        freq = None
    #print(lowfreq)
    return lowfreq

def create_production_frequency_estimator(recipe, machine_list: List[Machine]):
    machine_id_to_index_mapping = {m.machine_ID: i for i, m in enumerate(machine_list)}

    def production_frequency(x: List[float]):
        current_lowest_frequency = 1000
        for step_id, machine_list in getRecipeStepToMachineListMapping(recipe).items():
            step_freq = 0
            for m in machine_list:
                step_freq += getFrequency(m.machine_ID) * x[machine_id_to_index_mapping[m.machine_ID]]
            if step_freq < current_lowest_frequency:
                current_lowest_frequency = step_freq
        return current_lowest_frequency
    print(production_frequency)
    return production_frequency

def create_total_costs_estimator(recipe, machine_list: List[Machine]):
    machine_id_to_index_mapping = {m.machine_ID: i for i, m in enumerate(machine_list)}

    def total_costs(x: List[float]):
        totCosts = 0
        for i, m in enumerate(machine_list):
            totCosts += getCostsPerMinute(m.machine_ID)* x[i]
        # loop over machines and add up all costs and scale with usage times x
        return totCosts

    return total_costs

def create_costs_per_product_estimator(recipe, machine_list):
    production_frequency = create_production_frequency_estimator(recipe, machine_list)
    total_costs = create_total_costs_estimator(recipe, machine_list)

    def costs_per_product(x: List[float]):
        return total_costs(x) / production_frequency(x)

    return costs_per_product

def getBounds(recipe):
    l = len(getMachineList(recipe))
    i = 0
    bounds = []
    while i < l:
        bounds.append((1e-6,1))
        i+=1
    return bounds

machine_list = getMachineList(Product.recipes[0])
costs_per_product = create_costs_per_product_estimator(Product.recipes[0], machine_list)
bounds = getBounds(Product.recipes[0])
opt = minimize(costs_per_product, x0=[1 for m in machine_list],bounds=bounds)
print(opt)

arr = opt.x
sum = 0
sum2 = 0
for i, m in enumerate(machine_list):
    if i < 3:
        sum += m.clockRate*arr[i]
    else:
        sum2 += m.clockRate*arr[i]
print("Frequency for Step 1:",sum, "\n""Frequency for Step 2:", sum2)

optimizeFrequency(Product.recipes[0])