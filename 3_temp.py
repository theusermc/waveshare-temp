import subprocess
import time
import sys
import os
import logging
import epd2in13_V3
from PIL import Image, ImageDraw, ImageFont

# Define the directory where the script and font file are located
picdir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(level=logging.DEBUG)

def get_cpu_temperature():
    try:
        output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
        temperature_celsius = float(output.split('=')[1].split('\'')[0])
        temperature_fahrenheit = (temperature_celsius * 9/5) + 32
        return temperature_celsius, temperature_fahrenheit
    except subprocess.CalledProcessError:
        return None, None

try:
    logging.info("epd2in13_V3 CPU Temperature")

    epd = epd2in13_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font24 = ImageFont.truetype(os.path.join(picdir, 'trebuc.ttf'), 24)

    logging.info("Displaying CPU temperature...")

    # Create image buffer for the static part
    static_image = Image.new('1', (epd.height, epd.width), 255)
    static_draw = ImageDraw.Draw(static_image)

    # Draw the static part (CPU Temperature label) only once
    static_draw.text((10, 10), "CPU Temperature:", font=font24, fill=0)
    epd.displayPartial(epd.getbuffer(static_image))

    while True:
        celsius, fahrenheit = get_cpu_temperature()

        # Create image buffer for the dynamic part
        dynamic_image = Image.new('1', (epd.height, epd.width), 255)
        dynamic_draw = ImageDraw.Draw(dynamic_image)

        # Clear the dynamic part of the image
        dynamic_draw.rectangle((10, 40, 250, 122), fill=255)

        if celsius is not None and fahrenheit is not None:
            dynamic_draw.text((10, 40), f"{celsius:.2f} °C", font=font24, fill=0)
            dynamic_draw.text((10, 70), f"{fahrenheit:.2f} °F", font=font24, fill=0)
        else:
            dynamic_draw.text((10, 40), "Failed to read CPU temperature.", font=font24, fill=0)

        # Combine static and dynamic parts of the image
        combined_image = Image.new('1', (epd.height, epd.width), 255)
        combined_image.paste(static_image, (0, 0))
        combined_image.paste(dynamic_image, (0, 0))

        # Display only the dynamic part of the image
        epd.displayPartial(epd.getbuffer(combined_image))
        time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
