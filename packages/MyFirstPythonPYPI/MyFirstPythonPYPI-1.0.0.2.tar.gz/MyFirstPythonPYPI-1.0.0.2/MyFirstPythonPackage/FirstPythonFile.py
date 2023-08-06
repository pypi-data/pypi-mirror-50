class MyClass:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def returnId(self):
        return self.id

    def returnName(self):
        return self.name


if __name__ == '__main__':
    my_obj = MyClass('Divya Jyoti Das', 1)
    print(my_obj.returnId())
    print(my_obj.returnName())
