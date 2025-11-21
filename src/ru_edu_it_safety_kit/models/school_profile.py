from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class SchoolType(str, Enum):
    SCHOOL = "school"
    COLLEGE = "college"


class NetworkRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    GUEST = "guest"
    IOT = "iot"


class VlanConfig(BaseModel):
    id: int = Field(..., ge=2, le=4094, description="VLAN ID")
    name: str = Field(..., description="VLAN Name (e.g., 'students')")
    role: NetworkRole = Field(..., description="Associated role")
    subnet: str = Field(..., description="CIDR subnet (e.g., '10.10.20.0/24')")


class Building(BaseModel):
    name: str = Field(..., description="Building name or identifier")
    is_hq: bool = Field(False, description="Is this the main building?")
    vlans: List[VlanConfig] = Field(default_factory=list, description="VLANs present in this building")


class IspConnection(BaseModel):
    name: str = Field(..., description="ISP Name")
    speed_mbps: int = Field(..., description="Connection speed in Mbps")
    is_primary: bool = Field(True, description="Is this the primary link?")


class SchoolProfile(BaseModel):
    name: str = Field(..., description="Name of the educational institution")
    type: SchoolType = Field(..., description="Type: school or college")
    buildings: List[Building] = Field(..., min_length=1, description="List of buildings")
    isps: List[IspConnection] = Field(..., min_length=1, description="Internet connections")

    @property
    def is_multi_building(self) -> bool:
        return len(self.buildings) > 1
