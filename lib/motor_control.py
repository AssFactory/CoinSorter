from machine import Pin, PWM, I2C
from ina219 import INA219
import config
import utime  # <-- 1. Import the time library

class MotorControl:
    def __init__(self):
        self.in1 = PWM(Pin(config.MOTOR_IN1_PIN))
        self.in2 = PWM(Pin(config.MOTOR_IN2_PIN))
        self.in1.freq(config.MOTOR_PWM_FREQUENCY)
        self.in2.freq(config.MOTOR_PWM_FREQUENCY)
        
        self.is_running = False
        self.start_time = 0  # <-- 2. Add a variable to store the start time
        
        self.ina = INA219(I2C(0, sda=Pin(0), scl=Pin(1), freq=100000))
        self.ina.set_calibration_32V_1A()
        self.stop()
    
    def stop(self):
        self.in1.duty_u16(0)
        self.in2.duty_u16(0)
        self.is_running = False
        self.start_time = 0  # <-- 3. Reset time when stopped
    
    def ccw(self):
        self.in1.duty_u16(65535 - config.MOTOR_SPEED_CCW)
        self.in2.duty_u16(65535)
        self.is_running = True
        self.start_time = utime.ticks_ms()  # <-- 4. Record start time

    def cw(self):
        self.in1.duty_u16(65535)
        self.in2.duty_u16(65535 - config.MOTOR_SPEED_CW)
        self.is_running = True
        #self.start_time = utime.ticks_ms()  # <-- 4. Record start time

    def is_stalled(self):
        # --- 5. Add the new time-check logic ---
        
        # If motor isn't running, it can't be stalled.
        if not self.is_running:
            return False
            
        # Calculate how long the motor has been running
        time_since_start = utime.ticks_diff(utime.ticks_ms(), self.start_time)
        
        # If it's been less than 200ms, ignore the current and return False
        if time_since_start < config.MOTOR_STARTUP_DELAY_MS:
            return False  # In the "ignore" period

        # --- Original logic (only runs *after* 200ms) ---
        current_ma = self.ina.current
        #print("Motor current: {} mA".format(current_ma))
        
        if current_ma > config.MOTOR_MAX_CURRENT_MA:
            return True
        else:
            return False