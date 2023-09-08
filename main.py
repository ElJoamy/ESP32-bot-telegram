import telebot
import requests
import os
import speech_recognition as sr
from pydub import AudioSegment
import os
from dotenv import load_dotenv
import csv
import datetime

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén el valor de las variables de entorno
TOKEN = os.getenv("TOKEN")
ESP32_IP = os.getenv("ESP32_IP")
ESP32_PORT = os.getenv("ESP32_PORT")
# Carpeta para guardar archivos de voz
REPORTS_FOLDER = os.getenv("REPORTS_FOLDER")
# Carpeta para guardar registros CSV
VOICE_FOLDER = os.getenv("VOICE_FOLDER")

# Combina la IP y el puerto para formar la URL completa
ESP32_URL = f"http://{ESP32_IP}:{ESP32_PORT}"

# Inicializa el reconocimiento de voz
recognizer = sr.Recognizer()

# Configura el bot de Telegram
bot = telebot.TeleBot(TOKEN)


# Crear la carpeta "voices" si no existe
if not os.path.exists(VOICE_FOLDER):
    os.makedirs(VOICE_FOLDER)

# Crear la carpeta "reports" si no existe
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

# Función para registrar eventos en un archivo CSV
def log_event(user_name, user_id, message, timestamp):
    with open(os.path.join(REPORTS_FOLDER, 'registro.csv'), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, user_name, user_id, message])

# Función para manejar los mensajes entrantes
@bot.message_handler(func=lambda message: True)
def handle(messages):
    global CHAT_ID

    for msg in messages:
        chat_id = msg.chat.id
        user_name = msg.from_user.first_name
        user_id = msg.from_user.id
        command = msg.text
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_event(user_name, user_id, command, timestamp)

        if command == '/start':
            bot.send_message(chat_id, '¡Hola! Soy tu bot de control de LED. Envía /encender para encender el LED, /apagar para apagarlo, /parpadear para hacer parpadear el LED o /alto para detener el parpadeo.')
            CHAT_ID = chat_id
        elif command == '/encender':
            response = requests.get(ESP32_URL + '/encender')
            bot.send_message(chat_id, 'LED encendido.' if response.status_code == 200 else 'Error al encender el LED.')
        elif command == '/apagar':
            response = requests.get(ESP32_URL + '/apagar')
            bot.send_message(chat_id, 'LED apagado.' if response.status_code == 200 else 'Error al apagar el LED.')
        elif command == '/parpadear':
            response = requests.get(ESP32_URL + '/parpadear')
            bot.send_message(chat_id, 'LED parpadeando.' if response.status_code == 200 else 'Error al iniciar el parpadeo del LED.')
        elif command == '/alto':
            response = requests.get(ESP32_URL + '/alto')
            bot.send_message(chat_id, 'Parpadeo del LED detenido.' if response.status_code == 200 else 'Error al detener el parpadeo del LED.')

@bot.message_handler(content_types=['voice'])
@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    global CHAT_ID

    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Descargar el archivo de audio en la carpeta "voices"
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    
    # Guardar el archivo de audio localmente como OGG en la carpeta "voices"
    audio_filename = os.path.join(VOICE_FOLDER, f'{file_id}.ogg')
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(audio_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk:
                    f.write(chunk)

    # Convertir el archivo de audio de OGG a WAV
    audio = AudioSegment.from_ogg(audio_filename)
    audio.export(os.path.join(VOICE_FOLDER, 'audio.wav'), format='wav')

    # Reconocimiento de voz en el archivo WAV
    with sr.AudioFile(os.path.join(VOICE_FOLDER, 'audio.wav')) as source:
        audio_data = recognizer.record(source)

    try:
        # Utiliza Google Web Speech API para transcribir el audio
        text = recognizer.recognize_google(audio_data, language="es-ES")

        # Comprueba si la palabra "encender" está en el texto reconocido
        if "encender" in text.lower():
            response = requests.get(ESP32_URL + '/encender')
            bot.send_message(chat_id, 'LED encendido.' if response.status_code == 200 else 'Error al encender el LED.')
        elif "apagar" in text.lower():
            response = requests.get(ESP32_URL + '/apagar')
            bot.send_message(chat_id, 'LED apagado.' if response.status_code == 200 else 'Error al apagar el LED.')
        elif "parpadear" in text.lower():
            response = requests.get(ESP32_URL + '/parpadear')
            bot.send_message(chat_id, 'LED parpadeando.' if response.status_code == 200 else 'Error al iniciar el parpadeo del LED.')
        elif "alto" in text.lower():
            response = requests.get(ESP32_URL + '/alto')
            bot.send_message(chat_id, 'Parpadeo del LED detenido.' if response.status_code == 200 else 'Error al detener el parpadeo del LED.')
        else:
            bot.send_message(chat_id, 'No se detectó la palabra "encender" en el audio.')

        log_event(user_name, user_id, text, timestamp)

    except sr.UnknownValueError:
        bot.send_message(chat_id, 'No se pudo reconocer el audio.')
    except sr.RequestError as e:
        bot.send_message(chat_id, f'Error en la solicitud al servicio de reconocimiento de voz: {e}')

# Asignar el manejador de actualización al bot
bot.set_update_listener(handle)

print('Bot iniciado a las:', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

bot.polling()
