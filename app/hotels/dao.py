from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, location: str, date_from: date, date_to: date):

    async with async_session_maker() as session:
        bookings_for_selected_dates = (
            select(Bookings)
            .filter(
                or_(
                    and_(
                        Bookings.date_from < date_from, Bookings.date_to > date_from
                    ),
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_to < date_to,
                    ),
                )
            )
            .subquery("filtered_bookings")
        )

        hotels_rooms_left = (
            select(
                (
                    Hotels.rooms_quantity
                    - func.count(bookings_for_selected_dates.c.room_id)
                ).label("rooms_left"),
                Rooms.hotel_id,
            )
            .select_from(Hotels)
            .outerjoin(Rooms, Rooms.hotel_id)
        )
