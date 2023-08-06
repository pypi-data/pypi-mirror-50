// Данный пример поочерёдно включает и выключает каналы модуля.     // * Строки со звёздочкой являются необязательными.
                                                                    //
#include "iarduino_I2C_Relay.h"                                     //   Подключаем библиотеку для работы с реле и силовыми ключами.
iarduino_I2C_Relay relay(0x09);                                     //   Объявляем объект relay для работы с функциями и методами библиотеки iarduino_I2C_Relay, указывая адрес модуля на шине I2C.
                                                                    //   Если объявить объект без указания адреса (iarduino_I2C_Relay relay;), то адрес будет найден автоматически.
																	//
void loop(){                                                        //
	while(1){
//Включаем и выключаем каналы модуля:                             	//
    relay.digitalWrite(1,HIGH); relay.digitalWrite(4,LOW);          //   Включаем 1 канал и выключаем 4.
    delay(500);                                                     //   Ждём   500 мс.
    relay.digitalWrite(2,HIGH); relay.digitalWrite(1,LOW);          //   Включаем 2 канал и выключаем 1.
    delay(500);                                                     //   Ждём   500 мс.
    relay.digitalWrite(3,HIGH); relay.digitalWrite(2,LOW);          //   Включаем 3 канал и выключаем 2.
    delay(500);                                                     //   Ждём   500 мс.
    relay.digitalWrite(4,HIGH); relay.digitalWrite(3,LOW);          //   Включаем 4 канал и выключаем 3.
    delay(500);                                                     //   Ждём   500 мс.
	}
}
int main(){                                                       	//
//Готовим модуль к работе:                                        	//
  relay.begin();                                                  	//   Инициируем работу с модулем.
  relay.digitalWrite(ALL_CHANNEL,LOW);                            	// * Выключаем все каналы модуля.
	loop();
}                                                                   //
                                                                    //
