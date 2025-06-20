from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from test app!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_main:app", host="127.0.0.1", port=8000, reload=True)
