#include <ros.h>
#include <std_msgs/Float64.h>
#include <Wire.h>
#include <MPU6050_light.h>
#include <geometry_msgs/Twist.h>
#include <ESP32Servo.h>

ros::NodeHandle nh;
const char* ssid = "vivo V3Max";
const char* password = "mukesh123";
const int port = 11411;
IPAddress server(192,168,43,250);

unsigned long timer = 0;
std_msgs::Float64 pub_msg;
ros::Publisher pub("/bot/pose", &pub_msg);
MPU6050 mpu(Wire);

Servo flipper;
int freq=1000;
int resolution=4;

int m1=19;
int m2=23;
int m3=4;
int m4=5;
int servo_pin = 13;
int left , right,flip;
void msgcb( const geometry_msgs::Twist& msg){           //Callback function
  left=msg.linear.x;
  right=msg.linear.y;
  flip= msg.linear.z;
  }
  ros::Subscriber <geometry_msgs::Twist> sub("/bot4/drive",&msgcb);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password); 
  
  while (WiFi.status() != WL_CONNECTED) { }
  
    nh.initNode();
    nh.advertise(pub);

  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ 
    Serial.println("Not connected to mpu");
    delay(500);
    } // stop everything if could not connect to MPU6050
  
  delay(1000);
  // mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  Serial.println("connected to mpu");
    delay(500);
//  mpu.calcOffsets(); // gyro and accelero

  nh.subscribe(sub);
    nh.getHardware()->setConnection(server, port);

  ledcSetup(5,freq,resolution);
  ledcSetup(2,freq,resolution);
  ledcSetup(3,freq,resolution);
  ledcSetup(4,freq,resolution);
  ledcAttachPin(m1,5);
  ledcAttachPin(m2,2);
  ledcAttachPin(m3,3);
  ledcAttachPin(m4,4);

//  pinMode(m1,OUTPUT);
//  pinMode(m2,OUTPUT);
//  pinMode(m3,OUTPUT);
//  pinMode(m4,OUTPUT);
//  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  Serial.println("All setup");
}

void loop() {
  mpu.update();
  nh.spinOnce();
  if((millis()-timer)>10){ // print data every 10ms

  pub_msg.data=mpu.getAngleZ();
  Serial.println(mpu.getAngleZ());
  Serial.println("value published");
  timer = millis(); 
  pub.publish(&pub_msg); 
  }
  drive();
  delay(5);
  
}

void drive(){
  if (left>0){
    ledcWrite(5,abs(left));
    ledcWrite(2,0);
//    digitalWrite(m1,HIGH);
//    digitalWrite(m2,LOW);
    }
    
   else{
    ledcWrite(2 ,abs(left));
    ledcWrite(5,0);
//    digitalWrite(m2,HIGH);
//    digitalWrite(m1,LOW);
    }


  if (right>0){
    ledcWrite(3 ,abs(right));
    ledcWrite(4,0);
//    digitalWrite(m3,HIGH);
//    digitalWrite(m4,LOW);
    }

   else{
    ledcWrite(4 ,abs(right));
    ledcWrite(3,0);
//    digitalWrite(m4,HIGH);
//    digitalWrite(m3,LOW);
    }

    if (flip==1){
      flipper.write(100);
      flip =0;
      delay(500);
      flipper.write(5);
      }

  }
