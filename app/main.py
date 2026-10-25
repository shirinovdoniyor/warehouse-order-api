from fastapi import FastAPI

app = FastAPI(title="Warehouse Order API", version="0.1.0")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
