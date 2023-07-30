import subprocess
import time
import sys
import os
import logging
import epd2in13_V3
from PIL import Image, ImageDraw, ImageFont

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

    while True:
        image = Image.new('1', (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        celsius, fahrenheit = get_cpu_temperature()

        if celsius is not None and fahrenheit is not None:
            draw.text((10, 10), f"CPU Temperature:", font=font24, fill=0)
            draw.text((10, 40), f"{celsius:.2f} °C", font=font24, fill=0)
            draw.text((10, 70), f"{fahrenheit:.2f} °F", font=font24, fill=0)
        else:
            draw.text((10, 10), "Failed to read CPU temperature.", font=font24, fill=0)

        epd.display(epd.getbuffer(image))
        time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
