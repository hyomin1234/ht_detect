#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import argparse
import re
import io

# ==========================================
# [SETTINGS]
# ==========================================
# Default paths (can be overridden by arguments)
DEFAULT_ROOT_DIR = "/home/suwankim/students/hyomin/CAD/RTL/0_contest_open/"
DEFAULT_OUT_DIR = "/home/suwankim/students/hyomin/CAD/inc_design/0_contest_open/"

def get_top_module_and_ports(category, files):
    """
    Determine the top module name and if it has clk/rst ports.
    Scans for the first .v file and extracts the module name.
    Returns: (module_name, has_clk, has_rst)
    """
    for fname in files:
        if fname.endswith(".v"):
            try:
                # fname is full path
                with io.open(fname, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r'module\s+(\w+)', content)
                    if match:
                        mod_name = match.group(1)
                        # Simple port detection (case insensitive)
                        has_clk = bool(re.search(r'input\s+.*clk', content, re.IGNORECASE))
                        has_rst = bool(re.search(r'input\s+.*rst', content, re.IGNORECASE))
                        return mod_name, has_clk, has_rst
            except Exception as e:
                print("Error reading {}: {}".format(fname, e))
    return "top", False, False

def generate_script_content(unique_id, real_top, has_clk, has_rst, rtl_dir, project_root):
    """
    Generates the bashrc content.
    """
    # Clean paths for Tcl/Bash compatibility (forward slashes)
    rtl_dir = rtl_dir.replace("\\", "/")
    project_root = project_root.replace("\\", "/")
    
    # Logic for clk/rst variables in bashrc
    clk_var = "clk" if has_clk else ""
    rst_var = "rst" if has_rst else ""
    
    # Logic to comment out variables in variables.tcl if they are empty
    # This is appended to the bash script to run after copying variables.template.tcl
    fix_vars_script = ""
    if not has_clk:
        fix_vars_script += """
# Comment out clkName/Period in variables.tcl if no clock
if [ -f "$designDir/$build_name.variables.tcl" ]; then
    sed -i 's/^set vars(Syn,clkName)/#set vars(Syn,clkName)/g' "$designDir/$build_name.variables.tcl"
    sed -i 's/^set vars(Syn,clkPeriod)/#set vars(Syn,clkPeriod)/g' "$designDir/$build_name.variables.tcl"
fi
"""
    if not has_rst:
        fix_vars_script += """
# Comment out rstName in variables.tcl if no reset
if [ -f "$designDir/$build_name.variables.tcl" ]; then
    sed -i 's/^set vars(Syn,rstName)/#set vars(Syn,rstName)/g' "$designDir/$build_name.variables.tcl"
fi
"""

    template = u"""#! /bin/bash/ -f

################ Modify Here ################
# Benchmark top module name
export build_name={real_top}

# RTL directory
export RTLDir={rtl_dir}

# Design directory name
dirName={unique_id}_util${{UTIL}}_clk${{CLK}}

# Clock pin & period
export clkName={clk_var}
export rstName={rst_var}
export clkPeriod=$CLK
export HM=0

#############################################

########### PATH FIX #######
# Explicit paths
baseDir="{project_root}/designs/{unique_id}"
designDir="$baseDir/$dirName"

mkdir -p "$designDir" 
mkdir -p "$designDir/log" "$designDir/data"

# Copy template if it exists (Assuming scripts are in project_root/scripts)
if [ ! -e "$designDir/$build_name.variables.tcl" ]; then
    if [ -e "{project_root}/scripts/variables.template.tcl" ]; then
        cp "{project_root}/scripts/variables.template.tcl" "$designDir/$build_name.variables.tcl"
        {fix_vars_script}
    fi
fi

if [ ! -e "$designDir/_run_all" ]; then
    if [ -e "{project_root}/scripts/exec/_run_all" ]; then
        cp "{project_root}/scripts/exec/_run_all" "$designDir/_run_all"
    fi
fi
""".format(unique_id=unique_id, real_top=real_top, rtl_dir=rtl_dir, 
           project_root=project_root, clk_var=clk_var, rst_var=rst_var,
           fix_vars_script=fix_vars_script)
    return template

def main():
    parser = argparse.ArgumentParser(description="Generate synthesis config files for benchmarks.")
    parser.add_argument("--root-dir", default=DEFAULT_ROOT_DIR, help="Root directory of dataset")
    parser.add_argument("--out-dir", default=DEFAULT_OUT_DIR, help="Directory to save config files")
    args = parser.parse_args()

    # Use args directly as strings, no Path object
    root_path = args.root_dir
    out_path = args.out_dir
    
    # Determine project_root
    abs_root = os.path.abspath(root_path)
    # Assuming standard structure c:/HT_detect/00_contest/trojan_definition
    # We want c:/HT_detect
    project_root = os.path.dirname(os.path.dirname(abs_root))
    project_root = project_root.replace("\\", "/")
    
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    print("Scanning: {}".format(root_path))
    print("Output to: {}".format(out_path))

    configs_generated = 0

    if not os.path.exists(root_path):
        print("Error: Root directory {} does not exist.".format(root_path))
        return

    # Iterate over trojan directories
    for item in os.listdir(root_path):
        item_path = os.path.join(root_path, item)
        if os.path.isdir(item_path):
            unique_id = item
            
            # Find all files in the directory
            files = [os.path.join(item_path, f) for f in os.listdir(item_path)]
            
            # Determine Top Module and Ports
            real_top, has_clk, has_rst = get_top_module_and_ports(unique_id, files)
            print("Found {} -> Top: {}, Has Clk: {}, Has Rst: {}".format(unique_id, real_top, has_clk, has_rst))

            # Generate Script
            script_content = generate_script_content(unique_id, real_top, has_clk, has_rst, item_path, project_root)
            
            # Save
            save_name = "{}.bashrc".format(unique_id)
            save_file = os.path.join(out_path, save_name)
            
            with io.open(save_file, "w", encoding='utf-8', newline='\n') as f:
                f.write(script_content)
                
            configs_generated += 1

    print("\n[Done] Generated {} config files in {}".format(configs_generated, out_path))

if __name__ == "__main__":
    main()
