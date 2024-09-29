import RPi.GPIO as GPIO
import time

# Pin configuration for 7-segment display segments (A to G)
segments = [2, 3, 4, 17, 27, 22, 10]

# GPIO pin for the switch
switch_pin = 18

# Number representations for the 7-segment display
numbers = {
    0: [1, 1, 1, 1, 1, 1, 0],  # 0
    1: [0, 1, 1, 0, 0, 0, 0],  # 1
    2: [1, 1, 0, 1, 1, 0, 1],  # 2
    3: [1, 1, 1, 1, 0, 0, 1],  # 3
    4: [0, 1, 1, 0, 0, 1, 1],  # 4
    5: [1, 0, 1, 1, 0, 1, 1],  # 5
    6: [1, 0, 1, 1, 1, 1, 1],  # 6
    7: [1, 1, 1, 0, 0, 0, 0],  # 7
    8: [1, 1, 1, 1, 1, 1, 1],  # 8
    9: [1, 1, 1, 0, 0, 1, 1]   # 9
}

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up 7-segment display pins as output
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)

# Set up the switch pin
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to display a number on the 7-segment display
def display_number(num):
    for i in range(7):
        GPIO.output(segments[i], numbers[num][i])

# Main program
try:
    counter = 0
    display_number(counter)
    
    while True:
        if GPIO.input(switch_pin) == GPIO.LOW:  # Check if the switch is pressed
            counter = (counter + 1) % 10  # Increment counter and reset to 0 after 9
            display_number(counter)
            time.sleep(0.4)  # Debounce delay

finally:
    GPIO.cleanup()