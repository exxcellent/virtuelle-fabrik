# represents an employee
class Employee(object):
    def init(self, employee_ID: int, changeoverTime):
        self.employee_ID = employee_ID
        self.changeoverTime = changeoverTime

# defines which steps an employee can execute and the clock rate
class EmployeeEmpowerment(object):
    def init(self, employee_ID: int, step_ID: int, clockRate: float):
        self.employee_ID = employee_ID
        self.step_ID = step_ID
        self.clockRate = clockRate

# records the working hours of an employee
class EmployeeWorkingHours(object):
    def init(self, employee_ID: int, start, finish):
        self.employee_ID = employee_ID
        self.start = start
        self.finish = finish