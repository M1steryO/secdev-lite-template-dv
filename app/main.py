
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from .models import LoginRequest
from .db import query, query_one

app = FastAPI(title="secdev-seed-s06-s08")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def index(request: Request, msg: str | None = None):
    # XSS: намеренно рендерим message без экранирования через шаблон (см. index.html)
    return templates.TemplateResponse("index.html", {"request": request, "message": msg or "Hello!"})

@app.get("/echo", response_class=HTMLResponse)
def echo(request: Request, msg: str | None = None):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"message": msg or "Hello!"}
    )

@app.get("/search")
def search(q: str | None = None):
    if q:
        # S06: параметризованный LIKE вместо подстановки строки (защита от SQLi в search)
        sql = "SELECT id, name, description FROM items WHERE name LIKE ?"
        params = [f"%{q}%"]
    else:
        sql = "SELECT id, name, description FROM items LIMIT 10"
        params: list[Any] = []
    items = query(sql, params)
    return JSONResponse(content={"items": items})

@app.post("/login")
def login(payload: LoginRequest):
    """
    S06: убрали конкатенацию в SQL и перешли на параметризованный запрос,
    чтобы закрыть обход авторизации через SQL-инъекцию.
    """
    sql = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    row = query_one(sql, [payload.username, payload.password])
    if not row:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # фиктивный токен (для учебного шаблона этого достаточно)
    return {"status": "ok", "user": row["username"], "token": "dummy"}
