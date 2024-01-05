import subprocess

# Run first_script.py
subprocess.run(["python", "Grouping.py"])

# After Grouping.py is done, run GA.py
subprocess.run(["python", "GA.py"])

# After GA.py is done, run barname saz.py
subprocess.run(["python", "barname saz.py"])
