"""
Configures servers

" and ' fix
yeet global variable
Docstrings
"""
import sys, os, time
import serial

import csv

def importIpConfigs(ipsTxt):
    configList =[]
    
    with open("ips.csv", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=",")
    
        for row in csv_reader:
            configList.append(row)
    return configList  

def sleep():
    time.sleep(.2)

def openSerial(comPort):
    return serial.Serial(port=comPort, baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=None, xonxoff=0, rtscts=0)

def closeSerial(serialConnection):
    ser.close()

def writeLine(serialConnection, machine, infoKey):
    serialConnection.write(machine[infoKey].encode())
    writeNewLine(serialConnection)
    sleep()

def writeYes(serialConnection):
    serialConnection.write(b"y\n")
    sleep()

def writeExit(serialConnection):
    serialConnection.write(b"exit\n")
    sleep()

def writeNewLine(serialConnection):
    serialConnection.write(b"\n")

def writeMachine(serialConnection, machine):
    writeYes(serialConnection)
    writeLine(serialConnection, machine, "IP")
    print(repr(yeet[2]["IP"]))
    print(repr(yeet[3]["NETMASK"]))
    print(repr(yeet[3]["GATEWAY"]))
    print(repr(yeet[3]["RACK_NUMBER"]))
    print(repr(yeet[3]["MACHINE_NUMBER"]))
    writeLine(serialConnection, machine, "NETMASK")
    writeLine(serialConnection, machine, "GATEWAY")
    writeNewLine(serialConnection)
    writeNewLine(serialConnection)
    writeLine(serialConnection, machine, 'RACK_NUMBER')
    writeLine(serialConnection, machine, 'MACHINE_NUMBER')
    writeNewLine(serialConnection)

def writeMachine2Table(IpConfigs, table, machineNumber):
    table.item_at(1, 0).set_text(yeet[machineNumber]['MACHINE_NUMBER'])
    table.item_at(1, 1).set_text(yeet[machineNumber]['IP'])
    table.item_at(1, 2).set_text(yeet[machineNumber]['NETMASK'])
    table.item_at(1, 3).set_text(yeet[machineNumber]['GATEWAY'])
    table.item_at(1, 4).set_text(yeet[machineNumber]['RACK_NUMBER'])

IPS_CSV = open('ips.csv')
yeet = importIpConfigs(IPS_CSV)
  
import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        self.currentMachine = 0
        cont = gui.Container(width='75%', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
        ser = serial.Serial()
        self.title = gui.Label('Auto IP Config', width='100%', margin='10px', style={'margin-top':'20px', 'font-size': '20px', 'text-align': 'center'})
        self.table = gui.TableWidget(2, 5, True, True)
        self.table.item_at(0, 0).set_text("Machine #")
        self.table.item_at(0, 1).set_text("IP")
        self.table.item_at(0, 2).set_text("Netmask")
        self.table.item_at(0, 3).set_text("Gateway")
        self.table.item_at(0, 4).set_text("Rack Number")

        self.spin = gui.SpinBox(self.currentMachine, 0, 100, width=200, height=30, margin='10px')
        self.screenTable = gui.TableWidget(9, 1, True, True, width='100%')
        
        writeMachine2Table(yeet, self.table, self.currentMachine)
        
        nextBT = gui.Button('Next Machine!', width=200, height=30, margin='10px')
        prevBT = gui.Button('Previous Machine!', width=200, height=30, margin='10px')
        self.connBT = gui.Button('Connect Machine!', width=200, height=30, margin='10px', style={'background-color': 'red'})
        self.confBT = gui.Button('Configure Machine!', width=200, height=30, margin='10px', style={'background-color': 'red'})
        self.exitBT = gui.Button('Exit!', width=200, height=30, margin='10px', style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})
        
        nextBT.onclick.do(self.nextMachinePressed)
        prevBT.onclick.do(self.prevMachinePressed)
        self.connBT.onclick.do(self.connMachinePressed)
        self.confBT.onclick.do(self.confMachinePressed)
        self.exitBT.onclick.do(self.exitPressed)

        cont.append([self.title, self.table, nextBT, prevBT, self.connBT, self.confBT, self.spin, self.screenTable, self.exitBT])
    
        self.spin.onchange.do(self.on_spin_change)
        
        return cont

    def nextMachinePressed(self, emitter):
        self.currentMachine += 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def prevMachinePressed(self, emitter):
        self.currentMachine -= 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def writeScreenTable(self, lineList):
        for i in range(len(lineList)):
            if bool(lineList[i]):
                self.screenTable.item_at(i+1, 0).set_text(lineList[i])
          
    def nextMachine(self):
        self.currentMachine+=1
        writeMachine2Table(yeet, self.table, self.currentMachine)
    
    def getConnectScreen(self, numLines):
        lineList = []
        writeNewLine(self.ser)
        while(True):
            line = self.ser.readline().decode('utf-8')
            lineList.append(line.strip())
            if line.find("Install") != -1:
                break
        return lineList[-numLines:]

    def connMachinePressed(self, emitter):
        try:
            self.ser = openSerial("COM4")
        except Exception as err:
            exception_type = type(err).__name__
            print(exception_type)
        else:
            time.sleep(1)
            self.connBT.set_style({'background-color': 'green'})
            self.connBT.set_text('Connected!')
            self.confBT.set_style({'background-color': 'red'})
            self.confBT.set_text('Configure Machine!')
            self.writeScreenTable(self.getConnectScreen(5))

    def confMachinePressed(self, emitter):
        print(yeet[self.currentMachine])
        writeMachine(self.ser, yeet[self.currentMachine])
        print('aaaaaa')
        self.writeScreenTable(self.getConnectScreen(8))
        self.ser.close()
        self.connBT.set_style({'background-color': 'red'})
        self.connBT.set_text('Connect Machine!')
        self.confBT.set_style({'background-color': 'green'})
        self.confBT.set_text('Configured!')
        self.nextMachine()

    def on_spin_change(self, widget, newValue):
        self.currentMachine = newValue - 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def exitPressed(self, emitter):
        self.close()
    
start(MyApp, address='0.0.0.0', port=8081, multiple_instance=False, enable_file_cache=True, update_interval=0.1, start_browser=True)





