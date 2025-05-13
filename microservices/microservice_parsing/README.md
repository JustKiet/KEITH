# Getting Started

## Run Dockerfile

```bash
mdocker build -t microservice_parsing .

docker run -it -p 6091:6091 --rm microservice_parsing
```

## API Documentation

For API Documentation, refer to `/docs` endpoint.

# NOTE: For compiling torch dependencies with cpu support only.

```bash
pip-compile --extra-index-url https://download.pytorch.org/whl/cpu requirements.in
```
