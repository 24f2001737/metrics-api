from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time

EMAIL = "24f2001737@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-eo4q5n.example.com"

app = FastAPI()


class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
        return response


app.add_middleware(HeaderMiddleware)


@app.options("/stats")
async def options_stats(request: Request):
    response = Response(status_code=204)

    if request.headers.get("origin") == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Access-Control-Allow-Methods"] = "GET"
        response.headers["Access-Control-Allow-Headers"] = "*"

    return response


@app.get("/stats")
async def stats(request: Request, values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]

    response = JSONResponse(
        {
            "email": EMAIL,
            "count": len(nums),
            "sum": sum(nums),
            "min": min(nums),
            "max": max(nums),
            "mean": sum(nums) / len(nums),
        }
    )

    if request.headers.get("origin") == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN

    return response
