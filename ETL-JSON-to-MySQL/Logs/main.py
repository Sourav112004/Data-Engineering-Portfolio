import subprocess

print("Starting Extract...")
subprocess.run(["python", "Logs/extract.py"])

print("Starting Transform...")
subprocess.run(["python", "Logs/transform.py"])

print("Starting Load...")
subprocess.run(["python", "Logs/load.py"])

print("ETL Completed!")