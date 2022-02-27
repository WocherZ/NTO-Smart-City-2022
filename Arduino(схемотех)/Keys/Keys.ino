#include <DHT.h>                                              // подключаем библиотеку для датчика температуры
#include "HX711.h"                                            //подключении библиотеки для тензодатчика
#include <TroykaOLED.h>                                       // библиотека для работы с OLED-дисплеем
#include <Servo.h>                                            //библиотека для работы с сервоприводом
#include <Wire.h>
#include <SPI.h>                                               // библиотека для работы с RFID/NFC
#include <Adafruit_PN532.h>
#include <TroykaCurrent.h>
#define dvish 1
#define DT  A1                                               // Указываем номер вывода, к которому подключен вывод DT  датчика
#define SCK A0                                               // Указываем номер вывода, к которому подключен вывод SCK датчика
#define PN532_IRQ   9                                             //пин для RFIT
  HX711 scale;                                                // создаём объект scale
  float calibration_factor = -74.7;                           // этот калибровочный коэффициент настраивается в соответствии с тензодатчиком
  float units;                                                // задаём переменную для измерений в граммах
  float ounces;                                               // задаём переменную для измерений в унциях
  TroykaOLED myOLED(0x3C);                                    // создаём объект для работы с дисплеем и передаём I²C адрес дисплея
  DHT dht(2, DHT11);                                          // сообщаем на каком порту будет датчик температуры
  Adafruit_PN532 nfc(PN532_IRQ, 100);            // создаём объект для работы со сканером и передаём ему два параметра первый — номер пина прерывания вторым — число 100
  Servo servol;                                    // объявляем переменную servo типа "servo1"
int servo=0;                                 //серво привод. 0 - закрыта, 1 - открыта 
ACS712 sensorCurrent(A3);                    //выход для датчика тока
 // Массивы в которые необходимо записать ID карт:
uint8_t uidFirstCard[] = {0x67, 0xE6, 0xC7, 0x49};     //ключ
uint8_t uidSecondCard[] = {0xE9, 0x0E, 0x8A, 0x99};    //карта

  //функция для вывода с датчиков в порт
void basic_data(int x,int y,float k){                        //svet,vla,t                                  
     Serial.print("Light: ");                               //датчик света
     Serial.print(x);
    Serial.print("   Humidity: ");          
    Serial.print(y);                                                     
    Serial.print("   Temperature: ");                         //датчик температуры
    Serial.print(k);
}



//функция вывода значений с датчика на дисплей                 
/*void display_data(int x,int y,float z,int k){
myOLED.begin();                   
  myOLED.setFont(font6x8);
  myOLED.print("Temperature:", 0, 10);
  myOLED.print(z, 80, 10);
   myOLED.print("C", 120, 10);
    myOLED.print("Humidity:", 0, 20);
   myOLED.print(y, 80, 20);
   myOLED.print("%", 120, 20);
   myOLED.print("Light:", 0, 30);
   myOLED.print("U", 120, 30);
   myOLED.print(x, 80, 30);
   myOLED.print("Consumption:", 0, 40);
   myOLED.print(k, 80, 40);
}*/


  //функция датчика присутствия
void motion_sensor(){
   int motion;
   motion= digitalRead(dvish);
  Serial.print("   Motion: ");
  Serial.print(motion);
}



//функция для измерения веса пациента при помощи тензодатчика
void load_cell(){
  for (int i = 0; i < 10; i ++) {                             // усредняем показания, считав значения датчика 10 раз
    units = + scale.get_units(), 10;                          // суммируем показания 10 замеров
  }                                                           // суммируем показания 10 замеров
  Serial.print("  Weight: ");
  units = units / 10;                                         // усредняем показания, разделив сумму значений на 10
  ounces = units * 0.035274;                                  // переводим вес из унций в граммы
  Serial.print(ounces);                                       // выводим в монитор последовательного порта вес в граммах
  Serial.print(" grams");                                   // выводим текст в монитор последовательного порта
}



//функция нажатия кнопки и вывода на экран рекомендуемой температуры
/*void rec_temp(float x){
myOLED.begin();
myOLED.setFont(font6x8);
myOLED.print("Recommended:", 30, 10);
myOLED.print("Temperature:", 30, 20);
myOLED.setFont(font12x10);
myOLED.print(x, 50, 40);
myOLED.print("C", 70, 40);
}*/
//функция для работы вентилятора
void cooling(float rec_temp,float temp){
float temper = rec_temp-temp;
int N_nag;
int N_ven;
if ((temper > 0)&&(temper < 10)){
  analogWrite(12,abs(20*temper));
   int N_nag =25.5*temper ;
  int N_ven = 0;
}
  else if((temper<=0)&&(abs(temper)<10)){
    analogWrite(13,abs(20*abs(temper)));
     int N_nag = 0;
  int N_ven = 25.5*temper;
  }
  else if(temper>10){
  analogWrite(12,200);
   int N_nag = 255;
  int N_ven = 0;
  }
  else if(temper<-10){
    analogWrite(13,200);
     int N_nag = 0;
  int N_ven = 255;
  }
  int R_nag = 110;
  int R_ven = 23200;
  float U_nag = N_nag*5/255;
  float U_ven = N_ven*5/255;
  float P_nag = (U_nag*U_nag)/R_nag;
  float P_ven = (U_ven*U_ven)/R_ven;
  Serial.print("   fan power:");
  Serial.print(P_ven,4);
  Serial.print("   heater power:");
  Serial.println(P_nag,4);
}
//функция для проверки карты RFIT
boolean comparisonOfUid(uint8_t uidRead[8], uint8_t uidComp[8], uint8_t uidLen) {
 for (uint8_t i = 0; i < uidLen; i++) {
    if (uidRead[i] != uidComp[i]) {
      return false;
    }
    if (i == (uidLen)-0x01) {
      return true;
    }
  }
}
//функция работы серво и RFIT
void RFIT_servo(){
   uint8_t success;        // буфер для хранения ID карты
    uint8_t uid[8];         // размер буфера карты
    uint8_t uidLength;       // слушаем новые метки
     success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);        // если найдена карта
      if (success) {
    if (comparisonOfUid(uid, uidFirstCard, uidLength)) {
      servol.write(0);    //поворачиваем в исходное положение
      servol.write(90);   //открываем
      delay(100000);
      servol.write(0);    //поворачиваем в исходное положение
       } 
       else{
        Serial.print("penetration");
       }
      }
}
//функция для считывания мощности цепи
void power(){
  Serial.print("Current is ");
  Serial.print(sensorCurrent.readCurrentAC());
  Serial.println(" mA");
}
void setup() {
 Serial.begin(9600);
 scale.begin(DT, SCK);                                       // инициируем работу с датчиком тензо
 scale.set_scale();                                          // выполняем измерение значения без калибровочного коэффициента
  scale.tare();                                               // сбрасываем значения веса на датчике в 0
  scale.set_scale(calibration_factor);                        // устанавливаем калибровочный коэффициент
 dht.begin();                // запускаем датчик DHT11
 pinMode(dvish,INPUT);       //вход для датчика движения
pinMode(A2, INPUT);          //настраиваем на вход датчик освещённости
pinMode(15,INPUT);           //кнопка
pinMode(13,OUTPUT);
pinMode(14,OUTPUT);           //выходы для вентилятора(охлаждения)
pinMode(12, OUTPUT);   //выход для нагревателя
servol.attach(13); // привязываем сервопривод к аналоговому выходу 13
nfc.begin();        //инициализация 
int versiondata = nfc.getFirmwareVersion();
}

void loop() {
  int svet,h;
  float t;
  int face=0;    //значение для включения RFID
    for(int i=0;i<100;i++){
      int buttonState = 1;    //считываем значение на кнопке
      if (buttonState==1){
h = dht.readHumidity();
  svet = analogRead(A2); 
  t = dht.readTemperature();
   cooling(25.01,t);
      basic_data(svet,h,t);
      power();
      load_cell();
      motion_sensor();
//      display_data(svet,vla,t,0);
     if (face==1){
      RFIT_servo();
     }
      }
    else{
  svet = analogRead(A2);
  h = dht.readHumidity(); 
  t = dht.readTemperature();
      cooling(25.01,t);
      basic_data(svet,h,t);
      power();
      load_cell();
      motion_sensor();
     // rec_temp(25.01);
      if(face==1){
        RFIT_servo();
      }
    }
    delay(300000);
    }
  Serial.print("Finish");
  do {} while(1);
}
