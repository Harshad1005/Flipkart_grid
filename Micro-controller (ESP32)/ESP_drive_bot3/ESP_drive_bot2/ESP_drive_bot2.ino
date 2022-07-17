#include <ros.h>
#include <turtlesim/Pose.h>
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
turtlesim::Pose pub_msg;
ros::Publisher pub("/bot/pose", &pub_msg);
MPU6050 mpu(Wire);

Servo flipper;
int freq=1000;
int resolution=4;

int m1=19;                                                    //Defining pins
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
  ros::Subscriber <geometry_msgs::Twist> sub("/bot2/drive",&msgcb);     //Subscriber

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password); 
  
  while (WiFi.status() != WL_CONNECTED) { }
  // Ros setup initialize
    nh.initNode();
    nh.advertise(pub);
    nh.subscribe(sub);
    nh.getHardware()->setConnection(server, port);

  Wire.begin();
  byte status = mpu.begin();
  while(status!=0){ 
    Serial.println("Not connected to mpu");
    delay(500);
    } 
  Serial.println("connected to mpu");
    delay(500);
  mpu.calcOffsets(); // gyro and accelero

  ledcSetup(5,freq,resolution);
  ledcSetup(2,freq,resolution);
  ledcSetup(3,freq,resolution);
  ledcSetup(4,freq,resolution);
  ledcAttachPin(m1,5);
  ledcAttachPin(m2,2);
  ledcAttachPin(m3,3);
  ledcAttachPin(m4,4);

  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
  Serial.println("All setup");
  
//Setup for servo flipper
  flipper.setPeriodHertz(20);    
  flipper.attach(servo_pin,600, 2000);
  flipper.write(5);
}

void loop() {
  mpu.update();
  nh.spinOnce();
  if((millis()-timer)>10){ // print data every 10ms

  pub_msg.theta=mpu.getAngleZ();
  Serial.println(mpu.getAngleZ());
//  Serial.println("value published");
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
//    pub.publish(&pub_msg); 
    }
    
   else{
    ledcWrite(2 ,abs(left));
    ledcWrite(5,0);
//    pub.publish(&pub_msg); 
    }


  if (right>0){
    ledcWrite(3 ,abs(right));
    ledcWrite(4,0);
//    pub.publish(&pub_msg); 
    }

   else{
    ledcWrite(4 ,abs(right));
    ledcWrite(3,0);
//    pub.publish(&pub_msg); 
    }

    if (flip==1){
      flipper.write(100);
      flip =0;
      delay(500);
      flipper.write(5);
//      pub.publish(&pub_msg); 
      }

  }
