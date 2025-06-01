from schema.scup_loop import calculate_SCUP
import csv
import os

output_file = "juliet_flowers/cluster_report/scup_validation_results.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Header
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["delta_vector", "pulse_pressure", "drift_variance", "SCUP"])

    # Sweep edge cases
    for delta in [0.0, 0.25, 0.5, 0.75, 1.0]:
        for pressure in [0.0, 0.5, 1.0, 1.5, 2.0]:
            for drift in [0.0, 0.25, 0.5, 0.75, 1.0]:
                scup = calculate_SCUP(delta, pressure, drift)
                writer.writerow([delta, pressure, drift, scup])
