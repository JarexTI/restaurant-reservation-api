from fastapi import FastAPI

from app.routers import reservation, table


def get_app() -> FastAPI:
    app = FastAPI(
        title='Restaurant Table Booking API',
        version='1.0.0'
    )

    @app.get("/")
    def read_root():
        return {"message": "API is working!"}

    app.include_router(
        table.router,
        prefix='/tables',
        tags=['Tables']
    )
    app.include_router(
        reservation.router,
        prefix='/reservations',
        tags=['Reservation']
    )

    return app


app = get_app()
