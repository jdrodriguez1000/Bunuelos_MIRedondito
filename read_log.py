import os

log_path = r"c:\Users\USUARIO\Documents\Forecaster\Bunuelos_MIRedondito\pipeline_test.log"
if os.path.exists(log_path):
    with open(log_path, 'r', encoding='utf-8', errors='replace') as f:
        print(f.read())
else:
    print("Log file not found.")
