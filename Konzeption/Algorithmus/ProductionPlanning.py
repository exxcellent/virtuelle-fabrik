from scipy.optimize import minimize
import Product
import WorkingRessources
from typing import List, Dict
from WorkingRessources import Machine

def getStepList(recipe):
    """This function returns a list of all steps, which are needed to be executed in a recipe

    :param recipe: Recipe object, which stores the required steps
    :type recipe: object
    :return: Returns a List of steps
    :rtype: list
    """
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
    """This function returns a list of all machines, which are needed to be executed in a recipe

    :param recipe: Recipe object, which stores the required steps
    :type recipe: object
    :return: Returns a List of machines
    :rtype: list
    """
    ml = []
    for s in recipe.steps:
        for m in WorkingRessources.machineCapabilities:
            if s.step_ID == m.step_ID:
                ml.append(m)
    return ml

# 1 -> [machine1, machine3]
# 2 -> [machine2, machine4]
def getRecipeStepToMachineListMapping(recipe) -> Dict[int, List[Machine]]:
    """This function is mapping the individual machines to the fitting recipe steps

    :param recipe: Recipe object, which stores the required steps
    :type recipe: object
    :return: Returns a dictionary
    :rtype: dict
    """
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
    """This function returns the amount of steps in a recipe

    :param recipe: Recipe object, which stores the required steps
    :type recipe: object
    :return: Returns the amount of steps
    :rtype: int
    """
    return len(recipe.steps)

def getFrequency(mID):
    """This is a getter function for the clock rate of a machine

    :param mID: Machine ID, which is needed to get the fitting clock rate
    :type mID: int
    :return: Returns the clock rate
    :rtype: float
    """
    for m in WorkingRessources.machineCapabilities:
        if mID == m.machine_ID:
            return m.clockRate

def getStepAbility(mID):
    """This is a getter function for the step ability of a machine

    :param mID: Machine ID, which is needed to get the fitting step ability
    :type mID: int
    :return: Returns the step ID, which the machine is able to execute
    :rtype: int
    """
    for m in WorkingRessources.machineCapabilities:
        if mID == m.machine_ID:
            return m.step_ID

def getCostsPerTimeUnit(mID):
    """This is a getter function for the costs per minute of a machine

    :param mID: Machine ID, which is needed to get the fitting costs per minute
    :type mID: int
    :return: Returns the costs per time unit
    :rtype: float
    """
    for m in WorkingRessources.machines:
        if mID == m.machine_ID:
            return m.costsPerTimeUnit

def getMachineCapabilities(recipe, arr):
    """This function lists all machines which could be taken in account for the optimization of frequency and costs

    :param recipe: Recipe object, which stores the required steps
    :type recipe: object
    :param arr: Inputs a list of capacity utilisation (a result of the frequency and costs optimization) for the machines
    :type arr: list
    """
    machineList = getMachineList(recipe)
    stepList = getStepList(recipe)
    i = 0
    for s in stepList:
        x = 0
        while (x < s):
            print("Machine ID:", machineList[i].machine_ID, ", Step Ability:", machineList[i].step_ID,
                  ", Frequency:", machineList[i].clockRate, ", Costs per time unit:",
                  getCostsPerTimeUnit(machineList[i].machine_ID),"\033[1m", ", Capacity Utilisation:", round(arr[i],2), "\033[0;0m")
            i += 1
            x += 1


def create_production_frequency_estimator(recipe, machine_list: List[Machine]):
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the production frequency

    :param x: Inputs a recipe
    :type x: object
    :param x: Inputs a list of machines
    :type x: list

    :return: Returns the adjusted production frequency
    :rtype: float
    """
    machine_id_to_index_mapping = {m.machine_ID: i for i, m in enumerate(machine_list)}

    def production_frequency(x: List[float]):
        """This function calculates the maximum frequency for each step. The step with the lowest frequency will decide
        the overall frequency for the production

        :param x: Inputs a list of starting values for the capacity utilisation of a machine
        :type x: list
        :return: Returns the overall production frequency
        :rtype: float
        """
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
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the total costs

    :param x: Inputs a recipe
    :type x: object
    :param x: Inputs a list of machines
    :type x: list

    :return: Returns the total costs
    :rtype: float
    """
    machine_id_to_index_mapping = {m.machine_ID: i for i, m in enumerate(machine_list)}

    def total_costs(x: List[float]):
        """This function calculates the total machine costs per time unit

        :param x: Inputs a list of starting values for the capacity utilisation of a machine
        :type x: list
        :return: Returns total costs per timeunit
        :rtype: float
        """
        totCosts = 0
        for i, m in enumerate(machine_list):
            totCosts += getCostsPerTimeUnit(m.machine_ID)* x[i] +1        #little penalty with +1
        # loop over machines and add up all costs and scale with usage times x
        return totCosts

    return total_costs

def create_costs_per_product_estimator(recipe, machine_list):
    production_frequency = create_production_frequency_estimator(recipe, machine_list)
    total_costs = create_total_costs_estimator(recipe, machine_list)

    def costs_per_product(x: List[float]):
        """This function calculates the costs per product

        :param x: Inputs a list of starting values
        :type x: list
        :return: Returns costs per product
        :rtype: float
        """
        return total_costs(x) / production_frequency(x)

    return costs_per_product

def getBounds(recipe):
    """This function creates the bounds for the optimization in a generic way

    :param recipe: Recipe object
    :type recipe: object
    :return: Returns the bounds
    :rtype: list
    """
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
print("\nCosts per product:","\033[1m",round(opt.fun,2), "monetary units", "\033[0;0m"
      "\nThe capacity utilisation of the individual machines are:")
getMachineCapabilities(Product.recipes[0], opt.x)

