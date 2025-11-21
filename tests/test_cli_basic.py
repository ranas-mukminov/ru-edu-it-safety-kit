import pytest
from click.testing import CliRunner

from ru_edu_it_safety_kit.cli import generate_leaflets, plan, validate


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def sample_profile_path(tmp_path):
    p = tmp_path / "profile.yml"
    p.write_text(
        """
name: "Test CLI School"
type: school
isps:
  - name: "ISP1"
    speed_mbps: 100
buildings:
  - name: "Main"
    is_hq: true
    vlans:
      - id: 10
        name: "admin"
        role: admin
        subnet: "10.0.0.0/24"
    """,
        encoding="utf-8",
    )
    return str(p)


def test_cli_validate(runner, sample_profile_path):
    result = runner.invoke(validate, [sample_profile_path])
    assert result.exit_code == 0
    assert "valid" in result.output


def test_cli_plan(runner, sample_profile_path):
    result = runner.invoke(plan, [sample_profile_path])
    assert result.exit_code == 0
    assert "Safety Plan" in result.output
    assert "Technical Measures" in result.output


def test_cli_generate_leaflets(runner, sample_profile_path, tmp_path):
    out_dir = tmp_path / "out"
    result = runner.invoke(generate_leaflets, [sample_profile_path, "--output-dir", str(out_dir)])
    assert result.exit_code == 0
    assert (out_dir / "parents.md").exists()
    assert (out_dir / "students.md").exists()
    assert (out_dir / "teachers.md").exists()


def test_cli_invalid_file(runner):
    result = runner.invoke(validate, ["non_existent.yml"])
    assert result.exit_code != 0
    assert "does not exist" in result.output
