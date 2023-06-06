# wine_catalog_backend
Fastapi project for Wine catalog web application (Fastapi + Node.js)



### How to run in windows:
1. install python on your system, if you don't have it 
https://www.python.org/downloads/
2. in command line in your IDE
```
git clone https://github.com/inrock1/wine_catalog_backend
pip install -r requirements.txt
uvicorn main:app --reload
```
3. project will be available at http://127.0.0.1:8000

### How to run with docker:
1. in command line in your IDE
```
git clone https://github.com/inrock1/wine_catalog_backend
docker build -t wine_backend .
docker run -d -p 8000:8000 wine_backend

```
2. project will be available at http://localhost:8000/