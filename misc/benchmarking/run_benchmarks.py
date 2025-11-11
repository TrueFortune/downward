import os
from pathlib import Path
import subprocess
import psutil

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
additional_considered_folders = [
                        #"pddl-axioms",
                        #"pddl-axioms-conditional-effects",
                        #"pddl-axioms-conditional-effects-sdac",
                        #"pddl-axioms-sdac",
                        ]


def cleanup():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            elif proc.info['cmdline'] and any('downward' in str(arg) for arg in proc.info['cmdline']):
                proc.terminate()
        except:
            pass

# HARDCODED
benchmark_path = Path("/home/user/Documents/downward-projects/downward-benchmarks/")
additional_benchmarks_path = Path("/home/user/Documents/downward-projects/additional-benchmarks/")
downward_path = Path("/home/user/Documents/downward-projects/downward/")
output_file = Path("/home/user/Documents/downward-projects/downward/misc/benchmarking/output.txt")


current_pid = os.getpid()

for folder in considered_folders:
    benchmark_folder = f"{benchmark_path}/{folder}/"
    for file in sorted(os.listdir(benchmark_folder)):
        if file == "domain.pddl":
            continue
        if file.endswith(".pddl"):
            print(f"Testing {file}")
            cmd = f'ulimit -v 200000; {downward_path}/fast-downward.py {benchmark_path}/{folder}/domain.pddl {benchmark_path}/{folder}/{file} --search "lazy_greedy([add(axioms=exact_negative_cycles)])"'

            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
                if result.returncode == 0:
                    with open(output_file, "a") as output:
                        output.write(f"SUCCESS: {folder}/{file}\n")
                elif result.returncode == 11: # Set custom exit code in loop detection
                    with open(output_file, "a") as output:
                        output.write(f"ERROR: {folder}/{file}\n")
            except:
                with open(output_file, "a") as output:
                    output.write(f"TIMEOUT: {folder}/{file}\n")
        cleanup()


for outer_folder in additional_considered_folders:
    benchmark_folder = f"{additional_benchmarks_path}/{outer_folder}/"
    for folder in sorted(os.listdir(f"{additional_benchmarks_path}/{outer_folder}")):
        if folder in ["README.md", "suites.py"]:
            continue
        for file in sorted(os.listdir(f"{additional_benchmarks_path}/{outer_folder}/{folder}")):
            if file == "domain.pddl":
                continue
            if file.endswith(".pddl"):
                print(f"Testing {file}")
                cmd = f'ulimit -v 200000; {downward_path}/fast-downward.py {additional_benchmarks_path}/{outer_folder}/{folder}/domain.pddl {additional_benchmarks_path}/{outer_folder}/{folder}/{file} --search "lazy_greedy([add(axioms=exact_negative_cycles)])"'

                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
                    if result.returncode == 0:
                        with open(output_file, "a") as output:
                            output.write(f"SUCCESS: {folder}/{file}\n")
                    elif result.returncode == 11: # Set custom exit code in loop detection
                        with open(output_file, "a") as output:
                            output.write(f"ERROR: {folder}/{file}\n")
                except:
                    with open(output_file, "a") as output:
                        output.write(f"TIMEOUT: {folder}/{file}\n")
            cleanup()
                    
        