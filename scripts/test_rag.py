import sys
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from agents import generate_care_card

# Test with a plant in the vector store
plant_name = "Aloe Vera"
print(f"Testing RAG system with: {plant_name}\n")
print("=" * 70)

care_card = generate_care_card(plant_name)

print("\n" + "=" * 70)
print("GENERATED CARE CARD:")
print("=" * 70)
print(f"Latin Name: {care_card['latin_name']}")
print(f"Family: {care_card['plant_family']}")
print(f"Common Names: {', '.join(care_card['common_names'])}")
print(f"Watering: {care_card['watering_schedule']}")
print(f"Light: {care_card['lighting_conditions']}")
print("\nRAG system working!")