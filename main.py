from server.application_builder import ApplicationBuilder
from starlette.staticfiles import StaticFiles

app = ApplicationBuilder().build()
app.mount("/", StaticFiles(directory="client/build", html=True), name="static")

if __name__ == '__main__':
    import uvicorn as uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
