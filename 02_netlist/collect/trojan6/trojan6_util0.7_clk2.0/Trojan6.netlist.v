/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:48:17 2026
/////////////////////////////////////////////////////////////


module Trojan6 ( m0_data_o_31_, m0_data_o_30_, m0_data_o_29_, m0_data_o_28_, 
        m0_data_o_27_, m0_data_o_26_, m0_data_o_25_, m0_data_o_24_, 
        m0_data_o_23_, m0_data_o_22_, m0_data_o_21_, m0_data_o_20_, 
        m0_data_o_19_, m0_data_o_18_, m0_data_o_17_, m0_data_o_16_, 
        m0_data_o_15_, m0_data_o_14_, m0_data_o_13_, m0_data_o_12_, 
        m0_data_o_11_, m0_data_o_10_, m0_data_o_9_, m0_data_o_8_, m0_data_o_7_, 
        m0_data_o_6_, m0_data_o_5_, m0_data_o_4_, m0_data_o_3_, m0_data_o_2_, 
        m0_data_o_1_, m0_data_o_0_, i_s15_data_o_31_, i_s15_data_o_30_, 
        i_s15_data_o_29_, i_s15_data_o_28_, i_s15_data_o_27_, i_s15_data_o_26_, 
        i_s15_data_o_25_, i_s15_data_o_24_, i_s15_data_o_23_, i_s15_data_o_22_, 
        i_s15_data_o_21_, i_s15_data_o_20_, i_s15_data_o_19_, i_s15_data_o_18_, 
        i_s15_data_o_17_, i_s15_data_o_16_, i_s15_data_o_15_, i_s15_data_o_14_, 
        i_s15_data_o_13_, i_s15_data_o_12_, i_s15_data_o_11_, i_s15_data_o_10_, 
        i_s15_data_o_9_, i_s15_data_o_8_, i_s15_data_o_7_, i_s15_data_o_6_, 
        i_s15_data_o_5_, i_s15_data_o_4_, i_s15_data_o_3_, i_s15_data_o_2_, 
        i_s15_data_o_1_, i_s15_data_o_0_, i_s15_data_o_TrojanPayload_31_, 
        i_s15_data_o_TrojanPayload_30_, i_s15_data_o_TrojanPayload_29_, 
        i_s15_data_o_TrojanPayload_28_, i_s15_data_o_TrojanPayload_27_, 
        i_s15_data_o_TrojanPayload_26_, i_s15_data_o_TrojanPayload_25_, 
        i_s15_data_o_TrojanPayload_24_, i_s15_data_o_TrojanPayload_23_, 
        i_s15_data_o_TrojanPayload_22_, i_s15_data_o_TrojanPayload_21_, 
        i_s15_data_o_TrojanPayload_20_, i_s15_data_o_TrojanPayload_19_, 
        i_s15_data_o_TrojanPayload_18_, i_s15_data_o_TrojanPayload_17_, 
        i_s15_data_o_TrojanPayload_16_, i_s15_data_o_TrojanPayload_15_, 
        i_s15_data_o_TrojanPayload_14_, i_s15_data_o_TrojanPayload_13_, 
        i_s15_data_o_TrojanPayload_12_, i_s15_data_o_TrojanPayload_11_, 
        i_s15_data_o_TrojanPayload_10_, i_s15_data_o_TrojanPayload_9_, 
        i_s15_data_o_TrojanPayload_8_, i_s15_data_o_TrojanPayload_7_, 
        i_s15_data_o_TrojanPayload_6_, i_s15_data_o_TrojanPayload_5_, 
        i_s15_data_o_TrojanPayload_4_, i_s15_data_o_TrojanPayload_3_, 
        i_s15_data_o_TrojanPayload_2_, i_s15_data_o_TrojanPayload_1_, 
        i_s15_data_o_TrojanPayload_0_ );
  input m0_data_o_31_, m0_data_o_30_, m0_data_o_29_, m0_data_o_28_,
         m0_data_o_27_, m0_data_o_26_, m0_data_o_25_, m0_data_o_24_,
         m0_data_o_23_, m0_data_o_22_, m0_data_o_21_, m0_data_o_20_,
         m0_data_o_19_, m0_data_o_18_, m0_data_o_17_, m0_data_o_16_,
         m0_data_o_15_, m0_data_o_14_, m0_data_o_13_, m0_data_o_12_,
         m0_data_o_11_, m0_data_o_10_, m0_data_o_9_, m0_data_o_8_,
         m0_data_o_7_, m0_data_o_6_, m0_data_o_5_, m0_data_o_4_, m0_data_o_3_,
         m0_data_o_2_, m0_data_o_1_, m0_data_o_0_, i_s15_data_o_31_,
         i_s15_data_o_30_, i_s15_data_o_29_, i_s15_data_o_28_,
         i_s15_data_o_27_, i_s15_data_o_26_, i_s15_data_o_25_,
         i_s15_data_o_24_, i_s15_data_o_23_, i_s15_data_o_22_,
         i_s15_data_o_21_, i_s15_data_o_20_, i_s15_data_o_19_,
         i_s15_data_o_18_, i_s15_data_o_17_, i_s15_data_o_16_,
         i_s15_data_o_15_, i_s15_data_o_14_, i_s15_data_o_13_,
         i_s15_data_o_12_, i_s15_data_o_11_, i_s15_data_o_10_, i_s15_data_o_9_,
         i_s15_data_o_8_, i_s15_data_o_7_, i_s15_data_o_6_, i_s15_data_o_5_,
         i_s15_data_o_4_, i_s15_data_o_3_, i_s15_data_o_2_, i_s15_data_o_1_,
         i_s15_data_o_0_;
  output i_s15_data_o_TrojanPayload_31_, i_s15_data_o_TrojanPayload_30_,
         i_s15_data_o_TrojanPayload_29_, i_s15_data_o_TrojanPayload_28_,
         i_s15_data_o_TrojanPayload_27_, i_s15_data_o_TrojanPayload_26_,
         i_s15_data_o_TrojanPayload_25_, i_s15_data_o_TrojanPayload_24_,
         i_s15_data_o_TrojanPayload_23_, i_s15_data_o_TrojanPayload_22_,
         i_s15_data_o_TrojanPayload_21_, i_s15_data_o_TrojanPayload_20_,
         i_s15_data_o_TrojanPayload_19_, i_s15_data_o_TrojanPayload_18_,
         i_s15_data_o_TrojanPayload_17_, i_s15_data_o_TrojanPayload_16_,
         i_s15_data_o_TrojanPayload_15_, i_s15_data_o_TrojanPayload_14_,
         i_s15_data_o_TrojanPayload_13_, i_s15_data_o_TrojanPayload_12_,
         i_s15_data_o_TrojanPayload_11_, i_s15_data_o_TrojanPayload_10_,
         i_s15_data_o_TrojanPayload_9_, i_s15_data_o_TrojanPayload_8_,
         i_s15_data_o_TrojanPayload_7_, i_s15_data_o_TrojanPayload_6_,
         i_s15_data_o_TrojanPayload_5_, i_s15_data_o_TrojanPayload_4_,
         i_s15_data_o_TrojanPayload_3_, i_s15_data_o_TrojanPayload_2_,
         i_s15_data_o_TrojanPayload_1_, i_s15_data_o_TrojanPayload_0_;
  wire   i_s15_data_o_31_, i_s15_data_o_30_, i_s15_data_o_29_,
         i_s15_data_o_28_, i_s15_data_o_27_, i_s15_data_o_26_,
         i_s15_data_o_25_, i_s15_data_o_24_, i_s15_data_o_23_,
         i_s15_data_o_22_, i_s15_data_o_21_, i_s15_data_o_20_,
         i_s15_data_o_19_, i_s15_data_o_18_, i_s15_data_o_17_,
         i_s15_data_o_16_, i_s15_data_o_15_, i_s15_data_o_14_,
         i_s15_data_o_13_, i_s15_data_o_12_, i_s15_data_o_11_,
         i_s15_data_o_10_, i_s15_data_o_9_, i_s15_data_o_8_, i_s15_data_o_7_,
         i_s15_data_o_6_, i_s15_data_o_5_, i_s15_data_o_4_, i_s15_data_o_3_,
         i_s15_data_o_2_, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22,
         n23, n24;
  assign i_s15_data_o_TrojanPayload_31_ = i_s15_data_o_31_;
  assign i_s15_data_o_TrojanPayload_30_ = i_s15_data_o_30_;
  assign i_s15_data_o_TrojanPayload_29_ = i_s15_data_o_29_;
  assign i_s15_data_o_TrojanPayload_28_ = i_s15_data_o_28_;
  assign i_s15_data_o_TrojanPayload_27_ = i_s15_data_o_27_;
  assign i_s15_data_o_TrojanPayload_26_ = i_s15_data_o_26_;
  assign i_s15_data_o_TrojanPayload_25_ = i_s15_data_o_25_;
  assign i_s15_data_o_TrojanPayload_24_ = i_s15_data_o_24_;
  assign i_s15_data_o_TrojanPayload_23_ = i_s15_data_o_23_;
  assign i_s15_data_o_TrojanPayload_22_ = i_s15_data_o_22_;
  assign i_s15_data_o_TrojanPayload_21_ = i_s15_data_o_21_;
  assign i_s15_data_o_TrojanPayload_20_ = i_s15_data_o_20_;
  assign i_s15_data_o_TrojanPayload_19_ = i_s15_data_o_19_;
  assign i_s15_data_o_TrojanPayload_18_ = i_s15_data_o_18_;
  assign i_s15_data_o_TrojanPayload_17_ = i_s15_data_o_17_;
  assign i_s15_data_o_TrojanPayload_16_ = i_s15_data_o_16_;
  assign i_s15_data_o_TrojanPayload_15_ = i_s15_data_o_15_;
  assign i_s15_data_o_TrojanPayload_14_ = i_s15_data_o_14_;
  assign i_s15_data_o_TrojanPayload_13_ = i_s15_data_o_13_;
  assign i_s15_data_o_TrojanPayload_12_ = i_s15_data_o_12_;
  assign i_s15_data_o_TrojanPayload_11_ = i_s15_data_o_11_;
  assign i_s15_data_o_TrojanPayload_10_ = i_s15_data_o_10_;
  assign i_s15_data_o_TrojanPayload_9_ = i_s15_data_o_9_;
  assign i_s15_data_o_TrojanPayload_8_ = i_s15_data_o_8_;
  assign i_s15_data_o_TrojanPayload_7_ = i_s15_data_o_7_;
  assign i_s15_data_o_TrojanPayload_6_ = i_s15_data_o_6_;
  assign i_s15_data_o_TrojanPayload_5_ = i_s15_data_o_5_;
  assign i_s15_data_o_TrojanPayload_4_ = i_s15_data_o_4_;
  assign i_s15_data_o_TrojanPayload_3_ = i_s15_data_o_3_;
  assign i_s15_data_o_TrojanPayload_2_ = i_s15_data_o_2_;

  NAND4xp25_ASAP7_75t_R U17 ( .A(m0_data_o_4_), .B(m0_data_o_7_), .C(
        m0_data_o_5_), .D(m0_data_o_3_), .Y(n23) );
  NAND4xp25_ASAP7_75t_R U18 ( .A(m0_data_o_21_), .B(m0_data_o_12_), .C(
        m0_data_o_16_), .D(m0_data_o_13_), .Y(n22) );
  NAND4xp25_ASAP7_75t_R U19 ( .A(m0_data_o_27_), .B(m0_data_o_19_), .C(
        m0_data_o_25_), .D(m0_data_o_14_), .Y(n13) );
  NOR3xp33_ASAP7_75t_R U20 ( .A(m0_data_o_10_), .B(m0_data_o_18_), .C(n13), 
        .Y(n20) );
  NOR4xp25_ASAP7_75t_R U21 ( .A(m0_data_o_24_), .B(m0_data_o_22_), .C(
        m0_data_o_20_), .D(m0_data_o_17_), .Y(n17) );
  NOR4xp25_ASAP7_75t_R U22 ( .A(m0_data_o_29_), .B(m0_data_o_31_), .C(
        m0_data_o_28_), .D(m0_data_o_26_), .Y(n16) );
  NOR4xp25_ASAP7_75t_R U23 ( .A(m0_data_o_1_), .B(m0_data_o_0_), .C(
        m0_data_o_8_), .D(m0_data_o_9_), .Y(n15) );
  NOR4xp25_ASAP7_75t_R U24 ( .A(m0_data_o_15_), .B(m0_data_o_11_), .C(
        m0_data_o_6_), .D(m0_data_o_2_), .Y(n14) );
  NAND4xp25_ASAP7_75t_R U25 ( .A(n17), .B(n16), .C(n15), .D(n14), .Y(n18) );
  NOR2xp33_ASAP7_75t_R U26 ( .A(n18), .B(m0_data_o_30_), .Y(n19) );
  NAND3xp33_ASAP7_75t_R U27 ( .A(m0_data_o_23_), .B(n20), .C(n19), .Y(n21) );
  NOR3xp33_ASAP7_75t_R U28 ( .A(n23), .B(n22), .C(n21), .Y(n24) );
  OR2x2_ASAP7_75t_R U29 ( .A(n24), .B(i_s15_data_o_0_), .Y(
        i_s15_data_o_TrojanPayload_0_) );
  OR2x2_ASAP7_75t_R U30 ( .A(n24), .B(i_s15_data_o_1_), .Y(
        i_s15_data_o_TrojanPayload_1_) );
endmodule

