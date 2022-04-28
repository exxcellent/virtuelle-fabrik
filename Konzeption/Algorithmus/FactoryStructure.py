class Batch(object):

    def __init__(self, product_ID, productCount, produced, finished, priority):
        self.product_ID = product_ID
        self.procuctCount = productCount
        self.produced = produced
        self.finished = finished
        self.priority = priority

class Default(object):

    def __init__(self, machine_ID, start, finish):
        self.machine_ID = machine_ID
        self.start = start
        self.finish = finish

class Employee(object):

    def __init__(self, employee_ID, changeoverTime):
        self.employee_ID = employee_ID
        self.changeoverTime = changeoverTime

class EmployeeEmpowerment(object):

    def __init__(self, employee_ID, step_ID, clockRate):
        self.employee_ID = employee_ID
        self.step_ID = step_ID
        self.clockRate = clockRate

class EmployeeWorkingHours(object):

    def __init__(self, employee_ID, start, finish):
        self.employee_ID = employee_ID
        self.start = start
        self.finish = finish

class Machine(object):

    def __init__(self, machine_ID, station_ID, setupTime, costsPerMinute, finished, employeeCapacity,
                minimumNumberOfEmployees, probabilityOfDefault):
        self.machine_ID = machine_ID
        self.station_ID = station_ID
        self.setupTime = setupTime
        self.costsPerMinute = costsPerMinute
        self.finished = finished
        self.employeeCapacity = employeeCapacity
        self.minimumNumberOfEmployees = minimumNumberOfEmployees
        self.probabilityOfDefault = probabilityOfDefault

class MachineCapability(object):

    def __init__(self, machine_ID, step_ID, clockRate):
        self.machine_ID = machine_ID
        self.step_ID = step_ID
        self.clockRate = clockRate

class Material(object):

    def __init__(self, material_ID, materialName, pricePerUnit):
        self.material_ID = material_ID
        self.materialName = materialName
        self.pricePerUnit = pricePerUnit

class MaterialRequirements(object):

    def __init__(self, recipe_ID, material_ID, requiredQuantities):
        self.recipe_ID = recipe_ID
        self.material_ID = material_ID
        self.requiredQuantities = requiredQuantities

class MaterialWarehouse(object):

    def __init__(self, material_ID, stock, stockUp):
        self.material_ID = material_ID
        self.stock = stock
        self.stockUp = stockUp

class Product(object):

    def __init__(self, product_ID, sellPrice, recipe_ID):
        self.product_ID = product_ID
        self.sellPrice = sellPrice
        self.recipe_ID = recipe_ID

class Recipe(object):

    def __init__(self, recipe_ID, steps):
        self.recipe_ID = recipe_ID
        self.steps = steps

class Scheduling(object):

    def __init__(self, batch_ID, station_ID, employee_ID):
        self.batch_ID = batch_ID
        self.station_ID = station_ID
        self.employee_ID = employee_ID

class Station(object):

    def __init__(self, station_ID, employeeCapacity):
        self.station_ID = station_ID
        self.employeeCapacity = employeeCapacity

class Step(object):

    def __init__(self, step_ID, name):
        self.step_ID = step_ID
        self.name = name

class Warehouse(object):

    def __init__(self, stock, capacity, output, product_ID):
        self.stock = stock
        self.capacity = capacity
        self.output = output
        self.product_ID = product_ID

class WorkingTimeMachine(object):

    def __init__(self, machine_ID, start, finish):
        self.machine_ID = machine_ID
        self.start = start
        self.finish = finish

step1 = Step(step_ID=1, name="Producing bottle")
step2 = Step(2, "Fill bottle with water")

recipe1 = Recipe(recipe_ID=1, steps=[step1,step2])

product1 = Product(1, 2.0, 1)

materials =[
    Material(material_ID=1, materialName="glass", pricePerUnit=0.2),
    Material(2, "water", 0.1),
]

matRequirements = [
    MaterialRequirements(recipe_ID=1, material_ID=1, requiredQuantities=2),
    MaterialRequirements(1, 2, 1),
]

stations = [
    Station(station_ID=1, employeeCapacity=15),
    Station(2,11),
]

employeesStation1 = stations[0].employeeCapacity
employeesStation2 = stations[1].employeeCapacity

machines = [
    Machine(machine_ID=1,station_ID=1, setupTime=0, costsPerMinute=5.0, finished='false', employeeCapacity=5,
            minimumNumberOfEmployees=3, probabilityOfDefault=0.01),
    Machine(2, 1, 0, 7.0, 'false', 7, 5, 0.005),
    Machine(3, 1, 0, 4.0, 'false', 3, 2, 0.02),
    Machine(4, 2, 0, 4.0, 'false', 5, 3, 0.01),
    Machine(5, 2, 0, 5.0, 'false', 5, 3, 0.008),
]

machineCapabilities = [
    MachineCapability(machine_ID=1,step_ID=1,clockRate=5),      #1
    MachineCapability(2,2,7),                                   #2
    MachineCapability(3,1,3),                                   #1
    MachineCapability(4,1,5),                                   #1
    MachineCapability(5,2,5),                                   #2
]

def machineSort(recipe: Recipe):
    machineList = []
    counter = None
    stepList = []
    for s in recipe.steps:
        if counter is not None:
            stepList.append(counter)
        counter = 0
        for m in machineCapabilities:
            if s.step_ID == m.step_ID:
                machineList += m
                counter += 1

    numberOfSteps = len(stepList)
    for m in machineList:





# calculate Price per Product
