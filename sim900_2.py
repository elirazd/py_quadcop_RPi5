import time
import serial

class SIM900:
    def __init__(self, port, baudrate, timeout):
        self.mPort = port
        self.mPBaudrate = baudrate
        self.mTimeout = timeout
        
    def connect(self):
        try:
            self.mConn = serial.Serial(port=self.mPort, baudrate=self.mPBaudrate, timeout=self.mTimeout)
            # Check if the module is responding
            self.mConn.write('AT\r'.encode())
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print("Send command:", response)
            print("AT Response:", response2)
            return True
        except Exception as e:
            print(str(e))
            return False

    def call(self, phoneNumber):
        try:
            time.sleep(1)
            print("Start call")
            cmd = "ATD{};\r".format(phoneNumber)
            self.mConn.write(cmd.encode())
            time.sleep(30)
            print("End call")
        except Exception as e:
            print(str(e))
            return False

    def sendMessage(self, phoneNumber, msg):
        try:
            self.mConn.write('AT+CMGF=1\r'.encode())
            time.sleep(0.5)
            cmd = 'AT+CMGS=\"{}\"\r'.format(phoneNumber)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)
            cmd = '{}\r'.format(msg)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)
            self.mConn.write(bytes([26]))
            time.sleep(0.5)
            return True
        except Exception as e:
            print(str(e))
            return False
    
    def checkProvider(self):
        try:
            self.mConn.write('AT+CSPN?\r'.encode())
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print("Send command:", response)
            print("AT Response:", response2)
            return True
        except Exception as e:
            print(str(e))
            return False

    def disconnect(self):
        try:
            self.mConn.close()
            return False
        except Exception as e:
            print(str(e))
            return False

    def setupGPRS(self, apn):
        try:
            self.mConn.write('AT+SAPBR=3,1,"CONTYPE","GPRS"\r'.encode())
            time.sleep(0.5)
            cmd = 'AT+SAPBR=3,1,"APN","{}"\r'.format(apn)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)
            self.mConn.write('AT+SAPBR=1,1\r'.encode())
            time.sleep(1)
            self.mConn.write('AT+SAPBR=2,1\r'.encode())
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print("GPRS Setup command:", response)
            print("GPRS Setup Response:", response2)
            return True
        except Exception as e:
            print(str(e))
            return False
    
    def sendHTTPRequest(self, url):
        try:
            self.mConn.write('AT+HTTPINIT\r'.encode())
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print(response,response2)
            cmd = 'AT+HTTPPARA="URL","{}"\r'.format(url)
            self.mConn.write(cmd.encode())
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print(response,response2)
            self.mConn.write('AT+HTTPACTION=0\r'.encode())
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print(response,response2)
            time.sleep(5)  # Give some time for the request to complete
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print(response,response2)
            self.mConn.write('AT+HTTPREAD\r'.encode())
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print(response,response2)
            time.sleep(0.5)
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print("HTTP Request command:", response)
            print("HTTP Request Response:", response2)
            self.mConn.write('AT+HTTPTERM\r'.encode())
            response = self.mConn.readline().decode('UTF-8')
            response2 = self.mConn.readline().decode('UTF-8')
            print("HTTP Request command:", response)
            print("HTTP Request Response:", response2)
            return True
        except Exception as e:
            print(str(e))
            return False

if __name__=="__main__":
    sim = SIM900("/dev/ttyAMA0", 19200, 1.0)
    if sim.connect():
        
        sim.checkProvider()
        #sim.setupGPRS("Sphone")  # For Cellcom APN = Sphone
        sim.sendHTTPRequest("http://google.com")
        #sim.disconnect()
        
    while(1):
    #if sim.mConn.in_waiting() > 0:
        try:
            print(self.mConn.readline().decode('UTF-8'))
        except:
            pass
            
        
