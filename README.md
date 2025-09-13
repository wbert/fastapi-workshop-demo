# Project Setup

## Create virtual environment
For Windows: 
```
py -m venv venv
.\venv\Scripts\Activate
```

For MacOS/Linux: 
```
python -m venv venv
source venv/bin/activate
```

## Install dependencies
under venv
```
pip install -r requirements.txt
```

## Running the FastAPI
```
uvicorn app.main:app --restart
```
