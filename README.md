# openapi3-diff-analyser

## Requirements

- Python 3.9+
- Consult dependencies at `./app/requirements.txt`

To generate a new requirements.txt file, use the command `py -m pip freeze > ./app/requirements.txt`

## API Rest Server on Docker

Default Image Parameters, running on port *5000* 

```bash
docker build -t openapi3-diff-analyser:latest .
docker run -p 5000:5000 openapi3-diff-analyser:latest
```

Parameterized image

```bash
# Changing default server port for image building
docker build --build-arg SERVER_PORT=8080 -t openapi3-diff-analyser:latest .

# Changing server port for the image exec
docker run -p 8083:8083 -e SERVER_PORT=8083 openapi3-diff-analyser:latest
```

## Running Locally

**USAGE** - CLI Program:  
`py main.py -b <base_file> -t <target_file> [-o <output_dir>]`

**USAGE** - REST API Server:  
`py main.py --server=5000`

Options:  
- **--server=[]**: Starts up a REST API Server listening on port 5000 by default or a given port number.
- **-b, --base**: Path to the OpenAPI3 specification base file for comparison.
- **-t, --target**: Path to the OpenAPI3 specification target file for comparison.
- **-o, --output_dir**: Optional directory for writing comparison reports. Defaults to './target'. 
- **-h, --help**: prints help doc
