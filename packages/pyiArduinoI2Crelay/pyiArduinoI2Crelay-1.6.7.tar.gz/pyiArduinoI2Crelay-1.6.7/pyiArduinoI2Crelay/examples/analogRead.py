#encoding=utf-8
# Данный пример считывает текущее состояние ШИМ на каналах модуля.
from pyiArduinoI2Crelay import *   # Подключаем модуль для работы с ключём
from time import sleep
pwrkey = pyiArduinoI2Crelay(9)     # Объявляем объект pwrkey
                                   #
#  Устанавливаем ШИМ на каналах модуля:
                                   #
pwrkey.analogWrite(1, 0x0000)      # Устанавливаем 0% ШИМ на 1 канале
pwrkey.analogWrite(2, 0x0555)      # Устанавливаем 33.3% ШИМ на 2 канале
pwrkey.analogWrite(3, 0x0AAA)      # Устанавливаем 66.6% ШИМ на 3 канале
pwrkey.analogWrite(4, 0x0FFF)      # Устанавливаем 100% ШИМ на 4 канале
                                   #
#  Проверяем состояние каналов модуля в цикле: 
#while True:                                   #
for i in range(1, 5):              # Проходим по всем каналам модуля.
    print("ШИМ на канале ", (i),   # Выводим номер очередного канала.
          " имеет значение ",      # Выводим значение которое вернула
          (pwrkey.analogRead(i)))  # функция analogRead().
#        sleep(.05)
#           (pwrkey.getStateWDT()))
#print(pwrkey.analogRead(3))  # функция analogRead().
#sleep(.001)
