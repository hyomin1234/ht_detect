#! /bin/bash/ -f


################ Modify Here ################
# Benchmark top module name
export build_name=aes_128
# RTL directory 
export RTLDir=$PRJ/RTL/aes_128

# Design directory name (as you want)
dirName=aes_128_util${UTIL}_clk${CLK}

# Clock pin & period (in ns)
export clkName=clk
export rstName=reset
export clkPeriod=$CLK

# 0: Design doesn't have hard macro (ex. memory, ...)
# 1: Design has hard macro
export HM=0

#############################################

########### DO NOT MODIFY BELOW #############
baseDir=$PRJ/designs/${build_name}
designDir=$baseDir/$dirName

mkdir -p $designDir 
mkdir -p $designDir/log $designDir/data

if [ ! -e $designDir/$build_name.variables.tcl ] 
then
    cp $PRJ/scripts/variables.template.tcl $designDir/$build_name.variables.tcl
fi

if [ ! -e $designDir/_run_all ] 
then
	cp $PRJ/scripts/exec/_run_all $designDir/_run_all
fi

if [ $HM == 1 ] 
then
	export HMDir=$baseDir/hardMacroTech
	export HARDMACRODB_DIR="$HMDir/hard_db"
	export HARDMACROLEF_DIR="$HMDir/hard_lef"
	export HARDMACROLIB_DIR="$HMDir/hard_lib"
	mkdir -p $HMDir $HARDMACRODB_DIR $HARDMACROLEF_DIR $HARDMACROLIB_DIR
fi

############################################################## 
