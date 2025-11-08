"""Application entrypoint exposed as `main:app` for ASGI servers."""

from app.main import app as _app

# Re-export FastAPI instance so `fastapi dev main:app` works.
app = _app


def main() -> None:
    """Run a local dev server if this module is executed directly."""
    try:
        import uvicorn
    except ImportError as exc:
        raise RuntimeError("uvicorn must be installed to run main.py directly") from exc

    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
