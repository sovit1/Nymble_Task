import serial, time, os

# Configurations
SERIAL_PORT = 'COM3'
BAUD_RATE = 2400
DATA_TO_SEND = 'Your string of data goes here.'
CHUNK_SIZE = 20  # Number of characters to send at a time.


# Function to calculate the speed of transmission
def calculate_speed(init_time, final_time, num_bytes):
    duration = final_time - init_time
    speed = (num_bytes * 8) / (duration)  # Speed in bits/second
    return speed


# Function to clear the console screen
def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')  # For windows
    else:
        _ = os.system('clear')  # For mac/linux


# Initialize serial port
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, timeout=0)

# Break the string data into chunks
data_chunks = [DATA_TO_SEND[i:i + CHUNK_SIZE] for i in range(0, len(DATA_TO_SEND), CHUNK_SIZE)]

try:
    while True:
        clear_screen()  # Clear screen for each message
        print(f"Initiating transmission at {BAUD_RATE} baud.")

        # Transmit data and calculate speed
        for chunk in data_chunks:
            print(f"\nTransmitting chunk: {chunk}")
            init_time = time.perf_counter()

            # Transmit data
            ser.write(chunk.encode())

            # Wait for echo. This delay ensures we don't run far ahead of actual transmission
            time.sleep(len(chunk) * 10.0 / BAUD_RATE)

            # Read the received echo
            echo = ser.read(ser.in_waiting).decode()
            final_time = time.perf_counter()

            # Calculate speed
            speed = calculate_speed(init_time, final_time, len(echo))
            print(f"Received echo: {echo}, transmission speed: {speed} bits/sec")

        # Wait before resending data - adjust this sleep time if needed
        time.sleep(2)

except KeyboardInterrupt:  # Stop the loop when Ctrl+C is pressed
    print("Interrupted! Stopping transmission.")

finally:
    # Close the serial port
    if ser:
        ser.close()