# Circuito 4: Conexión WiFi y Publicación MQTT hacia Adafruit IO (ESP32)

## Descripción
Enlace IoT mediante la red virtual 'Wokwi-GUEST' hacia el broker MQTT 'io.adafruit.com', publicando periódicamente la temperatura y voltaje en Feeds de Adafruit IO.

## Instrucciones en Wokwi
1. Pega `sketch.ino` y `diagram.json`.
2. En `libraries.txt`, añade `Adafruit MQTT Library` y `DHT sensor library`.
3. Configura tus credenciales AIO_USERNAME y AIO_KEY en sketch.ino.
4. Presiona Play y verifica los datos en tu Dashboard de Adafruit IO.
