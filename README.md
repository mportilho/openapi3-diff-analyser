# openapi3-diff-analyser

## Requirements

- Python 3.9+
- Consult application dependencies at `./app/requirements.txt`

## API Rest Server on Docker

### Default Image Parameters, running on port *5000*

```bash
docker build -t openapi3-diff-analyser:latest .
docker run -p 5000:5000 openapi3-diff-analyser:latest
```

### Parameterizing Image

```bash
# Changing default server port for the image
docker build --build-arg SERVER_PORT=8080 -t openapi3-diff-analyser:latest .

# Changing server port for the image exec
docker run -p 8083:8083 -e SERVER_PORT=8083 openapi3-diff-analyser:latest
```

### Comparison URI

- POST http://localhost:5000/openapi-diff/files/
- Multipart/form-data
  - base_spec=@C:\path\to\resources\swagger_channels_apis.yaml
  - target_spec=@C:\path\to\resources\api-canais-atendimento.yaml

#### CURL Example

```bash
curl --request POST \
  --url http://localhost:5000/openapi-diff/files/ \
  --header 'Content-Type: multipart/form-data; boundary=---011000010111000001101001' \
  --form 'base_spec=@C:\openapi3-diff-analyser\resources\specs_obk\swagger_channels_apis.yaml' \
  --form 'target_spec=@C:\openapi3-diff-analyser\resources\specs_api\api-canais-atendimento.yaml'
```

#### Javascript Axios Example

```javascript
import axios from "axios";

const form = new FormData();
form.append("base_spec", "C:\\openapi3-diff-analyser\\resources\\specs_obk\\swagger_channels_apis.yaml");
form.append("target_spec", "C:\\openapi3-diff-analyser\\resources\\specs_api\\api-canais-atendimento.yaml");

const options = {
  method: 'POST',
  url: 'http://localhost:8083/openapi-diff/files/',
  headers: {
    'Content-Type': 'multipart/form-data; boundary=---011000010111000001101001'
  },
  data: '[form]'
};

axios.request(options).then(function (response) {
  console.log(response.data);
}).catch(function (error) {
  console.error(error);
});
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
