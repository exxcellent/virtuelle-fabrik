class Employee(object):
    """This constructor represents an employee

        :param employee_ID: primary Key
        :type employee_ID: int
        :param changeoverTime: shift changes
        :type changeoverTime: float
    """
    def init(self, employee_ID: int, changeoverTime):
        self.employee_ID = employee_ID
        self.changeoverTime = changeoverTime


class EmployeeEmpowerment(object):
    """This constructor defines which steps an employee can execute and the clock rate

        :param employee_ID: primary Key
        :type employee_ID: int
        :param step_ID: foreign key
        :type step_ID: int
        :param clockrate: workflow of an employee
        :type clockrate: float
    """
    def init(self, employee_ID: int, step_ID: int, clockRate: float):
        self.employee_ID = employee_ID
        self.step_ID = step_ID
        self.clockRate = clockRate


class EmployeeWorkingHours(object):
    """This constructor records the working hours of an employee

        :param employee_ID: primary Key
        :type employee_ID: int
        :param start: shiftbegin of an employee
        :type start: int
        :param finish: shiftend of an employee
        :type finish: int
    """
    def init(self, employee_ID: int, start, finish):
        self.employee_ID = employee_ID
        self.start = start
        self.finish = finish