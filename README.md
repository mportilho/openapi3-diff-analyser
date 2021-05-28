# openapi3-diff-analyser

## Requirements

- Python 3.9+
- Consult dependencies at `./app/requirements.txt`

To generate a new requirements.txt file, use the command `py -m pip freeze > ./app/requirements.txt`

## Run on Docker

```bash
docker build -t openapi3-diff-analyser:latest .
docker run -p 5000:5000 openapi3-diff-analyser:latest
```

## Run Locally

```bash
py server.py
```

#### Running on Windows
- `pip install waitress`  
- `waitress-server --listen=*:8000 app:app`  
- `waitress-serve --listen=*:8000 myapp.wsgi:application`