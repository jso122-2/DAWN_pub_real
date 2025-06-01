# File Path: /src/mycelium/nutrient_logger.py

import os
import json
import csv
from datetime import datetime

# Paths for logging
LOG_JSON_PATH = "logs/mycelium_logs/nutrient_log.json"
LOG_CSV_PATH = "logs/mycelium_logs/nutrient_flow.csv"

# Function to log bloom data into a JSON file
def log_bloom_to_nutrient(bloom):
    os.makedirs(os.path.dirname(LOG_JSON_PATH), exist_ok=True)
    try:
        # Check if the JSON file exists
        if os.path.exists(LOG_JSON_PATH):
            with open(LOG_JSON_PATH, "r") as f:
                nutrient_data = json.load(f)
        else:
            nutrient_data = {}

        # Update the nutrient data with the bloom's lineage depth
        lineage = str(bloom.get("lineage_depth", 0))
        nutrient_data[lineage] = nutrient_data.get(lineage, 0) + 1

        # Write the updated data back to the JSON file
        with open(LOG_JSON_PATH, "w") as f:
            json.dump(nutrient_data, f, indent=2)

        print(f"[Mycelium] 🌱 Logged lineage {lineage} explicitly to nutrient grid.")

    except Exception as e:
        print(f"[Mycelium] ⚠️ Logging explicitly failed: {e}")

# Function to classify nutrient levels based on flow strength
def classify_nutrient_level(value):
    if value < 0.3:
        return "low"
    elif value < 0.7:
        return "medium"
    else:
        return "high"

# Function to log nutrient flow to a CSV file
def log_nutrient_flow(bloom, flow_strength: float):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("logs", "mycelium_logs", today)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "nutrient_flow.csv")
    file_exists = os.path.isfile(path)

    # Open the CSV file in append mode
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writerow([
                "timestamp", "bloom_id", "seed", "mood", "entropy_score",
                "bloom_factor", "lineage_depth", "flow_strength", "pressure_zone"
            ])

        # Determine the pressure zone based on flow strength
        pressure_zone = classify_nutrient_level(flow_strength)

        # Write the bloom data and nutrient flow details to the CSV
        writer.writerow([
            datetime.now().isoformat(),
            bloom["seed_id"],
            bloom["seed_id"],
            bloom["mood"],
            bloom["entropy_score"],
            bloom["bloom_factor"],
            bloom["lineage_depth"],
            flow_strength,
            pressure_zone
        ])

        print(f"[MyceliumLog] 🌱 Nutrient explicitly logged: {bloom['seed_id']}, strength: {flow_strength:.2f}")


# Function to adjust the soot level of a given seed
def adjust_seed_soot(seed_id, soot_amount):
    """
    Adjusts the soot level of a given seed.
    This function might update the seed's nutrient properties or log the adjustment.
    """
    # Example: Adjusting soot amount for the seed (this could involve updating a database or an in-memory structure)
    print(f"Adjusting soot level for seed {seed_id} by {soot_amount}.")
    
    # Assuming we have an in-memory structure like a dictionary to store seed information
    seeds = {}  # Replace this with actual storage logic

    if seed_id not in seeds:
        seeds[seed_id] = {"soot_level": 0}  # Initialize if the seed doesn't exist in the structure
    
    # Adjust the soot level (add the soot amount to the existing level)
    seeds[seed_id]["soot_level"] += soot_amount

    # You can also log the adjustment to a file or database, if needed
    log_soot_adjustment(seed_id, soot_amount)

    return True  # Return a status or any required result

# Function to log the soot adjustment to a log file
def log_soot_adjustment(seed_id, soot_amount):
    # Log the adjustment to a file
    log_path = "logs/mycelium_logs/soot_adjustments.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", newline="", encoding="utf-8") as log_file:
        writer = csv.writer(log_file)
        writer.writerow([datetime.now().isoformat(), seed_id, soot_amount])

    print(f"[MyceliumLog] 🌱 Soot level adjustment logged for seed {seed_id}: {soot_amount}")
