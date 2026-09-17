import os
import sys
import argparse
import subprocess

def run_step(step_name, command_args):
    print("=" * 60)
    print(f"RUNNING STEP: {step_name}")
    print("=" * 60)
    
    try:
        # Run script using subprocess to isolate execution namespaces and argparse configs
        res = subprocess.run(
            [sys.executable] + command_args,
            check=True,
            capture_output=False
        )
        print(f"STEP SUCCESSFUL: {step_name}\n")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Step '{step_name}' failed with exit code {e.returncode}")
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Master Orchestrator for the Portfolio Company Financial Health Dashboard Pipeline."
    )
    parser.add_argument("--skip-extract", action="store_true", help="Skip data extraction from Yahoo Finance.")
    parser.add_argument("--skip-transform", action="store_true", help="Skip data cleaning and normalization.")
    parser.add_argument("--skip-load", action="store_true", help="Skip loading data into the SQLite database.")
    parser.add_argument("--skip-report", action="store_true", help="Skip generating the GenAI stakeholder report.")
    parser.add_argument("--force-extract", action="store_true", help="Force new data extraction, bypassing cache.")
    
    args = parser.parse_args()
    
    # 1. Ingestion / Extraction
    if not args.skip_extract:
        # Check python syntax
        extract_args = ["src/extract.py"]
        if args.force_extract:
            extract_args.append("--force")
        run_step("1. Data Ingestion & Local Caching", extract_args)
    else:
        print("Skipping step: 1. Data Ingestion & Caching\n")
        
    # 2. Transformation / Cleaning
    if not args.skip_transform:
        run_step("2. Data Cleaning & Normalization", ["src/transform.py"])
    else:
        print("Skipping step: 2. Data Cleaning & Normalization\n")
        
    # 3. SQLite DB Loading
    if not args.skip_load:
        run_step("3. SQLite Storage & Database Load", ["src/load.py"])
    else:
        print("Skipping step: 3. SQLite Storage & Database Load\n")
        
    # 4. Narrative / Report Generation
    if not args.skip_report:
        run_step("4. GenAI Executive Stakeholder Narrative Generation", ["src/narrative.py"])
    else:
        print("Skipping step: 4. GenAI Executive Stakeholder Narrative Generation\n")
        
    print("=" * 60)
    print("PIPELINE EXECUTION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
