from gpiozero import DistanceSensor, Servo
from time import sleep

class HYPERSONIC:
    def __init__(self, trig, echo, id):
        self.sensor = DistanceSensor(echo=echo, trigger=trig)
        self.id = id
        print("Sensor", id, "Activated")

    def getDistance(self):
        distance = self.sensor.distance * 100  # Convert to cm
        return self.id, round(distance, 2)

    def close(self):
        self.sensor.close()


class SERVO:
    def __init__(self, pin):
        self.servo = Servo(pin)
        self.current_angle = 0
        self.set_angle(self.current_angle)

    def set_angle(self, angle):
        # Convert angle in degrees to a value between -1 and 1
        angle_value = (angle / 180) - 0.5
        self.servo.value = angle_value
        sleep(0.5)  # Give the servo time to move

    def rotate_90_degrees(self):
        self.current_angle = (self.current_angle + 90) % 360
        self.set_angle(self.current_angle)

    def cleanup(self):
        self.servo.detach()


def main():
    sensor1 = HYPERSONIC(23, 24, 1)
    servo1 = SERVO(12)
    try:
        while True:
            servo1.rotate_90_degrees()
            sleep(1.5)
            id, dist = sensor1.getDistance()
            print("Sensor", id, "Distance: ", dist, "cm")
            sleep(0.5)
    except KeyboardInterrupt:  # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        print("Cleaning up!")
        servo1.cleanup()
        sensor1.close()

if __name__ == "__main__":
    main()
