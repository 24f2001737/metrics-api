from fastapi import FastAPI, Query, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time

EMAIL = "24f2001737@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-eo4q5n.example.com"

app = FastAPI()


@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    origin = request.headers.get("origin")

    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        response = Response(status_code=204)

        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET"
            response.headers["Access-Control-Allow-Headers"] = "*"

        return response

    # Handle normal requests
    response = await call_next(request)

    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = origin

    return response


class HeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        process_time = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        return response


app.add_middleware(HeaderMiddleware)


@app.get("/stats")
async def stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
