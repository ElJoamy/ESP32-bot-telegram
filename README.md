# 🤖 Bot de Telegram para Control de Comandos por Wi-Fi en ESP32

## 📋 Descripción del Proyecto
Este proyecto se centra en el uso de un bot de Telegram para controlar un ESP32 a través de Wi-Fi. Puede utilizarse para controlar dispositivos IoT, como robots 🤖, sistemas de domótica 🏠, entre otros. Este proyecto se considera un dispositivo IoT, ya que permite el control desde cualquier parte del mundo 🌎, siempre que haya acceso a Internet 📡.

## 📦 Requisitos
Para utilizar este proyecto, necesitarás:

* Un módulo ESP32 🛠️.
* Una cuenta de Telegram 📱.
* Un bot de Telegram 🤖.
* Un LED (para probar el funcionamiento) 💡.
* Una resistencia de 330 ohmios (para probar el funcionamiento) ⚡.
* Un cable micro USB (para programar el ESP32) 🌐.
* 3 jumpers (para probar el funcionamiento) 🧰.

## 🛠️ Instalación

### Configuración del Entorno

1. Descarga e instala el [IDE de Arduino](https://www.arduino.cc/en/software) si aún no lo tienes instalado.

2. Opcionalmente, puedes utilizar un IDE de programación de texto, como [Visual Studio Code](https://code.visualstudio.com/download), para editar el código de manera más eficiente.

3. Abre el IDE de Arduino y configura las preferencias para agregar el soporte del ESP32. Ve a "Archivo" > "Preferencias" y en "URLs Adicionales de Gestor de Tarjetas", agrega el siguiente enlace:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```

4. Ve a "Herramientas" > "Placa" > "Gestor de Tarjetas" y busca "ESP32". Instala el soporte para el ESP32.

5. Desde el menú "Sketch", selecciona "Incluir Biblioteca" > "Administrar Bibliotecas" e instala las siguientes bibliotecas:
   - ArduinoJson (de Benoit Blanchon)
   - AsyncTCP (de dvarrel)
   - ESPAsyncTCP (de dvarell)
   - ESPAsyncWebSrv (de dvarrel)

6. Si deseas ejecutar el bot de Telegram en Python, asegúrate de tener Python instalado. Luego, instala las dependencias del proyecto ejecutando el siguiente comando en la terminal, en la carpeta del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

7. También necesitarás instalar FFmpeg para procesar archivos de audio. Puedes descargarlo desde los siguientes enlaces según tu sistema operativo:
   - [Windows](https://ffmpeg.org/download.html#build-windows) ⚙️
   - [Linux](https://ffmpeg.org/download.html#build-linux) 🐧
   - [macOS](https://ffmpeg.org/download.html#build-mac) 🍏
   
   Asegúrate de agregar la carpeta bin de FFmpeg a tus variables de entorno para que el bot pueda usarlo.
   Puedes seguir los pasos graficos [aqui](/media/ffmpeg)

### Armado del Circuito 🧩

El circuito para pruebas es bastante simple y consta de un LED 💡 y una resistencia de 330 ohmios ⚡. Puedes ver un esquema del circuito en la plataforma [wokwi](https://wokwi.com/).

### Código en el Arduino IDE 💻

1. Descarga el repositorio del proyecto:
   ```bash
   git clone https://github.com/ElJoamy/ESP32-bot-telegram.git
   ```

2. Abre el archivo [wifiTele.ino](/wifiTele.ino) en el IDE de Arduino.

3. Modifica las siguientes líneas del código con la información de tu red Wi-Fi:
   ```c
   const char *ssid = "EL NOMBRE DE LA RED DE WIFI A LA QUE TE CONECTARÁS";
   const char *password = "LA CONTRASEÑA DE LA RED DE WIFI A LA QUE TE CONECTARÁS";

   AsyncWebServer server(80);
   ```
   Donde:
   - `ssid` es el nombre de la red Wi-Fi a la que te conectarás.
   - `password` es la contraseña de la red Wi-Fi.
   - `server` es el puerto al que se conectará el ESP32 (por defecto, 80).

4. Luego de modificar estas líneas, sube el código al ESP32.

### Código en Visual Studio Code 🐍

1. Descarga el repositorio del proyecto:
   ```bash
   git clone https://github.com/ElJoamy/ESP32-bot-telegram.git
   ```

2. Abre el archivo [.env](.env.example) y configura los siguientes valores:

   ```
   TOKEN=token de tu bot
   ESP32_IP=http://IP DE TU ESP32
   ESP32_PORT=80
   REPORTS_FOLDER=reports
   VOICE_FOLDER=voices
   ```
   Donde:
   - `TOKEN` es el token de tu bot de Telegram 🤖 (si no sabes cómo crear un bot de Telegram, sigue los siguientes pasos [aquí](/pasos/CreateBotTelegram.md)).
   - `ESP32_IP` es la IP de tu ESP32 (se mostrará cuando ejecutes el código del Arduino en la consola; debes copiarla y pegarla en este campo).
   - `ESP32_PORT` es el puerto al que se conectará el ESP32 (por defecto, 80).
   - `REPORTS_FOLDER` es la carpeta donde se guardarán los informes de los comandos 📊.
   - `VOICE_FOLDER` es la carpeta donde se guardarán los archivos de audio enviados al bot 🎙️.

3. Ejecuta el código en Visual Studio Code:

   ```bash 
   python main.py
   ```

## 🚀 Uso

Accede a tu bot de Telegram y prueba los comandos descritos en el archivo [comandos.md](/pasos/comandos.md) ⌨️.

¡Disfruta del control remoto de tu ESP32 a través de Telegram! 🎉

## Mejoras Futuras 🚀

El desarrollo de este proyecto está en constante evolución, y hay muchas mejoras emocionantes que se pueden implementar en el futuro para enriquecer su funcionalidad. Algunas de las mejoras planificadas incluyen:

1. **Integración de Sensores** 🌡️: Agregar soporte para una variedad de sensores (por ejemplo, temperatura, humedad, movimiento, luz) para que el bot pueda proporcionar información en tiempo real sobre el entorno controlado.

2. **Control de Múltiples Dispositivos** 🤖: Extender la capacidad del bot para controlar varios dispositivos o sistemas IoT al mismo tiempo. Esto puede incluir la gestión de una variedad de actuadores y sensores.

3. **Notificaciones Push** 📩: Implementar notificaciones push para informar a los usuarios sobre eventos importantes o cambios en el estado de los dispositivos controlados.

4. **Seguridad Mejorada** 🔒: Reforzar la seguridad del sistema, incluida la autenticación de usuarios y la encriptación de las comunicaciones para garantizar la privacidad y la integridad de los datos.

## Contribuciones 🤝

¡Las contribuciones de la comunidad son bienvenidas y ayudan a mejorar este proyecto! Si deseas contribuir, aquí hay algunas formas en las que puedes hacerlo:

1. **Documentación Mejorada** 📚: Continuar mejorando la documentación del proyecto, incluyendo instrucciones detalladas para configurar el entorno, diagramas de circuitos y guías de uso.

2. **Mejoras en la Eficiencia del Código** ⚙️: Realizar revisiones de código para optimizar el rendimiento y la eficiencia del programa, identificando áreas que pueden requerir mejoras.

3. **Soporte Multilingüe** 🌍: Agregar soporte para varios idiomas para que el bot pueda interactuar con usuarios de todo el mundo.

4. **Pruebas y Depuración** 🐞: Contribuir con pruebas exhaustivas y depuración para garantizar que el proyecto sea robusto y libre de errores.

5. **Añadir Funcionalidades Adicionales** ➕: Introducir nuevas funcionalidades interesantes que mejoren la utilidad y versatilidad del bot.

## Licencia 📝

Este proyecto está bajo la Licencia MIT. Puedes encontrar más detalles en el archivo [LICENSE](LICENSE) del repositorio. La Licencia MIT es una licencia de código abierto que permite el uso, modificación y distribución del código con pocas restricciones.
