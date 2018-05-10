from Tkinter import *
from tkFileDialog import askopenfilename
import tkFont
from enum import Enum
import sys
import RPi.GPIO as io
io.setmode(io.BCM)
import sys, tty, termios, time
import threading
import thread
pages=[]
frameName=""
currentSpeed=0.1
duration=0
info=""
enableForward=False
enableReverse=False
motorEnable=False
currentDirection=""
isBusy=False
#motor control
motor_enable_pin = 4
motor_direction_pin = 17
motor_step_pin = 27
io.setup(motor_enable_pin, io.OUT)
io.setup(motor_direction_pin, io.OUT)
io.setup(motor_step_pin, io.OUT)

class motorControl():
    def __init__(self, *args, **kwargs):
        print "MotorControl"
        
    def stepper_enable(self):
        global motorEnable
        io.output(motor_enable_pin, True)
        motorEnable=True

    def stepper_disable(self):
        global motorEnable
        io.output(motor_enable_pin, False)
        motorEnable=False

    def step_once(self):
        if motorEnable:
            io.output(motor_step_pin, True)
            time.sleep(float(currentSpeed))
            io.output(motor_step_pin, False)
            time.sleep(float(currentSpeed))
        else:
            info="motor is not enabled"
    def step_forward(self):
            global info
            io.output(motor_direction_pin, True)
            self.step_once()

    def step_reverse(self):
            io.output(motor_direction_pin, False)
            self.step_once()      
    def step_automated(self,a,b):
        global duration,info,enableForward,enableReverse,motorEnable,currentSpeed
        stepCountx2= float(duration)/float(currentSpeed)
        stepCount=int(stepCountx2/2)
        
        for i in range(stepCount):
            if enableForward:
                self.step_forward()
            elif enableReverse:
                self.step_reverse()
            else:
                info="direction is not given"





class Page(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
		
class PageGui(Page):
    def __init__(self, *args, **kwargs):
        global frameName,currentSpeed,duration,currentDirection,motorEnable
        Page.__init__(self, *args, **kwargs)
        
        #HEAD
        self.labelHead = Label(self,background='#ffffff',text="Wire Coating Machine")
        self.labelHead.config(font=("Courier", 44))
	self.labelHead.place(x=appResolution[0]/2,y=100,anchor="center")       

        #GENERAL SETTINGS
	self.generalHeight=appResolution[1]*2/10
	
        self.labelGeneral = Label(self,background='#ffffff',text="General Settings")
        self.labelGeneral.config(font=("Courier", 20))
	self.labelGeneral.place(x=0 ,y=self.generalHeight,anchor="sw")       

	
        self.buttonStart = Button(self,background='#ffffff',text="Start")
        self.buttonStart.config(font=("Courier", 20))
	self.buttonStart.place(x=300 ,y=self.generalHeight,anchor="sw")
	self.buttonStart.bind("<Button 1>",self.motorStart)

        self.buttonStop = Button(self,background='#ffffff',text="Stop")
        self.buttonStop.config(font=("Courier", 20))
	self.buttonStop.place(x=500 ,y=self.generalHeight,anchor="sw")
	self.buttonStop.bind("<Button 1>",self.motorStop)

	self.showMotor = Label(self,background='#ffffff',text= "Current Speed " + str(currentSpeed))
        self.showMotor.config(font=("Courier", 20))
	self.showMotor.place(x=700 ,y=self.generalHeight,anchor="sw")       

	
        self.motorStatus = Button(self,background='#ffffff',text="Motor Status " + str(motorEnable))
        self.motorStatus.config(font=("Courier", 20))
	self.motorStatus.place(x=300 ,y=self.generalHeight+ 120,anchor="sw")
        self.motorStatus.bind("<Button 1>",self.setMotorStatus)
	

	self.showSpeed = Label(self,background='#ffffff',text= "Current Speed " + str(currentSpeed))
        self.showSpeed.config(font=("Courier", 20))
	self.showSpeed.place(x=700 ,y=self.generalHeight,anchor="sw")


	self.showDirection = Label(self,background='#ffffff',text= "Direction " + str(currentDirection))
        self.showDirection.config(font=("Courier", 20))
	self.showDirection.place(x=700 ,y=self.generalHeight + 120 ,anchor="sw")

        self.buttonSetDirectionForward = Button(self,background='#ffffff',text="Forward")
        self.buttonSetDirectionForward.config(font=("Courier", 20))
	self.buttonSetDirectionForward.place(x=1300 ,y=self.generalHeight + 120,anchor="sw")
        self.buttonSetDirectionForward.bind("<Button 1>",self.setDirectionForward)

        self.buttonSetDirectionReverse = Button(self,background='#ffffff',text="Reverse")
        self.buttonSetDirectionReverse.config(font=("Courier", 20))
	self.buttonSetDirectionReverse.place(x=1500 ,y=self.generalHeight + 120,anchor="sw")
        self.buttonSetDirectionReverse.bind("<Button 1>",self.setDirectionReverse)
        
        self.buttonEntry = Entry(self,background='#ffffff',textvariable=currentSpeed)
        self.buttonEntry.config(font=("Courier", 20))
	self.buttonEntry.place(x=1300 ,y=self.generalHeight,anchor="sw")
	
        self.buttonSet = Button(self,background='#ffffff',text="Set")
        self.buttonSet.config(font=("Courier", 20))
	self.buttonSet.place(x=1700 ,y=self.generalHeight,anchor="sw")
        self.buttonSet.bind("<Button 1>",self.setSpeed)

        #Manuel Settings
        self.manuelHeight=appResolution[1]*4/10
        
        self.labelManuel = Label(self,background='#ffffff',text="Manuel Settings")
        self.labelManuel.config(font=("Courier", 20))
	self.labelManuel.place(x=0 ,y=self.manuelHeight,anchor="sw")       

	
        self.buttonManuelStart = Button(self,background='#ffffff',text="Ileri")
        self.buttonManuelStart.config(font=("Courier", 20))
	self.buttonManuelStart.place(x=300 ,y=self.manuelHeight,anchor="sw")
	self.buttonManuelStart.bind("<Button 1>",self.manuelForward)

        self.buttonManuelStop = Button(self,background='#ffffff',text="Geri")
        self.buttonManuelStop.config(font=("Courier", 20))
	self.buttonManuelStop.place(x=500 ,y=self.manuelHeight,anchor="sw")
	self.buttonManuelStop.bind("<Button 1>",self.manuelReverse)

        #Automated Settings
        self.automatedHeight=appResolution[1]*6/10
        
        self.labelAutomated = Label(self,background='#ffffff',text="Automated Settings")
        self.labelAutomated.config(font=("Courier", 20))
	self.labelAutomated.place(x=0 ,y=self.automatedHeight,anchor="sw")       

	self.showDuration = Label(self,background='#ffffff',text= "Current Duration " + str(duration))
        self.showDuration.config(font=("Courier", 20))
	self.showDuration.place(x=700 ,y=self.automatedHeight,anchor="sw")
	
        self.entryDuration = Entry(self,background='#ffffff',textvariable=duration)
        self.entryDuration.config(font=("Courier", 20))
	self.entryDuration.place(x=1300 ,y=self.automatedHeight,anchor="sw")
	
        self.durationSet = Button(self,background='#ffffff',text="Set")
        self.durationSet.config(font=("Courier", 20))
	self.durationSet.place(x=1700 ,y=self.automatedHeight,anchor="sw")
        self.durationSet.bind("<Button 1>",self.setDuration)	

	
        #infotext
        self.info=""
	self.showInfo = Label(self,background='#ffffff',text= self.info)
        self.showInfo.config(font=("Courier", 20))
	self.showInfo.place(x=1400 ,y= appResolution[1]*9/10,anchor="sw")        
        
    def setSpeed(self,event):
        global currentSpeed,info
        self.currentSpeed = self.buttonEntry.get()
        if self.currentSpeed>0.5 or self.currentSpeed < 0.025:
            info="Error!!!Please Choose between 0.025-0.5"
        else:
            currentSpeed=self.currentSpeed
        print currentSpeed

    def setDuration(self,event):
        global duration
        self.duration = self.entryDuration.get()
        duration=self.duration
        print duration
    def setDirectionForward(self,event):
        global enableForward,enableReverse,info
        enableForward=True
        enableReverse=False
        info="direction is forward"
    def setDirectionReverse(self,event):
        global enableForward,enableReverse,info
        enableForward=False
        enableReverse=True
        info="direction is reverse"
    def setMotorStatus(self,event):
        global motorEnable,info
        if motorEnable:
            motorEnable=False
        else:
            motorEnable=True
    def motorStart(self,event):
        print "motorStart"
        motor=motorControl()
        thread.start_new_thread (motor.step_automated,(1,1))
    def motorStop(self,event):
        global motorEnable
        motorEnable=False
    def manuelForward(self,event):
        motor=motorControl()
        motor.step_forward()
    def manuelReverse(self,event):
        motor=motorControl()
        motor.step_reverse()   
		
		
class Pages(Enum):
    Gui=0


class Application():
    def __init__(self):
        global appResolution
        self.root = Tk()
        self.root.geometry("1000x500")
        self.root.attributes('-fullscreen', True)
        appResolution=(self.root.winfo_screenwidth(),self.root.winfo_screenheight())
        print appResolution[0]
        print appResolution[1]
        pages.append(PageGui(self.root, background='#ffffff'))
		
	self.container = Frame(self.root)
	self.container.pack(side="top", fill="both", expand=True)
		
        for p in pages:
            p.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        pages[0].show()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(20, self.update)
    def update(self):
        global currentSpeed,duration,info,motorEnable
        pages[0].showSpeed.configure(text="Current Speed "+str(currentSpeed))
        pages[0].showDuration.configure(text="Current Duration "+str(duration))

        if enableForward:
            self.direction="Forward"
        elif enableReverse:
            self.direction="Reverse"
        else:
            self.direction="Null"
        pages[0].showDirection.configure(text="Direction "+str(self.direction))
        pages[0].motorStatus.configure(text="Motor Status " + str(motorEnable))
        pages[0].showInfo.configure(text=info)
    
        self.root.after(20, self.update)
    
    def on_closing(self):
        global unexpectedExit
        unexpectedExit = True
        self.root.destroy()
		
		
if __name__ == "__main__":
    try:
        global application
        application = Application()
        application.root.mainloop()
    except (KeyboardInterrupt, SystemExit):
        print "Thread has been stopped by your keyboard"
        unexpectedExit = True
        sys.exit()
