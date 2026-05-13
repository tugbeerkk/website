from flask import Flask, render_template, request, make_response
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    # İlk giriş tarihini kontrol et (Cookie kullanarak)
    start_date_str = request.cookies.get('start_date')
    days_elapsed = None
    
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            today = datetime.now()
            # Gün farkını hesapla
            diff = today - start_date
            days_elapsed = diff.days + 1 # İlk gün 1. gün sayılır
        except ValueError:
            days_elapsed = None

    return render_template('index.html', days_elapsed=days_elapsed)

@app.route('/start')
def start():
    # Kullanıcı butona bastığında bugünün tarihini cookie'ye kaydet
    response = make_response("<script>window.location.href='/';</script>")
    now = datetime.now().isoformat()
    # Cookie 10 yıl geçerli olsun (kalıcı olması için)
    response.set_cookie('start_date', now, max_age=60*60*24*365*10)
    return response

@app.route('/reset')
def reset():
    # Cookie'yi silerek sayacı sıfırla
    response = make_response("<script>window.location.href='/';</script>")
    response.delete_cookie('start_date')
    return response

if __name__ == '__main__':
    # AI Studio için 3000 portunda çalışması gerekir
    # Yerel bilgisayarında 'flask run' veya 'python app.py' ile çalıştırabilirsin
    app.run(host='0.0.0.0', port=3000, debug=True)
