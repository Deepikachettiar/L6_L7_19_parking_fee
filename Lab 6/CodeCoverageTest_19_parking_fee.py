import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


def test_parking_fee_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_parking_fee_exactly_30_minutes():
    assert parking_fee("bike", 30, False, False) == 0


def test_parking_fee_hourly_rounding():
    assert parking_fee("car", 31, False, False) == 30
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("car", 61, False, False) == 60


def test_parking_fee_all_vehicle_rates():
    assert parking_fee("bike", 61, False, False) == 20
    assert parking_fee("truck", 61, False, False) == 120


def test_parking_fee_ev_discount():
    assert parking_fee("car", 60, True, False) == 15
    assert parking_fee("bike", 60, True, False) == 5
    assert parking_fee("truck", 60, True, False) == 60


def test_parking_fee_lost_ticket():
    assert parking_fee("car", 60, False, True) == 230
    assert parking_fee("car", 20, False, True) == 200


def test_parking_fee_ev_and_lost_ticket():
    assert parking_fee("car", 60, True, True) == 215


def test_parking_fee_invalid_vehicle():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_parking_fee_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_find_slot_full():
    assert find_slot("car", 0, False) == "full"
    assert find_slot("bike", -1, True) == "full"


def test_find_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_find_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_find_slot_any_floor():
    assert find_slot("bike", 5, False) == "any floor"


def test_monthly_pass_bike():
    assert monthly_pass("bike", False) == 500


def test_monthly_pass_car():
    assert monthly_pass("car", False) == 1500


def test_monthly_pass_resident_discount():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("car", True) == 1200


def test_monthly_pass_invalid_vehicle():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
