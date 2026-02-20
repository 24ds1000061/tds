from fastapi import FastAPI, Response, Request
app = FastAPI()

def get_email_response():
    return Response(content="24ds1000061@ds.study.iitm.ac.in", media_type="text/plain")

@app.get("/")
async def read_root(request: Request):
    return get_email_response()

@app.get("/email")
async def read_email(request: Request):
    return get_email_response()

@app.get("/24ds1000061@ds.study.iitm.ac.in")
async def read_email_path(request: Request):
    return get_email_response()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
