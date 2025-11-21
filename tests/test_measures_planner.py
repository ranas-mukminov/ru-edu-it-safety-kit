from ru_edu_it_safety_kit.generators.measures_planner import MeasuresPlanner
from ru_edu_it_safety_kit.models.school_profile import Building, IspConnection, SchoolProfile, SchoolType


def test_measures_planner_basic():
    profile = SchoolProfile(
        name="Test School",
        type=SchoolType.SCHOOL,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="Main", is_hq=True)],
    )

    plan = MeasuresPlanner.plan(profile)

    assert "technical" in plan
    assert "organizational" in plan

    # Check for mandatory measures
    assert any("DNS-фильтрацию" in m for m in plan["technical"])
    assert any("логирование" in m.lower() for m in plan["technical"])
    assert any("AUP" in m for m in plan["organizational"])


def test_measures_planner_college_specific():
    profile = SchoolProfile(
        name="Test College",
        type=SchoolType.COLLEGE,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="Main", is_hq=True)],
    )

    plan = MeasuresPlanner.plan(profile)
    assert any("BYOD" in m for m in plan["organizational"])


def test_measures_planner_multi_building():
    profile = SchoolProfile(
        name="Test Multi",
        type=SchoolType.SCHOOL,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="Main", is_hq=True), Building(name="Branch", is_hq=False)],
    )

    plan = MeasuresPlanner.plan(profile)
    assert any("VPN" in m for m in plan["technical"])
