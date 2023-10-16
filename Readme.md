# MCLAPS


## Runing the API locally

1. create a .env file inside app with the following:
```
OPEN-AI-API-KEY=your_api_key
BUBBLE-DATA-API-URL=
BUBBLE-DATA-API-TOKEN=
BUBBLE-VERSION=test
```

2. run with uvicorn
```shell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. create a new pricing simulation request

```shell
curl "http://localhost:8000/simulations/pricing?runs=1&age=20&country_of_residence=spain&income_level=20000"
```