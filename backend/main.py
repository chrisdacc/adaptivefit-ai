from fastapi import FastAPI

app = FastAPI(
    title="AdaptiveFit AI",
    description="Intelligent adaptive strength training engine",
    version="0.1.0",
)


@app.get("/", tags=["System"])
def root():
    return {
        "name": "AdaptiveFit AI",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy"}
