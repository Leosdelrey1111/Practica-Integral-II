import machine
import time
import dht
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C

# Configurar el sensor DHT11
dht_pin = Pin(2)  # GPIO2 o D4 en ESP8266/ESP32
sensor = dht.DHT11(dht_pin)

# Configurar el buzzer (utilizando PWM para controlar la frecuencia del sonido)
buzzer = PWM(Pin(4, Pin.OUT))  # GPIO4 o D2
buzzer.duty(0)  # Asegúrate de que el buzzer esté apagado al inicio

# Configurar el LED RGB
led_rojo = Pin(14, Pin.OUT)  # GPIO14 o D5
led_verde = Pin(12, Pin.OUT)  # GPIO12 o D6
led_azul = Pin(13, Pin.OUT)  # GPIO13 o D7

# Configurar la pantalla OLED
i2c = I2C(scl=Pin(5), sda=Pin(16))  # GPIO5 y GPIO16 en ESP8266/ESP32
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

# Variables de control
limite_temp = 40  # Umbral de temperatura
tiempo_lectura = 1  # Tiempo entre lecturas (segundos)

# Frecuencias de las notas (Hz)
NOTA_DO = 261  # Do
NOTA_RE = 294  # Re
NOTA_MI = 329  # Mi
NOTA_FA = 349  # Fa
NOTA_SOL = 392  # Sol
NOTA_LA = 440  # La
NOTA_SI = 494  # Si

# Melodía armoniosa (frecuencias y duraciones)
melodia = [
    (NOTA_DO, 400),  # Do
    (NOTA_RE, 400),  # Re
    (NOTA_MI, 400),  # Mi
    (NOTA_FA, 400),  # Fa
    (NOTA_SOL, 400), # Sol
    (NOTA_LA, 400),  # La
    (NOTA_SI, 400),  # Si
    (NOTA_LA, 400),  # La
    (NOTA_SOL, 400), # Sol
    (NOTA_MI, 400),  # Mi
    (NOTA_RE, 400),  # Re
    (NOTA_DO, 400)   # Do
]

# Función para actualizar la pantalla OLED
def actualizar_oled(temperatura, humedad, estado):
    oled.fill(0)
    oled.text("Temp: {} C".format(temperatura), 0, 0)
    oled.text("Hum: {} %".format(humedad), 0, 10)
    oled.text("Estado: {}".format(estado), 0, 20)
    oled.show()

# Función para reproducir una melodía armoniosa
def melodia_buzzer():
    for frecuencia, duracion in melodia:
        buzzer.freq(frecuencia)  # Establecer frecuencia
        buzzer.duty(12)  # Encender el buzzer a un volumen medio
        time.sleep_ms(duracion)  # Esperar la duración de la nota
        buzzer.duty(0)  # Apagar el buzzer
        time.sleep(0.2)  # Pequeña pausa entre notas

# Función para controlar el LED RGB y el buzzer según la temperatura
def controlar_alertas(temperatura, limite_temp):
    estado = "Normal"
    if temperatura > limite_temp:
        # Cambia el LED RGB a rojo
        led_rojo.on()
        led_verde.off()
        led_azul.off()
        # Reproduce la melodía armoniosa
        melodia_buzzer()
        estado = "Alerta!"
    else:
        # Cambia el LED RGB a verde
        led_rojo.off()
        led_verde.on()
        led_azul.off()
    return estado

# Función para manejar las lecturas del sensor y controlar el sistema
def manejar_lectura():
    try:
        # Leer la temperatura y la humedad del sensor DHT11
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()

        # Controlar el LED y el buzzer
        estado = controlar_alertas(temperatura, limite_temp)

        # Mostrar los valores en la pantalla OLED
        actualizar_oled(temperatura, humedad, estado)

    except OSError as e:
        print('Error al leer el sensor DHT11:', e)
        oled.fill(0)
        oled.text("Error de lectura", 0, 0)
        oled.show()

# Bucle principal
while True:
    manejar_lectura()
    time.sleep(tiempo_lectura)