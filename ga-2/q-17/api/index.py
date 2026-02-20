from fastapi import FastAPI, Response
app = FastAPI()
@app.get("/")
def read_root():
    return Response(content="24ds1000061@ds.study.iitm.ac.in", media_type="text/plain")
@app.get("/api")
def read_api():
    return Response(content="24ds1000061@ds.study.iitm.ac.in", media_type="text/plain")
