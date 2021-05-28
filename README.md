# openapi3-diff-analyser

## Requirements

- Python 3.9+
- Consult application dependencies at `./app/requirements.txt`

## API Rest Server on Docker

Default Image Parameters, running on port *5000*

```bash
docker build -t openapi3-diff-analyser:latest .
docker run -p 5000:5000 openapi3-diff-analyser:latest
```

Parameterizing Image

```bash
# Changing default server port for the image
docker build --build-arg SERVER_PORT=8080 -t openapi3-diff-analyser:latest .

# Changing server port for the image exec
docker run -p 8083:8083 -e SERVER_PORT=8083 openapi3-diff-analyser:latest
```

## Running Locally

Depending on the local Python installation, the exec command can be `py` or `python`

### Installing Dependencies

```bash
pip install -r ./app/requirements.txt
# OR
py -m pip install -r ./app/requirements.txt
```

To generate a new requirements.txt file, use the command `py -m pip freeze > ./app/requirements.txt`

### CLI Options

**USAGE** - CLI Program:  
`py main.py -b <base_file> -t <target_file> [-o <output_dir>]`

**USAGE** - REST API Server:  
`py main.py --server=5000`

Options:

- **--server=[]**: Starts up a REST API Server listening on port 5000 by default or a given port number.
- **-b, --base**: Path to the OpenAPI3 specification base file for comparison.
- -rt=[], --report_type=[]: 
  - FILE: creates error and full reports on the output_dir
  - ERROR: returns the error report to the console
  - FULL: returns the full report to the console
- **-t, --target**: Path to the OpenAPI3 specification target file for comparison.
- **-o, --output_dir**: Optional directory for writing comparison reports. Defaults to './target'.
- **-h, --help**: prints help doc
