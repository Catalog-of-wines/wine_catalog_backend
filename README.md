# wine_catalog_backend
Fastapi project for Wine catalog web application (Fastapi + Node.js)

### 1. How to run with docker:
- in command line in your IDE
```
git clone https://github.com/inrock1/wine_catalog_backend
```
- copy .env file in the project folder. (the file can be obtained from the backend developer)
```
docker build -t wine_backend .
docker run -d -p 8000:8000 wine_backend
```
- project will be available at http://localhost:8000/

<!--
### 2. How to run in windows:
- install python on your system, if you don't have it 
https://www.python.org/downloads/
- in command line in your IDE
```
git clone https://github.com/inrock1/wine_catalog_backend
```
- copy .env file in the project folder. (the file can be obtained from the backend developer)
```
pip install -r requirements.txt
uvicorn main:app --reload
```
- project will be available at http://127.0.0.1:8000
-->
