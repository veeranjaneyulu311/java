
ser_conf = [2,3,[5,10,[10,[20,30,[100,50,[20]]]]],50]
class A:
    pass


class B(A):
    pass


class C:
    pass


class Gadget:
    """A class used for modelling Gadgets in a web shop."""
    __weight = 100
    __operating_system = None
    __battery_capacity = 2000
    __screen_size = 1

    def __init__(self, weight, operating_system, battery_capacity, screen_size):
        self.__weight = weight
        self.__operating_system = operating_system
        self.__battery_capacity = battery_capacity
        self.__screen_size = screen_size

    def get_weight(self):
        print('get_weight')
        return self.__weight

    def set_weight(self, weight):
        self.__weight = weight

    weight = property(get_weight, set_weight)

    @property
    def operating_system(self):
        print('get')
        return self.__operating_system

    @operating_system.setter
    def operating_system(self, new_os):
        print('set')
        self.__operating_system = new_os


# my_iphone = Gadget(240,'iOS',1980,4)
#
# print(my_iphone.get_weight())
#
# my_iphone.weight
# my_iphone.operating_system='android'
# print(my_iphone.operating_system)
def ser_test(test_data):
    total = 0
    for x in test_data:
        if isinstance(x, list):
            l = ser_test(x)
            total += l
        else:
            total += x
    return total


print(ser_test(ser_conf))


print(dict(zip('x','z')))