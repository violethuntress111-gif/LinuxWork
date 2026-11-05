from fastapi import FastAPI
from app.api import books, categories

app = FastAPI(
    title="Bookstore API",
    description="API для управления каталогом книг и категорий",
    version="1.0.0",
)

app.include_router(categories.router)
app.include_router(books.router)


@app.get("/health", tags=["health"])
def health():
    """Проверка, что сервис жив"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.fastapi_app:app", host="127.0.0.1", port=8000, reload=True)