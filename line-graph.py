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
        return temperature_celsius
    except subprocess.CalledProcessError:
        return None

def draw_line_graph(image_draw, data_points, max_data_points):
    graph_width = 240
    graph_height = 100
    x_interval = graph_width // max_data_points

    # Shift the existing data points to make room for the new one
    data_points = data_points[-max_data_points:]

    # Draw the line graph
    for i in range(1, len(data_points)):
        x1 = (i - 1) * x_interval
        y1 = graph_height - int(data_points[i - 1])
        x2 = i * x_interval
        y2 = graph_height - int(data_points[i])
        image_draw.line([(x1, y1), (x2, y2)], fill=0, width=2)

    return data_points

try:
    logging.info("epd2in13_V3 CPU Temperature Line Graph")

    epd = epd2in13_V3.EPD()
    logging.info("init and clear")
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font24 = ImageFont.truetype(os.path.join(picdir, 'trebuc.ttf'), 24)

    logging.info("Displaying CPU Temperature Line Graph...")

    # Create initial image buffer
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)
    data_points = []

    # Set the maximum number of temperature data points to display on the graph
    max_data_points = 60  # Display the last 60 data points

    while True:
        celsius = get_cpu_temperature()

        # Update the temperature values
        draw.rectangle((10, 40, 250, 90), fill=255)  # Clear previous temperature values
        if celsius is not None:
            draw.text((10, 40), f"{celsius:.2f} °C", font=font24, fill=0)
            data_points.append(celsius)  # Add new temperature data point to the list
        else:
            draw.text((10, 40), "get cpu temperature failure", font=font24, fill=0)
            logging.error("CPU temperature get failure")
            logging.error("if this persists, do something lmao")

        # Update the line graph
        draw.rectangle((0, 120, 250, 220), fill=255)  # Clear previous graph
        data_points = draw_line_graph(draw, data_points, max_data_points)

        # Display the updated image
        epd.displayPartial(epd.getbuffer(image))

        time.sleep(2)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V3.epdconfig.module_exit()
    exit()
