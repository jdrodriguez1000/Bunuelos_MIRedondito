import os

log_path = r"c:\Users\USUARIO\Documents\Forecaster\Bunuelos_MIRedondito\pipeline_test.log"
def try_read(enc):
    try:
        with open(log_path, 'r', encoding=enc) as f:
            print(f"--- {enc} ---")
            print(f.read()[-1000:]) # Last 1000 chars
            return True
    except:
        return False

if os.path.exists(log_path):
    if not try_read('utf-16'):
        if not try_read('utf-8'):
            try_read('latin1')
else:
    print("Log file not found.")
