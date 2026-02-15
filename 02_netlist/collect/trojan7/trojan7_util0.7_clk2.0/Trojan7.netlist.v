/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:50:11 2026
/////////////////////////////////////////////////////////////


module Trojan7 ( wb_addr_i_31_, wb_addr_i_30_, wb_addr_i_29_, wb_addr_i_28_, 
        wb_addr_i_27_, wb_addr_i_26_, wb_addr_i_25_, wb_addr_i_24_, 
        wb_addr_i_23_, wb_addr_i_22_, wb_addr_i_21_, wb_addr_i_20_, 
        wb_addr_i_19_, wb_addr_i_18_, wb_addr_i_17_, wb_addr_i_16_, 
        wb_addr_i_15_, wb_addr_i_14_, wb_addr_i_13_, wb_addr_i_12_, 
        wb_addr_i_11_, wb_addr_i_10_, wb_addr_i_9_, wb_addr_i_8_, wb_addr_i_7_, 
        wb_addr_i_6_, wb_addr_i_5_, wb_addr_i_4_, wb_addr_i_3_, wb_addr_i_2_, 
        wb_addr_i_1_, wb_addr_i_0_, wb_data_i_31_, wb_data_i_30_, 
        wb_data_i_29_, wb_data_i_28_, wb_data_i_27_, wb_data_i_26_, 
        wb_data_i_25_, wb_data_i_24_, wb_data_i_23_, wb_data_i_22_, 
        wb_data_i_21_, wb_data_i_20_, wb_data_i_19_, wb_data_i_18_, 
        wb_data_i_17_, wb_data_i_16_, wb_data_i_15_, wb_data_i_14_, 
        wb_data_i_13_, wb_data_i_12_, wb_data_i_11_, wb_data_i_10_, 
        wb_data_i_9_, wb_data_i_8_, wb_data_i_7_, wb_data_i_6_, wb_data_i_5_, 
        wb_data_i_4_, wb_data_i_3_, wb_data_i_2_, wb_data_i_1_, wb_data_i_0_, 
        s0_data_i_31_, s0_data_i_30_, s0_data_i_29_, s0_data_i_28_, 
        s0_data_i_27_, s0_data_i_26_, s0_data_i_25_, s0_data_i_24_, 
        s0_data_i_23_, s0_data_i_22_, s0_data_i_21_, s0_data_i_20_, 
        s0_data_i_19_, s0_data_i_18_, s0_data_i_17_, s0_data_i_16_, 
        s0_data_i_15_, s0_data_i_14_, s0_data_i_13_, s0_data_i_12_, 
        s0_data_i_11_, s0_data_i_10_, s0_data_i_9_, s0_data_i_8_, s0_data_i_7_, 
        s0_data_i_6_, s0_data_i_5_, s0_data_i_4_, s0_data_i_3_, s0_data_i_2_, 
        s0_data_i_1_, s0_data_i_0_, slv_sel_3_, slv_sel_2_, slv_sel_1_, 
        slv_sel_0_ );
  input wb_addr_i_31_, wb_addr_i_30_, wb_addr_i_29_, wb_addr_i_28_,
         wb_addr_i_27_, wb_addr_i_26_, wb_addr_i_25_, wb_addr_i_24_,
         wb_addr_i_23_, wb_addr_i_22_, wb_addr_i_21_, wb_addr_i_20_,
         wb_addr_i_19_, wb_addr_i_18_, wb_addr_i_17_, wb_addr_i_16_,
         wb_addr_i_15_, wb_addr_i_14_, wb_addr_i_13_, wb_addr_i_12_,
         wb_addr_i_11_, wb_addr_i_10_, wb_addr_i_9_, wb_addr_i_8_,
         wb_addr_i_7_, wb_addr_i_6_, wb_addr_i_5_, wb_addr_i_4_, wb_addr_i_3_,
         wb_addr_i_2_, wb_addr_i_1_, wb_addr_i_0_, wb_data_i_31_,
         wb_data_i_30_, wb_data_i_29_, wb_data_i_28_, wb_data_i_27_,
         wb_data_i_26_, wb_data_i_25_, wb_data_i_24_, wb_data_i_23_,
         wb_data_i_22_, wb_data_i_21_, wb_data_i_20_, wb_data_i_19_,
         wb_data_i_18_, wb_data_i_17_, wb_data_i_16_, wb_data_i_15_,
         wb_data_i_14_, wb_data_i_13_, wb_data_i_12_, wb_data_i_11_,
         wb_data_i_10_, wb_data_i_9_, wb_data_i_8_, wb_data_i_7_, wb_data_i_6_,
         wb_data_i_5_, wb_data_i_4_, wb_data_i_3_, wb_data_i_2_, wb_data_i_1_,
         wb_data_i_0_, s0_data_i_31_, s0_data_i_30_, s0_data_i_29_,
         s0_data_i_28_, s0_data_i_27_, s0_data_i_26_, s0_data_i_25_,
         s0_data_i_24_, s0_data_i_23_, s0_data_i_22_, s0_data_i_21_,
         s0_data_i_20_, s0_data_i_19_, s0_data_i_18_, s0_data_i_17_,
         s0_data_i_16_, s0_data_i_15_, s0_data_i_14_, s0_data_i_13_,
         s0_data_i_12_, s0_data_i_11_, s0_data_i_10_, s0_data_i_9_,
         s0_data_i_8_, s0_data_i_7_, s0_data_i_6_, s0_data_i_5_, s0_data_i_4_,
         s0_data_i_3_, s0_data_i_2_, s0_data_i_1_, s0_data_i_0_;
  output slv_sel_3_, slv_sel_2_, slv_sel_1_, slv_sel_0_;
  wire   n22, n23, n24, n25, n26, n27, n28, n29, n30, n31, n32, n33, n34, n35,
         n36, n37, n38, n39, n40, n41, n42;

  NOR4xp25_ASAP7_75t_R U26 ( .A(s0_data_i_0_), .B(s0_data_i_1_), .C(
        s0_data_i_4_), .D(s0_data_i_6_), .Y(n25) );
  NOR4xp25_ASAP7_75t_R U27 ( .A(s0_data_i_8_), .B(s0_data_i_10_), .C(
        s0_data_i_11_), .D(s0_data_i_13_), .Y(n24) );
  NOR4xp25_ASAP7_75t_R U28 ( .A(s0_data_i_15_), .B(s0_data_i_17_), .C(
        s0_data_i_19_), .D(s0_data_i_21_), .Y(n23) );
  NOR4xp25_ASAP7_75t_R U29 ( .A(s0_data_i_23_), .B(s0_data_i_24_), .C(
        s0_data_i_29_), .D(s0_data_i_30_), .Y(n22) );
  AND4x1_ASAP7_75t_R U30 ( .A(n25), .B(n24), .C(n23), .D(n22), .Y(n41) );
  NOR4xp25_ASAP7_75t_R U31 ( .A(s0_data_i_31_), .B(wb_data_i_0_), .C(
        wb_data_i_1_), .D(wb_data_i_2_), .Y(n29) );
  NOR4xp25_ASAP7_75t_R U32 ( .A(wb_data_i_3_), .B(wb_data_i_4_), .C(
        wb_data_i_8_), .D(wb_data_i_9_), .Y(n28) );
  NOR4xp25_ASAP7_75t_R U33 ( .A(wb_data_i_14_), .B(wb_data_i_16_), .C(
        wb_data_i_18_), .D(wb_data_i_24_), .Y(n27) );
  NOR4xp25_ASAP7_75t_R U34 ( .A(wb_data_i_26_), .B(wb_data_i_28_), .C(
        wb_data_i_30_), .D(wb_data_i_31_), .Y(n26) );
  AND4x1_ASAP7_75t_R U35 ( .A(n29), .B(n28), .C(n27), .D(n26), .Y(n40) );
  NAND4xp25_ASAP7_75t_R U36 ( .A(s0_data_i_16_), .B(s0_data_i_14_), .C(
        s0_data_i_12_), .D(s0_data_i_9_), .Y(n33) );
  NAND4xp25_ASAP7_75t_R U37 ( .A(s0_data_i_7_), .B(s0_data_i_5_), .C(
        s0_data_i_3_), .D(s0_data_i_2_), .Y(n32) );
  NAND4xp25_ASAP7_75t_R U38 ( .A(wb_data_i_5_), .B(s0_data_i_28_), .C(
        s0_data_i_27_), .D(s0_data_i_26_), .Y(n31) );
  NAND4xp25_ASAP7_75t_R U39 ( .A(s0_data_i_25_), .B(s0_data_i_22_), .C(
        s0_data_i_20_), .D(s0_data_i_18_), .Y(n30) );
  NOR4xp25_ASAP7_75t_R U40 ( .A(n33), .B(n32), .C(n31), .D(n30), .Y(n39) );
  NAND4xp25_ASAP7_75t_R U41 ( .A(wb_data_i_17_), .B(wb_data_i_15_), .C(
        wb_data_i_13_), .D(wb_data_i_12_), .Y(n37) );
  NAND4xp25_ASAP7_75t_R U42 ( .A(wb_data_i_11_), .B(wb_data_i_10_), .C(
        wb_data_i_7_), .D(wb_data_i_6_), .Y(n36) );
  NAND4xp25_ASAP7_75t_R U43 ( .A(wb_data_i_29_), .B(wb_data_i_27_), .C(
        wb_data_i_25_), .D(wb_data_i_23_), .Y(n35) );
  NAND4xp25_ASAP7_75t_R U44 ( .A(wb_data_i_22_), .B(wb_data_i_21_), .C(
        wb_data_i_20_), .D(wb_data_i_19_), .Y(n34) );
  NOR4xp25_ASAP7_75t_R U45 ( .A(n37), .B(n36), .C(n35), .D(n34), .Y(n38) );
  NAND4xp25_ASAP7_75t_R U46 ( .A(n41), .B(n40), .C(n39), .D(n38), .Y(n42) );
  HAxp5_ASAP7_75t_R U47 ( .A(wb_addr_i_28_), .B(n42), .SN(slv_sel_0_) );
  HAxp5_ASAP7_75t_R U48 ( .A(wb_addr_i_29_), .B(n42), .SN(slv_sel_1_) );
  HAxp5_ASAP7_75t_R U49 ( .A(wb_addr_i_30_), .B(n42), .SN(slv_sel_2_) );
  HAxp5_ASAP7_75t_R U50 ( .A(wb_addr_i_31_), .B(n42), .SN(slv_sel_3_) );
endmodule

