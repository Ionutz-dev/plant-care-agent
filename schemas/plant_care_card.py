from pydantic import BaseModel, Field
from typing import List


class PlantCareCard(BaseModel):
    """Structured plant care information."""

    latin_name: str = Field(description="Scientific/Latin name of the plant")
    common_names: List[str] = Field(description="List of common names for this plant")
    plant_family: str = Field(description="Botanical family the plant belongs to")
    native_region: str = Field(description="Geographic origin of the plant")

    outdoors: bool = Field(description="Whether plant can be grown outdoors")
    indoor_suitable: bool = Field(description="Whether plant is suitable for indoor growing")
    lighting_conditions: str = Field(description="Optimal light requirements")
    temperature_range: str = Field(description="Ideal temperature range")
    humidity_requirements: str = Field(description="Preferred humidity levels")

    watering_schedule: str = Field(description="How often and how much to water")
    soil_type: str = Field(description="Recommended soil composition")
    fertilization: str = Field(description="Fertilization needs and schedule")
    pruning_needs: str = Field(description="Pruning requirements and timing")

    growth_rate: str = Field(description="How fast the plant grows")
    mature_size: str = Field(description="Expected size when fully grown")
    toxicity: str = Field(description="Toxicity information for pets/humans")
    common_pests: List[str] = Field(description="Common pests that affect this plant")
    special_care_notes: str = Field(description="Any special care requirements or tips")