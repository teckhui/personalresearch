import subprocess
import numpy as np
import matplotlib.pyplot as plt


#SigGenerator set value
# picoscope /a Siggen.Frequency.Value=
# picoscope /a Siggen.Amplitude.Value=

#Set Timebase 
# picoscope /a CollectionTime.SelectedIndex=

#Set Range
# picoscope /a Channel.#0.Range.SelectedIndex=

def getMeasurements():
    output = subprocess.check_output(['picoscope','/a','Measurements.CSV?'])
    output = str(output)
    output = output.split('\n')
    space = " "
    channelA = output[0].split(",")
    channelB = output[0].split(",") 
    channelA = channelA[5].split(space) #index in output1 is the columns in picoscope measurements
    channelB = channelB[14].split(space)
  
    if channelA[1] == "V":
        volt_A=float(channelA[0])*1
    elif channelA[1] == "mV":
        volt_A = float(channelA[0])*1E-3
    else:
        volt_A = float(channelA[0])*1E-6
        
    if channelB[1] == "V":
        volt_B=float(channelB[0])*1
    elif channelB[1] == "mV":
        volt_B = float(channelB[0])*1E-3
    else:
        volt_B = float(channelB[0])*1E-6
        
    return volt_A, volt_B

def configureSignalGenerator(amp,freq):
    amp_string = "picoscope /a Siggen.Amplitude.Value="+str(amp)
    freq_string = "picoscope /a Siggen.Frequency.Value="+str(freq)
    subprocess.call(amp_string,stdout=False)
    subprocess.call(freq_string,stdout=False)
#configureSignalGenerator(1.32,50E3) sets voltage to 1.32v and freq to 50khz

def timeBase(freq):
    time_base = 1/float(freq) * 6/10
    time_index = [100E-9,200E-9,500E-9,1E-6,2E-6,5E-6,10E-6,20E-6,50E-6,100E-6,200E-6,500E-6,1E-3,2E-3,5E-3,10E-3,20E-3,50E-3,100E-3,200E-3,500E-3]
    
    for n in range(0,len(time_index)):
        if time_base < time_index[n]:
            break
        time_base_string = "picoscope /a CollectionTime.SelectedIndex="+str(n)
        subprocess.call(time_base_string,stdout=False)
        
startFrequency = 10000
endFrequency = 20000
intervalFrequency = 10000
intervals = (endFrequency - startFrequency)//intervalFrequency +1
frequencySpace = np.linspace(startFrequency, endFrequency, intervals)

channelAVoltage = np.linspace(startFrequency, endFrequency, intervals)
channelBVoltage = np.linspace(startFrequency, endFrequency, intervals)
impedance = np.linspace(startFrequency, endFrequency, intervals)

for n in range(0, len(frequencySpace)):
    configureSignalGenerator(2,frequencySpace[n])
    timeBase(frequencySpace[n])
    channelAVoltage[n], channelBVoltage[n] = getMeasurements()
    impedance[n] = (channelAVoltage[n] / (channelBVoltage[n] / 325.0)) #325 is value of resistor

head = "frequency (Hz), ChA Voltage, ChB Voltage, Impedance"
np.savetxt("results.csv", np.transpose([frequencySpace,channelAVoltage,channelBVoltage,impedance]), delimiter=",", header=head)

plt.plot(frequencySpace,impedance)
plt.show()