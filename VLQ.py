
# Подготовка для теста. Если нет бинарного файла, то можно для теста создать его вручную
# Cначала вводится количество элементов списка, а потом и сами элементы списка

a=input ( "Нужно создавать двоичный файл? (y/n)" )
if a=='y':
    # Создаём бинарный файл и вводим в него двоичные данные
    try :
        file_handler = open("string.bin", "wb")
    except FileNotFoundError:
           print ( "Невозможно открыть файл" )

    # Объявляем список с числовыми данными
    numbers=[]

    try:
        k=int(input("Сколько чисел будем вводить? "))
    except ValueError:
        print('Введите десятичное число')

    for i in range (k):
        try :
            n=int(input ())
        except ValueError:
            print('Введите десятичное число')
        numbers.append(n)

# Конвертируем список в массив
    barray=bytearray(numbers)

# Записываем массив в файл
    file_handler.write(barray)
    file_handler.close()
#----------------------------------------------------------------------
#Открываем и читаем бинарный файл целиком в список как бинарный
try:
    with open("string.bin", "rb") as binary_file:
        data = list(map(bin, binary_file.read()))

except FileNotFoundError:
           print ( "Невозможно открыть файл" )

print('Подключен файл с данными   ',data)


#----------------------------------------------------------------------
#Конвертер десятичного числа в VLQ
#       Что такое VLQ?
#       https://wiki5.ru/wiki/Variable-length_quantity
#
#предполагается, что из-за трудоемкости побитового введения числа в формате base128
#число вводится в десятичном формате, и затем конвертируется в формат VLQ
#----------------------------------------------------------------------

#вводим десятичное число, преобразовываем в строку, а затем в список с бинарными данными
try:
    num=int(input ('Введите десятичное число для преобразования в VLQ  '))
except ValueError:
    pass
string = format(num, 'b')
binary_list = [0 if c == '0' else 1 for c in string]
#----------------------------------------------------------------------
# реверсируем список, смотрим, сколько нужно дополнить нулями с начала и дополняем
binary_list.reverse()

l=len(binary_list)
k=7-l%7 #количество нулей

if l%7>0:#количество нулей не кратно 7
    for i in range (0,k ):
        binary_list.append(0)
# в список вставляем ноль в знаковый бит младшего байта
binary_list.insert(7,0)

# в список добавляем единицу в знаковый бит старшего байта, если он есть
l=len(binary_list)
k=l//7
if k>1:
    binary_list.append(1)
#----------------------------------------------------------------------
#смотрим, сколько раз нужно вставить знаковые единичные биты со второго по старший байт минус 1
# потом крутим лист обратно
j=15
for i in range (0,k-2 ):
       binary_list.insert(j,1)
       j+=8
binary_list.reverse()
print ('Величина переменной длины (VLQ )  ',binary_list,    'создана')
#----------------------------------------------------------------------
#Ввод позиции числа
try :
    pos=int ( input ( "На какой позиции будет наше VLQ?  " ) )
except ValueError :
    pass
#----------------------------------------------------------------------
#Выгружаем файл, надеемся, что мы сможем его обработать, иначе придется обрабатывать его кусками

try:
    with open("string.bin", "rb") as binary_file:
        list =list(map(bin, binary_file.read()))#получили список чисел в бинарном виде

except FileNotFoundError:
    print("Невозможно открыть файл")

string_join=''.join(list)#объединили в строку
string_join = string_join.replace('0b','')#выкинули 0b
file_list = [0 if c == '0' else 1 for c in string_join]#собрали из строки битовый список

#----------------------------------------------------------------------
#Анализ файла, преобразованного в массив
#
index=0
count_bytes=0
while count_bytes<pos and i<=len(file_list):
    if index >= len ( file_list )-9:
        print ( "Позиция {pos} не найдена.".format ( pos=pos) )
        break
    if file_list[index]==1:
            index+=8

    else:
        count_bytes+=1
        #print ( 'значение',file_list [i] )
        #print ( 'нулевое по индексу', i )
        index+=8

        print("Найдена позиция {pos}, по индексу {index}.".format(pos=pos, index=index))
#----------------------------------------------------------------------
#Запись VLQ по найденной позиции в массив с выгруженными из файла данными
j=index
for i in range (0,len(binary_list)-1 ):
    file_list.insert(j,binary_list[i])
    j+=1


#Запись массива с выгруженными в файл данных
#Переводим в str

string_join="".join(map(str, file_list))
print ( string_join )


try:
     file=open("string.bin", "wb")
     bin_result = ''.join(format(ord(x), '08b') for x in string_join)
     print ( bin_result )
#    bin_result1=bytes(bin_result)
#    print ( bin_result1 )
     file.write(bin_result)

except FileNotFoundError:
          print("Невозможно открыть файл")


