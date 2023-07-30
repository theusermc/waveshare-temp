import subprocess
import time

def get_cpu_temperature():
    try:
        output = subprocess.check_output(['vcgencmd', 'measure_temp']).decode('utf-8')
        temperature_celsius = float(output.split('=')[1].split('\'')[0])
        temperature_fahrenheit = (temperature_celsius * 9/5) + 32
        return temperature_celsius, temperature_fahrenheit
    except subprocess.CalledProcessError:
        return None, None

if __name__ == "__main__":
    while True:
        celsius, fahrenheit = get_cpu_temperature()
        if celsius is not None and fahrenheit is not None:
            print(f"CPU Temperature: {celsius:.2f} °C / {fahrenheit:.2f} °F")
            print("")
            
        else:
            print("Failed to read CPU temperature.")
        
        time.sleep(2)
