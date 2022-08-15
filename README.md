# Cleanform
A simple form builder

## Tech Stack
### Backend - Django
### Frontend - Vue
### Database - Postgresql



# Setting up the project locally
### Prerequisites
1- Make sure postgresql is installed in your system
2- Create .env file in root of the project and copy the following code
```
VITE_API_BASE_URL=http://127.0.0.1:8000
DJANGO_SETTINGS_MODULE=cleanform.settings.development
```


## Backend
### Step 1. Setting up the virtualenv

```
# Linux/MacOS
python3 -m venv venv

# Windows (Command Prompt)
python -m venv venv
```

### Step 2. Activating virtual env
```
# Linux/MacOS
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate.bat
```
### Step 3. Setting up database for cleanform Backend

### Step 4. Installing the requirements
```
pip install -r requirements.txt
```
### Step 5. Running the db migrations
```
python3 manage.py migrate
```
### Step 6. Running the server
```
python3 manage.py runserver
```
### Step 7. Running the worker
```
celery -A cleanform worker -E -l INFO
```


## Frontend

### Step 1 Installing the dependencies
```
npm install
```

### Step 2 Starting the frontend server
```
npm run dev
```