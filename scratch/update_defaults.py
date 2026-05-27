import os
import re

directory = 'warera/resources'

for filename in os.listdir(directory):
    if filename.endswith(".py") and not filename.startswith("_"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            content = f.read()

        # Update time_slice_days=kwargs.pop("time_slice_days", X) to 0.2
        content = re.sub(r'time_slice_days=kwargs\.pop\("time_slice_days", [0-9.]+\)', r'time_slice_days=kwargs.pop("time_slice_days", 0.2)', content)

        # Update concurrency=kwargs.pop("concurrency", X) to 500
        content = re.sub(r'concurrency=kwargs\.pop\("concurrency", \d+\)', r'concurrency=kwargs.pop("concurrency", 500)', content)

        # Update collect_all signature defaults if they exist
        content = re.sub(r'def collect_all\([^)]+concurrency: int = \d+', lambda m: m.group(0).split('concurrency: int = ')[0] + 'concurrency: int = 500', content)
        
        with open(filepath, 'w') as f:
            f.write(content)
print("Done updating resources.")
