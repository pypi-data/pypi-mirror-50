"""
   用于计算员工的薪资情况
"""
company = "fenda"

def yearSalary(monthSalary):
    """ 计算年薪 """
    return monthSalary * 12

def daySalary(monthSalary):
    """ 计算日薪 """
    return monthSalary / 22