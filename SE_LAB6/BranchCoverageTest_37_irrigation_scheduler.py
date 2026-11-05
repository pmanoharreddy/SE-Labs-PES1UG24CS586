import pytest
from irrigation_scheduler import should_irrigate, water_volume, schedule


# ---------- should_irrigate: every decision True and False ----------
def test_wet_soil_no_irrigation():                 # moisture >= 60 True
    assert should_irrigate(70, 0, "seedling") is False

def test_moisture_boundary_60():
    assert should_irrigate(60, 0, "vegetative") is False

def test_heavy_rain_no_irrigation():               # rain >= 10 True
    assert should_irrigate(30, 10, "vegetative") is False

def test_seedling_dry_irrigates():                 # seedling, moisture < 45 True
    assert should_irrigate(44, 0, "seedling") is True

def test_seedling_moderate_no_irrigation():        # seedling, moisture < 45 False
    assert should_irrigate(45, 0, "seedling") is False

def test_flowering_dry_irrigates():                # flowering, moisture < 55 True
    assert should_irrigate(54, 0, "flowering") is True

def test_flowering_boundary_no_irrigation():       # flowering, moisture < 55 False
    assert should_irrigate(55, 0, "flowering") is False

def test_light_rain_other_stage():                 # rain >= 5 True
    assert should_irrigate(30, 5, "vegetative") is False

def test_other_stage_very_dry():                   # rain >= 5 False, moisture < 40 True
    assert should_irrigate(39, 4, "vegetative") is True

def test_other_stage_not_dry_enough():             # moisture < 40 False
    assert should_irrigate(40, 0, "vegetative") is False


# ---------- water_volume: every branch ----------
@pytest.mark.parametrize("stage,temp,expected", [
    ("seedling", 20, 20),      # base seedling, normal temp
    ("flowering", 20, 50),     # flowering
    ("vegetative", 20, 40),    # else stage
    ("seedling", 36, 30),      # temp > 35
    ("seedling", 35, 20),      # boundary: not hot
    ("seedling", 9, 10),       # temp < 10
    ("seedling", 10, 20),      # boundary: not cold
])
def test_water_volume_branches(stage, temp, expected):
    assert water_volume(10, stage, temp) == expected

@pytest.mark.parametrize("area", [0, -5])
def test_invalid_area_raises(area):
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(area, "seedling", 20)


# ---------- schedule: loop, skip, budget break ----------
def test_schedule_empty_zones():                   # loop never entered
    assert schedule([], 100) == []

def test_schedule_all_zones_watered():
    zones = [("A", 10, 30, 0, "seedling", 20),
             ("B", 10, 30, 0, "vegetative", 20)]
    assert schedule(zones, 100) == ["A", "B"]

def test_schedule_skips_zone_not_needing_water():  # continue branch
    zones = [("A", 10, 80, 0, "seedling", 20),
             ("B", 10, 30, 0, "seedling", 20)]
    assert schedule(zones, 100) == ["B"]

def test_schedule_breaks_when_over_budget():       # break branch
    zones = [("A", 10, 30, 0, "seedling", 20),
             ("B", 10, 30, 0, "vegetative", 20),
             ("C", 1, 30, 0, "seedling", 20)]
    assert schedule(zones, 30) == ["A"]

def test_schedule_exact_budget_allowed():
    zones = [("A", 10, 30, 0, "seedling", 20)]
    assert schedule(zones, 20) == ["A"]
