import serial
import serial.tools.list_ports
import struct

# Mac ports, for windows you have to find the ports yourself
#frdm_port = "/dev/cu.COM3"
frdm_port = "COM6"


Start = b'\x16' #putting a value in bits into a variable bcuz the var will be added to the byte stream and sent over to simulink
SYNC = b'\x22'
#Fn_set = b'\x55'
Fn_set = struct.pack("B",55)
p_aPaceWidth = struct.pack('B', 2)
p_vPaceWidth = struct.pack('B', 7)
p_aPaceAmp = struct.pack('f', 1.2)#f is single
p_vPaceAmp = struct.pack('f', 2.5)
p_atrialsensitivity = struct.pack('f', 4)
p_ventriclesensitivity = struct.pack('f', 9)
p_ARP = struct.pack('H', 200) #H is uint16
p_VRP = struct.pack('H', 300)
p_lowratelimit = struct.pack('B', 3) #we used B becasue its uint8
p_Mode = struct.pack('B', 2)
#blue_en = struct.pack("B", 1)

Signal_set = Start + Fn_set + p_aPaceWidth + p_vPaceWidth + p_aPaceAmp + p_vPaceAmp + p_atrialsensitivity + p_ventriclesensitivity + p_ARP + p_VRP + p_lowratelimit + p_Mode
Signal_echo = Start + SYNC + p_aPaceWidth + p_vPaceWidth + p_aPaceAmp + p_vPaceAmp + p_atrialsensitivity + p_ventriclesensitivity + p_ARP + p_VRP + p_lowratelimit + p_Mode

with serial.Serial(frdm_port, 115200) as pacemaker: #pushes signal to the baord
    pacemaker.write(Signal_set)

with serial.Serial(frdm_port, 115200) as pacemaker: #send the byte stream that echos to the pacemaker (the block that sends parameter back to you)
    pacemaker.write(Signal_echo)
    data = pacemaker.read(24)
    p_aPaceWidth = data[0]
    p_vPaceWidth = data[1]
    p_aPaceAmp = struct.unpack('f', data[2:6])[0] 
    p_vPaceAmp = struct.unpack('f', data[6:10])[0]
    p_atrialsensitivity = struct.unpack('f', data[10:14])[0]
    p_ventriclesensitivity = struct.unpack('f', data[14:18])[0]
    p_ARP = struct.unpack('H', data[18:20])[0]  #H is uint16
    p_VRP = struct.unpack('H', data[20:22])[0] 
    p_lowratelimit = data[22] #we used B becasue its uint8
    p_Mode = data[23]
    

print("From the board:")
print("p_aPaceWidth = ", p_aPaceWidth)
print("p_vPaceWidth = ", p_vPaceWidth)
print("p_aPaceAmp = ", p_aPaceAmp)
print("p_vPaceAmp = ",  p_vPaceAmp)
print("p_atrialsensitivity = ", p_atrialsensitivity)
print("p_ventriclesensitivity = ",  p_ventriclesensitivity)
print("p_ARP = ",  p_ARP)
print("p_VRP = ",  p_VRP)
print("p_lowratelimit = ",  p_lowratelimit)
print("p_Mode = ",  p_Mode)


