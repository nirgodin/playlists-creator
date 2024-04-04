import uvicorn as uvicorn
from starlette.staticfiles import StaticFiles

from server.application_builder import ApplicationBuilder

app = ApplicationBuilder().build()

if __name__ == '__main__':
    app.mount("/", StaticFiles(directory="client/build", html=True), name="static")
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
