
# setup link & target libraries
proc prc_setLinkTargetLibs { } {

	uplevel \#0 {
		#set link_library [list * $::env(DBFILE)]
		#set target_library " * $link_library "

		set link_library [list *]
		set target_library [list ]

        foreach fileName [glob -d $::env(MACRODB_DIR) *.db] {
			set link_library [linsert $link_library end $fileName]
        	set target_library [linsert $target_library end $fileName]
        }


        if { [ info exists env(HARDMACRODB_DIR) ] } {
        	foreach fileName [glob -d $::env(HARDMACRODB_DIR) *.db] {
        		set link_library [linsert $link_library end $fileName]
        		set target_library [linsert $target_library end $fileName]
        	}
        }
	}
}

proc prc_icc2_lm_setupConfig {} {
	uplevel \#0 {
		set libName "$::env(TECHNOLOGY)"
		
		
		# .tf file
		set TFfiles [list ]
		if {[info exists env(TF_DIR)]} {
	        foreach fileName [glob -d $::env(TF_DIR) *.tf] {
				set TFfiles [linsert $TFfiles end $fileName]
			}
		}
		if { $TFfiles == "" } {
			puts "ERR> You need .tf for ndm library generation."
			exit
		}

		# .db file(s)
		set DBfiles [list ]
 	        foreach fileName [glob -d $::env(MACRODB_DIR) *.db] {
			set DBfiles [linsert $DBfiles end $fileName]
		}


		# tech LEF file(s) (.lef, .lef.gz)
		set techLEF "$::env(TECHLEF_DIR)"
		set techLEFfiles [list ]
		if { $techLEF != "" } {
			foreach fileName [glob -nocomplain -d $::env(TECHLEF_DIR) *lef] {
				set techLEFfiles [linsert $techLEFfiles end $fileName]
			}
			foreach fileName [glob -nocomplain -d $::env(TECHLEF_DIR) *lef.gz] {
				set techLEFfiles [linsert $techLEFfiles end $fileName]
			}
		}
		
		# macro LEF file(s) (.lef, .lef.gz)
		set macroLEFfiles [list ]
		foreach fileName [glob -nocomplain -d $::env(MACROLEF_DIR) *lef] {
			set macroLEFfiles [linsert $macroLEFfiles end $fileName]
		}
		foreach fileName [glob -nocomplain -d $::env(MACROLEF_DIR) *lef.gz] {
			set macroLEFfiles [linsert $macroLEFfiles end $fileName]
		}
		if { [ info exists env(HARDMACROLEF_DIR) ] } {
			foreach fileName [glob -nocomplain -d $::env(HARDMACROLEF_DIR) *lef] {
				set macroLEFfiles [linsert $macroLEFfiles end $fileName]
			}
			foreach fileName [glob -nocomplain -d $::env(HARDMACROLEF_DIR) *lef.gz] {
				set macroLEFfiles [linsert $macroLEFfiles end $fileName]
			}
		}
		if { [llength $macroLEFfiles] == 0 } {
			puts "ERR> You should have at least one macro LEF file for macro_ndm."
			exit
		}

		# TLUP file
		set TLUPfiles [list ]
		if {[info exists env(TLUP_DIR)]} {
	        foreach fileName [glob -d $::env(TLUP_DIR) *.tlup] {
				set TLUPfiles [linsert $TLUPfiles end $fileName]
			}
		}
		
	}
}
		
proc prc_icc2_setupConfig {} {
	uplevel \#0 {
		# Set each file path and design name
		set tech_ndm $::env(techDir)/tech_ndm
		if {[info exists REVISION] && $REVISION == "MCellPre"} {
			set full_ndm [join "$tech_ndm $::env(techDir)/macro_ndm_MCellPre"]
		} elseif {[info exists REVISION] && $REVISION == "MCellPost"} {
			set full_ndm [join "$tech_ndm $::env(techDir)/macro_ndm_MCellPost"]
		} elseif {[info exists REVISION] && $REVISION == "Popt"} {
			set full_ndm [join "$tech_ndm $::env(techDir)/macro_ndm_Popt"]
		} else {
			set full_ndm [join "$tech_ndm $::env(techDir)/macro_ndm"]
		}
		# TLUP file (should be only 1)
		set TLUPfiles ""
		if {[info exist env(TLUP_DIR)]} {
	        foreach fileName [glob -d $::env(TLUP_DIR) *.tlup] {
				append TLUPfiles "$fileName"
			}
		}
		
		# Create design library
		if { ![file exists $DESIGN_LIB] } {
			create_lib -use_technology_lib $tech_ndm -ref_libs $full_ndm $DESIGN_LIB
		} else {
			open_lib $DESIGN_LIB
		}
		
	}
}
		
proc prc_icc2_mmmcConfig {} {
	uplevel \#0 {
		
		# Set technology node
		set_technology -node $vars(LibUnit,Process)

		create_mode on
		create_corner typical
		create_scenario -name on_typical -mode on -corner typical
		
		set_parasitic_parameters -library tech_ndm -early_spec $TLUPfiles -late_spec $TLUPfiles
		set_temperature $::env(techTemp)
		set_process_number 1
		set_voltage $::env(techVol) -object_list VDD
		set_voltage 0.0 -object_list VSS

		source $::env(build_name).sdc
	}
}

proc prc_PT_readParasitics {} {
	uplevel \#0 { 
		if {[info exists REVISION]} {
			set SPEFdir "./SPEF/$REVISION"
		} else {
			set SPEFdir "./SPEF"
		}
	    foreach fileName [glob -nocomplain -d $SPEFdir *.spef] {
			read_parasitics -format spef $fileName
		}
	    foreach fileName [glob -nocomplain -d $SPEFdir *.spef.gz] {
			read_parasitics -format spef $fileName
		}
		complete_net_parasitics -complete_with zero
		report_annotated_parasitics	-check
	}
}

proc prc_icc2_setPNRmodes {} {
	uplevel \#0 { 
		# Set some design specific variables
		set placeMaxDensity $vars(PNR,placeMaxDensity)
		set maxRouteLayer $vars(PNR,maxRouteLayer)
		set minRouteLayer $vars(PNR,minRouteLayer)
		set maxPinRouteLayer $vars(PNR,maxPinRouteLayer)
		set minPinRouteLayer $vars(PNR,minPinRouteLayer)
		set leakageToDynamicRatio $vars(PNR,leakageToDynamicRatio)
		
		# place mode
		set_app_options -name place.coarse.max_density -value $placeMaxDensity
		set_app_options -name place.coarse.auto_density_control -value true
		set_app_options -name place.coarse.continue_on_missing_scandef -value true	
		
		# pin assignment mode
		## TBA. Now: default

		# CTS mode
		if { [info exists vars(CTS,ccdopt_design)] && $vars(CTS,ccdopt_design) } {
			set_app_options -name clock_opt.flow.enable_ccd -value true
			set_app_options -name route_opt.flow.enable_ccd -value true
		} else {
			set_app_options -name clock_opt.flow.enable_ccd -value false
			set_app_options -name route_opt.flow.enable_ccd -value false
		}

		# route mode
		set_ignored_layers -min_routing_layer $minRouteLayer -max_routing_layer $maxRouteLayer
		
		# optimization mode
		## TBA. Now: default
	}
}

proc prc_Snps_setSwitchingActivity { } {
	uplevel \#0 {
		#this should be updated for the multiple clock-domain design
		set thisClkPort [get_ports -filter {is_clock_used_as_clock==true}]
		set thisSeqOut [all_registers -output_pins]
		set thisIp [all_inputs]

		if { [sizeof_collection $thisSeqOut] > 0 } {
			set_switching_activity $thisSeqOut -static_probability $vars(SwitchingActivity,DutyRatio) -toggle_count $vars(SwitchingActivity,RegToggle) -base_clock [get_clock]
			#set_switching_activity $thisSeqOut -static_probability $vars(SwitchingActivity,DutyRatio) -toggle_count $vars(SwitchingActivity,RegToggle)
		}

		if { [sizeof_collection $thisIp] > 0 } {
			set_switching_activity $thisIp -static_probability $vars(SwitchingActivity,DutyRatio) -toggle_count $vars(SwitchingActivity,IpToggle) -base_clock [get_clock]
		}
			
		if { [sizeof_collection $thisClkPort] > 0 } {
			set_switching_activity $thisClkPort -static_probability $vars(SwitchingActivity,DutyRatio) -toggle_count $vars(SwitchingActivity,ClkToggle) -base_clock [get_clock]
		}
	}
}


proc prc_reportTNS {} {
	suppress_message CMD-041

	set design_tns 0
	set design_wns 100000
	set design_tps 0
	foreach_in_collection group [get_path_groups *] {
		set group_tns 0
		set group_wns 100000
		set group_tps 0
		# Report 1 path per end point. (like Encounter)
		foreach_in_collection path \
		[get_timing_paths -nworst 1 -max_paths 1000000 -group $group -slack_lesser_than $group_wns] {
			set slack [get_attribute $path slack]
			if {$slack < $group_wns} {
				set group_wns $slack
				if {$slack < $design_wns} {
					set design_wns $slack
				}
			}
			if {$slack < 0.0} {
				set group_tns [expr $group_tns + $slack]
			} else {
				set group_tps [expr $group_tps + $slack]
			}
		}
		set design_tns [expr $design_tns + $group_tns]
		set design_tps [expr $design_tps + $group_tps]
		set group_name [get_attribute $group full_name]
		echo [format "Group %s Worst Negative Slack : %g" $group_name $group_wns]
		echo [format "Group %s Total Negative Slack : %g" $group_name $group_tns]
		echo [format "Group %s Total Positive Slack : %g" $group_name $group_tps]
		echo ""
	}

	echo "------------------------------------------"
	echo [format "Design Worst Negative Slack : %g" $design_wns]
	echo [format "Design Total Negative Slack : %g" $design_tns]
	echo [format "Design Total Positive Slack : %g" $design_tps]
	
	unsuppress_message CMD-041
}


proc close_file {} {

	upvar fileId outfile
	close $outfile
}

proc cell_count {} {

	upvar fileId outfile
	## cell count ##
	global TotCellCount
	set TotCellCount [sizeof_collection [get_cells -hierarchical]]
	puts $outfile "cells_count\t\t$TotCellCount"
}

proc FF_count {} {

	upvar fileId outfile
	global TotCellCount

	## FF count ##
	set TotFFCount	[sizeof_collection [all_registers -cells]]
	puts $outfile "FFs_count\t\t$TotFFCount"

	## FF % ##
	set TotFFper	[expr {int(100 * $TotFFCount / $TotCellCount)}]
	puts $outfile "FFs%\t\t$TotFFper"

}

proc buf_count {args} {

	upvar fileId outfile
	global TotCellCount

	set buf_list [string trim $args "{}"]
	#puts $buf_list
	set TotBufCount 0	
	## buf count ##
	foreach buf_name $buf_list {
		puts $buf_name
		incr TotBufCount [sizeof_collection [get_cells -hierarchical -filter "ref_name == $buf_name"]]
		puts $TotBufCount
		
	}
	puts $outfile "buf_count\t\t$TotBufCount"

	set TotBufper [expr {int(100 * $TotBufCount / $TotCellCount)}]
	puts $outfile "bufs%\t\t\t$TotBufper"

}
proc total_power {} {
	
	upvar fileId outfile

	## Total power ##
	global totpower
	set totpower [get_attribute [get_design] total_power]
	puts $outfile "total_power\t\t$totpower"

}

proc clk_total_power {} {

	upvar fileId outfile

	global totpower

	#total clock network power
	#report_power -include_boundary_net -groups clock_network > tmp
	report_power -groups clock_network > tmp
	set TotClockPower [exec awk {{if($1 == "Total"){print $4}}} tmp]
	puts $outfile "Total_Clock_network_power\t\t$TotClockPower"
	sh rm -rf tmp

	set clkpower_per [expr {int(100 * $TotClockPower / $totpower)}]
	puts $outfile "Clk_power\t\t$TotClockPower ($clkpower_per%)"
}

proc switching_power {} {

	upvar fileId outfile

	set spower [get_attribute [get_design] switching_power]
	puts $outfile "switching_power\t\t$spower"
}

proc internal_power {} {

	upvar fileId outfile

	set ipower [get_attribute [get_design] internal_power]
	puts $outfile "internal_power\t\t$ipower"
}

proc sw_int {} {

	upvar fileId outfile

	#Switching power : internal power
	set spower [get_attribute [get_design] switching_power]
	set ipower [get_attribute [get_design] internal_power]
	set sum [expr $spower + $ipower]
	set spower_per [expr {int(100 * $spower / $sum)}]
	set ipower_per [expr {int(100 * $ipower / $sum)}]
	puts $outfile "sw:int_power\t\t$spower_per:$ipower_per"
}

proc clock_period {} {

	upvar fileId outfile
	#target clock period
	set target_clk_period [get_attribute [get_clocks] period]
	puts $outfile "target_clock_period\t\t$target_clk_period"
}

proc TPS {} {

	upvar fileId outfile
	#TPS
	prc_reportTNS > tmp
	set TPS [exec awk {{if($1 == "Design" && $2 == "Total" && $3 == "Positive"){print $6}}} tmp]
	puts $outfile "TPS\t\t$TPS"
	sh rm -rf tmp

}

proc TNS {} {

	upvar fileId outfile
	#TNS
	prc_reportTNS > tmp
	set TNS [exec awk {{if($1 == "Design" && $2 == "Total" && $3 == "Negative"){print $6}}} tmp]
	puts $outfile "TNS\t\t$TNS"
	sh rm -rf tmp

}

proc WNS {} {

	upvar fileId outfile
	#WNS
	prc_reportTNS > tmp
	set WNS [exec awk {{if($1 == "Design" && $2 == "Worst" && $3 == "Negative"){print $6}}} tmp]
	puts $outfile "WNS\t\t$WNS"
	sh rm -rf tmp

}

## Report ##
proc prc_PT_report {} {
	set design_name [get_attribute [get_design] full_name]
	set file ${design_name}.benchmark
	sh rm -rf $file
	set fileId [open $file w]

	set systemTime [clock seconds]

	# Area
	cell_count
	FF_count

	# Timing
	clock_period
	WNS
	TNS
	TPS
	
	# Power
	total_power
	switching_power
	internal_power
	clk_total_power
	sw_int
	close_file
}
