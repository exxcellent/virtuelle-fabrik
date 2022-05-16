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