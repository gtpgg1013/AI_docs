from tkinter import *

class Car:
    # 자동차 속성
    color = None
    speed = 0
    # 자동차의 행위(--> 함수, 기능)
    def upSpeed(self, value):
        self.speed += value
    def downSpeed(self, value):
        self.speed -= value

car1 = Car() ; car2 = Car()

car1.color = "레-드"
car1.speed = 50
car1.upSpeed(100)

print(car1.color," ",car1.speed)

button1 = Button() # Button class의 instance를 만들어 준 것!