# Each Station has their specific employee Capacity and Machines
class Station(object):
    def __init__(self, station_ID, employeeCapacity):
        self.station_ID = station_ID
        self.employeeCapacity = employeeCapacity

# This class defines many attributes about a machine
class Machine(object):
    def __init__(self, machine_ID, station_ID, setupTime, costsPerTimeUnit, finished, employeeCapacity,
                 minimumNumberOfEmployees, probabilityOfBreakdown):
        self.machine_ID = machine_ID
        self.station_ID = station_ID
        self.setupTime = setupTime
        self.costsPerTimeUnit = costsPerTimeUnit
        self.finished = finished
        self.employeeCapacity = employeeCapacity
        self.minimumNumberOfEmployees = minimumNumberOfEmployees
        self.probabilityOfBreakdown = probabilityOfBreakdown

# This class defines which step a machine can execute and the clockRate the machine can reach
class MachineCapability(object):
    def __init__(self, machine_ID, step_ID, clockRate):
        self.machine_ID = machine_ID
        self.step_ID = step_ID
        self.clockRate = clockRate

# records the working time of a machine
class WorkingTimeMachine(object):
    def __init__(self, machine_ID, start, finish):
        self.machine_ID = machine_ID
        self.start = start
        self.finish = finish

# records the breakdown time of a machine
class Breakdown(object):
    def __init__(self, machine_ID, start, finish):
        self.machine_ID = machine_ID
        self.start = start
        self.finish = finish

stations = [
    Station(station_ID=1, employeeCapacity=15),
    Station(2,11),
]

machines = [
    Machine(machine_ID=1, station_ID=1, setupTime=0, costsPerTimeUnit=5.0, finished='false',
            employeeCapacity=5, minimumNumberOfEmployees=3, probabilityOfBreakdown=0.01),
    Machine(2, 1, 0, 7.0, 'false', 7, 5, 0.005),
    Machine(3, 1, 0, 4.0, 'false', 3, 2, 0.02),
    Machine(4, 2, 0, 4.0, 'false', 5, 3, 0.01),
    Machine(5, 2, 0, 5.0, 'false', 7, 3, 0.008),
    Machine(6, 2, 0, 6.0, 'false', 2, 1, 0.018)
]


machineCapabilities = [
    MachineCapability(machine_ID=1,step_ID=1,clockRate=5),      #1
    MachineCapability(2,2,5),                                   #2
    MachineCapability(3,1,7),                                   #1
    MachineCapability(4,1,6),                                   #1
    MachineCapability(5,2,5),                                   #2
    MachineCapability(6,3,2),                                   #3
]

def machineSort(recipe):
    machineList = []
    counter = None
    stepList = []
    for s in recipe.steps:
        if counter is not None:
            stepList.append(counter)
        counter = 0
        for m in machineCapabilities:
            if s.step_ID == m.step_ID:
                machineList.append(m)
                counter += 1

    numberOfSteps = len(stepList)
    for m in machineList:
        print("Machine ID:" ,m.machine_ID , ", Step ID:" , m.step_ID)

#machineSort(Product.recipes[0])