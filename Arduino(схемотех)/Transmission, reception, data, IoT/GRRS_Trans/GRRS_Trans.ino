#include <SoftwareSerial.h>
SoftwareSerial GSMport(7, 8); // RX, TX
int char_;
int SensorPin = 10;
int SensorState;
int SensorLastState = HIGH;

void setup() {
  delay(3000); //дадим время на инициализацию GSM модулю
  pinMode(SensorPin, INPUT);
  digitalWrite(SensorPin, HIGH);  //вкл. подтягивающий резистор 20ом
  Serial.begin(9600);  //скорость порта
  Serial.println("GPRS test");
  GSMport.begin(9600);
  gprs_init();
}

void loop() {
  SensorState = digitalRead(SensorPin);
  if (SensorState != SensorLastState) {  //если смена состояния датчика
    Serial.print("sensor changed to: ");
    Serial.println(SensorState);
    SensorLastState = SensorState;
    gprs_send(String(SensorState));
    delay(100);
  }
  if (GSMport.available()) {  //если GSM модуль что-то послал нам, то
    Serial.println(ReadGSM());  //печатаем в монитор порта пришедшую строку
  }
  delay(100);
}

void gprs_init() {  //Процедура начальной инициализации GSM модуля
  int d = 1000;
  int ATsCount = 7;
  String ATs[] = {  //массив АТ команд
    "AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"",  //Установка настроек подключения
    "AT+SAPBR=3,1,\"APN\",\"internet.mts.ru\"",
    "AT+SAPBR=3,1,\"USER\",\"mts\"",
    "AT+SAPBR=3,1,\"PWD\",\"mts\"",
    "AT+SAPBR=1,1",  //Устанавливаем GPRS соединение
    "AT+HTTPINIT",  //Инициализация http сервиса
    "AT+HTTPPARA=\"CID\",1"  //Установка CID параметра для http сессии
  };
  int ATsDelays[] = {6, 1, 1, 1, 3, 3, 1}; //массив задержек
  Serial.println("GPRG init start");
  for (int i = 0; i < ATsCount; i++) {
    Serial.println(ATs[i]);  //посылаем в монитор порта
    GSMport.println(ATs[i]);  //посылаем в GSM модуль
    delay(d * ATsDelays[i]);
    Serial.println(ReadGSM());  //показываем ответ от GSM модуля
    delay(d);
  }
  Serial.println("GPRG init complete");
}

void gprs_send(String data) {  //Процедура отправки данных на сервер
  //отправка данных на сайт
  int d = 1000;
  Serial.println("Send start");
  Serial.println("setup url");
  //GSMport.println("AT+HTTPPARA=\"URL\",\"http://10.128.30.42/post2_chart.php?api_key=tPmAT5Ab3j7F9&value1=7&value2=8&value3=9");
  GSMport.println("AT+HTTPPARA=\"URL\",\"http://172.20.10.2/post2-data.php?api_key=tPmAT5Ab3j7F9&value1=9&value2=10&value3=11\"");
  //GSMport.println("AT+HTTPPARA=\"URL\",\"http:////127.0.0.1//post2_chart.php?api_key=tPmAT5Ab3j7F9&value1=7&value2=8&value3=9\"");
  //GSMport.println("AT+HTTPPARA=\"URL\",\"http://127.0.0.1/post2_chart.php?api_key=tPmAT5Ab3j7F9&value1=7&value2=8&value3=9\"");
  delay(d * 2);
  Serial.println(ReadGSM());
  delay(d);
  Serial.println("GET url");
  GSMport.println("AT+HTTPACTION=0");
  delay(d * 2);
  Serial.println(ReadGSM());
  delay(d);
  Serial.println("Send done");
}

String ReadGSM() {  //функция чтения данных от GSM модуля
  int c;
  String v;
  while (GSMport.available()) {  //сохраняем входную строку в переменную v
    c = GSMport.read();
    v += char(c);
    delay(10);
  }
  return v;
}
