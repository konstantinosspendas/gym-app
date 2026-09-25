# Καταγραφή Προπονήσεων

Το GymLogger Lite είναι μια απλή εφαρμογή για καταγραφή προπονήσεων, ασκήσεων και επιδόσεων.

Η εφαρμογή δημιουργήθηκε με FastAPI, SQLAlchemy και SQLite.

## Λειτουργίες

- Δημιουργία, προβολή, αλλαγή και διαγραφή προπονήσεων
- Δημιουργία, προβολή, αλλαγή και διαγραφή ασκήσεων
- Καταγραφή επιδόσεων με sets, reps και βάρος
- Βασικά στατιστικά προπόνησης
- In-memory cache για τα στατιστικά
- Βασικό validation δεδομένων
- Basic API tests

## Βάση δεδομένων

Η βάση περιλαμβάνει τρεις βασικούς πίνακες:

- προπονησεις
- ασκησεις
- επιδόσεις

## Εγκατάσταση

### Linux / macOS

Δημιουργία virtual environment:

python3 -m venv venv

Ενεργοποίηση:

source venv/bin/activate

### Windows

Δημιουργία virtual environment:

python -m venv venv

Ενεργοποίηση:

venv\Scripts\activate

## Εγκατάσταση dependencies

pip install -r requirements.txt

## Εκτέλεση εφαρμογής

uvicorn app.main:app --reload

Το API είναι διαθέσιμο στο:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### Workouts

- GET /workouts/
- GET /workouts/{id}
- POST /workouts/
- PUT /workouts/{id}
- DELETE /workouts/{id}

### Exercises

- GET /exercises/
- GET /exercises/{id}
- POST /exercises/
- PUT /exercises/{id}
- DELETE /exercises/{id}

### Performances

- GET /performances/
- POST /performances/

### Stats

- GET /stats/

## Tests

Για εκτέλεση των tests:

python -m pytest testakia -v
