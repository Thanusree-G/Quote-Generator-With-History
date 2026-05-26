from flask import Flask, render_template
import requests
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect('quotes.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT
)
''')
conn.close()

@app.route('/')
def home():

    # Fetch random quote
    response = requests.get('https://api.quotable.io/random', verify=False)
    data = response.json()

    quote = data['content']

    # Save quote to database
    conn = sqlite3.connect('quotes.db')
    conn.execute('INSERT INTO quotes (quote) VALUES (?)', (quote,))
    conn.commit()

    # Fetch history
    history = conn.execute('SELECT * FROM quotes').fetchall()
    conn.close()

    return render_template('index.html', quote=quote, history=history)

if __name__ == '__main__':
    app.run(debug=True)