/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:46:23 2026
/////////////////////////////////////////////////////////////


module Trojan5 ( pon_rst_n_i, prog_dat_i_13_, prog_dat_i_12_, prog_dat_i_11_, 
        prog_dat_i_10_, prog_dat_i_9_, prog_dat_i_8_, prog_dat_i_7_, 
        prog_dat_i_6_, prog_dat_i_5_, prog_dat_i_4_, prog_dat_i_3_, 
        prog_dat_i_2_, prog_dat_i_1_, prog_dat_i_0_, pc_reg_12_, pc_reg_11_, 
        pc_reg_10_, pc_reg_9_, pc_reg_8_, pc_reg_7_, pc_reg_6_, pc_reg_5_, 
        pc_reg_4_, pc_reg_3_, pc_reg_2_, pc_reg_1_, pc_reg_0_, prog_adr_o_12_, 
        prog_adr_o_11_, prog_adr_o_10_, prog_adr_o_9_, prog_adr_o_8_, 
        prog_adr_o_7_, prog_adr_o_6_, prog_adr_o_5_, prog_adr_o_4_, 
        prog_adr_o_3_, prog_adr_o_2_, prog_adr_o_1_, prog_adr_o_0_ );
  input pon_rst_n_i, prog_dat_i_13_, prog_dat_i_12_, prog_dat_i_11_,
         prog_dat_i_10_, prog_dat_i_9_, prog_dat_i_8_, prog_dat_i_7_,
         prog_dat_i_6_, prog_dat_i_5_, prog_dat_i_4_, prog_dat_i_3_,
         prog_dat_i_2_, prog_dat_i_1_, prog_dat_i_0_, pc_reg_12_, pc_reg_11_,
         pc_reg_10_, pc_reg_9_, pc_reg_8_, pc_reg_7_, pc_reg_6_, pc_reg_5_,
         pc_reg_4_, pc_reg_3_, pc_reg_2_, pc_reg_1_, pc_reg_0_;
  output prog_adr_o_12_, prog_adr_o_11_, prog_adr_o_10_, prog_adr_o_9_,
         prog_adr_o_8_, prog_adr_o_7_, prog_adr_o_6_, prog_adr_o_5_,
         prog_adr_o_4_, prog_adr_o_3_, prog_adr_o_2_, prog_adr_o_1_,
         prog_adr_o_0_;
  wire   pc_reg_0_, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14,
         n15, n16, n17, n18, n19;
  assign prog_adr_o_0_ = pc_reg_0_;

  OAI211xp5_ASAP7_75t_R U5 ( .A1(prog_dat_i_11_), .A2(prog_dat_i_10_), .B(
        prog_dat_i_13_), .C(prog_dat_i_12_), .Y(n2) );
  OA211x2_ASAP7_75t_R U6 ( .A1(prog_dat_i_13_), .A2(prog_dat_i_12_), .B(
        pon_rst_n_i), .C(n2), .Y(n11) );
  NAND2xp33_ASAP7_75t_R U7 ( .A(n11), .B(pc_reg_1_), .Y(n10) );
  INVxp33_ASAP7_75t_R U8 ( .A(pc_reg_2_), .Y(n7) );
  NOR2xp33_ASAP7_75t_R U9 ( .A(n10), .B(n7), .Y(n13) );
  NAND2xp33_ASAP7_75t_R U10 ( .A(n13), .B(pc_reg_3_), .Y(n12) );
  INVxp33_ASAP7_75t_R U11 ( .A(pc_reg_4_), .Y(n6) );
  NOR2xp33_ASAP7_75t_R U12 ( .A(n12), .B(n6), .Y(n15) );
  NAND2xp33_ASAP7_75t_R U13 ( .A(n15), .B(pc_reg_5_), .Y(n14) );
  INVxp33_ASAP7_75t_R U14 ( .A(pc_reg_6_), .Y(n5) );
  NOR2xp33_ASAP7_75t_R U15 ( .A(n14), .B(n5), .Y(n17) );
  NAND2xp33_ASAP7_75t_R U16 ( .A(n17), .B(pc_reg_7_), .Y(n16) );
  INVxp33_ASAP7_75t_R U17 ( .A(pc_reg_8_), .Y(n4) );
  NOR2xp33_ASAP7_75t_R U18 ( .A(n16), .B(n4), .Y(n19) );
  NAND2xp33_ASAP7_75t_R U19 ( .A(n19), .B(pc_reg_9_), .Y(n18) );
  INVxp33_ASAP7_75t_R U20 ( .A(pc_reg_10_), .Y(n3) );
  NOR2xp33_ASAP7_75t_R U21 ( .A(n18), .B(n3), .Y(n8) );
  AOI21xp33_ASAP7_75t_R U22 ( .A1(n18), .A2(n3), .B(n8), .Y(prog_adr_o_10_) );
  AOI21xp33_ASAP7_75t_R U23 ( .A1(n16), .A2(n4), .B(n19), .Y(prog_adr_o_8_) );
  AOI21xp33_ASAP7_75t_R U24 ( .A1(n14), .A2(n5), .B(n17), .Y(prog_adr_o_6_) );
  AOI21xp33_ASAP7_75t_R U25 ( .A1(n12), .A2(n6), .B(n15), .Y(prog_adr_o_4_) );
  AOI21xp33_ASAP7_75t_R U26 ( .A1(n10), .A2(n7), .B(n13), .Y(prog_adr_o_2_) );
  NAND2xp33_ASAP7_75t_R U27 ( .A(n8), .B(pc_reg_11_), .Y(n9) );
  OA21x2_ASAP7_75t_R U28 ( .A1(n8), .A2(pc_reg_11_), .B(n9), .Y(prog_adr_o_11_) );
  HAxp5_ASAP7_75t_R U29 ( .A(pc_reg_12_), .B(n9), .SN(prog_adr_o_12_) );
  OA21x2_ASAP7_75t_R U30 ( .A1(n11), .A2(pc_reg_1_), .B(n10), .Y(prog_adr_o_1_) );
  OA21x2_ASAP7_75t_R U31 ( .A1(n13), .A2(pc_reg_3_), .B(n12), .Y(prog_adr_o_3_) );
  OA21x2_ASAP7_75t_R U32 ( .A1(n15), .A2(pc_reg_5_), .B(n14), .Y(prog_adr_o_5_) );
  OA21x2_ASAP7_75t_R U33 ( .A1(n17), .A2(pc_reg_7_), .B(n16), .Y(prog_adr_o_7_) );
  OA21x2_ASAP7_75t_R U34 ( .A1(n19), .A2(pc_reg_9_), .B(n18), .Y(prog_adr_o_9_) );
endmodule

