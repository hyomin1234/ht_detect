/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:42:34 2026
/////////////////////////////////////////////////////////////


module Trojan3 ( clk, rst, data_in_15_, data_in_14_, data_in_13_, data_in_12_, 
        data_in_11_, data_in_10_, data_in_9_, data_in_8_, data_in_7_, 
        data_in_6_, data_in_5_, data_in_4_, data_in_3_, data_in_2_, data_in_1_, 
        data_in_0_, data_out_15_, data_out_14_, data_out_13_, data_out_12_, 
        data_out_11_, data_out_10_, data_out_9_, data_out_8_, data_out_7_, 
        data_out_6_, data_out_5_, data_out_4_, data_out_3_, data_out_2_, 
        data_out_1_, data_out_0_ );
  input clk, rst, data_in_15_, data_in_14_, data_in_13_, data_in_12_,
         data_in_11_, data_in_10_, data_in_9_, data_in_8_, data_in_7_,
         data_in_6_, data_in_5_, data_in_4_, data_in_3_, data_in_2_,
         data_in_1_, data_in_0_;
  output data_out_15_, data_out_14_, data_out_13_, data_out_12_, data_out_11_,
         data_out_10_, data_out_9_, data_out_8_, data_out_7_, data_out_6_,
         data_out_5_, data_out_4_, data_out_3_, data_out_2_, data_out_1_,
         data_out_0_;
  wire   N3, N4, N5, N6, N7, N8, N9, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12,
         n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26,
         n27, n28, n29, n30, n31, n32, n33, n34, n35, n36, n37, n38, n39, n40,
         n41, n42, n43, n44, n45, n46, n47, n48, n49, n50, n51, n52, n53, n54,
         n55, n56, n57, n58, n59, n60, n62, n63, n64, n65, n66, n67, n68, n69,
         n70, n71, n72, n73, n74, n75, n76, n77, n78, n79, n80, n81, n82, n83,
         n84, n85, n86, n87, n88, n89, n90, n91, n92, n93, n94, n95, n96;

  DFFASRHQNx1_ASAP7_75t_R counter_reg_7_ ( .D(N9), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n28) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_6_ ( .D(N8), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n27) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_5_ ( .D(N7), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n26) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_4_ ( .D(N6), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n25) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_3_ ( .D(N5), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n24) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_2_ ( .D(N4), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n23) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_1_ ( .D(N3), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n22) );
  DFFASRHQNx1_ASAP7_75t_R counter_reg_0_ ( .D(n19), .CLK(clk), .RESETN(n21), 
        .SETN(n20), .QN(n19) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_15_ ( .D(n18), .CLK(clk), .RESETN(n60), 
        .SETN(n59), .QN(data_out_15_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_14_ ( .D(n17), .CLK(clk), .RESETN(n58), 
        .SETN(n57), .QN(data_out_14_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_13_ ( .D(n16), .CLK(clk), .RESETN(n56), 
        .SETN(n55), .QN(data_out_13_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_12_ ( .D(n15), .CLK(clk), .RESETN(n54), 
        .SETN(n53), .QN(data_out_12_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_11_ ( .D(n14), .CLK(clk), .RESETN(n52), 
        .SETN(n51), .QN(data_out_11_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_10_ ( .D(n13), .CLK(clk), .RESETN(n50), 
        .SETN(n49), .QN(data_out_10_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_9_ ( .D(n12), .CLK(clk), .RESETN(n48), 
        .SETN(n47), .QN(data_out_9_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_8_ ( .D(n11), .CLK(clk), .RESETN(n46), 
        .SETN(n45), .QN(data_out_8_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_7_ ( .D(n10), .CLK(clk), .RESETN(n44), 
        .SETN(n43), .QN(data_out_7_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_6_ ( .D(n9), .CLK(clk), .RESETN(n42), 
        .SETN(n41), .QN(data_out_6_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_5_ ( .D(n8), .CLK(clk), .RESETN(n40), 
        .SETN(n39), .QN(data_out_5_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_4_ ( .D(n7), .CLK(clk), .RESETN(n38), 
        .SETN(n37), .QN(data_out_4_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_3_ ( .D(n6), .CLK(clk), .RESETN(n36), 
        .SETN(n35), .QN(data_out_3_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_2_ ( .D(n5), .CLK(clk), .RESETN(n34), 
        .SETN(n33), .QN(data_out_2_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_1_ ( .D(n4), .CLK(clk), .RESETN(n32), 
        .SETN(n31), .QN(data_out_1_) );
  DFFASRHQNx1_ASAP7_75t_R data_out_reg_0_ ( .D(n3), .CLK(clk), .RESETN(n30), 
        .SETN(n29), .QN(data_out_0_) );
  INVx1_ASAP7_75t_R U21 ( .A(rst), .Y(n21) );
  TIEHIx1_ASAP7_75t_R U65 ( .H(n20) );
  INVxp33_ASAP7_75t_R U66 ( .A(data_in_0_), .Y(n3) );
  NAND2xp33_ASAP7_75t_R U67 ( .A(rst), .B(n3), .Y(n29) );
  INVxp33_ASAP7_75t_R U68 ( .A(data_in_9_), .Y(n82) );
  NAND2xp33_ASAP7_75t_R U69 ( .A(n82), .B(n96), .Y(n47) );
  INVxp33_ASAP7_75t_R U70 ( .A(data_in_1_), .Y(n95) );
  NAND2xp33_ASAP7_75t_R U71 ( .A(n95), .B(n96), .Y(n31) );
  INVxp33_ASAP7_75t_R U72 ( .A(data_in_3_), .Y(n91) );
  NAND2xp33_ASAP7_75t_R U73 ( .A(n91), .B(n96), .Y(n35) );
  INVxp33_ASAP7_75t_R U74 ( .A(data_in_5_), .Y(n88) );
  NAND2xp33_ASAP7_75t_R U75 ( .A(n88), .B(n96), .Y(n39) );
  INVxp33_ASAP7_75t_R U76 ( .A(data_in_7_), .Y(n85) );
  NAND2xp33_ASAP7_75t_R U77 ( .A(n85), .B(n96), .Y(n43) );
  INVxp33_ASAP7_75t_R U78 ( .A(data_in_13_), .Y(n76) );
  NAND2xp33_ASAP7_75t_R U79 ( .A(n76), .B(n96), .Y(n55) );
  INVxp33_ASAP7_75t_R U80 ( .A(data_in_11_), .Y(n79) );
  NAND2xp33_ASAP7_75t_R U81 ( .A(n79), .B(n96), .Y(n51) );
  NAND2xp33_ASAP7_75t_R U82 ( .A(rst), .B(data_in_0_), .Y(n30) );
  NAND2xp33_ASAP7_75t_R U83 ( .A(data_in_13_), .B(rst), .Y(n56) );
  NAND2xp33_ASAP7_75t_R U84 ( .A(data_in_11_), .B(rst), .Y(n52) );
  NAND2xp33_ASAP7_75t_R U85 ( .A(data_in_15_), .B(rst), .Y(n60) );
  NAND2xp33_ASAP7_75t_R U86 ( .A(data_in_12_), .B(rst), .Y(n54) );
  NAND2xp33_ASAP7_75t_R U87 ( .A(data_in_10_), .B(rst), .Y(n50) );
  NAND2xp33_ASAP7_75t_R U88 ( .A(data_in_14_), .B(rst), .Y(n58) );
  NAND2xp33_ASAP7_75t_R U89 ( .A(data_in_2_), .B(rst), .Y(n34) );
  NAND2xp33_ASAP7_75t_R U90 ( .A(data_in_5_), .B(rst), .Y(n40) );
  NAND2xp33_ASAP7_75t_R U91 ( .A(data_in_1_), .B(rst), .Y(n32) );
  NAND2xp33_ASAP7_75t_R U92 ( .A(data_in_9_), .B(rst), .Y(n48) );
  NAND2xp33_ASAP7_75t_R U93 ( .A(data_in_4_), .B(rst), .Y(n38) );
  NAND2xp33_ASAP7_75t_R U94 ( .A(data_in_7_), .B(rst), .Y(n44) );
  NAND2xp33_ASAP7_75t_R U95 ( .A(data_in_8_), .B(rst), .Y(n46) );
  NAND2xp33_ASAP7_75t_R U96 ( .A(data_in_3_), .B(rst), .Y(n36) );
  NAND2xp33_ASAP7_75t_R U97 ( .A(data_in_6_), .B(rst), .Y(n42) );
  NOR3xp33_ASAP7_75t_R U98 ( .A(n23), .B(n19), .C(n22), .Y(n63) );
  O2A1O1Ixp33_ASAP7_75t_R U99 ( .A1(n19), .A2(n22), .B(n23), .C(n63), .Y(N4)
         );
  NOR2xp33_ASAP7_75t_R U100 ( .A(n19), .B(n22), .Y(n62) );
  AOI21xp33_ASAP7_75t_R U101 ( .A1(n22), .A2(n19), .B(n62), .Y(N3) );
  INVxp33_ASAP7_75t_R U102 ( .A(n63), .Y(n64) );
  NOR4xp25_ASAP7_75t_R U103 ( .A(n24), .B(n23), .C(n19), .D(n22), .Y(n65) );
  AOI21xp33_ASAP7_75t_R U104 ( .A1(n24), .A2(n64), .B(n65), .Y(N5) );
  INVxp33_ASAP7_75t_R U105 ( .A(n65), .Y(n66) );
  NOR2xp33_ASAP7_75t_R U106 ( .A(n25), .B(n66), .Y(n67) );
  AOI21xp33_ASAP7_75t_R U107 ( .A1(n25), .A2(n66), .B(n67), .Y(N6) );
  INVxp33_ASAP7_75t_R U108 ( .A(n67), .Y(n68) );
  NOR2xp33_ASAP7_75t_R U109 ( .A(n68), .B(n26), .Y(n69) );
  AOI21xp33_ASAP7_75t_R U110 ( .A1(n26), .A2(n68), .B(n69), .Y(N7) );
  INVxp33_ASAP7_75t_R U111 ( .A(n69), .Y(n70) );
  NOR2xp33_ASAP7_75t_R U112 ( .A(n27), .B(n70), .Y(n71) );
  AOI21xp33_ASAP7_75t_R U113 ( .A1(n27), .A2(n70), .B(n71), .Y(N8) );
  INVxp33_ASAP7_75t_R U114 ( .A(n71), .Y(n72) );
  NOR2xp33_ASAP7_75t_R U115 ( .A(n72), .B(n28), .Y(n73) );
  AOI21xp33_ASAP7_75t_R U116 ( .A1(n28), .A2(n72), .B(n73), .Y(N9) );
  INVxp33_ASAP7_75t_R U117 ( .A(n73), .Y(n94) );
  NOR2xp33_ASAP7_75t_R U118 ( .A(n95), .B(n94), .Y(n93) );
  NAND2xp33_ASAP7_75t_R U119 ( .A(n93), .B(data_in_2_), .Y(n92) );
  OAI21xp33_ASAP7_75t_R U120 ( .A1(n93), .A2(data_in_2_), .B(n92), .Y(n5) );
  NOR2xp33_ASAP7_75t_R U121 ( .A(n92), .B(n91), .Y(n90) );
  NAND2xp33_ASAP7_75t_R U122 ( .A(n90), .B(data_in_4_), .Y(n89) );
  OAI21xp33_ASAP7_75t_R U123 ( .A1(n90), .A2(data_in_4_), .B(n89), .Y(n7) );
  NOR2xp33_ASAP7_75t_R U124 ( .A(n89), .B(n88), .Y(n87) );
  NAND2xp33_ASAP7_75t_R U125 ( .A(n87), .B(data_in_6_), .Y(n86) );
  OAI21xp33_ASAP7_75t_R U126 ( .A1(n87), .A2(data_in_6_), .B(n86), .Y(n9) );
  NOR2xp33_ASAP7_75t_R U127 ( .A(n86), .B(n85), .Y(n84) );
  NAND2xp33_ASAP7_75t_R U128 ( .A(n84), .B(data_in_8_), .Y(n83) );
  OAI21xp33_ASAP7_75t_R U129 ( .A1(n84), .A2(data_in_8_), .B(n83), .Y(n11) );
  NOR2xp33_ASAP7_75t_R U130 ( .A(n83), .B(n82), .Y(n81) );
  NAND2xp33_ASAP7_75t_R U131 ( .A(n81), .B(data_in_10_), .Y(n80) );
  OAI21xp33_ASAP7_75t_R U132 ( .A1(n81), .A2(data_in_10_), .B(n80), .Y(n13) );
  NOR2xp33_ASAP7_75t_R U133 ( .A(n80), .B(n79), .Y(n78) );
  NAND2xp33_ASAP7_75t_R U134 ( .A(n78), .B(data_in_12_), .Y(n77) );
  OAI21xp33_ASAP7_75t_R U135 ( .A1(n78), .A2(data_in_12_), .B(n77), .Y(n15) );
  NOR2xp33_ASAP7_75t_R U136 ( .A(n77), .B(n76), .Y(n75) );
  NAND2xp33_ASAP7_75t_R U137 ( .A(n75), .B(data_in_14_), .Y(n74) );
  OAI21xp33_ASAP7_75t_R U138 ( .A1(n75), .A2(data_in_14_), .B(n74), .Y(n17) );
  XOR2xp5_ASAP7_75t_R U139 ( .A(data_in_15_), .B(n74), .Y(n18) );
  OR2x2_ASAP7_75t_R U140 ( .A(data_in_2_), .B(n21), .Y(n33) );
  OR2x2_ASAP7_75t_R U141 ( .A(data_in_4_), .B(n21), .Y(n37) );
  OR2x2_ASAP7_75t_R U142 ( .A(data_in_14_), .B(n21), .Y(n57) );
  OR2x2_ASAP7_75t_R U143 ( .A(data_in_15_), .B(n21), .Y(n59) );
  OR2x2_ASAP7_75t_R U144 ( .A(data_in_10_), .B(n21), .Y(n49) );
  OR2x2_ASAP7_75t_R U145 ( .A(data_in_6_), .B(n21), .Y(n41) );
  OR2x2_ASAP7_75t_R U146 ( .A(data_in_8_), .B(n21), .Y(n45) );
  OR2x2_ASAP7_75t_R U147 ( .A(data_in_12_), .B(n21), .Y(n53) );
  AO21x1_ASAP7_75t_R U148 ( .A1(n77), .A2(n76), .B(n75), .Y(n16) );
  AO21x1_ASAP7_75t_R U149 ( .A1(n80), .A2(n79), .B(n78), .Y(n14) );
  AO21x1_ASAP7_75t_R U150 ( .A1(n83), .A2(n82), .B(n81), .Y(n12) );
  AO21x1_ASAP7_75t_R U151 ( .A1(n86), .A2(n85), .B(n84), .Y(n10) );
  AO21x1_ASAP7_75t_R U152 ( .A1(n89), .A2(n88), .B(n87), .Y(n8) );
  AO21x1_ASAP7_75t_R U153 ( .A1(n92), .A2(n91), .B(n90), .Y(n6) );
  AO21x1_ASAP7_75t_R U154 ( .A1(n95), .A2(n94), .B(n93), .Y(n4) );
  INVx1_ASAP7_75t_R U155 ( .A(n21), .Y(n96) );
endmodule

