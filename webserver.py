from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return 'Discord Bot is running!'

def run():
    port = int(os.getenv('PORT', 8080))  # Render sets PORT env var
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run, daemon=True)
    t.start()