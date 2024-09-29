import RPi.GPIO as GPIO
import time

# GPIO pin configuration for 7-segment displays

# Display 1 (ones place)
segments_1 = [2, 3, 4, 17, 27, 22, 10]

# Display 2 (tens place)
segments_2 = [5, 6, 13, 19, 26, 21, 0]

# GPIO pin for the switch
switch_pin = 18

# Number representations for the 7-segment display (same for both displays)
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

# Set up both 7-segment display pins as output
for segment in segments_1 + segments_2:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)

# Set up the switch pin
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to display a number on a 7-segment display
def display_number(display, num):
    for i in range(7):
        GPIO.output(display[i], numbers[num][i])

# Function to split a number into tens and ones digits
def split_number(num):
    tens = num // 10
    ones = num % 10
    return tens, ones

# Main program
try:
    counter = 0
    tens, ones = split_number(counter)
    display_number(segments_1, ones)  # Display initial ones
    display_number(segments_2, tens)  # Display initial tens
    
    while True:
        if GPIO.input(switch_pin) == GPIO.LOW:  # Check if the switch is pressed
            counter = (counter + 1) % 100  # Increment counter and reset to 0 after 99
            tens, ones = split_number(counter)
            display_number(segments_1, ones)  # Update ones place display
            display_number(segments_2, tens)  # Update tens place display
            time.sleep(0.2)  # Debounce delay

finally:
    GPIO.cleanup()
