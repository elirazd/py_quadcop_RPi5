import time
import serial
import subprocess

class SIM900:
    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            ok=self.send_at_command('AT')
            if str(ok).find('OK')>=0:
                self.send_at_command('ATE0')
                return True
            else:
                raise Exception("SIM900 turned off")
        except Exception as e:
            print(f"Error connecting to SIM900: {e}")
            return False

    def check_provider(self):
        try:
            provider=self.send_at_command('AT+CSPN?')
            if str(provider).find('ERROR')>=0:
                raise Exception("No Mobile Carrier found")
            else:
                return True
        except Exception as e:
            print(str(e))
            return False

    def sendMessage(self, phoneNumber, msg):
        try:
            self.send_at_command('AT+CMGF=1\r'.encode())
            self.send_at_command('AT+CMGS=\"{}\"\r'.format(phoneNumber))
            self.send_at_command('{}\r'.format(msg))
            self.mConn.write(cmd.encode())
            return True
        except Exception as e:
            print(str(e))
            return False

    def send_at_command(self, command, wait_for_response=True):
        try:
            self.connection.write((command + '\r').encode())
            time.sleep(0.5)
            if wait_for_response:
                response = self.connection.readlines()
                for line in response:
                    print(line.decode().strip())
            return response
        except Exception as e:
            print(f"Error sending AT command: {e}")

    def setup_gprs(self, apn):
        try:
            self.send_at_command('AT+SAPBR=3,1,"CONTYPE","GPRS"')
            self.send_at_command(f'AT+SAPBR=3,1,"APN","{apn}"')
            self.send_at_command('AT+SAPBR=1,1')
            self.send_at_command('AT+SAPBR=2,1')
            return True
        except Exception as e:
            print(f"Error setting up GPRS: {e}")
            return False

    def start_ppp_connection(self):
        try:
            # Write chat scripts
            chat_connect = '''ABORT 'BUSY'
ABORT 'NO CARRIER'
ABORT 'ERROR'
ABORT 'NO DIALTONE'
ABORT 'NO DIAL TONE'
ABORT 'Invalid Login'
ABORT 'Login incorrect'
'' 'ATZ'
OK 'ATE0'
OK 'AT+CGDCONT=1,"IP","your_apn_here"'
OK 'ATD*99***1#'
CONNECT '' '''

            chat_disconnect = '''ABORT 'BUSY'
ABORT 'ERROR'
ABORT 'NO DIALTONE'
ABORT 'Invalid Login'
ABORT 'Login incorrect'
'' '\\K'
'' '+++ATH'
'' 'ATZ'
OK '\\c' '''
            # Make sure the scripts are executable
            #subprocess.run(['sudo', 'chmod', '+x', '/etc/chatscripts/gprs-connect-chat'], check=True)
            #subprocess.run(['sudo', 'chmod', '+x', '/etc/chatscripts/sim900-chat-disconnect'], check=True)
            with open('/etc/chatscripts/gprs-connect-chat', 'w') as f:
                f.write(chat_connect)

            with open('/etc/chatscripts/sim900-chat-disconnect', 'w') as f:
                f.write(chat_disconnect)

            # Write the PPP configuration
            ppp_conf = '''/dev/ttyAMA0 115200
connect 'chat -v -f /etc/chatscripts/gprs-connect-chat'
disconnect 'chat -v -f /etc/chatscripts/sim900-chat-disconnect'
defaultroute
usepeerdns
persist
noauth '''

            with open('/etc/ppp/peers/sim900', 'w') as f:
                f.write(ppp_conf)

            print("Start the PPP connection and capture output")
            result = subprocess.run(['sudo', 'pon', 'sim900'], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            
            if result.returncode != 0:
                print("Failed to start PPP connection.")
                return False

            return True
        except Exception as e:
            print(f"Error starting PPP connection: {e}")
            return False

    def stop_ppp_connection(self):
        try:
            result = subprocess.run(['sudo', 'poff', 'sim900'], capture_output=True, text=True)
            print(result.stdout)
            print(result.stderr)
            
            if result.returncode != 0:
                print("Failed to stop PPP connection.")
                return False

            return True
        except Exception as e:
            print(f"Error stopping PPP connection: {e}")
            return False

    def close(self):
        try:
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Error closing connection: {e}")

if __name__ == "__main__":
    sim = SIM900("/dev/ttyAMA0", 19200, 1.0)
    if sim.connect():
        sim.check_provider()
        sim.setup_gprs("Sphone")  # Replace with your APN
        sim.start_ppp_connection()
        # Now you can access the internet using the SIM900 module

        # To stop the PPP connection
        sim.stop_ppp_connection()

        #sim.close()
