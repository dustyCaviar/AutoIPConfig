"""
Configures servers

" and " fix
yeet global variable
Docstrings
"""
import sys, os, time, csv
import serial
import remi.gui as gui
from remi import start, App



# Designated sleep interval
SERIAL_SLEEP = 0.2

# Designated com port
COM_PORT = "COM4"

def importIpConfigs(ipsTxt):
    """ Take a path to a .csv and return csv dctionary of machines. """
    configList =[]
    
    with open(ipsTxt, newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=",")
        for row in csv_reader:
            configList.append(row)
    return configList
    

# String yeet determines path to .csv with ip configs
yeet = importIpConfigs("ips.csv") 

def openSerial(comPort):
    """ Take a com port as string and return open serial connection. """
    return serial.Serial(port=comPort, baudrate=115200, bytesize=8, parity="N", stopbits=1, timeout=None, xonxoff=0, rtscts=0)

def closeSerial(serialConnection):
    ser.close()

def writeLine(serialConnection, machine, infoKey):
    """
    Take an open serial connection, a machine from the csv dictionary of machines,
    and a key to that dictionary (one of the config lines) and writes that line over the serial connection.
    """
    serialConnection.write(machine[infoKey].encode())
    writeNewLine(serialConnection)
    time.sleep(SLEEP_SERIAL)

def writeYes(serialConnection):
    
    serialConnection.write(b"y\n")
    time.sleep(SLEEP_SERIAL)

def writeExit(serialConnection):
    serialConnection.write(b"exit\n")
    time.sleep(SLEEP_SERIAL)

def writeNewLine(serialConnection):
    serialConnection.write(b"\n")

def writeMachine(serialConnection, machine):
    '''
    Take a serial connection and a specific machine from the csv dictionary
    and configure it over serial connection.   
    '''
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
    writeLine(serialConnection, machine, "RACK_NUMBER")
    writeLine(serialConnection, machine, "MACHINE_NUMBER")
    writeNewLine(serialConnection)

def writeMachine2Table(ipConfigs, table, machineNumber):
    ''' Take csv dictionary and a machine number and write it to a remi gui table. '''
    table.item_at(1, 0).set_text(yeet[machineNumber]["MACHINE_NUMBER"])
    table.item_at(1, 1).set_text(yeet[machineNumber]["IP"])
    table.item_at(1, 2).set_text(yeet[machineNumber]["NETMASK"])
    table.item_at(1, 3).set_text(yeet[machineNumber]["GATEWAY"])
    table.item_at(1, 4).set_text(yeet[machineNumber]["RACK_NUMBER"])

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        ''' Set up structure of gui webpage, write initial data to the table. '''

        # Current machine:
        self.currentMachine = 0

        cont = gui.Container(width="75%", style={"display": "block", "margin-left": "auto", "margin-right": "auto"})
        ser = serial.Serial()
        self.title = gui.Label("Auto IP Config", width="100%", margin="10px", style={"margin-top":"20px", "font-size": "20px", "text-align": "center"})
        self.table = gui.TableWidget(2, 5, True, True)
        self.table.item_at(0, 0).set_text("Machine #")
        self.table.item_at(0, 1).set_text("IP")
        self.table.item_at(0, 2).set_text("Netmask")
        self.table.item_at(0, 3).set_text("Gateway")
        self.table.item_at(0, 4).set_text("Rack Number")

        self.spin = gui.SpinBox(self.currentMachine, 0, 100, width=200, height=30, margin="10px")
        self.screenTable = gui.TableWidget(9, 1, True, True, width="100%")
        
        writeMachine2Table(yeet, self.table, self.currentMachine)
        
        nextBT = gui.Button("Next Machine!", width=200, height=30, margin="10px")
        prevBT = gui.Button("Previous Machine!", width=200, height=30, margin="10px")
        self.connBT = gui.Button("Connect Machine!", width=200, height=30, margin="10px", style={"background-color": "red"})
        self.confBT = gui.Button("Configure Machine!", width=200, height=30, margin="10px", style={"background-color": "red"})
        self.exitBT = gui.Button("Exit!", width=200, height=30, margin="10px", style={"display": "block", "margin-left": "auto", "margin-right": "auto"})
        
        nextBT.onclick.do(self.nextMachinePressed)
        prevBT.onclick.do(self.prevMachinePressed)
        self.connBT.onclick.do(self.connMachinePressed)
        self.confBT.onclick.do(self.confMachinePressed)
        self.exitBT.onclick.do(self.exitPressed)

        cont.append([self.title, self.table, nextBT, prevBT, self.connBT, self.confBT, self.spin, self.screenTable, self.exitBT])
    
        self.spin.onchange.do(self.on_spin_change)
        
        return cont

    def nextMachinePressed(self, emitter):
        ''' Watch for button press and iterate to next machine and update remi gui table. '''
        self.currentMachine += 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def prevMachinePressed(self, emitter):
        ''' Watch for button press and iterate to next machine and update remi gui tbale. '''
        self.currentMachine -= 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def writeScreenTable(self, lineList):
        for i in range(len(lineList)):
            if bool(lineList[i]):
                self.screenTable.item_at(i+1, 0).set_text(lineList[i])
          
    def nextMachine(self):
        ''' Iterate to next machine. '''
        self.currentMachine+=1
        writeMachine2Table(yeet, self.table, self.currentMachine)
    
    def getConnectScreen(self, numLines):
        ''' Parse machines config screen via serial and output to gui screen table. '''
        lineList = []
        writeNewLine(self.ser)
        while(True):
            line = self.ser.readline().decode("utf-8")
            lineList.append(line.strip())
            if line.find("Install") != -1:
                break
        return lineList[-numLines:]

    def connMachinePressed(self, emitter):
        ''' Wait for button press and connect to current machine. '''
        try:
            self.ser = openSerial(COM_PORT)
        except Exception as err:
            exception_type = type(err).__name__
            print(exception_type)
        else:
            time.sleep(1)
            self.connBT.set_style({"background-color": "green"})
            self.connBT.set_text("Connected!")
            self.confBT.set_style({"background-color": "red"})
            self.confBT.set_text("Configure Machine!")
            self.writeScreenTable(self.getConnectScreen(5))

    def confMachinePressed(self, emitter):
        ''' Wait for button press and configure connected machine. '''
        print(yeet[self.currentMachine])
        writeMachine(self.ser, yeet[self.currentMachine])
        self.writeScreenTable(self.getConnectScreen(8))
        self.ser.close()
        self.connBT.set_style({"background-color": "red"})
        self.connBT.set_text("Connect Machine!")
        self.confBT.set_style({"background-color": "green"})
        self.confBT.set_text("Configured!")
        self.nextMachine()

    def on_spin_change(self, widget, newValue):
        ''' Update current machine based based on remi gui spin slider. '''
        self.currentMachine = newValue - 1
        writeMachine2Table(yeet, self.table, self.currentMachine)

    def exitPressed(self, emitter):
        self.close()
    
start(MyApp, address="0.0.0.0", port=8081, multiple_instance=False, enable_file_cache=True, update_interval=0.1, start_browser=True)





