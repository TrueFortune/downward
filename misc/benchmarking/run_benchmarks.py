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
                        "pddl",
                        "pddl-axioms",
                        "pddl-axioms-conditional-effects",
                        "pddl-axioms-conditional-effects-sdac",
                        "pddl-axioms-sdac",
                        "pddl-conditional-effects",
                        "pddl-sdac",
                        "sas-conditional-effects-sdac",
                        "sas-sdac"
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
BENCHMARK_PATH = Path("/home/user/Documents/downward-projects/downward-benchmarks/")
ADDITIONAL_BENCHMARKS_PATH = Path("/home/user/Documents/downward-projects/downward-benchmarks/additional-benchmarks/")
DOWNWARD_PATH = Path("/home/user/Documents/downward-projects/downward/")
OUTPUT_FILE = Path("/home/user/Documents/downward-projects/downward/misc/benchmarking/output.txt")


current_pid = os.getpid()

for folder in sorted(BENCHMARK_PATH.iterdir()): # Iterate over all, not only considered folders
    if folder == "additional-benchmarks" or not folder.is_dir():
        continue
    benchmark_folder = folder
    for file in sorted(os.listdir(benchmark_folder)):
        if "domain" in file:
            continue
        if file.endswith(".pddl"):
            print(f"Testing {file}")
            domain_file = f"{benchmark_folder}/domain.pddl"
            if not os.path.exists(domain_file):
                domain_file = f"{benchmark_folder}/{folder}/{file}-domain.pddl"
                if not os.path.exists(domain_file):
                    domain_file = f"{benchmark_folder}/{folder}/domain-{file}.pddl"
            cmd = f'ulimit -v 2000000; {DOWNWARD_PATH}/fast-downward.py {domain_file} {benchmark_folder}/{file} --search "lazy_greedy([add(axioms=exact_negative_cycles)])"'
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    with open(OUTPUT_FILE, "a") as output:
                        output.write(f"SUCCESS: {benchmark_folder}/{file}\n")
                        print("SUCCESS")
                elif result.returncode == 11: # Set custom exit code in loop detection
                    with open(OUTPUT_FILE, "a") as output:
                        output.write(f"ERROR: {benchmark_folder}/{file}\n")
                        print("ERROR")
                else:
                    with open(OUTPUT_FILE, "a") as output:
                        output.write(f"OOM: {benchmark_folder}/{file}\n")
                        print("OOM")
            except:
                with open(OUTPUT_FILE, "a") as output:
                    output.write(f"TIMEOUT: {benchmark_folder}/{file}\n")
                    print("TIMEOUT")
        cleanup()

for outer_folder in additional_considered_folders:
    benchmark_folder = f"{ADDITIONAL_BENCHMARKS_PATH}/{outer_folder}"
    for folder in sorted(os.listdir(f"{ADDITIONAL_BENCHMARKS_PATH}/{outer_folder}")):
        if folder in ["README.md", "suites.py"] or folder in os.listdir(BENCHMARK_PATH):
            print("Skipping ", folder)
            continue
        for file in sorted(os.listdir(f"{benchmark_folder}/{folder}")):
            if "domain" in file:
                continue
            if file.endswith(".pddl"):
                print(f"Testing {file}")
                domain_file = f"{benchmark_folder}/{folder}/domain.pddl"
                if not os.path.exists(domain_file):
                    domain_file = f"{benchmark_folder}/{folder}/{file[:-5]}-domain.pddl"
                    if not os.path.exists(domain_file):
                        domain_file = f"{benchmark_folder}/{folder}/domain-{file[:-5]}.pddl"
                cmd = f'ulimit -v 2000000; {DOWNWARD_PATH}/fast-downward.py {domain_file} {benchmark_folder}/{folder}/{file} --search "lazy_greedy([add(axioms=exact_negative_cycles)])"'

                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
                    if result.returncode == 0:
                        with open(OUTPUT_FILE, "a") as output:
                            output.write(f"SUCCESS: {benchmark_folder}/{folder}/{file}\n")
                            print("SUCCESS")
                    elif result.returncode == 11: # Set custom exit code in loop detection
                        with open(OUTPUT_FILE, "a") as output:
                            output.write(f"ERROR: {benchmark_folder}/{folder}/{file}\n")
                            print("ERROR")
                    else:
                        with open(OUTPUT_FILE, "a") as output:
                            output.write(f"OOM: {benchmark_folder}/{folder}/{file}\n")
                            print("OOM")
                except:
                    with open(OUTPUT_FILE, "a") as output:
                        output.write(f"TIMEOUT: {benchmark_folder}/{folder}/{file}\n")
                        print("TIMEOUT")
            cleanup()
                    
        