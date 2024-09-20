# Quick Start

Language identification microservice powered by the FastText language detection model, providing fast and accurate recognition of over 170 languages.

```sh
git clone git@github.com:vhidvz/language-identification.git
cd language-identification && docker-compose up -d
```

Endpoints are fully documented using OpenAPI Specification 3 (OAS3) at:

- ReDoc: <http://localhost:8000/redoc>
- Swagger: <http://localhost:8000/docs>

## Documentation

To generate the documentation for the python model, execute the following command:

```sh
pdoc --output-dir docs model.py
```
