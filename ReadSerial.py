import serial
import time

try:
    ser = serial.Serial(
        port='COM5',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1  # Set a small timeout
    )
    print(f"Connected to: {ser.portstr}")
except serial.SerialException as e:
    print(f"Failed to connect: {e}")
    exit()

count = 1

try:
    while True:
        data = ser.readline().decode('utf-8').strip()
        data = data.split()

        if len(data) >= 3:
            temp = float(''.join(filter(str.isdigit, data[0]))) / 10000
            lux = int(''.join(filter(str.isdigit, data[1])))
            tur = float(''.join(filter(str.isdigit, data[2]))) / 100
            
            print("{:.4f} {} {:.2f}".format(temp, lux, tur))     
except KeyboardInterrupt:
    print("Exiting...")
    
finally:
    ser.close()
    print("Serial port closed.")
