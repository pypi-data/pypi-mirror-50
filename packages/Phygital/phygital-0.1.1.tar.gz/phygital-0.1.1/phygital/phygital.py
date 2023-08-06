# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 11:06:33 2019

@author: Innotechway
"""


from threading import Timer
import serial
import requests


    
#variable for SMS function
global response
global Auth_Key1


name = "phygital"
#def serialInit(PortName):
   

SendData = list("@00000000000000000000000000^")
global receivedData                  
global data1
global data
global ser
receivedData = ['&', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0','0','0','0','0','0','0','0','0','0', '~']

global timer




class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            
i=0            
def Show():
    global SendData1
    global i
    global receivedData
    global data
    global data1
    str1 = ''.join(SendData)
    ser.write((str1).encode())
    data=str(ser.readline()) #Received Data in String
    data1=data
               
    if('&' in data):
        receivedData=list(data) #Converted Data to List(Array)
        #print(receivedData)
        if(debug1=='p'):
            print(data)
    return receivedData

class phygital:
    def init(PortName,debug='a'): 
        global debug1
        global ser
        global timer
        ser = serial.Serial()
        ser.baudrate=115200
        ser.port=PortName
        ser.open()     
        timer=RepeatTimer(0.01,Show)
        timer.start()
        debug1=debug
        return debug1
    
    def SendSMS(Channel,Number,Message):
        
        global response
        global Auth_Key1
        
        if Channel == 1:
            Auth_Key1 = "86AmSeoipQBCKcPz2l5ZU1j3XJRsabgMhYLdvDywNuqT9fGr7kJPYjaOrS50UomfLQGtd4IMgHp69R81"
        
        url = "https://www.fast2sms.com/dev/bulk"
        
        payload = "sender_id=FSTSMS&message="+":: SkillsCafe IoT :: "+ Message +"&language=english&route=p&numbers="+str(Number)
        
        headers = {
        
        'authorization': Auth_Key1,
        
        'Content-Type': "application/x-www-form-urlencoded",
        
        'Cache-Control': "no-cache"
        
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        
        return response
       
    
    
    def ConvertSpeed(Speed,MotorNum):
        
        Temp1 = list(str(Speed))
        if(Speed >=100):
            if(MotorNum==1):
                SendData[5]=Temp1[0]
                SendData[6]=Temp1[1]
                SendData[7]=Temp1[2]
                
            if(MotorNum==2):
                SendData[8]=Temp1[0]
                SendData[9]=Temp1[1]
                SendData[10]=Temp1[2]
                
        if(Speed <100) and (Speed >=10) :
            if(MotorNum==1):
                SendData[5]='0'
                SendData[6]=Temp1[0]
                SendData[7]=Temp1[1]
                
            if(MotorNum==2):
                SendData[8]='0'
                SendData[9]=Temp1[0]
                SendData[10]=Temp1[1]
                
        if(Speed <10)  :
            if(MotorNum==1):
                SendData[5]='0'
                SendData[6]='0'
                SendData[7]=Temp1[0]
                
            if(MotorNum==2):
                SendData[8]='0'
                SendData[9]='0'
                SendData[10]=Temp1[0]
       # print(Temp1)
       
    
       
    def ConvertAngle(ServoNum,Angle):
        
        Temp1 = list(str(Angle))
        if(Angle >=100):
            if(ServoNum==1):
                SendData[14]=Temp1[0]
                SendData[15]=Temp1[1]
                SendData[16]=Temp1[2]
                
            if(ServoNum==2):
                SendData[17]=Temp1[0]
                SendData[18]=Temp1[1]
                SendData[19]=Temp1[2]
                
            if(ServoNum==3):
                SendData[20]=Temp1[0]
                SendData[21]=Temp1[1]
                SendData[22]=Temp1[2]
                
        if(Angle <100) and (Angle >=10) :
            if(ServoNum==1):
                SendData[14]='0'
                SendData[15]=Temp1[0]
                SendData[16]=Temp1[1]
                
            if(ServoNum==2):
                SendData[17]='0'
                SendData[18]=Temp1[0]
                SendData[19]=Temp1[1]
                
            if(ServoNum==3):
                SendData[20]='0'
                SendData[21]=Temp1[0]
                SendData[22]=Temp1[1]
                
        if(Angle <10)  :
            if(ServoNum==1):
                SendData[14]='0'
                SendData[15]='0'
                SendData[16]=Temp1[0]
                
            if(ServoNum==2):
                SendData[17]='0'
                SendData[18]='0'
                SendData[19]=Temp1[0]    
            
            if(ServoNum==3):
                SendData[20]='0'
                SendData[21]='0'
                SendData[22]=Temp1[0]
    
    def MotorControl(motorNum,direction,Speed):
            if(motorNum == 1 ):
                #print(str(Speed))
                if(direction=="cw") or (direction=="CW") :
                   SendData[1]='0'
                   SendData[2]='1' 
                if(direction=="ccw") or (direction=="CCW"):
                   
                    SendData[1]='1'
                    SendData[2]='0' 
                    
                if(direction=="stp") or (direction=="STP")or (direction=="STOP"):
                    
                    SendData[1]='0'
                    SendData[2]='0' 
                    
                phygital.ConvertSpeed(Speed,1)   
                
                
            if(motorNum == 2 ):
                
                if(direction=="cw") or (direction=="CW") :
                    
                     SendData[3]='0'
                     SendData[4]='1' 
                    
                if(direction=="ccw") or (direction=="CCW"):
                   
                    SendData[3]='1'
                    SendData[4]='0'
                
                if(direction=="stp") or (direction=="STP")or (direction=="STOP"):
                  
                    SendData[3]='0'
                    SendData[4]='0'
                    
                phygital.ConvertSpeed(Speed,2)
                
    def MoveServo(ServoNum,Angle):
        
        if(Angle>180):
            Angle=180
        if(Angle<0):
            Angle=0
        
        phygital.ConvertAngle(ServoNum,Angle) 
    
    def dWrite(PinNum,Val): 
        if(PinNum==1):
            if(Val==1):
                SendData[23]='1'
            else:
                SendData[23]='0'
                
        if(PinNum==2):
            if(Val==1):
                SendData[24]='1'
            else:
                SendData[24]='0'    
        
        if(PinNum==3):
            if(Val==1):
                SendData[25]='1'
            else:
                SendData[25]='0'    
                
        if(PinNum==4):
            if(Val==1):
                SendData[26]='1'
            else:
                SendData[26]='0'            
            
            
            
    def RGB(Red,Green,Blue):
       Temp1 = list(str(Red))
       Temp2 = list(str(Green))
       Temp3 = list(str(Blue))
       if(Red >=100):
           
                SendData[5]=Temp1[0]
                SendData[6]=Temp1[1]
                SendData[7]=Temp1[2]
       if(Green >=100):      
            
                SendData[8]=Temp2[0]
                SendData[9]=Temp2[1]
                SendData[10]=Temp2[2]
       if(Blue >=100):      
            
                SendData[11]=Temp3[0]
                SendData[12]=Temp3[1]
                SendData[13]=Temp3[2]
                
       if(Red <100) and (Red >=10) :
                SendData[5]='0'
                SendData[6]=Temp1[0]
                SendData[7]=Temp1[1]
                
       if(Green <100) and (Green >=10) :
                SendData[8]='0'
                SendData[9]=Temp2[0]
                SendData[10]=Temp2[1]
                
       if(Blue <100) and (Blue >=10) :
                SendData[11]='0'
                SendData[12]=Temp3[0]
                SendData[13]=Temp3[1]  
                
       if(Red <10)  :
                SendData[5]='0'
                SendData[6]='0'
                SendData[7]=Temp1[0]
                
       if(Green <10)  :
                SendData[8]='0'
                SendData[9]='0'
                SendData[10]=Temp2[0] 
    
       if(Blue <10)  :
                SendData[11]='0'
                SendData[12]='0'
                SendData[13]=Temp3[0] 
    
    
    def aRead(PinNum):
        AData=''.join(receivedData)
        if(PinNum==1):
            A1Val=int(AData[7:11])
            return A1Val
        if(PinNum==2):
            A2Val=int(AData[11:15])
            return A2Val
        if(PinNum==3):
            A3Val=int(AData[15:19])
            return A3Val
        if(PinNum==4):
            A4Val=int(AData[19:23])
            return A4Val
    
    
    def dRead(PinNum):
       
         if(receivedData[PinNum+2]=='1'):
                
                return 1
         else:
                return 0
                #print(data)
    def close():
        global ser
        global timer
        ser.close()          
        timer.cancel()    