from fastapi import FastAPI, Response
app = FastAPI()

@app.get("/")
def read_root():
    return Response(content="24ds1000061@ds.study.iitm.ac.in", media_type="text/plain")

@app.get("/index.html")
def read_index():
    return Response(content="24ds1000061@ds.study.iitm.ac.in", media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
