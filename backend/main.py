from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="Wedding Tap Tap", root_path="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://game.chanelandnicholas.com"],
    allow_methods=["*"],
)

taps = {"bride": 0, "groom": 0}


@app.get("/health")
async def health() -> None:
    """Healthcheck."""
    return


@app.post("/bride")
async def bride() -> None:
    """Taps for bride."""
    taps["bride"] += 1


@app.post("/groom")
async def groom() -> None:
    """Taps for groom."""
    taps["groom"] += 1


@app.post("/reset")
async def reset() -> None:
    """Reset tap count."""
    taps["bride"] = 0
    taps["groom"] = 0


@app.get("/taps")
async def get_taps() -> dict[str, int]:
    """Get current tap count."""
    return taps
