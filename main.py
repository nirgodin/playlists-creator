import os

from server.application_builder import ApplicationBuilder
from starlette.staticfiles import StaticFiles

app = ApplicationBuilder().build()
app.mount("/", StaticFiles(directory="client/build", html=True), name="static")

if __name__ == '__main__':
    import uvicorn as uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
