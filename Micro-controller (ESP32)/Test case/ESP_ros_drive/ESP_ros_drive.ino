#include <ESP32Servo.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include "Wire.h"
#include <MPU6050_light.h>


ros::NodeHandle nh;

Servo flipper;
int freq=1000;
int resolution=2;

int m1=27;
int m2=12;
int m3=22;
int m4=19;
int servo_pin = 13;
int left , right,flip;

void msgcb( const geometry_msgs::Twist& msg){           //Callback function
  left=msg.linear.x;
  right=msg.linear.y;
  flip= msg.linear.z;
  }
  
geometry_msgs::Twist pub_msg;
ros::Subscriber <geometry_msgs::Twist> sub("/bot1/drive",&msgcb);
ros::Publisher pub("/bot/pose", &pub_msg);

const char* ssid = "Airtel_Zerotouch";
const char* passwd = "Airtel@123";
const int port = 11411;
IPAddress server(192,168,1, 6 );

MPU6050 mpu(Wire);
unsigned long timer = 0;



void setup() {

  
  // put your setup code here, to run once:
  WiFi.begin(ssid, passwd); 
  
  while (WiFi.status() != WL_CONNECTED) { }
  
  pinMode(2,OUTPUT);

  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(pub);
  nh.getHardware()->setConnection(server, port);
  
  digitalWrite(2,HIGH);
  ledcSetup(5,freq,resolution);
  ledcSetup(2,freq,resolution);
  ledcSetup(3,freq,resolution);
  ledcSetup(4,freq,resolution);
  ledcAttachPin(m1,5);
  ledcAttachPin(m2,2);
  ledcAttachPin(m3,3);
  ledcAttachPin(m4,4);



  flipper.setPeriodHertz(20);    // standard 50 hz servo
  flipper.attach(servo_pin,500,2000);
  flipper.write(5);
  
  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ } 
  mpu.calcOffsets();

  
}

void loop() {
  // put your main code here, to run repeatedly:
  nh.spinOnce();
  mpu.update();

    if((millis()-timer)>10){ // print data every 10ms
  pub_msg.angular.z =mpu.getAngleZ();
  pub.publish(&pub_msg);
  timer = millis();  
  }
  if (left>0){
    ledcWrite(5,abs(left));
//    digitalWrite(6,HIGH);
    ledcWrite(2,0);
    }
    
   else{
    ledcWrite(2 ,abs(left));
//    digitalWrite(5,HIGH);
    ledcWrite(5,0);
    }


  if (right>0){
    ledcWrite(3 ,abs(right));
//    digitalWrite(11,HIGH);
    ledcWrite(4,0);
    }

   else{
    ledcWrite(4 ,abs(right));
//    digitalWrite(10,HIGH);
    ledcWrite(3,0);
    }

    if (flip==1){
      flipper.write(100);
      flip =0;
      }

  delay(5);
}
