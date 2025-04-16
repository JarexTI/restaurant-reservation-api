from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.reservation import Reservation


def is_reservation_conflicting(
    db: Session,
    table_id: int,
    reservation_time: datetime,
    duration_minutes: int
):
    # Сделаем reservation_time наивным
    reservation_time = reservation_time.replace(tzinfo=None)
    new_end_time = reservation_time + timedelta(minutes=duration_minutes)

    reservations = db.query(Reservation).filter(
        Reservation.table_id == table_id
    ).all()

    for existing in reservations:
        existing_start = existing.reservation_time
        existing_end = existing_start + timedelta(
            minutes=int(existing.duration_minutes)
        )

        if existing_start < new_end_time and existing_end > reservation_time:
            return True

    return False
