import scipy
from scipy.optimize import minimize
import math
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
    ml = dict()
    for s in recipe.steps:
        for m in WorkingRessources.machineCapabilities:
            if s.step_ID == m.step_ID:
                ml[s.step_ID]
                ml[s.step_ID].append(m)
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
    lowfreq = 1000
    freq = None
    for s in stepList:
        x = 0
        if freq < lowfreq && freq is not None:
            lowfreq = freq
        freq = None
        while(x < s):
            freq += machineList[i].clockRate
            print("Machine ID:",machineList[i].machine_ID,", Step Ability:", machineList[i].step_ID,
            ", Frequency:",machineList[i].clockRate,", Costs per time unit:", getCostsPerMinute(machineList[i].machine_ID))

            i+=1
            x+=1
    print(lowfreq)

optimizeFrequency(Product.recipes[0])

def create_production_frequency_estimator(recipe, machine_list: List[Machine]):
    machine_id_to_index_mapping = {m.machine_ID: i for i, m in enumerate(machine_list)}

    def production_frequency(x: List[float]):
        current_lowest_frequency = 1000
        for step_id, machine_list in getRecipeStepToMachineListMapping(recipe).iteritems():
            step_freq = 0
            for m in machine_list:
                step_freq += getFrequency(m.machine_ID)*x[machine_id_to_index_mapping[m.id]]

            if step_freq < current_lowest_frequency:
                current_lowest_frequency = step_freq
        return current_lowest_frequency

    return production_frequency


def create_total_costs_estimator(recipe, machine_list: List[Machine], employee_list: list):
    def total_costs(x: List[float]):
        # loop over machines and add up all costs and scale with usage times x
        # loop over all employees and add up all costs
        pass

    return total_costs

def create_costs_per_product_estimator(recipe, machine_list):
    production_frequency = create_production_frequency_estimator(recipe, machine_list)
    total_costs = create_total_costs_estimator(recipe, machine_list)

    def costs_per_product(x: List[float]):
        return total_costs(x)/production_frequency(x)

    return costs_per_product


minimize(costs_per_product, x0=[1,1,1,1,1])


optimizeFrequency(Product.recipes[0])
print(getStepList(Product.recipes[0]))