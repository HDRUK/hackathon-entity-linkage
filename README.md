Welcome to the HDRUK-ELIXIR hackathon project for HDRUK Gateway entity linkages

### Run service

#### Backend

```
cd app
docker-compose up --build
```

example:

```
curl --location 'http://localhost:8000/find' \
--header 'Content-Type: application/json' \
--data '{
    "doi": "10.1038/s41541-024-00898-w"
}'
```

#### Frontend

```
cd fe
npx remix vite:build
npx remix-serve build/server/index.js
```

<div style="border: 2px solid black;">
<p align="center">
  <img src="https://github.com/user-attachments/assets/cef39f2a-97f6-49f7-99c5-73f6a81313a4" width="30%" />
  <img src="https://github.com/user-attachments/assets/d6d3f221-8813-4f0f-b86c-01dfc09968f6" width="30%" />
  <img src="https://github.com/user-attachments/assets/0e715d76-62f1-478c-8016-f3289c8a7adf" width="30%" />
</p>
</div>

We have provide a [Demo](https://github.com/HDRUK/hackathon-entity-linkage/blob/main/Python%20Demo.ipynb) ([HMTL render](https://hdruk.github.io/hackathon-entity-linkage/demo)) jupyter notebook here to get you started

Data to get you started can be found [here](https://github.com/HDRUK/hackathon-entity-linkage/tree/main/data)

What we aim to achieve:

- Find ways to create indirect linkages between gateway entities (datasets, publications, tools)
- Find additional linkages to external sources
