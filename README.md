# Wine catalog backend
Fastapi project for Wine catalog web application (Fastapi + Node.js)  
(The project in development)
Frontend part [here](https://github.com/Catalog-of-wines) 
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
