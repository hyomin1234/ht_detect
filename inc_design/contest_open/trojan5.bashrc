#! /bin/bash/ -f

################ Modify Here ################
# Benchmark top module name
export build_name=Trojan5

# RTL directory
export RTLDir=c:/HT_detect/00_contest/trojan_definition/trojan5

# Design directory name
dirName=trojan5_util${UTIL}_clk${CLK}

# Clock pin & period
export clkName=clk
export rstName=rst
export clkPeriod=$CLK
export HM=0

#############################################

########### PATH FIX #######
# Explicit paths
baseDir="c:/HT_detect/designs/trojan5"
designDir="$baseDir/$dirName"

mkdir -p "$designDir" 
mkdir -p "$designDir/log" "$designDir/data"

# Copy template if it exists (Assuming scripts are in project_root/scripts)
if [ ! -e "$designDir/$build_name.variables.tcl" ]; then
    if [ -e "c:/HT_detect/scripts/variables.template.tcl" ]; then
        cp "c:/HT_detect/scripts/variables.template.tcl" "$designDir/$build_name.variables.tcl"
    fi
fi

if [ ! -e "$designDir/_run_all" ]; then
    if [ -e "c:/HT_detect/scripts/exec/_run_all" ]; then
        cp "c:/HT_detect/scripts/exec/_run_all" "$designDir/_run_all"
    fi
fi
