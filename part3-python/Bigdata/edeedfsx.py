class A(object):
    def __init__(self):
        self.x = 'Hello'

    def method_a(self, foo):
        print (self.x + ' ' + foo)

    def method_b(self):
        kid = B()
        print(kid.x)

class B(object):
    def __init__(self):
        self.x = "gogogohoos"

a = A()
a.method_a('ddsf')
b = A()
b.method_b()