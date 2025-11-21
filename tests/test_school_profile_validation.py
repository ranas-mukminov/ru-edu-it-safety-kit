from ru_edu_it_safety_kit.models.school_profile import (
    Building,
    IspConnection,
    NetworkRole,
    SchoolProfile,
    SchoolType,
    VlanConfig,
)
from ru_edu_it_safety_kit.validators.config_validator import ConfigValidator


def test_valid_school_profile():
    profile = SchoolProfile(
        name="Test School",
        type=SchoolType.SCHOOL,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[
            Building(
                name="Main",
                is_hq=True,
                vlans=[VlanConfig(id=10, name="admin", role=NetworkRole.ADMIN, subnet="10.0.0.0/24")],
            )
        ],
    )
    assert profile.name == "Test School"
    assert not profile.is_multi_building


def test_multi_building_logic():
    profile = SchoolProfile(
        name="Test College",
        type=SchoolType.COLLEGE,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="HQ", is_hq=True), Building(name="Branch", is_hq=False)],
    )
    assert profile.is_multi_building

    warnings = ConfigValidator.validate_logic(profile)
    assert len(warnings) == 0


def test_missing_hq_warning():
    profile = SchoolProfile(
        name="Test College",
        type=SchoolType.COLLEGE,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="B1", is_hq=False), Building(name="B2", is_hq=False)],
    )
    warnings = ConfigValidator.validate_logic(profile)
    assert any("no building is marked as 'is_hq'" in w for w in warnings)


def test_duplicate_vlan_warning():
    profile = SchoolProfile(
        name="Test School",
        type=SchoolType.SCHOOL,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[
            Building(
                name="Main",
                is_hq=True,
                vlans=[
                    VlanConfig(id=10, name="admin", role=NetworkRole.ADMIN, subnet="10.0.0.0/24"),
                    VlanConfig(id=10, name="admin_dup", role=NetworkRole.ADMIN, subnet="10.0.1.0/24"),
                ],
            )
        ],
    )
    warnings = ConfigValidator.validate_logic(profile)
    assert any("Duplicate VLAN ID 10" in w for w in warnings)
