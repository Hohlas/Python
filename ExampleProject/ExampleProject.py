class VEHICLE(object):
    def __init__(self, color, doors, tires, vtype): # атрибуты класса
        self.color = color
        self.doors = doors
        self.tires = tires
        self.vtype = vtype
    def BREAK(self):    # Метод описывает, что делает класс
        return "%s braking" % self.vtype
    def DRIVE(self):
        return "I'm driving a %s %s!" % (self.color, self.vtype)
 

if __name__ == "__main__":
    Car = VEHICLE("blue", 5, 4, "car")
    print(Car.BREAK())
    print(Car.DRIVE())
 
    truck = VEHICLE("red", 3, 6, "truck")
    print(truck.DRIVE())
    print(truck.BREAK())


#! Examples
import functions as fn # ключевое слово fn позволяет сопоставить модуль functions с пространством имен fn
# from include import RND # импорт из модуля include в глобальное пространство имен функцию RND 
#from arrays import * # импорт всех функций из модуля arrays в глобальное пространство имен 
#from files import *



x = 0b101   # "101" в двоичной 5
y = 0x0a    # "0a"  в шест-ой 10
z = x + y   # 15
print("{0} in binary {0:08b}   in hex {0:02x} in octal {0:02o}".format(z)) # format - вывод числа в различных системах исчисления
# например {0:08b}, где 8 указывает, сколько знаков должно быть в записи числа



# типы данных
arr1=[] # array
bool(x) # True / False
int(x)  # целое число 4 байта 
float(x)# представляет число с плавающей точкой 8 байт, например, 1.2 или 34.76
complex(x)# комплексные числа
str(x)  # строки, набор символов в кодировке Unicode
bytes(x)# последовательность чисел в диапазоне 0-255
list(arr1) # список
tuple(arr1)# кортеж
set(arr1)  # неупорядоченная коллекция уникальных объектов
#dict(s) # словарь, где каждый элемент имеет ключ и значение
dir(x)# вводить в окне интерпретации выводит список всех методов объекта

x1 = 3.9e3;         print(x1)  # 3900.0
x2 = 3.9e-3;        print(x2)  # 0.0039
x3 = round(x2,3);   print(x3)  # 0.03
x = "smith";        print(type(x))  # <class 'str'>     узнать текущий тип переменной
"""
спецификаторы:
%3d   - выравнивание по правому краю в поле шириной 3 символа
%XXs
%0.2f - выводится два знака после запятой 
"""
print("целочисленный результат деления 7/2=",7 // 2)   # 3 - целочисленный результат деления, отбрасывая дробную часть
print("6 в квадрате ",6 ** 2)   # 36 - число 6 в степень 2
print("остаток от деления 7/2=",7 % 2)    # 1 - Получение остатка от деления числа 7 на 2

age = 22
isMarried = False
weight = 58
result = (weight==58 or isMarried) and not age>21  # False
print(result)

usd = 57
euro = 60 
try:
    money = int(input("Введите сумму, которую вы хотите обменять: "))
    if money < 0:   # вручную сгенерированное исключение. Для этого применяется оператор raise
        raise Exception("Сумма должна быть больше 0")
except ValueError: # исключение в результате преобразования строки в число
    print("Введена некорректная сумма")
except ZeroDivisionError:# деление на 0
    print("Попытка деления числа на ноль")
except Exception  as excpt:# общее исключение, под которое попадают все исключительные ситуации
    print("Общее исключение: ",excpt)
finally:# необязательный блок finally применяется для освобождения используемых ресурсов, например, для закрытия файлов
    print("ОК")
currency = input("Укажите код валюты (доллары - u, евро - e): ") 
if currency.lower() == "u": # .lower - преобразование в нижний регистр
    pass # Не выполняет никаких действий
    cache, part = fn.RND(money,usd)
    print("Валюта: доллары США")
elif currency == "e" or currency=="E":
    cache, part = fn.RND(cur=euro, mon=money)  # можно менять местами входные переменные с указанием их значений
    print("Валюта: евро")
else:
    cache=0; part=0
    print("Неизвестная валюта")
print("К получению:", cache, " остаток:",part)

#! пока переменная choice содержит латинскую букву "Y" или "y".
while True:
    choice = input("Для продолжения нажмите \"R\" или \"r\" ")
    if choice.lower() == "r":
        print("Привет"); continue
    else:
        break
    
print("Работа программы завешена")







