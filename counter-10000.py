import RPi.GPIO as GPIO
import time

# GPIO pin configuration for 7-segment display segments (A to G)
segments = [2, 3, 4, 17, 27, 22, 10]

# GPIO pins for digit control (D1 to D4)
digits = [5, 6, 13, 19]

# GPIO pin for the switch
switch_pin = 18

# Number representations for the 7-segment display
# numbers = {
#     0: [1, 1, 1, 1, 1, 1, 0],  # 0
#     1: [0, 1, 1, 0, 0, 0, 0],  # 1
#     2: [1, 1, 0, 1, 1, 0, 1],  # 2
#     3: [1, 1, 1, 1, 0, 0, 1],  # 3
#     4: [0, 1, 1, 0, 0, 1, 1],  # 4
#     5: [1, 0, 1, 1, 0, 1, 1],  # 5
#     6: [1, 0, 1, 1, 1, 1, 1],  # 6
#     7: [1, 1, 1, 0, 0, 0, 0],  # 7
#     8: [1, 1, 1, 1, 1, 1, 1],  # 8
#     9: [1, 1, 1, 0, 0, 1, 1]   # 9
# }


# Inverted number representations for common anode 7-segment display
numbers = {
    0: [0, 0, 0, 0, 0, 0, 1],  # 0
    1: [1, 0, 0, 1, 1, 1, 1],  # 1
    2: [0, 0, 1, 0, 0, 1, 0],  # 2
    3: [0, 0, 0, 0, 1, 1, 0],  # 3
    4: [1, 0, 0, 1, 1, 0, 0],  # 4
    5: [0, 1, 0, 0, 1, 0, 0],  # 5
    6: [0, 1, 0, 0, 0, 0, 0],  # 6
    7: [0, 0, 0, 1, 1, 1, 1],  # 7
    8: [0, 0, 0, 0, 0, 0, 0],  # 8
    9: [0, 0, 0, 0, 1, 0, 0]   # 9
}


# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up 7-segment display pins as output
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.HIGH)

# Set up digit control pins as output
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, GPIO.HIGH)

# Set up the switch pin
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to display a number on the active 7-segment display
def display_number(num):
    for i in range(7):
        GPIO.output(segments[i], numbers[num][i])

# Function to multiplex between the four digits
def display_multiplex(counter):
    digits_values = [counter // 1000, (counter // 100) % 10, (counter // 10) % 10, counter % 10]

    print(digits_values)

    # for each digit
    for i in range(4):
        # print(digits[i])
        GPIO.output(digits[i], GPIO.HIGH)  # Activate the digit
        display_number(digits_values[i])   # Display the corresponding number
        time.sleep(0.005)  # Small delay to let the digit light up
        GPIO.output(digits[i], GPIO.LOW)   # Deactivate the digit

while True:
    try:
        start_number = int(input("Enter a starting number (0-9999): "))
        if 0 <= start_number <= 9999:
            break
        else:
            print("Please enter a number between 0 and 9999.")
    except ValueError:
        print("Invalid input. Please enter a valid number between 0 and 9999.")


# Main program
try:
    counter = start_number

    while True:
        # Check if the switch is pressed
        if GPIO.input(switch_pin) == GPIO.LOW:
            counter = (counter + 1) % 10000  # Increment counter and reset to 0 after 9999
            time.sleep(0.2)  # Debounce delay

        # Continuously multiplex between digits
        display_multiplex(counter)

finally:
    GPIO.cleanup()
