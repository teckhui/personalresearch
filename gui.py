import os
import csv
import numpy as np
import sys
from time import sleep
from PyQt5 import QtWidgets
from picoscope_ui import Ui_MainWindow
import picoscope as ps

os.system('pyuic5 picoscope_ui.ui > picoscope_ui.py')
sleep(2)


def start():
    startFrequency = ui.startFrequency_input.text()
    startFrequency = float(startFrequency)
    endFrequency = ui.endFrequency_input.text()
    endFrequency = float(endFrequency)
    intervalFrequency = ui.intervalFrequency_input.text()
    intervalFrequency = float(intervalFrequency)
    intervals = int((endFrequency - startFrequency)//intervalFrequency +1)
    frequencySpace = np.linspace(startFrequency, endFrequency, intervals)

    channelAVoltage = np.linspace(startFrequency, endFrequency, intervals)
    channelBVoltage = np.linspace(startFrequency, endFrequency, intervals)
    impedance = np.linspace(startFrequency, endFrequency, intervals)

    for n in range(0, len(frequencySpace)):
        ps.configureSignalGenerator(2,frequencySpace[n])
        ps.timeBase(frequencySpace[n])
        channelAVoltage[n], channelBVoltage[n] = ps.getMeasurements()
        impedance[n] = (channelAVoltage[n] / (channelBVoltage[n] / 325.0)) 

    head = "frequency (Hz), ChA Voltage, ChB Voltage, Impedance"
    filename = ui.fileName.text()
    np.savetxt(str(filename) + ".csv", np.transpose([frequencySpace,channelAVoltage,channelBVoltage,impedance]), delimiter=",", header=head)

    # ui.matplotlibwidget.axes.plot(frequencySpace,impedance)
    # ui.matplotlibwidget.draw()


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.show()
ui = Ui_MainWindow()
ui.setupUi(window)
ui.startButton.clicked.connect(start)
sys.exit(app.exec_())  