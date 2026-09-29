# Library Management API

A simple REST API for managing a library system built with Flask and SQLite.

## Features
- Book management
- Member management
- Loan system
- Due date tracking

## Technologies
- Python 3
- Flask
- SQLite
- RESTful API

## API Endpoints

### Books
| Method | Endpoint |
|--------|----------|
| GET | `/api/books` |
| POST | `/api/books` |
| PUT | `/api/books/<id>` |
| DELETE | `/api/books/<id>` |

### Loans
| Method | Endpoint |
|--------|----------|
| POST | `/api/loans` |
| PUT | `/api/loans/<id>/return` |

## How to Run

pip install -r requirements.txt
python app.py

## Author
Moein - github.com/mynnjfy31-hub
