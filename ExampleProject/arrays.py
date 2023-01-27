import copy

a = "Hello, World"
c = a[:6]   # c = “Hello,”
d = a[8:]   # d = “orld  e”
e = a[3:9]  # e = “lo, Wo”  print("a: ",a," c: ",c," d: ",d," e: ",e)


# списки #######################################################################################################################################
arr1=[]; arr2=list() # способы создания пустых массивов 
arr3=list(arr1) # Конструктор list для создания списка может принимать другой список
arr1=list(range(10, 2, -2)) # [10, 8, 6, 4]
arr1=[5]*6 # [5, 5, 5, 5, 5, 5]
arr2=["Mike", 1, True, 2.16]
List=["Tom", "Bob", "Alice"] 


for user in List:           print(List.index(user),":",user)# 0:Tom 1:Bob 2:Alise ...
for i in range(0, 10, 2):   print(i)

l=len(List)
m=max(List)
List.append("John")  # добавляет элемент "John" в конец списка
List.insert(3, "Smith")# добавляет элемент "Smith" в список по индексу '3'
List.remove("Bob")  # удаляет элемент item. Удаляется только первое вхождение элемента. Если элемент не найден, генерирует исключение ValueError
arr1.clear()                # удаление всех элементов из списка
x=List.index("Alice") # возвращает индекс элемента "Alice". Если элемент не найден, генерирует исключение ValueError
d=List.pop(x)          # удаляет и возвращает элемент по индексу x. Если индекс не передан, то просто удаляет последний элемент.
List.count("Alice")   # возвращает количество вхождений элемента "Alice" в список
List.sort()                 # сортирует элементы по возрастанию
List.reverse()              # расставляет все элементы в списке в обратном порядке
arr2=List[1:4]         # копирование с 1 по 4, можно указать шаг [1:4:2]
arr3=arr1+arr2              # сложение массивов

i = 0
while i < len(List):
    print(List[i])
    i += 1

item = "Kolya"  # элемент для удаления
if item in List: # чтобы не генерировалось исключение в случае отсутствия удаляемого члена 
    List.remove(item)

# вложенные списки #################################################################################
DList = [ ["Tom",29], ["Alice",33], ["Bob",27] ]# print(DList[0][1]) # 29

for user in DList:#Перебор вложенных списков:
    for item in user:
        print(item, end=" | ")
print(); print(); print();
# добавление вложенного списка
user=["Bill"]
user.append(41)
DList.append(user)  # print(DList[-1]) #["Bill", 41]
 
# добавление во вложенный список
DList[-1].append("+79876543210")    # print(DList[-1])    # ["Bill", 41, "+79876543210"]
DList[-1].pop() # удаление последнего элемента из вложенного списка #print(DList[-1])         # ["Bill", 41]
DList.pop(-1)# удаление всего последнего вложенного списка
DList[0] = ["Sam", 18] # изменение первого элемента #print(DList)   # [ ["Sam", 18], ["Alice", 33], ["Bob", 27]]

# кортежи - неизменяемые списки.Так  как  кортежи  доступны только для чтения, для их хранения используется меньше памяти. ########################
List = ("Tom", 23)
List =  "Tom", 23
name,age = List # разложение картежа на переменные
List = tuple(DList) # создание кортежа из списка #print("кортеж List: ",List)

# Множества ######################################################################
List = {"Tom", "Bob", "Alice", "Tom"}; 
List1= set(["Mike", "Bob", "Bill", "Ted"]); # в функцию set() передается список или кортеж элементов
List2=List.copy() # копирование множества
List3=List1.union(List2) # объединение множеств
List3=List1.intersection(List2) # операция пересечения множеств и возвращает новое множество #print(List3)   # {"Bob"} аналогично можно использовать лог. умножение
List3=List1.difference(List2) # разность множеств  (возвращает отличия) аналогично List1-List2
user = "Teddy"
List.add("John")    # Для добавления одиночного элемента вызывается метод add()
List.discard(user)  # удаление методом discard() не будет генерировать исключения при отсутствии элемента
if user in List: 
    List.remove(user)   # при методе remove() если элемента нет в множестве, сгенерируется ошибка
List1.clear()    # удаление всех элементов


# Словари ######################################################################
objects={}; objects=dict() # определение пустых словарей 
DList = [ ["Tom",29], ["Alice",33], ["Bob",27] ] # имеем двумерный (вложенный) список
Dictionary = dict(DList) # создание словаря из двумерного! списка (или кортежа)
elements = {"Au":"Золото", "Fe":"Железо", "H":"Водород", "O":"Кислород"}
ComplexDict = { # комплексные словари могут хранить: списки, кортежи или другие словари
    "Tom": {"phone":"+971478745", "email":"tom12@gmail.com"},
    "Bob": {"phone":"+876390444", "email":"bob@gmail.com", "skype":"bob123"}
    }
# извлечение элемента из словаря с проверкой для избежания ошибки
key="Au"
if key in elements: # проверка наличия элемента в словаре
    element=elements[key]
    print(elements[key]) # золото
else:
    print("key ",key," not found")

element=elements.get(key) # возвращает элемент с ключом key. Если его нет, то возвращает None
element=elements.get(key,"not found!") # возвращает элемент с ключом key. Если его нет, то возвращает default
elements2=elements.copy() #  копирует содержимое словаря, возвращая новый словарь
elements2.update(elements) # в словарь elements2 добавляются элементы из elements
for key in elements:                print(key, " - ", elements[key])   # перебор словаря
for key, value in elements.items(): print(key, " - ", value)# Метод items() возвращает набор кортежей
for key in elements.keys():         print(key)  # перебор ключей аналогично
for value in elements.values():     print(value)   #перебор только значений
    

del element # если подобного ключа нет, будет выброшено исключение KeyError. Поэтому предварительно надо проверять наличие элемента с данным ключом
element=elements.pop(key) # удаляет элемент с ключом key. Если его нет, то генерируется исключение KeyError
element=elements.pop(key,"not found!") # удаляет элемент с ключом key. Если его нет, то возвращает default
elements.clear() # удаляет все элементы



# поверхностное копирование: users1 и users2 указывают на один и тот же список
users1 = ["Tom", "Bob", "Alice"]
users2 = users1
users2.append("Sam")
print(users1)   # ["Tom", "Bob", "Alice", "Sam"]
print(users2)   # ["Tom", "Bob", "Alice", "Sam"]

# глубокое копирование: users1 и users2 указывают на разные списки
users1 = ["Tom", "Bob", "Alice"]
users2 = copy.deepcopy(users1)
users2.append("Sam")
print(users1)   # ["Tom", "Bob", "Alice"]
print(users2)   # ["Tom", "Bob", "Alice", "Sam"]

