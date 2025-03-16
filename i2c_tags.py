import smbus
import time

# Set up I2C (use 1 for modern Raspberry Pi models)
bus = smbus.SMBus(1)

# Possible I2C addresses of the ST25DV16K
ST25DV_ADDRESSES = [0x2D, 0x53, 0x57]

# Define register to read (example: read chip ID)
REGISTER_ID = 0x00

# Function to read from a register
def read_register(address, register):
    try:
        data = bus.read_byte_data(address, register)
        return data
    except Exception as e:
        print(f"Error reading from register {register} at address {hex(address)}: {e}")
        return None

# Function to test communication with a list of addresses
def test_addresses():
    for address in ST25DV_ADDRESSES:
        print(f"Trying address {hex(address)}...")
        id_value = read_register(address, REGISTER_ID)
        if id_value is not None:
            print(f"Successfully read from address {hex(address)}: 0x{id_value:X}")
            return address  # Return the address that works
    print("Failed to read from any address.")
    return None

# Example usage
if __name__ == "__main__":
    print("Starting ST25DV16K communication...")
    working_address = test_addresses()

    if working_address:
        print(f"Found ST25DV16K at address {hex(working_address)}")
    else:
        print("No device found.")

    # You can add additional operations here once you've found the working address
    time.sleep(2)
