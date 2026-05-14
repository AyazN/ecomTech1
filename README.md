# ecom.tech intern repo

FastAPI service for uploading and analyzing student grades.  
Runs with Docker and includes basic tests.

## How to Run (Docker)

```bash
docker-compose up --build
```


## API URL

http://localhost:8000
### API Endpoints:
- POST /upload-grades

- GET /students/more-than-3-twos

- GET /students/less-than-5-twos

## Tests

Run in the main directory:
```bash
pytest
```
Tests endpoints and the input data validation 
