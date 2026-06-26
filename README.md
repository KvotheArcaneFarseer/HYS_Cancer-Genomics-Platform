# HYS_Cancer-Genomics-Platform


## How to Run the project locally
 ### Prerequisites
 - Python 3.11+
 - pip

 ### 1. Clone the repo
```bash
git clone https://github.com/KvotheArcaneFarseer/HYS_Cancer-Genomics-Platform.git
cd HYS_Cancer-Genomics-Platform
```

## Run Backend first
### Windows
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API will be running at http://localhost:8000

### Mac/Linux
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Run Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
App will open at http://localhost:8501
