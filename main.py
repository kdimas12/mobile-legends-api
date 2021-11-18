from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def read_root():
  return {"status": "ok", "code": 200,
	"message": "success", "maintainers": "Dimas Kurniawan"}

@app.get("/data/")
def read_data():
  data = json.load(open('data/hero.json'))

  return {"status": "ok", "code": 200,
	"message": "success", "data": data}

@app.get("/data/{data_id}")
async def read_data_id(data_id):
  return {"status": "ok", "code": 200,
	"message": "success", "data": data_id}