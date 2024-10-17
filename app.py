from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Отримуємо дані про курси валют
    response = requests.get("https://free.ratesdb.com/v1/rates?from=EUR")
    
    # Перевірка статусу відповіді
    if response.status_code != 200:
        return f"Не вдалося отримати дані про курси валют. Статус-код: {response.status_code}"

    data = response.json()['data']
    
    # Курси валют
    rates = data['rates']
    
    # Припустимо, що зміна курсу - це випадкове число від -0.05 до 0.05
    changes = {currency: round(rates[currency] * 0.01, 4) for currency in rates}

    # Передаємо базову валюту, курси, зміни курсів і дату в шаблон
    return render_template('index.html', base_currency=data['from'], rates=rates, changes=changes, current_date=data['date'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
