import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# parking_fee: valid and invalid vehicle
def test_vehicle_validation():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)

    assert parking_fee("bike", 60, False, False) == 10


# parking_fee: negative, free, and chargeable durations
def test_duration_branches():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)

    assert parking_fee("car", 30, False, False) == 0
    assert parking_fee("car", 31, False, False) == 30


# parking_fee: exact hours versus partial hours
def test_hour_rounding_branches():
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("car", 61, False, False) == 60


# parking_fee: EV condition and truck exception
def test_ev_branches():
    assert parking_fee("car", 60, True, False) == 15
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("truck", 60, True, False) == 60


# parking_fee: lost-ticket condition
def test_lost_ticket_branches():
    assert parking_fee("bike", 60, False, False) == 10
    assert parking_fee("bike", 60, False, True) == 210


# find_slot: full, disabled, truck, and ordinary slot
def test_find_slot_branches():
    assert find_slot("car", 0, False) == "full"
    assert find_slot("car", 2, True) == "ground floor"
    assert find_slot("truck", 2, False) == "basement"
    assert find_slot("car", 2, False) == "any floor"


# monthly_pass: bike, car, unsupported vehicle
def test_monthly_pass_vehicle_branches():
    assert monthly_pass("bike", False) == 500
    assert monthly_pass("car", False) == 1500

    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)


# monthly_pass: resident and non-resident branches
def test_monthly_pass_resident_branches():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("car", True) == 1200
