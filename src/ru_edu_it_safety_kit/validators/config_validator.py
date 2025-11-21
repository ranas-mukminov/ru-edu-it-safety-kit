from pathlib import Path
from typing import List, Union

import yaml
from pydantic import ValidationError

from ru_edu_it_safety_kit.models.school_profile import SchoolProfile


class ConfigValidator:
    @staticmethod
    def load_profile(path: Union[str, Path]) -> SchoolProfile:
        """
        Loads and validates a SchoolProfile from a YAML file.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Profile file not found: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}") from e

        try:
            profile = SchoolProfile(**data)
            return profile
        except ValidationError as e:
            raise ValueError(f"Profile validation failed: {e}") from e

    @staticmethod
    def validate_logic(profile: SchoolProfile) -> List[str]:
        """
        Performs additional logical checks not covered by Pydantic.
        Returns a list of warning messages.
        """
        warnings = []

        # Check if at least one building is marked as HQ in multi-building setup
        if profile.is_multi_building:
            hq_found = any(b.is_hq for b in profile.buildings)
            if not hq_found:
                warnings.append("Multi-building setup detected, but no building is marked as 'is_hq'.")

        # Check for duplicate VLAN IDs across the whole school
        vlan_ids = []
        for b in profile.buildings:
            for v in b.vlans:
                if v.id in vlan_ids:
                    warnings.append(
                        f"Duplicate VLAN ID {v.id} found in building '{b.name}'. "
                        "VLAN IDs should ideally be unique or consistent."
                    )
                vlan_ids.append(v.id)

        return warnings
