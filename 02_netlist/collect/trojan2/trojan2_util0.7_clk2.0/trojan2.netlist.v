/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:40:40 2026
/////////////////////////////////////////////////////////////


module trojan2 ( clk, rst, data_in_7_, data_in_6_, data_in_5_, data_in_4_, 
        data_in_3_, data_in_2_, data_in_1_, data_in_0_, force_reset );
  input clk, rst, data_in_7_, data_in_6_, data_in_5_, data_in_4_, data_in_3_,
         data_in_2_, data_in_1_, data_in_0_;
  output force_reset;
  wire   trigger, n6, n7, n8, n9, n12, n15, n18, n21, n24, n27, n30, n33, n34,
         n35, n36;

  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_7_ ( .D(data_in_7_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n30) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_6_ ( .D(data_in_6_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n27) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_5_ ( .D(data_in_5_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n24) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_4_ ( .D(data_in_4_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n21) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_3_ ( .D(data_in_3_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n18) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_2_ ( .D(data_in_2_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n15) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_1_ ( .D(data_in_1_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n12) );
  DFFASRHQNx1_ASAP7_75t_R prev_data_reg_0_ ( .D(data_in_0_), .CLK(clk), 
        .RESETN(n8), .SETN(n7), .QN(n9) );
  DFFASRHQNx1_ASAP7_75t_R force_reset_reg ( .D(trigger), .CLK(clk), .RESETN(n8), .SETN(n7), .QN(n6) );
  INVx1_ASAP7_75t_R U5 ( .A(rst), .Y(n8) );
  TIEHIx1_ASAP7_75t_R U11 ( .H(n7) );
  INVxp33_ASAP7_75t_R U12 ( .A(n6), .Y(force_reset) );
  OR4x1_ASAP7_75t_R U13 ( .A(data_in_1_), .B(data_in_3_), .C(data_in_5_), .D(
        data_in_7_), .Y(n36) );
  NAND4xp25_ASAP7_75t_R U14 ( .A(data_in_4_), .B(data_in_6_), .C(data_in_0_), 
        .D(data_in_2_), .Y(n35) );
  OR4x1_ASAP7_75t_R U15 ( .A(n12), .B(n18), .C(n24), .D(n30), .Y(n34) );
  NAND4xp25_ASAP7_75t_R U16 ( .A(n21), .B(n27), .C(n9), .D(n15), .Y(n33) );
  NOR4xp25_ASAP7_75t_R U17 ( .A(n36), .B(n35), .C(n34), .D(n33), .Y(trigger)
         );
endmodule

