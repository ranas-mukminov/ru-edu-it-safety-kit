import sys
from pathlib import Path

import click

from ru_edu_it_safety_kit.generators.leaflet_generator import LeafletGenerator
from ru_edu_it_safety_kit.generators.measures_planner import MeasuresPlanner
from ru_edu_it_safety_kit.validators.config_validator import ConfigValidator


@click.group()
def main():
    """ru-edu-it-safety-kit CLI tool."""
    pass


@main.command()
@click.argument("profile_path", type=click.Path(exists=True))
def validate(profile_path):
    """Validate a school profile YAML file."""
    try:
        profile = ConfigValidator.load_profile(profile_path)
        click.secho(f"✅ Profile '{profile.name}' is valid.", fg="green")

        warnings = ConfigValidator.validate_logic(profile)
        for w in warnings:
            click.secho(f"⚠️  Warning: {w}", fg="yellow")

    except Exception as e:
        click.secho(f"❌ Validation failed: {e}", fg="red")
        sys.exit(1)


@main.command()
@click.argument("profile_path", type=click.Path(exists=True))
def plan(profile_path):
    """Generate a safety measures plan."""
    try:
        profile = ConfigValidator.load_profile(profile_path)
        measures = MeasuresPlanner.plan(profile)

        click.secho(f"\n🛡️  Safety Plan for: {profile.name}\n", fg="blue", bold=True)

        click.secho("Technical Measures:", fg="cyan")
        for m in measures["technical"]:
            click.echo(f" - {m}")

        click.echo("")
        click.secho("Organizational Measures:", fg="magenta")
        for m in measures["organizational"]:
            click.echo(f" - {m}")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        sys.exit(1)


@main.command()
@click.argument("profile_path", type=click.Path(exists=True))
@click.option("--output-dir", "-o", type=click.Path(), default=".", help="Directory to save leaflets")
def generate_leaflets(profile_path, output_dir):
    """Generate leaflets for parents, students, and teachers."""
    try:
        profile = ConfigValidator.load_profile(profile_path)
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        leaflets = {
            "parents.md": LeafletGenerator.generate_for_parents(profile),
            "students.md": LeafletGenerator.generate_for_students(profile),
            "teachers.md": LeafletGenerator.generate_for_teachers(profile),
        }

        for filename, content in leaflets.items():
            file_path = out_path / filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            click.secho(f"📄 Generated: {file_path}", fg="green")

    except Exception as e:
        click.secho(f"❌ Error: {e}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    main()
