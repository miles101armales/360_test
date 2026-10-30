#TODO: мини апп дашборд HTML+JS+CSS

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse

from app.security import require_admin
from app.services.statistics import get_statistics
from app.settings import BASE_DIR


app = FastAPI(title="Дашборд")


@app.get("/")
async def dashboard() -> FileResponse:
	return FileResponse(
		BASE_DIR / "app" / "static" / "index.html",
		media_type="text/html"
	)


@app.get("/api/stats")
async def read_statistics(is_admin: bool = Depends(require_admin)) -> dict:
	if is_admin:
		return await get_statistics()