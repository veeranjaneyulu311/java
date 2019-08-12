import pandas as pd
df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 'B': ['B0', 'B1', 'B2', 'B3'], 'C': ['C0', 'C1', 'C2', 'C3'], 'D': ['D0', 'D1', 'D2', 'D3']}, index=[0, 1, 2, 3])
df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'], 'B': ['B4', 'B5', 'B6', 'B7'], 'C': ['C4', 'C5', 'C6', 'C7'], 'D': ['D4', 'D5', 'D6', 'D7']}, index=[4, 5, 6, 7])
df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'], 'B': ['B8', 'B9', 'B10', 'B11'], 'C': ['C8', 'C9', 'C10', 'C11'], 'D': ['D8', 'D9', 'D10', 'D11']}, index=[8, 9, 10, 11])
df4 = pd.DataFrame({'B': ['B2', 'B3', 'B6', 'B7'], 'D': ['D2', 'D3', 'D6', 'D7'], 'F': ['F2', 'F3', 'F6', 'F7']}, index=[2, 3, 6, 7])
df5 = pd.DataFrame()
df6 = None

print(pd.concat([df1, df6,df5,df2]))






'''
class Student:

    species = 'mammal'

    def __init__(self, name, age):
        self.myname = name
        self.myage = age
        self.college = False

    def description(self):
        return "{} is {} years old".format(self.myname, self.myage)

    def speak(self, sound):
        return "{} says {}".format(self.myname, sound)

    def setcollege(self):
        self.college = True


def get_biggest_number(*args):
    return max(args)


# x = Student('veer', 29)
# y = Student('Phani', 24)
# z = Student('Srinu', 25)


# print(get_biggest_number(x.myage, y.myage, z.myage))
# print(y.description())
# print(Student.description(y))
# print(y.speak("speaks"))


# print(x.myage, x.myname, x.species)
# print(y.myage, y.myname, y.species)
# print(z.myage, z.myname, z.species)

# x.setcollege()
# print(x.college)
# print(y.college)
# print(z.college)

class Dog:

    # Class attribute
    species = 'mammal'

    # Initializer / Instance attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # instance method
    def description(self):
        return "{} is {} years old".format(self.name, self.age)

    # instance method
    def speak(self, sound):
        return "{} says {}".format(self.name, sound)


class Russell(Dog):
    def speak(self, sound):
        return "override"


class Bull(Dog):
    def speak(self, sound):
        return "ov"


x = Russell("l", 25)
y = Bull("l", 25)
print(isinstance(x,y))
'''