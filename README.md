# Sammy
Voice assistant for PC

### RU

Требуемые зависимости: 

pip install PyAudio (использование микрофона)

pip install pyttsx3 (синтез речи)

pip install SpeechRecognition (распознавание речи)

pip install fuzzywuzzy (нечёткое сравнение запросов)

Установленные голоса RHVoice (https://rhvoice.su/voices/)

## Необходимо указать микрофон

1. Запустить test_microphone.py и найти свой микрофон в списке
2. Sammy.py строка 127: после device_index = указать номер микрофона

