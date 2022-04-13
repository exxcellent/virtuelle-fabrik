class Machine(object):

    def __init__(self, machine_ID, station_ID, setupTime, costsPerMinute, finished, employeeCapacity, minimumNumberOfEmployees, probabilityOfDefault):
        self.machine_ID = machine_ID
        self.station_ID = station_ID
        self.setupTime = setupTime
        self.costsPerMinute = costsPerMinute
        self.finished = finished
        self.employeeCapacity = employeeCapacity
        self.minimumNumberOfEmployees = minimumNumberOfEmployees
        self.probabilityOfDefault = probabilityOfDefault
