import subprocess
import time
import os
import logging
import epd2in13_V3
from PIL import Image, ImageDraw, ImageFont

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
    logging.critical("have you prayed today?")

    epd = epd2in13_V3.EPD()
    logging.info("init and clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font24 = ImageFont.truetype(os.path.join(picdir, 'trebuc.ttf'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'trebuc.ttf'), 18)

    logging.info("Displaying CPU temperature...")

    # Create initial image buffer and draw the static content
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    while True:
        celsius, fahrenheit = get_cpu_temperature()

        # Update the temperature values only
        draw.rectangle((0, 0, 250, 122), fill=255)  # Clear previous content
        draw.text((10, 10), "CPU Temperature:", font=font24, fill=0)
        if celsius is not None and fahrenheit is not None:
            draw.text((10, 40), f"{celsius:.2f} °C", font=font24, fill=0)
            draw.text((10, 70), f"{fahrenheit:.2f} °F", font=font24, fill=0)
            print(f"current temps: {celsius:.2f} °C / {fahrenheit:.2f} °F")
        else:
            draw.text((10, 40), "get cpu temperature failure", font=font24, fill=0)
            logging.error("CPU temperature get failure")
            logging.error("if this persists, do something lmao")

        # Display the partially updated image (rotated by 180 degrees)
        rotated_image = image.rotate(180)
        epd.displayPartial(epd.getbuffer(rotated_image))

        time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
