import logging
import gpiod
import subprocess

logging.basicConfig(level=logging.INFO)

def find_gpio_by_name(name):
    """Search for a GPIO by name using gpiofind binary."""
    try:
        ret, result = subprocess.getstatusoutput('gpioinfo ' + name)
        if ret == 0:
                parts = result.strip().split()
                if len(parts) > 2:
                        return parts[0], int(parts[1])
    except subprocess.CalledProcessError:
        return None

def list_available_gpios():
    """List all available GPIOs using gpioinfo."""
    try:
        result = subprocess.run(["gpioinfo"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        gpio_list = []
        for line in lines:
            parts = line.split(":")
            if len(parts) > 1:
                tokens = parts[1].strip().split()
                if tokens:
                    gpio_name = tokens[0]
                    gpio_list.append(gpio_name)
        return gpio_list
    except subprocess.CalledProcessError:
        return []

class GPIOController:
    def __init__(self, name, chip, number):
        """Initialize a GPIO controller for a single supply."""
        #self.chip = gpiod.Chip(chip_path)
        #self.line = self.chip.get_line(line_offset)
        self.gpio_name = name
        self.gpio_chip = chip
        self.gpio_number = str(number)
        self.gpio_set = 'gpioset -t0 -c ' + self.gpio_chip + ' ' + self.gpio_number
        self.gpio_get = 'gpioget -a -c ' + self.gpio_chip + ' ' + self.gpio_number
        
    def set_high(self):
        """Turn on the supply (set GPIO high)."""
        if self.gpio_set:
            try:
                ret, result = subprocess.getstatusoutput(self.gpio_set + '=1')
                if ret == 0:
                    logging.debug(f"{self.gpio_name} turned ON.")
            except:
                logging.error(f"GPIO {self.gpio_name} failed.")
        else:
            logging.error(f"GPIO {self.gpio_name} not found.")

    def set_low(self):
        """Turn on the supply (set GPIO high)."""
        if self.gpio_set:
            try:
                ret, result = subprocess.getstatusoutput(self.gpio_set + '=0')
                if ret == 0:
                    logging.debug(f"{self.gpio_name} turned OFF.")
            except:
                logging.error(f"GPIO {self.gpio_name} failed.")
        else:
            logging.error(f"GPIO {self.gpio_name} not found.")

    def get(self):
        """Check the status of the supply."""
        if self.gpio_get:
            try:
                ret, result = subprocess.getstatusoutput(self.gpio_get)
                if ret == 0:
                    token = result.partition("=")[2]
                    if token == "active":
                        value = 1
                    else:
                        value = 0
                    return value
            except:
                logging.error(f"GPIO {self.gpio_name} failed.")
        else:
            logging.error(f"GPIO {self.gpio_number} not found.")



# Create separate instances for each available GPIO
#available_gpios = list_available_gpios()
