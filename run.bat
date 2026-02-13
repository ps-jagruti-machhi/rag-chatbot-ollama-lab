@echo off
echo. | python -m streamlit run 3_chatbot.py
timeout /t 3 /nobreak >nul
start http://localhost:8502/