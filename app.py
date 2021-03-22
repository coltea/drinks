from fastapi import FastAPI
import json
import uvicorn

app = FastAPI()


@app.get("/")
async def read_own_items():
    return 'Coltea'


if __name__ == '__main__':
    uvicorn.run(app='run:app', host="127.0.0.1", port=8000, reload=True, debug=True)
