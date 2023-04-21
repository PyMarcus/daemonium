from fastapi import FastAPI
from core import Settings
from api import api_router


settings = Settings()
app = FastAPI(title="Daemonium API",
                  version='0.0.1',
                  description="An API to manager ransomware")
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9999,
        log_level=True,
        reload=True
    )

