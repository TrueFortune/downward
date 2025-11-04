import os.path
from pathlib import Path
import subprocess

considered_folders = [#"airport-adl",
                        #"assembly",
                        #"miconic-fulladl",
                        #"openstacks",
                        #"openstacks-opt08-adl",
                        #"openstacks-sat08-adl",
                        #"optical-telegraphs",
                        #"psr-large",
                        #"psr-middle",
                        #"trucks"
                        ]


base_path = Path("/home/user/Documents/GitHub/downward-benchmarks/")

for folder in considered_folders:
    benchmark_folder = f"{base_path}/{folder}/"
    for file in os.listdir(benchmark_folder):
        if file == "domain.pddl":
            continue
        if file.endswith(".pddl"):
            cmd = f'./downward/fast-downward.py ./downward-benchmarks/{folder}/domain.pddl ./downward-benchmarks/{folder}/{file} --search "lazy_greedy([add(axioms=exact_negative_cycles)])"'
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    with open("output.txt", "a") as output_file:
                        output_file.write(f"SUCCESS: {folder}/{file}\n")
                elif result.returncode == 11: # Set custom exit code in loop detection
                    with open("output.txt", "a") as output_file:
                        output_file.write(f"ERROR: {folder}/{file}\n")
            except:
                with open("output.txt", "a") as output_file:
                    output_file.write(f"TIMEOUT: {folder}/{file}\n")
        