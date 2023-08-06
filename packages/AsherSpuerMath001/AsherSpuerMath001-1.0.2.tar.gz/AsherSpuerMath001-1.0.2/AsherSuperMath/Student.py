class Student:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def __str__(self):
        return "姓名：{0}; 年纪：{1}; 性别：{2}".format(self.name, self.age, self.sex)


def printStudentInfo():
    student = Student("刘迪波", 29, "男")
    print(student)

if __name__ == "__main__":
    printStudentInfo()