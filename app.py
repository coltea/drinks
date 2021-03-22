from fastapi import FastAPI
import json
import uvicorn

app = FastAPI()


@app.get("/")
async def read_own_items():
    return '我爱落雨 -- ctj'


if __name__ == '__main__':
    uvicorn.run(app='run:app', host="0.0.0.0", port=80, reload=True, debug=True)
