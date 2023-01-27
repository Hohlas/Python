#! Программа Обменный пункт
def RND(mon=2, cur=2):  # заданы значения по умолчанию, если оствить () пустые
    total  = round(mon / cur, 2)
    if mon>cur:  part = mon % cur # остаток от деления
    else: part=0
    return total, part  # возвращаются два значения (кортеж)

result=RND() # результат из двух значений запишется в кортеж
total,part=result

def main(): 
    global result # Чтобы изменять глобальные переменные внутри функции применяется инструкция global
    result+=1
    print("hi")

def reverse(data):# генератор
    for index in range(len(data)-1, -1, -1):
        yield data[index]
for char in reverse('golf'):
    print(char)

#Переменная __name__ указывает на имя модуля. Для главного модуля, который непосредственно запускается, эта переменная всегда будет иметь значение __main__ вне зависимости от имени файла. Поэтому, если запускать скрипт ExampleProject.py отдельно, то Python присвоит переменной name_значение "main"__
if __name__=="__main__":
    main()