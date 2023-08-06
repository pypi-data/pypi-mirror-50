from MyFirstPythonPackage.FirstPythonFile import MyClass

if __name__ == '__main__':
    my_obj = MyClass('DJ', 2)
    print(my_obj.returnId())
    print(my_obj.returnName())
