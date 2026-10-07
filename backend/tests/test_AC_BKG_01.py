# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Booking, Slot
from tests.conftest import AUTH


def test_TC_BKG_01_1_booking_success(client, make_slot, db):
    # Given
    slot = make_slot(start="09:00", remaining=1)

    # When
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then
    assert res.status_code == 201
    payload = res.json()
    assert payload.get("queue_no") in (None, "")
    assert db.query(Slot).get(slot.id).remaining == 0
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1


def test_TC_BKG_01_2_single_booking_when_capacity_is_one(client, make_slot, db):
    # Given
    slot = make_slot(start="09:00", remaining=1)

    # When
    first = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)
    second = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then
    assert first.status_code == 201
    assert second.status_code == 409
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 1
    assert db.query(Slot).get(slot.id).remaining == 0


def test_TC_BKG_01_3_full_slot_handling(client, make_slot, db):
    # Given
    slot = make_slot(start="09:00", remaining=0, capacity=0)

    # When
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then
    assert res.status_code == 409
    assert "เต็ม" in res.json().get("detail", "").lower()
    assert db.query(Booking).filter_by(slot_id=slot.id).count() == 0
    assert db.query(Slot).get(slot.id).remaining == 0
