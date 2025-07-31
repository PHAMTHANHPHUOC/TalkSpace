@echo off
echo Installing Voice Chat Dependencies...
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing SpeechRecognition...
pip install SpeechRecognition==3.10.0

echo Installing PyAudio...
pip install pipwin
pipwin install pyaudio

echo.
echo Installation completed!
echo.
echo To test the voice chat:
echo 1. Start the Django server: python manage.py runserver
echo 2. Start the Vue.js frontend: npm run dev
echo 3. Navigate to: http://localhost:3000/voice-chat
echo.
pause 