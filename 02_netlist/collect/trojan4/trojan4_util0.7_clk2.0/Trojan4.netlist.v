/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:44:29 2026
/////////////////////////////////////////////////////////////


module Trojan4 ( clk, rst, key_63_, key_62_, key_61_, key_60_, key_59_, 
        key_58_, key_57_, key_56_, key_55_, key_54_, key_53_, key_52_, key_51_, 
        key_50_, key_49_, key_48_, key_47_, key_46_, key_45_, key_44_, key_43_, 
        key_42_, key_41_, key_40_, key_39_, key_38_, key_37_, key_36_, key_35_, 
        key_34_, key_33_, key_32_, key_31_, key_30_, key_29_, key_28_, key_27_, 
        key_26_, key_25_, key_24_, key_23_, key_22_, key_21_, key_20_, key_19_, 
        key_18_, key_17_, key_16_, key_15_, key_14_, key_13_, key_12_, key_11_, 
        key_10_, key_9_, key_8_, key_7_, key_6_, key_5_, key_4_, key_3_, 
        key_2_, key_1_, key_0_, leak_63_, leak_62_, leak_61_, leak_60_, 
        leak_59_, leak_58_, leak_57_, leak_56_, leak_55_, leak_54_, leak_53_, 
        leak_52_, leak_51_, leak_50_, leak_49_, leak_48_, leak_47_, leak_46_, 
        leak_45_, leak_44_, leak_43_, leak_42_, leak_41_, leak_40_, leak_39_, 
        leak_38_, leak_37_, leak_36_, leak_35_, leak_34_, leak_33_, leak_32_, 
        leak_31_, leak_30_, leak_29_, leak_28_, leak_27_, leak_26_, leak_25_, 
        leak_24_, leak_23_, leak_22_, leak_21_, leak_20_, leak_19_, leak_18_, 
        leak_17_, leak_16_, leak_15_, leak_14_, leak_13_, leak_12_, leak_11_, 
        leak_10_, leak_9_, leak_8_, leak_7_, leak_6_, leak_5_, leak_4_, 
        leak_3_, leak_2_, leak_1_, leak_0_ );
  input clk, rst, key_63_, key_62_, key_61_, key_60_, key_59_, key_58_,
         key_57_, key_56_, key_55_, key_54_, key_53_, key_52_, key_51_,
         key_50_, key_49_, key_48_, key_47_, key_46_, key_45_, key_44_,
         key_43_, key_42_, key_41_, key_40_, key_39_, key_38_, key_37_,
         key_36_, key_35_, key_34_, key_33_, key_32_, key_31_, key_30_,
         key_29_, key_28_, key_27_, key_26_, key_25_, key_24_, key_23_,
         key_22_, key_21_, key_20_, key_19_, key_18_, key_17_, key_16_,
         key_15_, key_14_, key_13_, key_12_, key_11_, key_10_, key_9_, key_8_,
         key_7_, key_6_, key_5_, key_4_, key_3_, key_2_, key_1_, key_0_;
  output leak_63_, leak_62_, leak_61_, leak_60_, leak_59_, leak_58_, leak_57_,
         leak_56_, leak_55_, leak_54_, leak_53_, leak_52_, leak_51_, leak_50_,
         leak_49_, leak_48_, leak_47_, leak_46_, leak_45_, leak_44_, leak_43_,
         leak_42_, leak_41_, leak_40_, leak_39_, leak_38_, leak_37_, leak_36_,
         leak_35_, leak_34_, leak_33_, leak_32_, leak_31_, leak_30_, leak_29_,
         leak_28_, leak_27_, leak_26_, leak_25_, leak_24_, leak_23_, leak_22_,
         leak_21_, leak_20_, leak_19_, leak_18_, leak_17_, leak_16_, leak_15_,
         leak_14_, leak_13_, leak_12_, leak_11_, leak_10_, leak_9_, leak_8_,
         leak_7_, leak_6_, leak_5_, leak_4_, leak_3_, leak_2_, leak_1_,
         leak_0_;
  wire   lfsr_15_, lfsr_14_, lfsr_12_, lfsr_11_, lfsr_10_, lfsr_9_, lfsr_7_,
         lfsr_5_, lfsr_3_, lfsr_2_, lfsr_0_, N1, N2, N3, N4, N5, N6, N7, N8,
         N9, N10, N11, N12, N13, N14, N15, N16, N17, N18, N19, N20, N21, N22,
         N23, N24, N25, N26, N27, N28, N29, N30, N31, N32, N33, N34, N35, N36,
         N37, N38, N39, N40, N41, N42, N43, N44, N45, N46, N47, N48, N49, N50,
         N51, N52, N53, N54, N55, N56, N57, N58, N59, N60, N61, N62, N63, N64,
         n4, n5, n6, n7, n10, n13, n16, n19, n22, n25, n28, n31, n34, n37, n40,
         n43, n46, n49, n52, n55, n58, n61, n64, n67, n70, n73, n76, n79, n82,
         n85, n88, n91, n94, n97, n100, n103, n106, n109, n112, n115, n118,
         n121, n124, n127, n130, n133, n136, n139, n142, n145, n148, n151,
         n154, n157, n160, n163, n166, n169, n172, n175, n178, n181, n184,
         n187, n190, n193, n196, n199, n202, n205, n208, n213, n219, n222,
         n225, n237, n243, n244, n245;

  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_0_ ( .D(n243), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_0_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_2_ ( .D(n208), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_2_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_3_ ( .D(n237), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_3_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_5_ ( .D(n205), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_5_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_7_ ( .D(n202), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_7_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_9_ ( .D(n199), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_9_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_10_ ( .D(n225), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_10_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_11_ ( .D(n222), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_11_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_12_ ( .D(n219), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_12_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_14_ ( .D(n196), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_14_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_15_ ( .D(n213), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(lfsr_15_) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_1_ ( .D(lfsr_0_), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n208) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_4_ ( .D(lfsr_3_), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n205) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_6_ ( .D(lfsr_5_), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n202) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_8_ ( .D(lfsr_7_), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n199) );
  DFFASRHQNx1_ASAP7_75t_R lfsr_reg_13_ ( .D(lfsr_12_), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n196) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_63_ ( .D(N1), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n193) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_62_ ( .D(N2), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n190) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_61_ ( .D(N3), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n187) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_60_ ( .D(N4), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n184) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_59_ ( .D(N5), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n181) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_58_ ( .D(N6), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n178) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_57_ ( .D(N7), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n175) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_56_ ( .D(N8), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n172) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_55_ ( .D(N9), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n169) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_54_ ( .D(N10), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n166) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_53_ ( .D(N11), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n163) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_52_ ( .D(N12), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n160) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_51_ ( .D(N13), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n157) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_50_ ( .D(N14), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n154) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_49_ ( .D(N15), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n151) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_48_ ( .D(N16), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n148) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_47_ ( .D(N17), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n145) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_46_ ( .D(N18), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n142) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_45_ ( .D(N19), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n139) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_44_ ( .D(N20), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n136) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_43_ ( .D(N21), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n133) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_42_ ( .D(N22), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n130) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_41_ ( .D(N23), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n127) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_40_ ( .D(N24), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n124) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_39_ ( .D(N25), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n121) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_38_ ( .D(N26), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n118) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_37_ ( .D(N27), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n115) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_36_ ( .D(N28), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n112) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_35_ ( .D(N29), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n109) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_34_ ( .D(N30), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n106) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_33_ ( .D(N31), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n103) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_32_ ( .D(N32), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n100) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_31_ ( .D(N33), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n97) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_30_ ( .D(N34), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n94) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_29_ ( .D(N35), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n91) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_28_ ( .D(N36), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n88) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_27_ ( .D(N37), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n85) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_26_ ( .D(N38), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n82) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_25_ ( .D(N39), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n79) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_24_ ( .D(N40), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n76) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_23_ ( .D(N41), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n73) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_22_ ( .D(N42), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n70) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_21_ ( .D(N43), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n67) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_20_ ( .D(N44), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n64) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_19_ ( .D(N45), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n61) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_18_ ( .D(N46), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n58) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_17_ ( .D(N47), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n55) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_16_ ( .D(N48), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n52) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_15_ ( .D(N49), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n49) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_14_ ( .D(N50), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n46) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_13_ ( .D(N51), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n43) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_12_ ( .D(N52), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n40) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_11_ ( .D(N53), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n37) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_10_ ( .D(N54), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n34) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_9_ ( .D(N55), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n31) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_8_ ( .D(N56), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n28) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_7_ ( .D(N57), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n25) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_6_ ( .D(N58), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n22) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_5_ ( .D(N59), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n19) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_4_ ( .D(N60), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n16) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_3_ ( .D(N61), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n13) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_2_ ( .D(N62), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n10) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_1_ ( .D(N63), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n7) );
  DFFASRHQNx1_ASAP7_75t_R leak_reg_0_ ( .D(N64), .CLK(clk), .RESETN(n6), 
        .SETN(n5), .QN(n4) );
  INVx1_ASAP7_75t_R U5 ( .A(rst), .Y(n6) );
  TIEHIx1_ASAP7_75t_R U141 ( .H(n5) );
  INVxp33_ASAP7_75t_R U142 ( .A(n160), .Y(leak_52_) );
  INVxp33_ASAP7_75t_R U143 ( .A(n187), .Y(leak_61_) );
  INVxp33_ASAP7_75t_R U144 ( .A(n178), .Y(leak_58_) );
  INVxp33_ASAP7_75t_R U145 ( .A(n145), .Y(leak_47_) );
  INVxp33_ASAP7_75t_R U146 ( .A(n172), .Y(leak_56_) );
  INVxp33_ASAP7_75t_R U147 ( .A(n169), .Y(leak_55_) );
  INVxp33_ASAP7_75t_R U148 ( .A(n142), .Y(leak_46_) );
  INVxp33_ASAP7_75t_R U149 ( .A(n151), .Y(leak_49_) );
  INVxp33_ASAP7_75t_R U150 ( .A(n127), .Y(leak_41_) );
  INVxp33_ASAP7_75t_R U151 ( .A(n118), .Y(leak_38_) );
  INVxp33_ASAP7_75t_R U152 ( .A(n109), .Y(leak_35_) );
  INVxp33_ASAP7_75t_R U153 ( .A(n124), .Y(leak_40_) );
  INVxp33_ASAP7_75t_R U154 ( .A(n154), .Y(leak_50_) );
  INVxp33_ASAP7_75t_R U155 ( .A(n103), .Y(leak_33_) );
  INVxp33_ASAP7_75t_R U156 ( .A(n100), .Y(leak_32_) );
  INVxp33_ASAP7_75t_R U157 ( .A(n133), .Y(leak_43_) );
  INVxp33_ASAP7_75t_R U158 ( .A(n190), .Y(leak_62_) );
  INVxp33_ASAP7_75t_R U159 ( .A(n136), .Y(leak_44_) );
  INVxp33_ASAP7_75t_R U160 ( .A(n91), .Y(leak_29_) );
  INVxp33_ASAP7_75t_R U161 ( .A(n106), .Y(leak_34_) );
  INVxp33_ASAP7_75t_R U162 ( .A(n184), .Y(leak_60_) );
  INVxp33_ASAP7_75t_R U163 ( .A(n181), .Y(leak_59_) );
  INVxp33_ASAP7_75t_R U164 ( .A(n82), .Y(leak_26_) );
  INVxp33_ASAP7_75t_R U165 ( .A(n79), .Y(leak_25_) );
  INVxp33_ASAP7_75t_R U166 ( .A(n163), .Y(leak_53_) );
  INVxp33_ASAP7_75t_R U167 ( .A(n76), .Y(leak_24_) );
  INVxp33_ASAP7_75t_R U168 ( .A(n73), .Y(leak_23_) );
  INVxp33_ASAP7_75t_R U169 ( .A(n70), .Y(leak_22_) );
  INVxp33_ASAP7_75t_R U170 ( .A(n166), .Y(leak_54_) );
  INVxp33_ASAP7_75t_R U171 ( .A(n67), .Y(leak_21_) );
  INVxp33_ASAP7_75t_R U172 ( .A(n64), .Y(leak_20_) );
  INVxp33_ASAP7_75t_R U173 ( .A(n61), .Y(leak_19_) );
  INVxp33_ASAP7_75t_R U174 ( .A(n157), .Y(leak_51_) );
  INVxp33_ASAP7_75t_R U175 ( .A(n193), .Y(leak_63_) );
  INVxp33_ASAP7_75t_R U176 ( .A(n58), .Y(leak_18_) );
  INVxp33_ASAP7_75t_R U177 ( .A(n55), .Y(leak_17_) );
  INVxp33_ASAP7_75t_R U178 ( .A(n94), .Y(leak_30_) );
  INVxp33_ASAP7_75t_R U179 ( .A(n52), .Y(leak_16_) );
  INVxp33_ASAP7_75t_R U180 ( .A(n49), .Y(leak_15_) );
  INVxp33_ASAP7_75t_R U181 ( .A(n46), .Y(leak_14_) );
  INVxp33_ASAP7_75t_R U182 ( .A(n139), .Y(leak_45_) );
  INVxp33_ASAP7_75t_R U183 ( .A(n43), .Y(leak_13_) );
  INVxp33_ASAP7_75t_R U184 ( .A(n40), .Y(leak_12_) );
  INVxp33_ASAP7_75t_R U185 ( .A(n37), .Y(leak_11_) );
  INVxp33_ASAP7_75t_R U186 ( .A(n130), .Y(leak_42_) );
  INVxp33_ASAP7_75t_R U187 ( .A(n34), .Y(leak_10_) );
  INVxp33_ASAP7_75t_R U188 ( .A(n31), .Y(leak_9_) );
  INVxp33_ASAP7_75t_R U189 ( .A(n28), .Y(leak_8_) );
  INVxp33_ASAP7_75t_R U190 ( .A(n121), .Y(leak_39_) );
  INVxp33_ASAP7_75t_R U191 ( .A(n25), .Y(leak_7_) );
  INVxp33_ASAP7_75t_R U192 ( .A(n115), .Y(leak_37_) );
  INVxp33_ASAP7_75t_R U193 ( .A(n22), .Y(leak_6_) );
  INVxp33_ASAP7_75t_R U194 ( .A(n112), .Y(leak_36_) );
  INVxp33_ASAP7_75t_R U195 ( .A(n19), .Y(leak_5_) );
  INVxp33_ASAP7_75t_R U196 ( .A(n88), .Y(leak_28_) );
  INVxp33_ASAP7_75t_R U197 ( .A(n148), .Y(leak_48_) );
  INVxp33_ASAP7_75t_R U198 ( .A(n16), .Y(leak_4_) );
  INVxp33_ASAP7_75t_R U199 ( .A(n7), .Y(leak_1_) );
  INVxp33_ASAP7_75t_R U200 ( .A(n97), .Y(leak_31_) );
  INVxp33_ASAP7_75t_R U201 ( .A(n175), .Y(leak_57_) );
  INVxp33_ASAP7_75t_R U202 ( .A(n13), .Y(leak_3_) );
  INVxp33_ASAP7_75t_R U203 ( .A(n85), .Y(leak_27_) );
  INVxp33_ASAP7_75t_R U204 ( .A(n4), .Y(leak_0_) );
  INVxp33_ASAP7_75t_R U205 ( .A(n10), .Y(leak_2_) );
  XOR2xp5_ASAP7_75t_R U206 ( .A(lfsr_15_), .B(key_63_), .Y(N1) );
  XOR2xp5_ASAP7_75t_R U207 ( .A(lfsr_15_), .B(key_47_), .Y(N17) );
  XOR2xp5_ASAP7_75t_R U208 ( .A(lfsr_15_), .B(key_15_), .Y(N49) );
  XOR2xp5_ASAP7_75t_R U209 ( .A(lfsr_15_), .B(key_31_), .Y(N33) );
  XOR2xp5_ASAP7_75t_R U210 ( .A(lfsr_12_), .B(key_28_), .Y(N36) );
  XOR2xp5_ASAP7_75t_R U211 ( .A(lfsr_12_), .B(key_44_), .Y(N20) );
  XOR2xp5_ASAP7_75t_R U212 ( .A(lfsr_12_), .B(key_60_), .Y(N4) );
  XOR2xp5_ASAP7_75t_R U213 ( .A(lfsr_12_), .B(key_12_), .Y(N52) );
  INVxp33_ASAP7_75t_R U214 ( .A(lfsr_10_), .Y(n222) );
  INVxp33_ASAP7_75t_R U215 ( .A(lfsr_11_), .Y(n219) );
  INVxp33_ASAP7_75t_R U216 ( .A(lfsr_14_), .Y(n213) );
  INVxp33_ASAP7_75t_R U217 ( .A(lfsr_2_), .Y(n237) );
  INVxp33_ASAP7_75t_R U218 ( .A(lfsr_9_), .Y(n225) );
  HAxp5_ASAP7_75t_R U219 ( .A(key_62_), .B(n213), .SN(N2) );
  HAxp5_ASAP7_75t_R U220 ( .A(n196), .B(key_61_), .SN(N3) );
  HAxp5_ASAP7_75t_R U221 ( .A(key_59_), .B(n219), .SN(N5) );
  HAxp5_ASAP7_75t_R U222 ( .A(key_58_), .B(n222), .SN(N6) );
  HAxp5_ASAP7_75t_R U223 ( .A(key_57_), .B(n225), .SN(N7) );
  HAxp5_ASAP7_75t_R U224 ( .A(n199), .B(key_56_), .SN(N8) );
  XOR2xp5_ASAP7_75t_R U225 ( .A(lfsr_7_), .B(key_55_), .Y(N9) );
  HAxp5_ASAP7_75t_R U226 ( .A(n202), .B(key_54_), .SN(N10) );
  XOR2xp5_ASAP7_75t_R U227 ( .A(lfsr_5_), .B(key_53_), .Y(N11) );
  HAxp5_ASAP7_75t_R U228 ( .A(n205), .B(key_52_), .SN(N12) );
  XOR2xp5_ASAP7_75t_R U229 ( .A(lfsr_3_), .B(key_51_), .Y(N13) );
  HAxp5_ASAP7_75t_R U230 ( .A(key_50_), .B(n237), .SN(N14) );
  HAxp5_ASAP7_75t_R U231 ( .A(n208), .B(key_49_), .SN(N15) );
  XOR2xp5_ASAP7_75t_R U232 ( .A(lfsr_0_), .B(key_48_), .Y(N16) );
  HAxp5_ASAP7_75t_R U233 ( .A(key_46_), .B(n213), .SN(N18) );
  HAxp5_ASAP7_75t_R U234 ( .A(n196), .B(key_45_), .SN(N19) );
  HAxp5_ASAP7_75t_R U235 ( .A(key_43_), .B(n219), .SN(N21) );
  HAxp5_ASAP7_75t_R U236 ( .A(key_42_), .B(n222), .SN(N22) );
  HAxp5_ASAP7_75t_R U237 ( .A(key_41_), .B(n225), .SN(N23) );
  HAxp5_ASAP7_75t_R U238 ( .A(n199), .B(key_40_), .SN(N24) );
  XOR2xp5_ASAP7_75t_R U239 ( .A(lfsr_7_), .B(key_39_), .Y(N25) );
  HAxp5_ASAP7_75t_R U240 ( .A(n202), .B(key_38_), .SN(N26) );
  XOR2xp5_ASAP7_75t_R U241 ( .A(lfsr_5_), .B(key_37_), .Y(N27) );
  HAxp5_ASAP7_75t_R U242 ( .A(n205), .B(key_36_), .SN(N28) );
  XOR2xp5_ASAP7_75t_R U243 ( .A(lfsr_3_), .B(key_35_), .Y(N29) );
  HAxp5_ASAP7_75t_R U244 ( .A(key_34_), .B(n237), .SN(N30) );
  HAxp5_ASAP7_75t_R U245 ( .A(n208), .B(key_33_), .SN(N31) );
  XOR2xp5_ASAP7_75t_R U246 ( .A(lfsr_0_), .B(key_32_), .Y(N32) );
  HAxp5_ASAP7_75t_R U247 ( .A(key_30_), .B(n213), .SN(N34) );
  HAxp5_ASAP7_75t_R U248 ( .A(n196), .B(key_29_), .SN(N35) );
  HAxp5_ASAP7_75t_R U249 ( .A(key_27_), .B(n219), .SN(N37) );
  HAxp5_ASAP7_75t_R U250 ( .A(key_26_), .B(n222), .SN(N38) );
  HAxp5_ASAP7_75t_R U251 ( .A(key_25_), .B(n225), .SN(N39) );
  HAxp5_ASAP7_75t_R U252 ( .A(n199), .B(key_24_), .SN(N40) );
  XOR2xp5_ASAP7_75t_R U253 ( .A(lfsr_7_), .B(key_23_), .Y(N41) );
  HAxp5_ASAP7_75t_R U254 ( .A(n202), .B(key_22_), .SN(N42) );
  XOR2xp5_ASAP7_75t_R U255 ( .A(lfsr_5_), .B(key_21_), .Y(N43) );
  HAxp5_ASAP7_75t_R U256 ( .A(n205), .B(key_20_), .SN(N44) );
  XOR2xp5_ASAP7_75t_R U257 ( .A(lfsr_3_), .B(key_19_), .Y(N45) );
  HAxp5_ASAP7_75t_R U258 ( .A(key_18_), .B(n237), .SN(N46) );
  HAxp5_ASAP7_75t_R U259 ( .A(n208), .B(key_17_), .SN(N47) );
  XOR2xp5_ASAP7_75t_R U260 ( .A(lfsr_0_), .B(key_16_), .Y(N48) );
  HAxp5_ASAP7_75t_R U261 ( .A(key_14_), .B(n213), .SN(N50) );
  HAxp5_ASAP7_75t_R U262 ( .A(n196), .B(key_13_), .SN(N51) );
  HAxp5_ASAP7_75t_R U263 ( .A(key_11_), .B(n219), .SN(N53) );
  HAxp5_ASAP7_75t_R U264 ( .A(key_10_), .B(n222), .SN(N54) );
  HAxp5_ASAP7_75t_R U265 ( .A(key_9_), .B(n225), .SN(N55) );
  HAxp5_ASAP7_75t_R U266 ( .A(n199), .B(key_8_), .SN(N56) );
  XOR2xp5_ASAP7_75t_R U267 ( .A(lfsr_7_), .B(key_7_), .Y(N57) );
  HAxp5_ASAP7_75t_R U268 ( .A(n202), .B(key_6_), .SN(N58) );
  XOR2xp5_ASAP7_75t_R U269 ( .A(lfsr_5_), .B(key_5_), .Y(N59) );
  HAxp5_ASAP7_75t_R U270 ( .A(n205), .B(key_4_), .SN(N60) );
  XOR2xp5_ASAP7_75t_R U271 ( .A(lfsr_3_), .B(key_3_), .Y(N61) );
  HAxp5_ASAP7_75t_R U272 ( .A(key_2_), .B(n237), .SN(N62) );
  HAxp5_ASAP7_75t_R U273 ( .A(n208), .B(key_1_), .SN(N63) );
  XOR2xp5_ASAP7_75t_R U274 ( .A(lfsr_0_), .B(key_0_), .Y(N64) );
  INVxp33_ASAP7_75t_R U275 ( .A(n196), .Y(n244) );
  AOI22xp33_ASAP7_75t_R U276 ( .A1(lfsr_10_), .A2(n244), .B1(n196), .B2(n222), 
        .Y(n245) );
  FAx1_ASAP7_75t_R U277 ( .A(lfsr_12_), .B(lfsr_15_), .CI(n245), .SN(n243) );
endmodule

