import os

log_path = r"c:\Users\USUARIO\Documents\Forecaster\Bunuelos_MIRedondito\pipeline_test.log"
if os.path.exists(log_path):
    with open(log_path, 'rb') as f:
        content = f.read()
    
    # Try different decodings
    for enc in ['utf-16', 'utf-8', 'latin1']:
        try:
            text = content.decode(enc)
            print(f"--- {enc} ---")
            # Replace non-ascii chars to avoid console issues
            clean_text = "".join([c if ord(c) < 128 else f'[{hex(ord(c))}]' for c in text])
            print(clean_text)
            break
        except:
            continue
else:
    print("Log file not found.")
