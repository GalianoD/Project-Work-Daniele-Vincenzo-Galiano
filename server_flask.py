from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secretkey'  
CORS(app)  

# Lista per memorizzare le prenotazioni
bookings = []

# Dati demo
USERNAME = 'mario_rossi'
PASSWORD = 'password'
DATE= datetime.now().date().strftime('%Y-%m-%d')
TIME = '20:00'

# Inserimento prenotazione
@app.route('/bookings', methods=['POST'])
def create_booking():
    booking = request.get_json()

    if booking['date'] == DATE and booking['time'] == TIME:
        return jsonify({"error": "Tutti i tavoli sono occupati per l'orario selezionato"}), 400
    
    booking_id = len(bookings)  
    booking['id'] = booking_id
    bookings.append(booking)
    print("Prenotazione ricevuta, prenotazioni attuali:\n", bookings)
    return jsonify(booking), 201

@app.route('/bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings), 200

# Aggiornamento prenotazione
@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = request.get_json()
    if 0 <= booking_id < len(bookings):
        updated_booking = bookings[booking_id]
        updated_booking.update(booking)  
        return jsonify(updated_booking), 200
    else:
        return jsonify({"error": "Prenotazione non trovata"}), 404

# Cancellazione prenotazione
@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    if 0 <= booking_id < len(bookings):
        bookings.pop(booking_id)
        return '', 204
    else:
        return jsonify({"error": "Prenotazione non trovata"}), 404

# Inserimento dati login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == USERNAME and password == PASSWORD:
        session['username'] = username
        return jsonify({"message": "Login effettuato con successo!"}), 200
    else:
        return jsonify({"error": "Nome utente o password errati"}), 401

@app.route('/session', methods=['GET'])
def get_session():
    if 'username' in session:
        return jsonify({"username": session['username']}), 200
    else:
        return jsonify({"message": "Non autenticato"}), 401

if __name__ == '__main__':
    app.run(debug=True)
