from fastapi import FastAPI

from app.api import setup_api

swagger_ui_parameters = {
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "tryItOutEnabled": True,
}

app = FastAPI(
    title="Travel planer",
    description="Travel planer api's documentation",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters=swagger_ui_parameters,
)

setup_api(app)


@app.get("/health")
async def health():
    return {"status": "ok"}
