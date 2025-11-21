from ru_edu_it_safety_kit.generators.leaflet_generator import LeafletGenerator
from ru_edu_it_safety_kit.models.school_profile import Building, IspConnection, SchoolProfile, SchoolType


def test_leaflet_generation():
    profile = SchoolProfile(
        name="Test School",
        type=SchoolType.SCHOOL,
        isps=[IspConnection(name="ISP1", speed_mbps=100)],
        buildings=[Building(name="Main", is_hq=True)],
    )

    parents = LeafletGenerator.generate_for_parents(profile)
    students = LeafletGenerator.generate_for_students(profile)
    teachers = LeafletGenerator.generate_for_teachers(profile)

    assert "Test School" in parents
    assert "Памятка для родителей" in parents

    assert "Test School" in students
    assert "безопасный интернет" in students

    assert "Test School" in teachers
    assert "Пароли" in teachers
