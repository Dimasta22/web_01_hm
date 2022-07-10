from abc import ABCMeta, abstractmethod
import pickle
import json


class SerializationInterface(metaclass=ABCMeta):
    def __init__(self, name, data):
        self.__name = None
        self.name = name
        self.data = data

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


class SerializationJSON(SerializationInterface):
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        parse = name.split('.')
        self.__name = '.'.join([parse.pop(0), 'json'])

    def read(self):
        with open(self.__name, "r") as fh:
            unpacked = json.load(fh)
            print(unpacked)

    def write(self):
        with open(self.__name, "w") as fh:
            json.dump(self.data, fh)


class SerializationBIN(SerializationInterface):
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        parse = name.split('.')
        self.__name = '.'.join([parse.pop(0), 'bin'])

    def read(self):
        with open(self.__name, "rb") as fh:
            unpacked = pickle.load(fh)
            print(unpacked)

    def write(self):
        with open(self.__name, "wb") as fh:
            pickle.dump(self.data, fh)


class Meta(type):
    children_number = 0
    class_number = 0

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance.class_number = cls.children_number
        cls.children_number = cls.children_number + 1
        cls.class_number = cls.class_number + 1
        return instance


Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


if __name__ == '__main__':
    file = 'test'
    file_data = [1, 2, 3, {'4': '5'}]

    abs_test = SerializationJSON(file, file_data)
    abs_test.write()
    abs_test.read()

    abs_test = SerializationBIN(file, file_data)
    abs_test.write()
    abs_test.read()

    assert (Cls1.class_number, Cls2.class_number) == (0, 1)
    a, b = Cls1(''), Cls2('')
    assert (a.class_number, b.class_number) == (0, 1)
