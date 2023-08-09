# Wine catalog backend
Fastapi project for Wine catalog web application (Fastapi + Node.js)  
## [Link to site](https://wine-catalog-et56.onrender.com)    
Frontend repository [here](https://github.com/Catalog-of-wines) 

### 1. Api is available at (AWS EC2): 
https://wine-catalog.pp.ua/docs

### 2. How to run locally with Docker:
- in command line in your IDE
```
git clone https://github.com/inrock1/wine_catalog_backend
```
- copy .env file in the project folder. (the file can be obtained from the backend developer)
```
docker build -t wine_backend .
docker run -d -p 8000:8000 wine_backend
```
- project will be available at http://localhost:8000/docs
- after usage stop docker container
```
docker stop <CONTAINER ID>
```
