# Button
BUTTON_PIN = 15                  # GPIO pin for button input

BUTTON_DEBOUNCE = 100           # Debounce time in milliseconds
BUTTON_LONG_PRESS = 1000        # Duration in milliseconds to consider a long press
BUTTON_POLL_INTERVAL = 10

#SPI interface
SPI_SCK_PIN = 18                # SPI clock pin (Shared)
SPI_MOSI_PIN = 19               # SPI Master Out Slave In pin (Shared)  
SPI_MISO_PIN = 16               # SPI Master In Slave Out pin (Shared)
          
SPI_BAUDRATE = 10000000          # SPI baudrate for general use

# Display
DISPLAY_CS_PIN = 17             # Chip select pin for display
DISPLAY_DC_PIN = 20             # Data/command pin for display
DISPLAY_RST_PIN = 21            # Reset pin for display

# Data logginng 
SD_CS_PIN = 9                   # Chip select pin for SD card

SD_FILE_NAME = "coin_log.txt"   # Log file name


# Motor control
MOTOR_IN1_PIN = 10               # Direction control pin 1
MOTOR_IN2_PIN = 11               # Direction control pin 2

MOTOR_PWM_FREQUENCY = 20000     # PWM frequency in Hz for speed control
MOTOR_SPEED_CW = 20000             # Motor speed (0-65535, where 65535 is 100% duty cycle)
MOTOR_SPEED_CCW = 50000             # Motor speed (0-65535, where 65535 is 100% duty cycle)
MOTOR_MAX_CURRENT_MA = 400      # Maximum allowable motor current in milliamps
MOTOR_STARTUP_DELAY_MS = 300        # Delay in milliseconds to allow motor to start before monitoring current
REVERSE_DURATION = 0.4         # Time in seconds to run in reverse during fault recovery
FAULT_RETRY_LIMIT = 3           # Number of times to try recovering from a fault
FAULT_COOLDOWN_MS = 2000 

# Coin sensor 
SENSOR_1_CENT_PIN = 26          # GPIO pin for 1 cent coin sensor
SENSOR_2_CENT_PIN = 26          # GPIO pin for 2 cent coin sensor
SENSOR_5_CENT_PIN = 26          # GPIO pin for 5 cent coin sensor
SENSOR_10_CENT_PIN = 27         # GPIO pin for 10 cent coin sensor
SENSOR_20_CENT_PIN = 26         # GPIO pin for 20 cent coin sensor
SENSOR_50_CENT_PIN = 26         # GPIO pin for 50 cent coin sensor
SENSOR_1_EURO_PIN = 26          # GPIO pin for 1 euro coin sensor
SENSOR_2_EURO_PIN = 26          # GPIO pin for 2 euro coin sensor

SENSOR_DEBOUNCE = 100           # Debounce time in milliseconds for coin sensors