/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Ultra(TM) in wire load mode
// Version   : W-2024.09-SP3
// Date      : Sat Feb 14 08:36:52 2026
/////////////////////////////////////////////////////////////


module trojan0 ( clk, rst, key_127_, key_126_, key_125_, key_124_, key_123_, 
        key_122_, key_121_, key_120_, key_119_, key_118_, key_117_, key_116_, 
        key_115_, key_114_, key_113_, key_112_, key_111_, key_110_, key_109_, 
        key_108_, key_107_, key_106_, key_105_, key_104_, key_103_, key_102_, 
        key_101_, key_100_, key_99_, key_98_, key_97_, key_96_, key_95_, 
        key_94_, key_93_, key_92_, key_91_, key_90_, key_89_, key_88_, key_87_, 
        key_86_, key_85_, key_84_, key_83_, key_82_, key_81_, key_80_, key_79_, 
        key_78_, key_77_, key_76_, key_75_, key_74_, key_73_, key_72_, key_71_, 
        key_70_, key_69_, key_68_, key_67_, key_66_, key_65_, key_64_, key_63_, 
        key_62_, key_61_, key_60_, key_59_, key_58_, key_57_, key_56_, key_55_, 
        key_54_, key_53_, key_52_, key_51_, key_50_, key_49_, key_48_, key_47_, 
        key_46_, key_45_, key_44_, key_43_, key_42_, key_41_, key_40_, key_39_, 
        key_38_, key_37_, key_36_, key_35_, key_34_, key_33_, key_32_, key_31_, 
        key_30_, key_29_, key_28_, key_27_, key_26_, key_25_, key_24_, key_23_, 
        key_22_, key_21_, key_20_, key_19_, key_18_, key_17_, key_16_, key_15_, 
        key_14_, key_13_, key_12_, key_11_, key_10_, key_9_, key_8_, key_7_, 
        key_6_, key_5_, key_4_, key_3_, key_2_, key_1_, key_0_, load_63_, 
        load_62_, load_61_, load_60_, load_59_, load_58_, load_57_, load_56_, 
        load_55_, load_54_, load_53_, load_52_, load_51_, load_50_, load_49_, 
        load_48_, load_47_, load_46_, load_45_, load_44_, load_43_, load_42_, 
        load_41_, load_40_, load_39_, load_38_, load_37_, load_36_, load_35_, 
        load_34_, load_33_, load_32_, load_31_, load_30_, load_29_, load_28_, 
        load_27_, load_26_, load_25_, load_24_, load_23_, load_22_, load_21_, 
        load_20_, load_19_, load_18_, load_17_, load_16_, load_15_, load_14_, 
        load_13_, load_12_, load_11_, load_10_, load_9_, load_8_, load_7_, 
        load_6_, load_5_, load_4_, load_3_, load_2_, load_1_, load_0_ );
  input clk, rst, key_127_, key_126_, key_125_, key_124_, key_123_, key_122_,
         key_121_, key_120_, key_119_, key_118_, key_117_, key_116_, key_115_,
         key_114_, key_113_, key_112_, key_111_, key_110_, key_109_, key_108_,
         key_107_, key_106_, key_105_, key_104_, key_103_, key_102_, key_101_,
         key_100_, key_99_, key_98_, key_97_, key_96_, key_95_, key_94_,
         key_93_, key_92_, key_91_, key_90_, key_89_, key_88_, key_87_,
         key_86_, key_85_, key_84_, key_83_, key_82_, key_81_, key_80_,
         key_79_, key_78_, key_77_, key_76_, key_75_, key_74_, key_73_,
         key_72_, key_71_, key_70_, key_69_, key_68_, key_67_, key_66_,
         key_65_, key_64_, key_63_, key_62_, key_61_, key_60_, key_59_,
         key_58_, key_57_, key_56_, key_55_, key_54_, key_53_, key_52_,
         key_51_, key_50_, key_49_, key_48_, key_47_, key_46_, key_45_,
         key_44_, key_43_, key_42_, key_41_, key_40_, key_39_, key_38_,
         key_37_, key_36_, key_35_, key_34_, key_33_, key_32_, key_31_,
         key_30_, key_29_, key_28_, key_27_, key_26_, key_25_, key_24_,
         key_23_, key_22_, key_21_, key_20_, key_19_, key_18_, key_17_,
         key_16_, key_15_, key_14_, key_13_, key_12_, key_11_, key_10_, key_9_,
         key_8_, key_7_, key_6_, key_5_, key_4_, key_3_, key_2_, key_1_,
         key_0_;
  output load_63_, load_62_, load_61_, load_60_, load_59_, load_58_, load_57_,
         load_56_, load_55_, load_54_, load_53_, load_52_, load_51_, load_50_,
         load_49_, load_48_, load_47_, load_46_, load_45_, load_44_, load_43_,
         load_42_, load_41_, load_40_, load_39_, load_38_, load_37_, load_36_,
         load_35_, load_34_, load_33_, load_32_, load_31_, load_30_, load_29_,
         load_28_, load_27_, load_26_, load_25_, load_24_, load_23_, load_22_,
         load_21_, load_20_, load_19_, load_18_, load_17_, load_16_, load_15_,
         load_14_, load_13_, load_12_, load_11_, load_10_, load_9_, load_8_,
         load_7_, load_6_, load_5_, load_4_, load_3_, load_2_, load_1_,
         load_0_;
  wire   load_56_, load_48_, load_40_, load_32_, load_24_, load_16_, load_8_,
         load_0_, counter_7_, counter_6_, counter_5_, counter_4_, counter_3_,
         counter_2_, counter_1_, counter_0_, n1, n2, n3, n4, n5, n6, n7, n8,
         lfsr_n3, lfsr_n2, lfsr_n1, lfsr_n24, lfsr_n23, lfsr_n22, lfsr_n21,
         lfsr_n20, lfsr_n19, lfsr_n18, lfsr_n17, lfsr_n16, lfsr_n15, lfsr_n14,
         lfsr_n13, lfsr_n12, lfsr_n11, lfsr_n10, lfsr_n9, lfsr_n8, lfsr_n7,
         lfsr_n6, lfsr_n5, lfsr_n4, lfsr_lfsr_8_, lfsr_lfsr_9_, lfsr_lfsr_10_,
         lfsr_lfsr_11_, lfsr_lfsr_12_, lfsr_lfsr_13_, lfsr_lfsr_14_,
         lfsr_lfsr_15_, lfsr_lfsr_16_, lfsr_lfsr_17_, lfsr_lfsr_18_,
         lfsr_lfsr_19_;
  assign load_57_ = load_56_;
  assign load_58_ = load_56_;
  assign load_59_ = load_56_;
  assign load_60_ = load_56_;
  assign load_61_ = load_56_;
  assign load_62_ = load_56_;
  assign load_63_ = load_56_;
  assign load_49_ = load_48_;
  assign load_50_ = load_48_;
  assign load_51_ = load_48_;
  assign load_52_ = load_48_;
  assign load_53_ = load_48_;
  assign load_54_ = load_48_;
  assign load_55_ = load_48_;
  assign load_41_ = load_40_;
  assign load_42_ = load_40_;
  assign load_43_ = load_40_;
  assign load_44_ = load_40_;
  assign load_45_ = load_40_;
  assign load_46_ = load_40_;
  assign load_47_ = load_40_;
  assign load_33_ = load_32_;
  assign load_34_ = load_32_;
  assign load_35_ = load_32_;
  assign load_36_ = load_32_;
  assign load_37_ = load_32_;
  assign load_38_ = load_32_;
  assign load_39_ = load_32_;
  assign load_25_ = load_24_;
  assign load_26_ = load_24_;
  assign load_27_ = load_24_;
  assign load_28_ = load_24_;
  assign load_29_ = load_24_;
  assign load_30_ = load_24_;
  assign load_31_ = load_24_;
  assign load_17_ = load_16_;
  assign load_18_ = load_16_;
  assign load_19_ = load_16_;
  assign load_20_ = load_16_;
  assign load_21_ = load_16_;
  assign load_22_ = load_16_;
  assign load_23_ = load_16_;
  assign load_9_ = load_8_;
  assign load_10_ = load_8_;
  assign load_11_ = load_8_;
  assign load_12_ = load_8_;
  assign load_13_ = load_8_;
  assign load_14_ = load_8_;
  assign load_15_ = load_8_;
  assign load_1_ = load_0_;
  assign load_2_ = load_0_;
  assign load_3_ = load_0_;
  assign load_4_ = load_0_;
  assign load_5_ = load_0_;
  assign load_6_ = load_0_;
  assign load_7_ = load_0_;

  DFFHQNx1_ASAP7_75t_R load_reg_56_ ( .D(n8), .CLK(clk), .QN(load_56_) );
  DFFHQNx1_ASAP7_75t_R load_reg_48_ ( .D(n7), .CLK(clk), .QN(load_48_) );
  DFFHQNx1_ASAP7_75t_R load_reg_40_ ( .D(n6), .CLK(clk), .QN(load_40_) );
  DFFHQNx1_ASAP7_75t_R load_reg_32_ ( .D(n5), .CLK(clk), .QN(load_32_) );
  DFFHQNx1_ASAP7_75t_R load_reg_24_ ( .D(n4), .CLK(clk), .QN(load_24_) );
  DFFHQNx1_ASAP7_75t_R load_reg_16_ ( .D(n3), .CLK(clk), .QN(load_16_) );
  DFFHQNx1_ASAP7_75t_R load_reg_8_ ( .D(n2), .CLK(clk), .QN(load_8_) );
  DFFHQNx1_ASAP7_75t_R load_reg_0_ ( .D(n1), .CLK(clk), .QN(load_0_) );
  HAxp5_ASAP7_75t_R U11 ( .A(key_7_), .B(counter_7_), .SN(n8) );
  HAxp5_ASAP7_75t_R U12 ( .A(key_6_), .B(counter_6_), .SN(n7) );
  HAxp5_ASAP7_75t_R U13 ( .A(key_5_), .B(counter_5_), .SN(n6) );
  HAxp5_ASAP7_75t_R U14 ( .A(key_4_), .B(counter_4_), .SN(n5) );
  HAxp5_ASAP7_75t_R U15 ( .A(key_3_), .B(counter_3_), .SN(n4) );
  HAxp5_ASAP7_75t_R U16 ( .A(key_2_), .B(counter_2_), .SN(n3) );
  HAxp5_ASAP7_75t_R U17 ( .A(key_1_), .B(counter_1_), .SN(n2) );
  HAxp5_ASAP7_75t_R U18 ( .A(key_0_), .B(counter_0_), .SN(n1) );
  OAI21xp33_ASAP7_75t_R lfsr_U26 ( .A1(counter_0_), .A2(lfsr_n3), .B(lfsr_n2), 
        .Y(lfsr_n10) );
  AOI21xp33_ASAP7_75t_R lfsr_U25 ( .A1(counter_0_), .A2(lfsr_n3), .B(rst), .Y(
        lfsr_n2) );
  FAx1_ASAP7_75t_R lfsr_U24 ( .A(lfsr_lfsr_15_), .B(lfsr_lfsr_11_), .CI(
        lfsr_n1), .SN(lfsr_n3) );
  INVxp33_ASAP7_75t_R lfsr_U23 ( .A(counter_7_), .Y(lfsr_n1) );
  NAND2xp33_ASAP7_75t_R lfsr_U22 ( .A(lfsr_lfsr_11_), .B(lfsr_n4), .Y(lfsr_n17) );
  NAND2xp33_ASAP7_75t_R lfsr_U21 ( .A(lfsr_lfsr_15_), .B(lfsr_n4), .Y(lfsr_n15) );
  NAND2xp33_ASAP7_75t_R lfsr_U20 ( .A(counter_7_), .B(lfsr_n4), .Y(lfsr_n21)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U19 ( .A(lfsr_n4), .B(counter_3_), .Y(lfsr_n23)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U18 ( .A(lfsr_n4), .B(counter_4_), .Y(lfsr_n22)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U17 ( .A(lfsr_n4), .B(counter_2_), .Y(lfsr_n24)
         );
  NOR2xp33_ASAP7_75t_R lfsr_U16 ( .A(rst), .B(counter_6_), .Y(lfsr_n6) );
  NOR2xp33_ASAP7_75t_R lfsr_U15 ( .A(rst), .B(counter_5_), .Y(lfsr_n5) );
  NOR2xp33_ASAP7_75t_R lfsr_U14 ( .A(rst), .B(counter_1_), .Y(lfsr_n9) );
  NAND2xp33_ASAP7_75t_R lfsr_U13 ( .A(lfsr_n4), .B(lfsr_lfsr_12_), .Y(lfsr_n16) );
  NAND2xp33_ASAP7_75t_R lfsr_U11 ( .A(lfsr_n4), .B(lfsr_lfsr_19_), .Y(lfsr_n11) );
  NAND2xp33_ASAP7_75t_R lfsr_U10 ( .A(lfsr_n4), .B(lfsr_lfsr_9_), .Y(lfsr_n19)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U9 ( .A(lfsr_n4), .B(lfsr_lfsr_8_), .Y(lfsr_n20)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U8 ( .A(lfsr_n4), .B(lfsr_lfsr_10_), .Y(lfsr_n18)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U7 ( .A(lfsr_n4), .B(lfsr_lfsr_17_), .Y(lfsr_n13)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U6 ( .A(lfsr_n4), .B(lfsr_lfsr_18_), .Y(lfsr_n12)
         );
  NAND2xp33_ASAP7_75t_R lfsr_U5 ( .A(lfsr_n4), .B(lfsr_lfsr_16_), .Y(lfsr_n14)
         );
  NOR2xp33_ASAP7_75t_R lfsr_U4 ( .A(rst), .B(lfsr_lfsr_13_), .Y(lfsr_n7) );
  NOR2xp33_ASAP7_75t_R lfsr_U3 ( .A(rst), .B(lfsr_lfsr_14_), .Y(lfsr_n8) );
  INVx1_ASAP7_75t_R lfsr_U12 ( .A(rst), .Y(lfsr_n4) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_1_ ( .D(lfsr_n24), .CLK(clk), .QN(
        counter_1_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_2_ ( .D(lfsr_n23), .CLK(clk), .QN(
        counter_2_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_3_ ( .D(lfsr_n22), .CLK(clk), .QN(
        counter_3_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_4_ ( .D(lfsr_n5), .CLK(clk), .QN(
        counter_4_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_5_ ( .D(lfsr_n6), .CLK(clk), .QN(
        counter_5_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_6_ ( .D(lfsr_n21), .CLK(clk), .QN(
        counter_6_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_7_ ( .D(lfsr_n20), .CLK(clk), .QN(
        counter_7_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_8_ ( .D(lfsr_n19), .CLK(clk), .QN(
        lfsr_lfsr_8_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_9_ ( .D(lfsr_n18), .CLK(clk), .QN(
        lfsr_lfsr_9_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_10_ ( .D(lfsr_n17), .CLK(clk), 
        .QN(lfsr_lfsr_10_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_11_ ( .D(lfsr_n16), .CLK(clk), 
        .QN(lfsr_lfsr_11_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_12_ ( .D(lfsr_n7), .CLK(clk), .QN(
        lfsr_lfsr_12_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_13_ ( .D(lfsr_n8), .CLK(clk), .QN(
        lfsr_lfsr_13_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_14_ ( .D(lfsr_n15), .CLK(clk), 
        .QN(lfsr_lfsr_14_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_15_ ( .D(lfsr_n14), .CLK(clk), 
        .QN(lfsr_lfsr_15_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_16_ ( .D(lfsr_n13), .CLK(clk), 
        .QN(lfsr_lfsr_16_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_17_ ( .D(lfsr_n12), .CLK(clk), 
        .QN(lfsr_lfsr_17_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_18_ ( .D(lfsr_n11), .CLK(clk), 
        .QN(lfsr_lfsr_18_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_19_ ( .D(lfsr_n10), .CLK(clk), 
        .QN(lfsr_lfsr_19_) );
  DFFHQNx1_ASAP7_75t_R lfsr_lfsr_stream_reg_0_ ( .D(lfsr_n9), .CLK(clk), .QN(
        counter_0_) );
endmodule

