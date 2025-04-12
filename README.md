# Django Question Generator Project

This project is a Django-based web application for automatic question generation and evaluation.

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone git@github.com:hniht3002/KLTN.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations (if needed)

```bash
python manage.py migrate
```

### 5. Start the Django development server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

---

## 📌 Available Endpoints

### 1. `/`
- **Method:** GET  
- **Description:** Homepage

### 2. `/generate-questions`
- **Method:** POST  
- **Description:** Form to generate question 

### 3. `/evaluate`
- **Method:** POST  
- **Description:** Evaluates the quality of the system
