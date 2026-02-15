/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:38:45 2026
/////////////////////////////////////////////////////////////


module trojan1 ( clk, rst, r1, trigger );
  input clk, rst, r1;
  output trigger;
  wire   counter_2_, counter_1_, counter_0_, n6, n10, n11, n12, n13, n14, n15,
         n16, n17, n18, n19, n20;

  DFFHQNx1_ASAP7_75t_R counter_reg_0_ ( .D(n13), .CLK(clk), .QN(counter_0_) );
  DFFHQNx1_ASAP7_75t_R counter_reg_1_ ( .D(n12), .CLK(clk), .QN(counter_1_) );
  DFFHQNx1_ASAP7_75t_R counter_reg_2_ ( .D(n11), .CLK(clk), .QN(counter_2_) );
  DFFHQNx1_ASAP7_75t_R counter_reg_3_ ( .D(n10), .CLK(clk), .QN(trigger) );
  INVx1_ASAP7_75t_R U10 ( .A(rst), .Y(n6) );
  NAND3xp33_ASAP7_75t_R U16 ( .A(rst), .B(counter_0_), .C(r1), .Y(n14) );
  A2O1A1Ixp33_ASAP7_75t_R U17 ( .A1(counter_0_), .A2(rst), .B(r1), .C(n14), 
        .Y(n13) );
  AOI31xp33_ASAP7_75t_R U18 ( .A1(counter_1_), .A2(counter_0_), .A3(r1), .B(n6), .Y(n15) );
  A2O1A1Ixp33_ASAP7_75t_R U19 ( .A1(counter_0_), .A2(r1), .B(counter_1_), .C(
        n15), .Y(n12) );
  NAND4xp25_ASAP7_75t_R U20 ( .A(rst), .B(counter_0_), .C(r1), .D(counter_1_), 
        .Y(n18) );
  INVxp33_ASAP7_75t_R U21 ( .A(counter_2_), .Y(n17) );
  INVxp33_ASAP7_75t_R U22 ( .A(n18), .Y(n16) );
  AOI32xp33_ASAP7_75t_R U23 ( .A1(counter_2_), .A2(n18), .A3(rst), .B1(n17), 
        .B2(n16), .Y(n11) );
  NOR2xp33_ASAP7_75t_R U24 ( .A(n18), .B(n17), .Y(n20) );
  NAND2xp33_ASAP7_75t_R U25 ( .A(trigger), .B(n20), .Y(n19) );
  OAI211xp5_ASAP7_75t_R U26 ( .A1(trigger), .A2(n20), .B(n19), .C(rst), .Y(n10) );
endmodule

