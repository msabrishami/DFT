/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Wed Nov 18 14:15:01 2020
/////////////////////////////////////////////////////////////


module top ( totalcoeffs_0_, totalcoeffs_1_, totalcoeffs_2_, totalcoeffs_3_, 
        totalcoeffs_4_, ctable_0_, ctable_1_, ctable_2_, trailingones_0_, 
        trailingones_1_, coeff_token_0_, coeff_token_1_, coeff_token_2_, 
        coeff_token_3_, coeff_token_4_, coeff_token_5_, ctoken_len_0_, 
        ctoken_len_1_, ctoken_len_2_, ctoken_len_3_, ctoken_len_4_ );
  input totalcoeffs_0_, totalcoeffs_1_, totalcoeffs_2_, totalcoeffs_3_,
         totalcoeffs_4_, ctable_0_, ctable_1_, ctable_2_, trailingones_0_,
         trailingones_1_;
  output coeff_token_0_, coeff_token_1_, coeff_token_2_, coeff_token_3_,
         coeff_token_4_, coeff_token_5_, ctoken_len_0_, ctoken_len_1_,
         ctoken_len_2_, ctoken_len_3_, ctoken_len_4_;
  wire   n575, n576, n577, n578, n579, n580, n581, n582, n583, n584, n585,
         n586, n587, n588, n589, n590, n591, n592, n593, n594, n595, n596,
         n597, n598, n599, n600, n601, n602, n603, n604, n605, n606, n607,
         n608, n609, n610, n611, n612, n613, n614, n615, n616, n617, n618,
         n619, n620, n621, n622, n623, n624, n625, n626, n627, n628, n629,
         n630, n631, n632, n633, n634, n635, n636, n637, n638, n639, n640,
         n641, n642, n643, n644, n645, n646, n647, n648, n649, n650, n651,
         n652, n653, n654, n655, n656, n657, n658, n659, n660, n661, n662,
         n663, n664, n665, n666, n667, n668, n669, n670, n671, n672, n673,
         n674, n675, n676, n677, n678, n679, n680, n681, n682, n683, n684,
         n685, n686, n687, n688, n689, n690, n691, n692, n693, n694, n695,
         n696, n697, n698, n699, n700, n701, n702, n703, n704, n705, n706,
         n707, n708, n709, n710, n711, n712, n713, n714, n715, n716, n717,
         n718, n719, n720, n721, n722, n723, n724, n725, n726, n727, n728,
         n729, n730, n731, n732, n733, n734, n735, n736, n737, n738, n739,
         n740, n741, n742, n743, n744, n745, n746, n747, n748, n749, n750,
         n751, n752, n753, n754, n755, n756, n757, n758, n759, n760, n761,
         n762, n763, n764, n765, n766, n767, n768, n769, n770, n771, n772,
         n773, n774, n775, n776, n777, n778, n779, n780, n781, n782, n783,
         n784, n785, n786, n787, n788, n789, n790, n791, n792, n793, n794,
         n795, n796, n797, n798, n799, n800, n801, n802, n803, n804, n805,
         n806, n807, n808, n809, n810, n811, n812, n813, n814, n815, n816,
         n817, n818, n819, n820, n821, n822, n823, n824, n825, n826, n827,
         n828, n829, n830, n831, n832, n833, n834, n835, n836, n837, n838,
         n839, n840, n841, n842, n843, n844, n845, n846, n847, n848, n849,
         n850, n851, n852, n853, n854, n855, n856, n857, n858, n859, n860,
         n861, n862, n863, n864, n865, n866, n867, n868, n869, n870, n871,
         n872, n873, n874, n875, n876, n877, n878, n879, n880, n881, n882,
         n883, n884, n885, n886, n887, n888, n889, n890, n891, n892, n893,
         n894, n895, n896, n897, n898, n899, n900, n901, n902, n903, n904,
         n905, n906, n907, n908, n909, n910, n911, n912, n913, n914, n915,
         n916, n917, n918, n919, n920, n921, n922, n923, n924, n925, n926,
         n927, n928, n929, n930, n931, n932, n933, n934, n935, n936, n937,
         n938, n939, n940, n941, n942, n943, n944, n945, n946, n947, n948,
         n949, n950, n951, n952, n953, n954, n955, n956, n957, n958, n959,
         n960, n961, n962, n963, n964, n965, n966, n967, n968, n969, n970,
         n971, n972, n973, n974, n975, n976, n977, n978, n979, n980, n981,
         n982, n983, n984, n985, n986, n987, n988, n989, n990, n991, n992,
         n993, n994, n995, n996, n997, n998, n999, n1000, n1001, n1002, n1003,
         n1004, n1005, n1006, n1007, n1008, n1009, n1010, n1011, n1012, n1013,
         n1014, n1015, n1016, n1017, n1018, n1019, n1020, n1021, n1022, n1023,
         n1024, n1025, n1026, n1027, n1028, n1029, n1030, n1031, n1032, n1033,
         n1034, n1035, n1036, n1037, n1038, n1039, n1040, n1041, n1042, n1043,
         n1044, n1045, n1046, n1047, n1048, n1049, n1050, n1051, n1052, n1053,
         n1054, n1055, n1056, n1057, n1058, n1059, n1060, n1061, n1062, n1063,
         n1064, n1065, n1066, n1067, n1068, n1069, n1070, n1071, n1072, n1073,
         n1074, n1075, n1076, n1077, n1078, n1079, n1080, n1081, n1082, n1083,
         n1084, n1085, n1086, n1087, n1088, n1089, n1090, n1091, n1092, n1093,
         n1094, n1095, n1096, n1097, n1098, n1099, n1100, n1101, n1102, n1103,
         n1104, n1105, n1106, n1107, n1108, n1109, n1110, n1111, n1112, n1113,
         n1114, n1115, n1116, n1117, n1118, n1119, n1120, n1121;

  NOR4_X1 U586 ( .A1(n575), .A2(n576), .A3(n577), .A4(n578), .ZN(ctoken_len_4_) );
  NOR2_X1 U587 ( .A1(n579), .A2(n580), .ZN(n578) );
  NOR2_X1 U588 ( .A1(n581), .A2(totalcoeffs_4_), .ZN(n580) );
  NOR2_X1 U589 ( .A1(n582), .A2(n583), .ZN(n581) );
  NOR4_X1 U590 ( .A1(n584), .A2(n585), .A3(n586), .A4(n587), .ZN(n583) );
  NOR2_X1 U591 ( .A1(totalcoeffs_1_), .A2(n588), .ZN(n585) );
  NAND2_X1 U592 ( .A1(n589), .A2(n590), .ZN(n576) );
  NOR4_X1 U593 ( .A1(n591), .A2(n592), .A3(n593), .A4(n594), .ZN(ctoken_len_3_) );
  NOR2_X1 U594 ( .A1(n595), .A2(n596), .ZN(n594) );
  NOR2_X1 U595 ( .A1(n597), .A2(n598), .ZN(n593) );
  NOR2_X1 U596 ( .A1(n599), .A2(n600), .ZN(n597) );
  NOR2_X1 U597 ( .A1(n601), .A2(n602), .ZN(n599) );
  NOR2_X1 U598 ( .A1(n603), .A2(ctable_1_), .ZN(n601) );
  NAND3_X1 U599 ( .A1(n604), .A2(n605), .A3(n606), .ZN(n592) );
  XNOR2_X1 U600 ( .A1(n607), .A2(totalcoeffs_4_), .ZN(n606) );
  NAND2_X1 U601 ( .A1(n608), .A2(n609), .ZN(n605) );
  NAND2_X1 U602 ( .A1(n610), .A2(n611), .ZN(n608) );
  NAND3_X1 U603 ( .A1(n612), .A2(n613), .A3(n614), .ZN(n611) );
  NAND2_X1 U604 ( .A1(n588), .A2(n615), .ZN(n612) );
  NAND2_X1 U605 ( .A1(n616), .A2(n617), .ZN(n610) );
  NAND2_X1 U606 ( .A1(totalcoeffs_1_), .A2(n618), .ZN(n604) );
  NAND4_X1 U607 ( .A1(n619), .A2(n620), .A3(n621), .A4(n622), .ZN(n618) );
  NAND3_X1 U608 ( .A1(n623), .A2(n617), .A3(n600), .ZN(n622) );
  NOR2_X1 U609 ( .A1(n624), .A2(n625), .ZN(n621) );
  NOR3_X1 U610 ( .A1(n626), .A2(n627), .A3(n628), .ZN(n625) );
  NAND2_X1 U611 ( .A1(n629), .A2(n630), .ZN(n620) );
  NAND2_X1 U612 ( .A1(n631), .A2(n602), .ZN(n630) );
  NAND2_X1 U613 ( .A1(n603), .A2(n632), .ZN(n619) );
  NAND4_X1 U614 ( .A1(n633), .A2(n634), .A3(n635), .A4(n589), .ZN(n591) );
  NAND2_X1 U615 ( .A1(n636), .A2(n637), .ZN(n635) );
  NAND2_X1 U616 ( .A1(n590), .A2(n638), .ZN(n637) );
  NAND3_X1 U617 ( .A1(n639), .A2(n595), .A3(n640), .ZN(n638) );
  NAND2_X1 U618 ( .A1(n609), .A2(n641), .ZN(n636) );
  NAND2_X1 U619 ( .A1(ctable_2_), .A2(n642), .ZN(n634) );
  NAND2_X1 U620 ( .A1(totalcoeffs_0_), .A2(n607), .ZN(n633) );
  NAND2_X1 U621 ( .A1(n643), .A2(n644), .ZN(ctoken_len_2_) );
  NAND2_X1 U622 ( .A1(totalcoeffs_4_), .A2(n645), .ZN(n644) );
  NAND3_X1 U623 ( .A1(n646), .A2(n590), .A3(n647), .ZN(n645) );
  NAND3_X1 U624 ( .A1(n648), .A2(n649), .A3(n650), .ZN(n643) );
  NAND2_X1 U625 ( .A1(n616), .A2(n651), .ZN(n649) );
  NAND3_X1 U626 ( .A1(n652), .A2(n653), .A3(n654), .ZN(n651) );
  NAND2_X1 U627 ( .A1(n655), .A2(n656), .ZN(n654) );
  NAND3_X1 U628 ( .A1(n657), .A2(n609), .A3(n658), .ZN(n653) );
  NAND2_X1 U629 ( .A1(n659), .A2(n660), .ZN(n652) );
  NAND2_X1 U630 ( .A1(n661), .A2(n662), .ZN(n659) );
  NAND3_X1 U631 ( .A1(n663), .A2(n664), .A3(n656), .ZN(n662) );
  INV_X1 U632 ( .I(n665), .ZN(n661) );
  NAND2_X1 U633 ( .A1(n590), .A2(n666), .ZN(n648) );
  NAND4_X1 U634 ( .A1(n667), .A2(n668), .A3(n669), .A4(n670), .ZN(n666) );
  NAND2_X1 U635 ( .A1(n575), .A2(n671), .ZN(n670) );
  NAND2_X1 U636 ( .A1(n628), .A2(n672), .ZN(n671) );
  NAND3_X1 U637 ( .A1(n673), .A2(n674), .A3(totalcoeffs_3_), .ZN(n672) );
  NAND2_X1 U638 ( .A1(n623), .A2(n675), .ZN(n673) );
  NAND2_X1 U639 ( .A1(n676), .A2(n640), .ZN(n669) );
  NAND2_X1 U640 ( .A1(n582), .A2(n677), .ZN(n668) );
  NOR3_X1 U641 ( .A1(n628), .A2(n623), .A3(n609), .ZN(n582) );
  NAND2_X1 U642 ( .A1(n595), .A2(n678), .ZN(n667) );
  NAND4_X1 U643 ( .A1(n679), .A2(n680), .A3(n681), .A4(n682), .ZN(n678) );
  NOR4_X1 U644 ( .A1(n683), .A2(n684), .A3(n685), .A4(n686), .ZN(n682) );
  AND2_X1 U645 ( .A1(n632), .A2(n687), .Z(n686) );
  NOR2_X1 U646 ( .A1(n688), .A2(n689), .ZN(n685) );
  NOR2_X1 U647 ( .A1(n690), .A2(n691), .ZN(n688) );
  NOR2_X1 U648 ( .A1(n588), .A2(n692), .ZN(n691) );
  NOR2_X1 U649 ( .A1(trailingones_1_), .A2(n693), .ZN(n690) );
  NOR4_X1 U650 ( .A1(n694), .A2(n695), .A3(n609), .A4(n587), .ZN(n684) );
  NOR2_X1 U651 ( .A1(n623), .A2(ctable_0_), .ZN(n695) );
  NOR2_X1 U652 ( .A1(n696), .A2(n697), .ZN(n683) );
  NOR2_X1 U653 ( .A1(n698), .A2(n699), .ZN(n696) );
  NOR2_X1 U654 ( .A1(ctable_0_), .A2(n596), .ZN(n699) );
  NOR2_X1 U655 ( .A1(totalcoeffs_0_), .A2(n700), .ZN(n698) );
  NOR2_X1 U656 ( .A1(n701), .A2(n702), .ZN(n681) );
  NOR2_X1 U657 ( .A1(n703), .A2(n704), .ZN(n702) );
  NOR2_X1 U658 ( .A1(n705), .A2(n706), .ZN(n703) );
  NOR2_X1 U659 ( .A1(n707), .A2(n598), .ZN(n706) );
  NOR2_X1 U660 ( .A1(totalcoeffs_0_), .A2(n677), .ZN(n707) );
  AND3_X1 U661 ( .A1(n694), .A2(n617), .A3(totalcoeffs_1_), .Z(n705) );
  AND3_X1 U662 ( .A1(n647), .A2(ctable_0_), .A3(n708), .Z(n701) );
  NAND3_X1 U663 ( .A1(n709), .A2(n588), .A3(n614), .ZN(n680) );
  NAND2_X1 U664 ( .A1(n710), .A2(n711), .ZN(n709) );
  NAND2_X1 U665 ( .A1(n677), .A2(n609), .ZN(n711) );
  NAND3_X1 U666 ( .A1(n712), .A2(n713), .A3(n714), .ZN(n679) );
  INV_X1 U667 ( .I(n689), .ZN(n714) );
  NAND2_X1 U668 ( .A1(n617), .A2(n715), .ZN(n689) );
  NAND2_X1 U669 ( .A1(n716), .A2(n717), .ZN(n715) );
  NAND2_X1 U670 ( .A1(ctable_0_), .A2(n609), .ZN(n716) );
  NAND2_X1 U671 ( .A1(n641), .A2(n718), .ZN(n712) );
  NOR3_X1 U672 ( .A1(n719), .A2(n720), .A3(n721), .ZN(ctoken_len_1_) );
  NOR2_X1 U673 ( .A1(ctable_2_), .A2(n722), .ZN(n721) );
  NOR2_X1 U674 ( .A1(n723), .A2(n724), .ZN(n722) );
  NOR2_X1 U675 ( .A1(totalcoeffs_4_), .A2(n725), .ZN(n724) );
  NOR4_X1 U676 ( .A1(n726), .A2(n727), .A3(n728), .A4(n729), .ZN(n725) );
  NOR3_X1 U677 ( .A1(n730), .A2(totalcoeffs_0_), .A3(ctable_0_), .ZN(n729) );
  NOR3_X1 U678 ( .A1(n626), .A2(n731), .A3(n598), .ZN(n728) );
  NOR2_X1 U679 ( .A1(n732), .A2(n733), .ZN(n731) );
  NOR2_X1 U680 ( .A1(n734), .A2(n735), .ZN(n727) );
  NOR4_X1 U681 ( .A1(n736), .A2(n665), .A3(n737), .A4(n738), .ZN(n734) );
  NOR2_X1 U682 ( .A1(n739), .A2(n586), .ZN(n738) );
  NOR2_X1 U683 ( .A1(n740), .A2(n741), .ZN(n739) );
  NOR2_X1 U684 ( .A1(n742), .A2(n743), .ZN(n740) );
  NOR2_X1 U685 ( .A1(n713), .A2(n744), .ZN(n737) );
  NAND4_X1 U686 ( .A1(n745), .A2(n746), .A3(n747), .A4(n748), .ZN(n726) );
  NAND2_X1 U687 ( .A1(totalcoeffs_1_), .A2(n749), .ZN(n748) );
  NAND2_X1 U688 ( .A1(n750), .A2(n751), .ZN(n749) );
  NAND3_X1 U689 ( .A1(n640), .A2(n617), .A3(n600), .ZN(n751) );
  NAND2_X1 U690 ( .A1(n646), .A2(n752), .ZN(n750) );
  NAND2_X1 U691 ( .A1(n753), .A2(n754), .ZN(n752) );
  NAND2_X1 U692 ( .A1(n627), .A2(totalcoeffs_2_), .ZN(n754) );
  NAND4_X1 U693 ( .A1(n755), .A2(n641), .A3(totalcoeffs_2_), .A4(n609), .ZN(
        n747) );
  NAND2_X1 U694 ( .A1(n735), .A2(n756), .ZN(n755) );
  NAND2_X1 U695 ( .A1(n757), .A2(n677), .ZN(n756) );
  NAND2_X1 U696 ( .A1(n577), .A2(n758), .ZN(n746) );
  NAND3_X1 U697 ( .A1(n759), .A2(n760), .A3(n761), .ZN(n758) );
  NAND2_X1 U698 ( .A1(n762), .A2(n657), .ZN(n761) );
  NAND3_X1 U699 ( .A1(n763), .A2(n764), .A3(n765), .ZN(n760) );
  NAND2_X1 U700 ( .A1(n742), .A2(n628), .ZN(n763) );
  NAND3_X1 U701 ( .A1(n623), .A2(n586), .A3(n766), .ZN(n759) );
  NAND2_X1 U702 ( .A1(n767), .A2(n595), .ZN(n745) );
  NAND4_X1 U703 ( .A1(n768), .A2(n769), .A3(n770), .A4(n771), .ZN(n767) );
  NAND3_X1 U704 ( .A1(n632), .A2(n772), .A3(n773), .ZN(n771) );
  NAND3_X1 U705 ( .A1(n639), .A2(trailingones_0_), .A3(n603), .ZN(n770) );
  NAND2_X1 U706 ( .A1(n774), .A2(n676), .ZN(n769) );
  NAND2_X1 U707 ( .A1(totalcoeffs_1_), .A2(n775), .ZN(n768) );
  NAND2_X1 U708 ( .A1(n776), .A2(n777), .ZN(n775) );
  NAND2_X1 U709 ( .A1(n694), .A2(n778), .ZN(n777) );
  NAND2_X1 U710 ( .A1(n779), .A2(n780), .ZN(n778) );
  NAND2_X1 U711 ( .A1(n704), .A2(n617), .ZN(n780) );
  NAND2_X1 U712 ( .A1(n658), .A2(n781), .ZN(n776) );
  NOR2_X1 U713 ( .A1(n782), .A2(n783), .ZN(n723) );
  NOR2_X1 U714 ( .A1(n784), .A2(n785), .ZN(n782) );
  NOR2_X1 U715 ( .A1(ctable_0_), .A2(n786), .ZN(n785) );
  NOR2_X1 U716 ( .A1(n787), .A2(n788), .ZN(n786) );
  NOR3_X1 U717 ( .A1(n609), .A2(n627), .A3(n628), .ZN(n788) );
  AND3_X1 U718 ( .A1(n789), .A2(n790), .A3(n623), .Z(n787) );
  NOR4_X1 U719 ( .A1(n617), .A2(n588), .A3(n609), .A4(n791), .ZN(n784) );
  NOR3_X1 U720 ( .A1(n783), .A2(n792), .A3(n717), .ZN(n720) );
  NOR3_X1 U721 ( .A1(n793), .A2(n794), .A3(n795), .ZN(n792) );
  NOR3_X1 U722 ( .A1(n590), .A2(n713), .A3(n753), .ZN(n795) );
  NOR3_X1 U723 ( .A1(ctable_2_), .A2(n609), .A3(n641), .ZN(n794) );
  NOR2_X1 U724 ( .A1(n796), .A2(n617), .ZN(n793) );
  NOR2_X1 U725 ( .A1(n797), .A2(n798), .ZN(n796) );
  NOR2_X1 U726 ( .A1(n602), .A2(n713), .ZN(n798) );
  NOR2_X1 U727 ( .A1(n743), .A2(n799), .ZN(n797) );
  INV_X1 U728 ( .I(n800), .ZN(n783) );
  NOR4_X1 U729 ( .A1(n801), .A2(n802), .A3(n803), .A4(n804), .ZN(ctoken_len_0_) );
  NOR2_X1 U730 ( .A1(totalcoeffs_4_), .A2(n805), .ZN(n803) );
  NOR3_X1 U731 ( .A1(n806), .A2(n807), .A3(n808), .ZN(n805) );
  NOR2_X1 U732 ( .A1(n809), .A2(n810), .ZN(n808) );
  NOR4_X1 U733 ( .A1(n811), .A2(n812), .A3(n813), .A4(n814), .ZN(n809) );
  AND2_X1 U734 ( .A1(n655), .A2(n815), .Z(n814) );
  NOR3_X1 U735 ( .A1(n744), .A2(n677), .A3(n697), .ZN(n813) );
  INV_X1 U736 ( .I(n816), .ZN(n744) );
  NOR3_X1 U737 ( .A1(n595), .A2(n742), .A3(n772), .ZN(n812) );
  NAND2_X1 U738 ( .A1(n587), .A2(n817), .ZN(n772) );
  NAND2_X1 U739 ( .A1(trailingones_1_), .A2(n617), .ZN(n817) );
  INV_X1 U740 ( .I(n781), .ZN(n587) );
  NOR2_X1 U741 ( .A1(n627), .A2(n708), .ZN(n742) );
  NOR3_X1 U742 ( .A1(ctable_1_), .A2(n588), .A3(n818), .ZN(n811) );
  NOR2_X1 U743 ( .A1(n819), .A2(n820), .ZN(n807) );
  INV_X1 U744 ( .I(n616), .ZN(n820) );
  NOR2_X1 U745 ( .A1(n717), .A2(ctable_1_), .ZN(n616) );
  INV_X1 U746 ( .I(n646), .ZN(n717) );
  NOR3_X1 U747 ( .A1(n821), .A2(n822), .A3(n823), .ZN(n819) );
  NOR2_X1 U748 ( .A1(n824), .A2(n590), .ZN(n823) );
  NOR3_X1 U749 ( .A1(n825), .A2(n741), .A3(n826), .ZN(n824) );
  NOR3_X1 U750 ( .A1(n713), .A2(totalcoeffs_0_), .A3(n617), .ZN(n826) );
  NOR2_X1 U751 ( .A1(n697), .A2(n753), .ZN(n825) );
  INV_X1 U752 ( .I(n655), .ZN(n753) );
  NOR2_X1 U753 ( .A1(n743), .A2(n663), .ZN(n822) );
  NOR2_X1 U754 ( .A1(n764), .A2(n675), .ZN(n821) );
  NOR2_X1 U755 ( .A1(ctable_2_), .A2(n827), .ZN(n806) );
  NOR3_X1 U756 ( .A1(n828), .A2(n829), .A3(n830), .ZN(n827) );
  NOR3_X1 U757 ( .A1(n602), .A2(n631), .A3(n596), .ZN(n830) );
  NOR3_X1 U758 ( .A1(n700), .A2(n677), .A3(n713), .ZN(n829) );
  NOR2_X1 U759 ( .A1(n615), .A2(n642), .ZN(n828) );
  NOR2_X1 U760 ( .A1(n831), .A2(n832), .ZN(n802) );
  NOR4_X1 U761 ( .A1(n833), .A2(n834), .A3(n835), .A4(n836), .ZN(n831) );
  NOR2_X1 U762 ( .A1(n837), .A2(n595), .ZN(n836) );
  NOR2_X1 U763 ( .A1(n838), .A2(n839), .ZN(n837) );
  NOR2_X1 U764 ( .A1(n840), .A2(n697), .ZN(n838) );
  NOR2_X1 U765 ( .A1(n816), .A2(n658), .ZN(n840) );
  NOR2_X1 U766 ( .A1(n841), .A2(n586), .ZN(n835) );
  NOR4_X1 U767 ( .A1(n842), .A2(n843), .A3(n665), .A4(n844), .ZN(n841) );
  NOR3_X1 U768 ( .A1(n845), .A2(n846), .A3(n626), .ZN(n844) );
  NOR2_X1 U769 ( .A1(n847), .A2(n623), .ZN(n846) );
  NOR2_X1 U770 ( .A1(totalcoeffs_0_), .A2(n609), .ZN(n847) );
  NOR2_X1 U771 ( .A1(n697), .A2(n848), .ZN(n665) );
  NOR2_X1 U772 ( .A1(trailingones_0_), .A2(n818), .ZN(n843) );
  INV_X1 U773 ( .I(n687), .ZN(n818) );
  NAND4_X1 U774 ( .A1(n849), .A2(n850), .A3(n851), .A4(n852), .ZN(n842) );
  NAND3_X1 U775 ( .A1(n766), .A2(n779), .A3(n791), .ZN(n852) );
  NAND2_X1 U776 ( .A1(n789), .A2(n640), .ZN(n851) );
  NAND2_X1 U777 ( .A1(n655), .A2(n600), .ZN(n850) );
  NAND2_X1 U778 ( .A1(n773), .A2(n732), .ZN(n849) );
  NOR2_X1 U779 ( .A1(n660), .A2(n730), .ZN(n834) );
  NAND4_X1 U780 ( .A1(n853), .A2(n854), .A3(n855), .A4(n856), .ZN(n833) );
  NAND3_X1 U781 ( .A1(n766), .A2(n639), .A3(n677), .ZN(n856) );
  NAND3_X1 U782 ( .A1(n857), .A2(n858), .A3(ctable_0_), .ZN(n855) );
  NAND2_X1 U783 ( .A1(n687), .A2(n617), .ZN(n854) );
  NOR2_X1 U784 ( .A1(n713), .A2(n791), .ZN(n687) );
  INV_X1 U785 ( .I(n640), .ZN(n791) );
  NAND2_X1 U786 ( .A1(totalcoeffs_2_), .A2(n859), .ZN(n853) );
  NAND3_X1 U787 ( .A1(n860), .A2(n861), .A3(n862), .ZN(n859) );
  NAND2_X1 U788 ( .A1(n863), .A2(n623), .ZN(n862) );
  NAND3_X1 U789 ( .A1(n658), .A2(n677), .A3(n789), .ZN(n861) );
  NAND3_X1 U790 ( .A1(ctable_1_), .A2(n641), .A3(totalcoeffs_1_), .ZN(n860) );
  NOR2_X1 U791 ( .A1(n864), .A2(n589), .ZN(coeff_token_5_) );
  NOR2_X1 U792 ( .A1(n865), .A2(n801), .ZN(n864) );
  NOR3_X1 U793 ( .A1(n832), .A2(n647), .A3(n586), .ZN(n865) );
  INV_X1 U794 ( .I(n866), .ZN(n832) );
  NAND2_X1 U795 ( .A1(n867), .A2(n868), .ZN(coeff_token_4_) );
  NAND4_X1 U796 ( .A1(n804), .A2(n647), .A3(totalcoeffs_4_), .A4(n586), .ZN(
        n868) );
  NOR2_X1 U797 ( .A1(n589), .A2(ctable_2_), .ZN(n804) );
  NAND3_X1 U798 ( .A1(n866), .A2(n869), .A3(n870), .ZN(n867) );
  NAND2_X1 U799 ( .A1(n871), .A2(n872), .ZN(n869) );
  NAND2_X1 U800 ( .A1(totalcoeffs_2_), .A2(n743), .ZN(n872) );
  INV_X1 U801 ( .I(n584), .ZN(n743) );
  NAND2_X1 U802 ( .A1(n647), .A2(totalcoeffs_3_), .ZN(n871) );
  NAND3_X1 U803 ( .A1(n873), .A2(n874), .A3(n875), .ZN(coeff_token_3_) );
  NAND2_X1 U804 ( .A1(n870), .A2(n801), .ZN(n875) );
  NAND2_X1 U805 ( .A1(n719), .A2(n627), .ZN(n874) );
  NOR2_X1 U806 ( .A1(n876), .A2(n626), .ZN(n719) );
  NAND2_X1 U807 ( .A1(n677), .A2(n595), .ZN(n626) );
  NAND2_X1 U808 ( .A1(n877), .A2(n590), .ZN(n873) );
  NAND2_X1 U809 ( .A1(n878), .A2(n879), .ZN(n877) );
  NAND2_X1 U810 ( .A1(n800), .A2(n880), .ZN(n879) );
  NAND4_X1 U811 ( .A1(n881), .A2(n882), .A3(n883), .A4(n884), .ZN(n880) );
  NOR3_X1 U812 ( .A1(n885), .A2(n886), .A3(n887), .ZN(n884) );
  NOR3_X1 U813 ( .A1(n609), .A2(totalcoeffs_0_), .A3(n888), .ZN(n887) );
  NOR2_X1 U814 ( .A1(n889), .A2(n890), .ZN(n888) );
  NOR3_X1 U815 ( .A1(n704), .A2(n677), .A3(n617), .ZN(n889) );
  NOR2_X1 U816 ( .A1(totalcoeffs_1_), .A2(n718), .ZN(n886) );
  NOR2_X1 U817 ( .A1(n628), .A2(n674), .ZN(n885) );
  NAND2_X1 U818 ( .A1(totalcoeffs_3_), .A2(n891), .ZN(n883) );
  NAND2_X1 U819 ( .A1(n848), .A2(n892), .ZN(n891) );
  NAND2_X1 U820 ( .A1(n789), .A2(n615), .ZN(n892) );
  NAND3_X1 U821 ( .A1(n774), .A2(ctable_0_), .A3(n741), .ZN(n882) );
  NAND3_X1 U822 ( .A1(trailingones_0_), .A2(n615), .A3(n694), .ZN(n881) );
  NAND2_X1 U823 ( .A1(n893), .A2(n650), .ZN(n878) );
  NAND4_X1 U824 ( .A1(n894), .A2(n895), .A3(n896), .A4(n897), .ZN(n893) );
  NAND2_X1 U825 ( .A1(n898), .A2(n660), .ZN(n896) );
  NAND4_X1 U826 ( .A1(n899), .A2(n900), .A3(n901), .A4(n902), .ZN(n898) );
  NAND2_X1 U827 ( .A1(n765), .A2(ctable_1_), .ZN(n902) );
  NAND2_X1 U828 ( .A1(totalcoeffs_1_), .A2(n903), .ZN(n901) );
  NAND3_X1 U829 ( .A1(n904), .A2(n905), .A3(n906), .ZN(n903) );
  NAND2_X1 U830 ( .A1(totalcoeffs_3_), .A2(n677), .ZN(n906) );
  NAND2_X1 U831 ( .A1(n907), .A2(n631), .ZN(n905) );
  NAND2_X1 U832 ( .A1(n575), .A2(n588), .ZN(n904) );
  NAND2_X1 U833 ( .A1(n575), .A2(totalcoeffs_2_), .ZN(n900) );
  NAND2_X1 U834 ( .A1(n656), .A2(totalcoeffs_3_), .ZN(n899) );
  NAND2_X1 U835 ( .A1(n575), .A2(n908), .ZN(n895) );
  NAND4_X1 U836 ( .A1(n909), .A2(n910), .A3(n911), .A4(n912), .ZN(n908) );
  NAND2_X1 U837 ( .A1(n708), .A2(n609), .ZN(n912) );
  NAND2_X1 U838 ( .A1(n766), .A2(trailingones_0_), .ZN(n911) );
  NAND2_X1 U839 ( .A1(n913), .A2(n586), .ZN(n909) );
  NAND2_X1 U840 ( .A1(n773), .A2(n914), .ZN(n894) );
  NAND4_X1 U841 ( .A1(n915), .A2(n916), .A3(n917), .A4(n918), .ZN(n914) );
  NOR4_X1 U842 ( .A1(n870), .A2(n790), .A3(n624), .A4(n919), .ZN(n918) );
  NOR3_X1 U843 ( .A1(n664), .A2(trailingones_1_), .A3(n677), .ZN(n919) );
  NAND2_X1 U844 ( .A1(n694), .A2(n588), .ZN(n917) );
  NAND2_X1 U845 ( .A1(n781), .A2(n920), .ZN(n916) );
  NAND2_X1 U846 ( .A1(n921), .A2(n700), .ZN(n920) );
  NAND2_X1 U847 ( .A1(n857), .A2(n603), .ZN(n915) );
  NAND4_X1 U848 ( .A1(n922), .A2(n923), .A3(n924), .A4(n925), .ZN(
        coeff_token_2_) );
  NAND4_X1 U849 ( .A1(n733), .A2(trailingones_0_), .A3(n926), .A4(
        totalcoeffs_4_), .ZN(n925) );
  NOR2_X1 U850 ( .A1(ctable_2_), .A2(n927), .ZN(n926) );
  NAND2_X1 U851 ( .A1(n866), .A2(n928), .ZN(n924) );
  NAND2_X1 U852 ( .A1(n929), .A2(n930), .ZN(n928) );
  NAND2_X1 U853 ( .A1(n640), .A2(n931), .ZN(n930) );
  NAND4_X1 U854 ( .A1(n932), .A2(n933), .A3(n934), .A4(n935), .ZN(n931) );
  NOR2_X1 U855 ( .A1(n936), .A2(n937), .ZN(n935) );
  NOR2_X1 U856 ( .A1(n781), .A2(n693), .ZN(n937) );
  NOR2_X1 U857 ( .A1(n938), .A2(n595), .ZN(n936) );
  NOR3_X1 U858 ( .A1(n939), .A2(n940), .A3(n941), .ZN(n938) );
  NOR2_X1 U859 ( .A1(totalcoeffs_1_), .A2(n693), .ZN(n941) );
  NOR2_X1 U860 ( .A1(n863), .A2(n664), .ZN(n940) );
  NOR2_X1 U861 ( .A1(n628), .A2(n697), .ZN(n939) );
  INV_X1 U862 ( .I(n789), .ZN(n697) );
  NAND3_X1 U863 ( .A1(n845), .A2(n617), .A3(n757), .ZN(n934) );
  INV_X1 U864 ( .I(n710), .ZN(n845) );
  NOR2_X1 U865 ( .A1(n789), .A2(n656), .ZN(n710) );
  INV_X1 U866 ( .I(n676), .ZN(n932) );
  NOR2_X1 U867 ( .A1(n641), .A2(n628), .ZN(n676) );
  NAND2_X1 U868 ( .A1(n942), .A2(n660), .ZN(n929) );
  NAND4_X1 U869 ( .A1(n943), .A2(n944), .A3(n945), .A4(n946), .ZN(n942) );
  NOR3_X1 U870 ( .A1(n947), .A2(n948), .A3(n949), .ZN(n946) );
  NOR2_X1 U871 ( .A1(n950), .A2(n617), .ZN(n949) );
  NOR2_X1 U872 ( .A1(n951), .A2(n870), .ZN(n950) );
  NOR2_X1 U873 ( .A1(n675), .A2(n921), .ZN(n951) );
  INV_X1 U874 ( .I(n952), .ZN(n921) );
  NOR3_X1 U875 ( .A1(n700), .A2(n713), .A3(n735), .ZN(n948) );
  INV_X1 U876 ( .I(n575), .ZN(n735) );
  NOR2_X1 U877 ( .A1(n953), .A2(n586), .ZN(n947) );
  NOR2_X1 U878 ( .A1(n954), .A2(n955), .ZN(n953) );
  NOR3_X1 U879 ( .A1(n956), .A2(totalcoeffs_2_), .A3(n815), .ZN(n955) );
  NOR2_X1 U880 ( .A1(n588), .A2(n675), .ZN(n956) );
  NOR2_X1 U881 ( .A1(totalcoeffs_1_), .A2(n799), .ZN(n954) );
  NAND2_X1 U882 ( .A1(ctable_0_), .A2(n957), .ZN(n945) );
  NAND3_X1 U883 ( .A1(n958), .A2(n663), .A3(n959), .ZN(n957) );
  NAND2_X1 U884 ( .A1(n765), .A2(n848), .ZN(n959) );
  NOR2_X1 U885 ( .A1(n629), .A2(totalcoeffs_1_), .ZN(n765) );
  NAND3_X1 U886 ( .A1(n718), .A2(n628), .A3(n766), .ZN(n958) );
  NAND2_X1 U887 ( .A1(n762), .A2(n600), .ZN(n944) );
  NAND2_X1 U888 ( .A1(n766), .A2(n632), .ZN(n943) );
  NOR2_X1 U889 ( .A1(n588), .A2(totalcoeffs_3_), .ZN(n632) );
  NAND2_X1 U890 ( .A1(n801), .A2(n960), .ZN(n923) );
  NAND2_X1 U891 ( .A1(n677), .A2(n961), .ZN(n960) );
  NAND2_X1 U892 ( .A1(n595), .A2(n588), .ZN(n961) );
  NAND2_X1 U893 ( .A1(n800), .A2(n962), .ZN(n922) );
  NAND3_X1 U894 ( .A1(n963), .A2(n964), .A3(n965), .ZN(n962) );
  NAND2_X1 U895 ( .A1(n966), .A2(n590), .ZN(n965) );
  NAND4_X1 U896 ( .A1(n967), .A2(n968), .A3(n969), .A4(n970), .ZN(n966) );
  NOR4_X1 U897 ( .A1(n971), .A2(n972), .A3(n973), .A4(n974), .ZN(n970) );
  NOR3_X1 U898 ( .A1(n677), .A2(totalcoeffs_3_), .A3(n975), .ZN(n974) );
  NOR2_X1 U899 ( .A1(n976), .A2(n977), .ZN(n975) );
  NOR2_X1 U900 ( .A1(n609), .A2(n641), .ZN(n977) );
  NOR2_X1 U901 ( .A1(n704), .A2(n978), .ZN(n976) );
  INV_X1 U902 ( .I(n627), .ZN(n704) );
  NOR2_X1 U903 ( .A1(n979), .A2(n596), .ZN(n973) );
  NOR3_X1 U904 ( .A1(n980), .A2(n656), .A3(n732), .ZN(n979) );
  NOR2_X1 U905 ( .A1(trailingones_1_), .A2(n588), .ZN(n980) );
  NOR3_X1 U906 ( .A1(n660), .A2(n598), .A3(n641), .ZN(n972) );
  NAND2_X1 U907 ( .A1(n790), .A2(n609), .ZN(n598) );
  NOR3_X1 U908 ( .A1(totalcoeffs_0_), .A2(n586), .A3(n799), .ZN(n971) );
  INV_X1 U909 ( .I(n732), .ZN(n799) );
  NAND2_X1 U910 ( .A1(n741), .A2(n640), .ZN(n969) );
  NOR2_X1 U911 ( .A1(n641), .A2(totalcoeffs_2_), .ZN(n741) );
  NAND3_X1 U912 ( .A1(n627), .A2(n981), .A3(n774), .ZN(n968) );
  NAND3_X1 U913 ( .A1(n646), .A2(totalcoeffs_1_), .A3(n657), .ZN(n967) );
  NAND4_X1 U914 ( .A1(n913), .A2(n607), .A3(n677), .A4(n588), .ZN(n964) );
  NAND2_X1 U915 ( .A1(totalcoeffs_1_), .A2(n982), .ZN(n963) );
  NAND2_X1 U916 ( .A1(n983), .A2(n984), .ZN(n982) );
  NAND3_X1 U917 ( .A1(n627), .A2(n640), .A3(n985), .ZN(n984) );
  NOR2_X1 U918 ( .A1(n986), .A2(n588), .ZN(n627) );
  NAND2_X1 U919 ( .A1(n733), .A2(n987), .ZN(n983) );
  NAND2_X1 U920 ( .A1(n810), .A2(n988), .ZN(n987) );
  NAND2_X1 U921 ( .A1(n629), .A2(n677), .ZN(n988) );
  INV_X1 U922 ( .I(n989), .ZN(n810) );
  NAND3_X1 U923 ( .A1(n990), .A2(n991), .A3(n992), .ZN(coeff_token_1_) );
  NAND2_X1 U924 ( .A1(n866), .A2(n993), .ZN(n992) );
  NAND4_X1 U925 ( .A1(n994), .A2(n995), .A3(n996), .A4(n997), .ZN(n993) );
  NOR4_X1 U926 ( .A1(n998), .A2(n999), .A3(n1000), .A4(n1001), .ZN(n997) );
  NOR2_X1 U927 ( .A1(ctable_1_), .A2(n1002), .ZN(n1001) );
  NOR3_X1 U928 ( .A1(n1003), .A2(n1004), .A3(n1005), .ZN(n1002) );
  NOR2_X1 U929 ( .A1(n1006), .A2(n675), .ZN(n1005) );
  NOR2_X1 U930 ( .A1(n640), .A2(n655), .ZN(n1006) );
  NOR2_X1 U931 ( .A1(n664), .A2(n660), .ZN(n655) );
  NOR2_X1 U932 ( .A1(n660), .A2(ctable_0_), .ZN(n640) );
  NOR4_X1 U933 ( .A1(n952), .A2(n757), .A3(n660), .A4(n713), .ZN(n1004) );
  NOR2_X1 U934 ( .A1(n1007), .A2(n1008), .ZN(n1003) );
  NOR2_X1 U935 ( .A1(n890), .A2(totalcoeffs_2_), .ZN(n1007) );
  AND2_X1 U936 ( .A1(n588), .A2(n1009), .Z(n1000) );
  NOR2_X1 U937 ( .A1(totalcoeffs_1_), .A2(n1010), .ZN(n999) );
  NOR4_X1 U938 ( .A1(n1011), .A2(n1012), .A3(n1013), .A4(n1014), .ZN(n1010) );
  NOR2_X1 U939 ( .A1(totalcoeffs_3_), .A2(n1015), .ZN(n1014) );
  NOR2_X1 U940 ( .A1(n1016), .A2(n1017), .ZN(n1015) );
  NOR2_X1 U941 ( .A1(n613), .A2(n663), .ZN(n1017) );
  INV_X1 U942 ( .I(n907), .ZN(n663) );
  NOR2_X1 U943 ( .A1(n1018), .A2(n677), .ZN(n1016) );
  NOR2_X1 U944 ( .A1(n1019), .A2(n1020), .ZN(n1018) );
  NOR2_X1 U945 ( .A1(n848), .A2(n1008), .ZN(n1020) );
  AND2_X1 U946 ( .A1(n657), .A2(n816), .Z(n1019) );
  NOR2_X1 U947 ( .A1(n660), .A2(n588), .ZN(n816) );
  NOR2_X1 U948 ( .A1(n1021), .A2(n642), .ZN(n1013) );
  NOR2_X1 U949 ( .A1(n1022), .A2(n1023), .ZN(n1012) );
  NOR2_X1 U950 ( .A1(n1024), .A2(n1025), .ZN(n1022) );
  NOR3_X1 U951 ( .A1(n848), .A2(n586), .A3(n660), .ZN(n1024) );
  NOR3_X1 U952 ( .A1(n693), .A2(n595), .A3(n613), .ZN(n1011) );
  NOR2_X1 U953 ( .A1(n1026), .A2(n609), .ZN(n998) );
  NOR4_X1 U954 ( .A1(n1027), .A2(n1028), .A3(n1029), .A4(n1030), .ZN(n1026) );
  NOR2_X1 U955 ( .A1(n1031), .A2(n628), .ZN(n1030) );
  NOR2_X1 U956 ( .A1(n1032), .A2(n600), .ZN(n1031) );
  NOR2_X1 U957 ( .A1(trailingones_0_), .A2(n615), .ZN(n1032) );
  INV_X1 U958 ( .I(n603), .ZN(n615) );
  NOR2_X1 U959 ( .A1(n986), .A2(n677), .ZN(n603) );
  NOR2_X1 U960 ( .A1(n1033), .A2(n613), .ZN(n1029) );
  INV_X1 U961 ( .I(n631), .ZN(n613) );
  NOR2_X1 U962 ( .A1(n1034), .A2(n1025), .ZN(n1033) );
  NOR2_X1 U963 ( .A1(n588), .A2(n596), .ZN(n1025) );
  INV_X1 U964 ( .I(n614), .ZN(n596) );
  AND2_X1 U965 ( .A1(n623), .A2(n624), .Z(n1034) );
  NOR2_X1 U966 ( .A1(n595), .A2(totalcoeffs_3_), .ZN(n624) );
  NAND2_X1 U967 ( .A1(n1035), .A2(n897), .ZN(n1028) );
  NAND2_X1 U968 ( .A1(n631), .A2(n790), .ZN(n897) );
  NAND4_X1 U969 ( .A1(n732), .A2(n629), .A3(ctable_0_), .A4(n660), .ZN(n1035)
         );
  NOR3_X1 U970 ( .A1(n641), .A2(totalcoeffs_3_), .A3(ctable_1_), .ZN(n1027) );
  INV_X1 U971 ( .I(n708), .ZN(n641) );
  NAND2_X1 U972 ( .A1(n577), .A2(n1036), .ZN(n996) );
  NAND2_X1 U973 ( .A1(n730), .A2(n1037), .ZN(n1036) );
  NAND2_X1 U974 ( .A1(n766), .A2(n660), .ZN(n1037) );
  INV_X1 U975 ( .I(n839), .ZN(n730) );
  NOR2_X1 U976 ( .A1(n848), .A2(n713), .ZN(n839) );
  INV_X1 U977 ( .I(n656), .ZN(n713) );
  NAND3_X1 U978 ( .A1(ctable_0_), .A2(n1038), .A3(n600), .ZN(n995) );
  NAND2_X1 U979 ( .A1(n629), .A2(n978), .ZN(n1038) );
  NAND3_X1 U980 ( .A1(n1039), .A2(n617), .A3(n631), .ZN(n994) );
  NAND2_X1 U981 ( .A1(n693), .A2(n1040), .ZN(n1039) );
  NAND3_X1 U982 ( .A1(n978), .A2(n602), .A3(ctable_1_), .ZN(n1040) );
  INV_X1 U983 ( .I(n623), .ZN(n602) );
  INV_X1 U984 ( .I(n890), .ZN(n693) );
  NOR2_X1 U985 ( .A1(n588), .A2(n586), .ZN(n890) );
  NAND2_X1 U986 ( .A1(n800), .A2(n1041), .ZN(n991) );
  NAND2_X1 U987 ( .A1(n1042), .A2(n1043), .ZN(n1041) );
  NAND2_X1 U988 ( .A1(n1009), .A2(n590), .ZN(n1043) );
  NOR3_X1 U989 ( .A1(n981), .A2(n1021), .A3(n978), .ZN(n1009) );
  NOR2_X1 U990 ( .A1(n600), .A2(n952), .ZN(n1021) );
  NAND2_X1 U991 ( .A1(n646), .A2(n1044), .ZN(n1042) );
  NAND2_X1 U992 ( .A1(n1045), .A2(n1046), .ZN(n1044) );
  NAND2_X1 U993 ( .A1(ctable_2_), .A2(n1047), .ZN(n1046) );
  NAND2_X1 U994 ( .A1(n1048), .A2(n933), .ZN(n1047) );
  INV_X1 U995 ( .I(n736), .ZN(n933) );
  NOR2_X1 U996 ( .A1(n675), .A2(n664), .ZN(n736) );
  NAND2_X1 U997 ( .A1(trailingones_0_), .A2(n617), .ZN(n664) );
  NAND2_X1 U998 ( .A1(n1049), .A2(n1050), .ZN(n1048) );
  NAND3_X1 U999 ( .A1(n692), .A2(n617), .A3(n978), .ZN(n1050) );
  INV_X1 U1000 ( .I(n773), .ZN(n978) );
  NAND2_X1 U1001 ( .A1(n1051), .A2(n848), .ZN(n1049) );
  NAND2_X1 U1002 ( .A1(n658), .A2(n609), .ZN(n1051) );
  NAND2_X1 U1003 ( .A1(n584), .A2(n781), .ZN(n1045) );
  NOR2_X1 U1004 ( .A1(totalcoeffs_0_), .A2(totalcoeffs_1_), .ZN(n584) );
  NAND2_X1 U1005 ( .A1(n989), .A2(n1052), .ZN(n990) );
  NAND2_X1 U1006 ( .A1(n1053), .A2(n1054), .ZN(n1052) );
  NAND3_X1 U1007 ( .A1(n781), .A2(trailingones_0_), .A3(n800), .ZN(n1054) );
  NAND2_X1 U1008 ( .A1(n647), .A2(n1055), .ZN(n1053) );
  NAND2_X1 U1009 ( .A1(n1056), .A2(n1057), .ZN(n1055) );
  NAND2_X1 U1010 ( .A1(totalcoeffs_4_), .A2(n1058), .ZN(n1057) );
  NAND2_X1 U1011 ( .A1(n1023), .A2(n1059), .ZN(n1058) );
  NAND2_X1 U1012 ( .A1(n815), .A2(trailingones_0_), .ZN(n1059) );
  NOR2_X1 U1013 ( .A1(ctable_1_), .A2(trailingones_1_), .ZN(n815) );
  INV_X1 U1014 ( .I(n600), .ZN(n1023) );
  NOR2_X1 U1015 ( .A1(n986), .A2(n595), .ZN(n600) );
  NAND2_X1 U1016 ( .A1(n577), .A2(n708), .ZN(n1056) );
  NOR2_X1 U1017 ( .A1(n764), .A2(totalcoeffs_1_), .ZN(n647) );
  NAND2_X1 U1018 ( .A1(n660), .A2(n617), .ZN(n764) );
  NOR2_X1 U1019 ( .A1(ctable_2_), .A2(totalcoeffs_3_), .ZN(n989) );
  NAND4_X1 U1020 ( .A1(n1060), .A2(n1061), .A3(n1062), .A4(n1063), .ZN(
        coeff_token_0_) );
  NAND3_X1 U1021 ( .A1(n1064), .A2(n590), .A3(n607), .ZN(n1063) );
  NAND2_X1 U1022 ( .A1(n1065), .A2(n1066), .ZN(n1064) );
  NAND3_X1 U1023 ( .A1(n1067), .A2(n660), .A3(n708), .ZN(n1066) );
  NOR2_X1 U1024 ( .A1(trailingones_0_), .A2(trailingones_1_), .ZN(n708) );
  NAND2_X1 U1025 ( .A1(n1068), .A2(n1069), .ZN(n1067) );
  NAND2_X1 U1026 ( .A1(ctable_1_), .A2(n589), .ZN(n1069) );
  INV_X1 U1027 ( .I(n577), .ZN(n1068) );
  NOR2_X1 U1028 ( .A1(n677), .A2(ctable_1_), .ZN(n577) );
  NAND3_X1 U1029 ( .A1(n623), .A2(totalcoeffs_4_), .A3(n870), .ZN(n1065) );
  NAND3_X1 U1030 ( .A1(n732), .A2(n589), .A3(n801), .ZN(n1062) );
  INV_X1 U1031 ( .I(n876), .ZN(n801) );
  NAND2_X1 U1032 ( .A1(n579), .A2(n590), .ZN(n876) );
  NOR3_X1 U1033 ( .A1(n927), .A2(totalcoeffs_0_), .A3(n650), .ZN(n579) );
  INV_X1 U1034 ( .I(totalcoeffs_4_), .ZN(n650) );
  INV_X1 U1035 ( .I(n607), .ZN(n927) );
  INV_X1 U1036 ( .I(n870), .ZN(n589) );
  NOR2_X1 U1037 ( .A1(n986), .A2(trailingones_0_), .ZN(n732) );
  NAND2_X1 U1038 ( .A1(n800), .A2(n1070), .ZN(n1061) );
  NAND4_X1 U1039 ( .A1(n1071), .A2(n1072), .A3(n1073), .A4(n1074), .ZN(n1070)
         );
  NAND3_X1 U1040 ( .A1(n952), .A2(n773), .A3(n985), .ZN(n1074) );
  NOR2_X1 U1041 ( .A1(n588), .A2(ctable_0_), .ZN(n952) );
  NAND3_X1 U1042 ( .A1(totalcoeffs_0_), .A2(n1075), .A3(n631), .ZN(n1073) );
  NOR2_X1 U1043 ( .A1(ctable_0_), .A2(trailingones_1_), .ZN(n631) );
  OR2_X1 U1044 ( .A1(n607), .A2(n985), .Z(n1075) );
  NOR2_X1 U1045 ( .A1(n590), .A2(n981), .ZN(n985) );
  NOR2_X1 U1046 ( .A1(n981), .A2(totalcoeffs_1_), .ZN(n607) );
  NAND2_X1 U1047 ( .A1(n646), .A2(n1076), .ZN(n1072) );
  NAND2_X1 U1048 ( .A1(n1077), .A2(n1078), .ZN(n1076) );
  NAND4_X1 U1049 ( .A1(n623), .A2(ctable_2_), .A3(n781), .A4(n609), .ZN(n1078)
         );
  NOR2_X1 U1050 ( .A1(n617), .A2(trailingones_1_), .ZN(n781) );
  NAND3_X1 U1051 ( .A1(n1079), .A2(n674), .A3(n857), .ZN(n1077) );
  NAND2_X1 U1052 ( .A1(totalcoeffs_1_), .A2(n1080), .ZN(n1079) );
  NAND2_X1 U1053 ( .A1(trailingones_1_), .A2(n660), .ZN(n1080) );
  NAND2_X1 U1054 ( .A1(n1081), .A2(n590), .ZN(n1071) );
  INV_X1 U1055 ( .I(ctable_2_), .ZN(n590) );
  NAND4_X1 U1056 ( .A1(n1082), .A2(n1083), .A3(n1084), .A4(n1085), .ZN(n1081)
         );
  NAND3_X1 U1057 ( .A1(trailingones_1_), .A2(n629), .A3(n773), .ZN(n1085) );
  NOR2_X1 U1058 ( .A1(n660), .A2(n609), .ZN(n773) );
  NOR2_X1 U1059 ( .A1(n762), .A2(n1086), .ZN(n1084) );
  NOR3_X1 U1060 ( .A1(n848), .A2(n766), .A3(n1087), .ZN(n1086) );
  NOR2_X1 U1061 ( .A1(n913), .A2(totalcoeffs_1_), .ZN(n1087) );
  INV_X1 U1062 ( .I(n857), .ZN(n848) );
  NOR2_X1 U1063 ( .A1(n700), .A2(n609), .ZN(n762) );
  INV_X1 U1064 ( .I(n757), .ZN(n700) );
  NOR2_X1 U1065 ( .A1(totalcoeffs_3_), .A2(trailingones_0_), .ZN(n757) );
  NAND2_X1 U1066 ( .A1(n907), .A2(n1088), .ZN(n1083) );
  NAND2_X1 U1067 ( .A1(n1008), .A2(n675), .ZN(n1088) );
  INV_X1 U1068 ( .I(n766), .ZN(n675) );
  INV_X1 U1069 ( .I(n733), .ZN(n1008) );
  NOR2_X1 U1070 ( .A1(n617), .A2(trailingones_0_), .ZN(n907) );
  NAND2_X1 U1071 ( .A1(n1089), .A2(n588), .ZN(n1082) );
  NAND3_X1 U1072 ( .A1(n910), .A2(n1090), .A3(n1091), .ZN(n1089) );
  NAND2_X1 U1073 ( .A1(n733), .A2(ctable_0_), .ZN(n1091) );
  NAND2_X1 U1074 ( .A1(n774), .A2(totalcoeffs_3_), .ZN(n1090) );
  NOR2_X1 U1075 ( .A1(n660), .A2(totalcoeffs_1_), .ZN(n774) );
  NAND2_X1 U1076 ( .A1(n863), .A2(n981), .ZN(n910) );
  INV_X1 U1077 ( .I(n629), .ZN(n981) );
  NOR2_X1 U1078 ( .A1(ctable_1_), .A2(totalcoeffs_4_), .ZN(n800) );
  NAND2_X1 U1079 ( .A1(n866), .A2(n1092), .ZN(n1060) );
  NAND4_X1 U1080 ( .A1(n1093), .A2(n1094), .A3(n1095), .A4(n1096), .ZN(n1092)
         );
  NAND3_X1 U1081 ( .A1(ctable_1_), .A2(n1097), .A3(n623), .ZN(n1096) );
  NOR2_X1 U1082 ( .A1(n588), .A2(totalcoeffs_0_), .ZN(n623) );
  NAND3_X1 U1083 ( .A1(n1098), .A2(n1099), .A3(n1100), .ZN(n1097) );
  NAND2_X1 U1084 ( .A1(n657), .A2(n586), .ZN(n1100) );
  NAND2_X1 U1085 ( .A1(n863), .A2(n790), .ZN(n1099) );
  NOR2_X1 U1086 ( .A1(n586), .A2(totalcoeffs_2_), .ZN(n790) );
  NAND2_X1 U1087 ( .A1(n766), .A2(n629), .ZN(n1098) );
  NOR2_X1 U1088 ( .A1(n609), .A2(trailingones_1_), .ZN(n766) );
  NAND2_X1 U1089 ( .A1(n656), .A2(n1101), .ZN(n1095) );
  NAND3_X1 U1090 ( .A1(n1102), .A2(n1103), .A3(n1104), .ZN(n1101) );
  NAND2_X1 U1091 ( .A1(n575), .A2(n857), .ZN(n1104) );
  NOR2_X1 U1092 ( .A1(totalcoeffs_2_), .A2(trailingones_0_), .ZN(n857) );
  NOR2_X1 U1093 ( .A1(n595), .A2(ctable_0_), .ZN(n575) );
  NAND2_X1 U1094 ( .A1(n658), .A2(n629), .ZN(n1103) );
  NAND2_X1 U1095 ( .A1(n646), .A2(n588), .ZN(n1102) );
  NOR2_X1 U1096 ( .A1(ctable_0_), .A2(totalcoeffs_3_), .ZN(n646) );
  NOR2_X1 U1097 ( .A1(totalcoeffs_1_), .A2(trailingones_1_), .ZN(n656) );
  NAND2_X1 U1098 ( .A1(trailingones_0_), .A2(n1105), .ZN(n1094) );
  NAND2_X1 U1099 ( .A1(n1106), .A2(n1107), .ZN(n1105) );
  NAND2_X1 U1100 ( .A1(n1108), .A2(n858), .ZN(n1107) );
  NAND2_X1 U1101 ( .A1(n1109), .A2(n1110), .ZN(n858) );
  NAND2_X1 U1102 ( .A1(n733), .A2(totalcoeffs_1_), .ZN(n1110) );
  NOR2_X1 U1103 ( .A1(totalcoeffs_0_), .A2(trailingones_1_), .ZN(n733) );
  NAND2_X1 U1104 ( .A1(n789), .A2(totalcoeffs_0_), .ZN(n1109) );
  NOR2_X1 U1105 ( .A1(n986), .A2(n609), .ZN(n789) );
  NAND2_X1 U1106 ( .A1(n1111), .A2(n1112), .ZN(n1108) );
  NAND2_X1 U1107 ( .A1(n694), .A2(totalcoeffs_2_), .ZN(n1112) );
  NOR2_X1 U1108 ( .A1(n586), .A2(n677), .ZN(n694) );
  NAND2_X1 U1109 ( .A1(n629), .A2(ctable_0_), .ZN(n1111) );
  NAND2_X1 U1110 ( .A1(n870), .A2(n1113), .ZN(n1106) );
  NAND2_X1 U1111 ( .A1(n629), .A2(n692), .ZN(n1113) );
  NOR2_X1 U1112 ( .A1(totalcoeffs_2_), .A2(totalcoeffs_3_), .ZN(n629) );
  NOR2_X1 U1113 ( .A1(n595), .A2(n677), .ZN(n870) );
  INV_X1 U1114 ( .I(ctable_1_), .ZN(n595) );
  NAND2_X1 U1115 ( .A1(n1114), .A2(n677), .ZN(n1093) );
  INV_X1 U1116 ( .I(ctable_0_), .ZN(n677) );
  NAND4_X1 U1117 ( .A1(n1115), .A2(n1116), .A3(n1117), .A4(n1118), .ZN(n1114)
         );
  NAND3_X1 U1118 ( .A1(trailingones_1_), .A2(totalcoeffs_3_), .A3(n658), .ZN(
        n1118) );
  OR2_X1 U1119 ( .A1(n642), .A2(n674), .Z(n1117) );
  INV_X1 U1120 ( .I(n863), .ZN(n674) );
  NOR2_X1 U1121 ( .A1(n986), .A2(totalcoeffs_1_), .ZN(n863) );
  NAND2_X1 U1122 ( .A1(n614), .A2(n660), .ZN(n642) );
  NOR2_X1 U1123 ( .A1(n617), .A2(totalcoeffs_3_), .ZN(n614) );
  NAND2_X1 U1124 ( .A1(n657), .A2(n588), .ZN(n1116) );
  NOR2_X1 U1125 ( .A1(n986), .A2(n617), .ZN(n657) );
  INV_X1 U1126 ( .I(trailingones_1_), .ZN(n986) );
  NOR2_X1 U1127 ( .A1(n1119), .A2(n1120), .ZN(n1115) );
  NOR3_X1 U1128 ( .A1(totalcoeffs_1_), .A2(n628), .A3(n692), .ZN(n1120) );
  INV_X1 U1129 ( .I(n913), .ZN(n692) );
  NOR2_X1 U1130 ( .A1(n660), .A2(trailingones_1_), .ZN(n913) );
  INV_X1 U1131 ( .I(totalcoeffs_0_), .ZN(n660) );
  INV_X1 U1132 ( .I(n639), .ZN(n628) );
  NOR2_X1 U1133 ( .A1(n586), .A2(n617), .ZN(n639) );
  INV_X1 U1134 ( .I(totalcoeffs_2_), .ZN(n617) );
  INV_X1 U1135 ( .I(totalcoeffs_3_), .ZN(n586) );
  NOR2_X1 U1136 ( .A1(n1121), .A2(n609), .ZN(n1119) );
  INV_X1 U1137 ( .I(totalcoeffs_1_), .ZN(n609) );
  AND2_X1 U1138 ( .A1(n718), .A2(n779), .Z(n1121) );
  INV_X1 U1139 ( .I(n658), .ZN(n779) );
  NOR2_X1 U1140 ( .A1(totalcoeffs_0_), .A2(trailingones_0_), .ZN(n658) );
  NAND2_X1 U1141 ( .A1(totalcoeffs_3_), .A2(n588), .ZN(n718) );
  INV_X1 U1142 ( .I(trailingones_0_), .ZN(n588) );
  NOR2_X1 U1143 ( .A1(ctable_2_), .A2(totalcoeffs_4_), .ZN(n866) );
endmodule

