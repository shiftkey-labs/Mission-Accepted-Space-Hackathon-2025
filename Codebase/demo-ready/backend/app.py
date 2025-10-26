import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.ice_extent import router as ice_extent_router
from api.route_prediction import router as route_prediction_router

API_PREFIX = os.getenv("API_PREFIX", "/api")
app = FastAPI(title="NASA Ice Backend", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(ice_extent_router, prefix=API_PREFIX)
app.include_router(route_prediction_router, prefix=API_PREFIX)

# CORS: allow local dev frontends by default
allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_host_port() -> tuple[str, int]:
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port_str = os.getenv("BACKEND_PORT", "5001")
    try:
        port = int(port_str)
    except ValueError as exc:
        raise RuntimeError(f"Invalid BACKEND_PORT '{port_str}' – must be an integer.") from exc
    return host, port


if __name__ == "__main__":
    import uvicorn

    host, port = _get_host_port()
    uvicorn.run("app:app", host=host, port=port, reload=True)
