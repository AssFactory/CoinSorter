import config
from machine import Pin, SPI
from display import CoinSortDisplay 
from motor_control import MotorControl
from sensor import CoinSensor
import utime

# --- Configuration (Add this to your config.py) ---
# I'm adding this constant here for the example.
# You should move this line to your 'config.py' file.
# config.FAULT_COOLDOWN_MS = 30000  # 30 seconds


# --- Initialize objects ---
button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)
spi = SPI(0, baudrate=config.SPI_BAUDRATE, polarity=0, phase=0, sck=Pin(config.SPI_SCK_PIN), mosi=Pin(config.SPI_MOSI_PIN), miso=Pin(config.SPI_MISO_PIN))
display = CoinSortDisplay(spi)
motor = MotorControl()
sensor_1_cent = CoinSensor(pin_number=config.SENSOR_1_CENT_PIN)
# ... other sensors

# --- Global State Variables ---
button_state = 0            # 0=IDLE, 1=DEBOUNCE, 2=PRESSED, 3=HELD
button_press_time = 0       # When was it first pressed?
button_last_check_time = 0  # For polling interval

fault_count = 0
last_fail_time = 0    # Timestamp (in ms) of the last fail


# --- Main Loop ---
print("Program started. Press the button to control the motor.")
display.show_message("Ready")
try:
    while True:
        # Get the current time once at the start of the loop
        current_time = utime.ticks_ms()
        
        # --- 1. Button State Machine (Polling) ---
        # We check the button state every 20ms
        if utime.ticks_diff(current_time, button_last_check_time) > config.BUTTON_POLL_INTERVAL:
            button_last_check_time = current_time
            is_pressed = (button.value() == 0) # Read the pin (0 = pressed for PULL_UP)

            # STATE 0: IDLE (Waiting for a press)
            if button_state == 0: 
                if is_pressed:
                    button_press_time = current_time # Record press time
                    button_state = 1                 # Move to DEBOUNCE state
            
            # STATE 1: DEBOUNCE (Waiting to confirm it wasn't a bounce)
            elif button_state == 1:
                if not is_pressed:
                    button_state = 0 # It was a bounce, go back to IDLE
                elif utime.ticks_diff(current_time, button_press_time) > config.BUTTON_DEBOUNCE:
                    button_state = 2 # Confirmed press, move to PRESSED
            
            # STATE 2: PRESSED (Confirmed press, waiting for release or long press)
            elif button_state == 2:
                
                # PRIORITY 1: Is the motor running? Stop it.
                if motor.is_running:
                    motor.stop()
                    print("Motor STOPPED.")
                    # *** THE FIX ***
                    # Don't go to IDLE. Go to HELD to wait for the button release.
                    button_state = 3 
                
                # PRIORITY 2: Is it a long press? (Motor is already OFF)
                elif utime.ticks_diff(current_time, button_press_time) > config.BUTTON_LONG_PRESS:
                    # --- ACTION: LONG PRESS DETECTED ---
                    print("LONG PRESS detected.")
                    # (We already know motor is off from the check above)
                    print(f"Resetting fault counter (was {fault_count}).")
                    fault_count = 0
                    last_fail_time = 0
                    button_state = 3 # Move to HELD state
                
                # PRIORITY 3: Is it a release? (And not a long press)
                elif not is_pressed:
                    # --- ACTION: SHORT PRESS RELEASE ---
                    print("SHORT PRESS released.")
                    print("Motor STARTING (resetting faults)...")
                    display.show_amount()
                    fault_count = 0
                    last_fail_time = 0
                    motor.ccw()
                    button_state = 0 # Go back to IDLE
            
            # STATE 3: HELD (Long press was triggered, now just waiting for release)
            elif button_state == 3:
                if not is_pressed:
                    # --- ACTION: LONG PRESS RELEASE ---
                    print("Long press RELEASED.")
                    if motor.is_running:
                         motor.stop()
                         print("Motor STOPPED.")
                    button_state = 0 # Go back to IDLE

        # We only care about stall logic if the motor is supposed to be running
        if motor.is_running:
            
            # 1. CHECK FOR STALL
            if motor.is_stalled(): 
                motor.stop() # Stop immediately
                fault_count += 1
                last_fail_time = utime.ticks_ms() # *** RECORD TIME OF THIS FAULT ***
                
                print(f"FAULT DETECTED! (Attempt {fault_count}/{config.FAULT_RETRY_LIMIT})")
                print("Attempting recovery: Reversing motor...")
                motor.cw() # Reverse
                utime.sleep(config.REVERSE_DURATION)
                motor.stop() 
                utime.sleep(0.5) # Pause
                
                # 2. CHECK IF RETRY LIMIT IS EXCEEDED
                if fault_count >= config.FAULT_RETRY_LIMIT:
                    #motor.stop() # This sets motor.is_running = False
                    print("--- FAULT LIMIT REACHED. MOTOR DISABLED. ---")
                    print("Press the button again to retry.")
                    display.show_message("Motor Blocked")
                    continue # Go to next loop (motor.is_running is now False)
                
                # 3. ATTEMPT FAULT RECOVERY
                else:
                    print("Retrying CCW run...")
                    motor.ccw() # Retry CCW
                    # The loop will now repeat, checking is_stalled() again
            
            # 4. NO FAULT - NORMAL OPERATION & COOLDOWN CHECK
            else:
                # This is the new logic you wanted.
                # If there are faults logged (fault_count > 0),
                # check if the cooldown period has passed since the *last* fault.
                if fault_count > 0:
                    time_since_last_fail = utime.ticks_diff(utime.ticks_ms(), last_fail_time)
                    
                    if time_since_last_fail > config.FAULT_COOLDOWN_MS:
                        print(f"Cooldown successful ({config.FAULT_COOLDOWN_MS / 1000}s passed). Resetting fault counter.")
                        fault_count = 0
                        last_fail_time = 0
                
                # If no fault, and cooldown not met, just let it run.
                # No 'pass' needed, it just loops.
        
        # 5. MOTOR IS NOT RUNNING
        else:
            # The motor is stopped (either by button or by fault limit).
            # We don't do anything here. The fault_count is preserved.
            # Only the button_handler (on START) can reset it now.
            pass

        # Main loop delay
        #utime.sleep_ms(50) 

except KeyboardInterrupt:
    motor.stop()
    print("\nProgram stopped.")