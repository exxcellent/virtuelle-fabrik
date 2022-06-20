class Station(object):
    """This constructor has their own stations with their specific employee capacity and machines

        :param station_ID: primary Key
        :type station_ID: int
        :param employeeCapacity: capacity of employees for each station
        :type employeeCapacity: int
    """
    def __init__(self, station_ID, employeeCapacity):
        self.station_ID = station_ID
        self.employeeCapacity = employeeCapacity


class Machine(object):
    """This constructor defines many attributes about a machine

        :param machine_ID: primary Key
        :type machine_ID: int
        :param station_ID: foreign Key
        :type station_ID: int
        :param setupTime: setup the machines before using
        :type setupTime: float
        :param costsPerTimeUnit: costs of the machine per timeunit
        :type costsPerTimeUnit: float
        :param finished: finished the production
        :type finished: int
        :param employeeCapacity: capacity of employees on every machine
        :type employeeCapacity: int
        :param minimumNumberOfEmployees: minimum number of employees, necessary for working
        :type minimumNumberOfEmployees: int
        :param probabilityOfBreakdown: probability of a breakdown of a machine
        :type probabilityOfBreakdown: float
    """
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


class MachineCapability(object):
    """This constructor defines which step a machine can execute and the clockrate the machine can reach

        :param machine_ID: primary Key
        :type machine_ID: int
        :param step_ID: foreign Key
        :type step_ID: int
        :param clockRate: workflow of a machine
        :type clockRate: float
    """
    def __init__(self, machine_ID, step_ID, clockRate):
        self.machine_ID = machine_ID
        self.step_ID = step_ID
        self.clockRate = clockRate


class WorkingTimeMachine(object):
    """This constructor records the working time of a machine

        :param machine_ID: primary Key
        :type machine_ID: int
        :param start: first/start time of the machine
        :type start: float
        :param finish: last use of the machine
        :type finish: float
    """
    def __init__(self, machine_ID, start, finish):
        self.machine_ID = machine_ID
        self.start = start
        self.finish = finish


class Breakdown(object):
    """This constructor records the breakdown time of a machine

        :param machine_ID: primary Key
        :type machine_ID: int
        :param start: first/start time of the breakdown
        :type start: float
        :param finish: solved breakdown
        :type finish: float
    """
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