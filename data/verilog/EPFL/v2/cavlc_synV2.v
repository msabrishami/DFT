/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Tue Nov 17 18:51:57 2020
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
         n1114, n1115, n1116, n1117, n1118, n1119, n1120, n1121, n1122;

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
  NAND4_X1 U599 ( .A1(n604), .A2(n605), .A3(n606), .A4(n607), .ZN(n592) );
  NAND2_X1 U600 ( .A1(totalcoeffs_4_), .A2(n608), .ZN(n607) );
  NAND2_X1 U601 ( .A1(n609), .A2(n610), .ZN(n606) );
  NAND2_X1 U602 ( .A1(n611), .A2(n612), .ZN(n605) );
  NAND2_X1 U603 ( .A1(n613), .A2(n614), .ZN(n611) );
  NAND3_X1 U604 ( .A1(n615), .A2(n616), .A3(n617), .ZN(n614) );
  NAND2_X1 U605 ( .A1(n588), .A2(n618), .ZN(n615) );
  NAND2_X1 U606 ( .A1(n619), .A2(n620), .ZN(n613) );
  NAND2_X1 U607 ( .A1(totalcoeffs_1_), .A2(n621), .ZN(n604) );
  NAND4_X1 U608 ( .A1(n622), .A2(n623), .A3(n624), .A4(n625), .ZN(n621) );
  NAND3_X1 U609 ( .A1(n626), .A2(n620), .A3(n600), .ZN(n625) );
  NOR2_X1 U610 ( .A1(n627), .A2(n628), .ZN(n624) );
  NOR3_X1 U611 ( .A1(n629), .A2(n630), .A3(n631), .ZN(n628) );
  NAND2_X1 U612 ( .A1(n632), .A2(n633), .ZN(n623) );
  NAND2_X1 U613 ( .A1(n634), .A2(n602), .ZN(n633) );
  NAND2_X1 U614 ( .A1(n603), .A2(n635), .ZN(n622) );
  NAND4_X1 U615 ( .A1(n636), .A2(n637), .A3(n638), .A4(n589), .ZN(n591) );
  NAND2_X1 U616 ( .A1(n639), .A2(n640), .ZN(n638) );
  NAND2_X1 U617 ( .A1(n590), .A2(n641), .ZN(n640) );
  NAND3_X1 U618 ( .A1(n642), .A2(n595), .A3(n643), .ZN(n641) );
  NAND2_X1 U619 ( .A1(n612), .A2(n644), .ZN(n639) );
  NAND2_X1 U620 ( .A1(ctable_2_), .A2(n645), .ZN(n637) );
  NAND2_X1 U621 ( .A1(totalcoeffs_0_), .A2(n609), .ZN(n636) );
  NAND2_X1 U622 ( .A1(n646), .A2(n647), .ZN(ctoken_len_2_) );
  NAND2_X1 U623 ( .A1(totalcoeffs_4_), .A2(n648), .ZN(n647) );
  NAND3_X1 U624 ( .A1(n649), .A2(n590), .A3(n650), .ZN(n648) );
  NAND3_X1 U625 ( .A1(n651), .A2(n652), .A3(n610), .ZN(n646) );
  NAND2_X1 U626 ( .A1(n619), .A2(n653), .ZN(n652) );
  NAND3_X1 U627 ( .A1(n654), .A2(n655), .A3(n656), .ZN(n653) );
  NAND2_X1 U628 ( .A1(n657), .A2(n658), .ZN(n656) );
  NAND3_X1 U629 ( .A1(n659), .A2(n612), .A3(n660), .ZN(n655) );
  NAND2_X1 U630 ( .A1(n661), .A2(n662), .ZN(n654) );
  NAND2_X1 U631 ( .A1(n663), .A2(n664), .ZN(n661) );
  NAND3_X1 U632 ( .A1(n665), .A2(n666), .A3(n658), .ZN(n664) );
  INV_X1 U633 ( .I(n667), .ZN(n663) );
  NAND2_X1 U634 ( .A1(n590), .A2(n668), .ZN(n651) );
  NAND4_X1 U635 ( .A1(n669), .A2(n670), .A3(n671), .A4(n672), .ZN(n668) );
  NAND2_X1 U636 ( .A1(n575), .A2(n673), .ZN(n672) );
  NAND2_X1 U637 ( .A1(n631), .A2(n674), .ZN(n673) );
  NAND3_X1 U638 ( .A1(n675), .A2(n676), .A3(totalcoeffs_3_), .ZN(n674) );
  NAND2_X1 U639 ( .A1(n626), .A2(n677), .ZN(n675) );
  NAND2_X1 U640 ( .A1(n678), .A2(n643), .ZN(n671) );
  NAND2_X1 U641 ( .A1(n582), .A2(n679), .ZN(n670) );
  NOR3_X1 U642 ( .A1(n631), .A2(n626), .A3(n612), .ZN(n582) );
  NAND2_X1 U643 ( .A1(n595), .A2(n680), .ZN(n669) );
  NAND4_X1 U644 ( .A1(n681), .A2(n682), .A3(n683), .A4(n684), .ZN(n680) );
  NOR4_X1 U645 ( .A1(n685), .A2(n686), .A3(n687), .A4(n688), .ZN(n684) );
  AND2_X1 U646 ( .A1(n635), .A2(n689), .Z(n688) );
  NOR2_X1 U647 ( .A1(n690), .A2(n691), .ZN(n687) );
  NOR2_X1 U648 ( .A1(n692), .A2(n693), .ZN(n690) );
  NOR2_X1 U649 ( .A1(n588), .A2(n694), .ZN(n693) );
  NOR2_X1 U650 ( .A1(trailingones_1_), .A2(n695), .ZN(n692) );
  NOR4_X1 U651 ( .A1(n696), .A2(n697), .A3(n612), .A4(n587), .ZN(n686) );
  NOR2_X1 U652 ( .A1(n626), .A2(ctable_0_), .ZN(n697) );
  NOR2_X1 U653 ( .A1(n698), .A2(n699), .ZN(n685) );
  NOR2_X1 U654 ( .A1(n700), .A2(n701), .ZN(n698) );
  NOR2_X1 U655 ( .A1(ctable_0_), .A2(n596), .ZN(n701) );
  NOR2_X1 U656 ( .A1(totalcoeffs_0_), .A2(n702), .ZN(n700) );
  NOR2_X1 U657 ( .A1(n703), .A2(n704), .ZN(n683) );
  NOR2_X1 U658 ( .A1(n705), .A2(n706), .ZN(n704) );
  NOR2_X1 U659 ( .A1(n707), .A2(n708), .ZN(n705) );
  NOR2_X1 U660 ( .A1(n709), .A2(n598), .ZN(n708) );
  NOR2_X1 U661 ( .A1(totalcoeffs_0_), .A2(n679), .ZN(n709) );
  AND3_X1 U662 ( .A1(n696), .A2(n620), .A3(totalcoeffs_1_), .Z(n707) );
  AND3_X1 U663 ( .A1(n650), .A2(ctable_0_), .A3(n710), .Z(n703) );
  NAND3_X1 U664 ( .A1(n711), .A2(n588), .A3(n617), .ZN(n682) );
  NAND2_X1 U665 ( .A1(n712), .A2(n713), .ZN(n711) );
  NAND2_X1 U666 ( .A1(n679), .A2(n612), .ZN(n713) );
  NAND3_X1 U667 ( .A1(n714), .A2(n715), .A3(n716), .ZN(n681) );
  INV_X1 U668 ( .I(n691), .ZN(n716) );
  NAND2_X1 U669 ( .A1(n620), .A2(n717), .ZN(n691) );
  NAND2_X1 U670 ( .A1(n718), .A2(n719), .ZN(n717) );
  NAND2_X1 U671 ( .A1(ctable_0_), .A2(n612), .ZN(n718) );
  NAND2_X1 U672 ( .A1(n644), .A2(n720), .ZN(n714) );
  NOR3_X1 U673 ( .A1(n721), .A2(n722), .A3(n723), .ZN(ctoken_len_1_) );
  NOR2_X1 U674 ( .A1(ctable_2_), .A2(n724), .ZN(n723) );
  NOR2_X1 U675 ( .A1(n725), .A2(n726), .ZN(n724) );
  NOR2_X1 U676 ( .A1(totalcoeffs_4_), .A2(n727), .ZN(n726) );
  NOR4_X1 U677 ( .A1(n728), .A2(n729), .A3(n730), .A4(n731), .ZN(n727) );
  NOR3_X1 U678 ( .A1(n732), .A2(totalcoeffs_0_), .A3(ctable_0_), .ZN(n731) );
  NOR3_X1 U679 ( .A1(n629), .A2(n733), .A3(n598), .ZN(n730) );
  NOR2_X1 U680 ( .A1(n734), .A2(n735), .ZN(n733) );
  NOR2_X1 U681 ( .A1(n736), .A2(n737), .ZN(n729) );
  NOR4_X1 U682 ( .A1(n738), .A2(n667), .A3(n739), .A4(n740), .ZN(n736) );
  NOR2_X1 U683 ( .A1(n741), .A2(n586), .ZN(n740) );
  NOR2_X1 U684 ( .A1(n742), .A2(n743), .ZN(n741) );
  NOR2_X1 U685 ( .A1(n744), .A2(n745), .ZN(n742) );
  NOR2_X1 U686 ( .A1(n715), .A2(n746), .ZN(n739) );
  NAND4_X1 U687 ( .A1(n747), .A2(n748), .A3(n749), .A4(n750), .ZN(n728) );
  NAND2_X1 U688 ( .A1(totalcoeffs_1_), .A2(n751), .ZN(n750) );
  NAND2_X1 U689 ( .A1(n752), .A2(n753), .ZN(n751) );
  NAND3_X1 U690 ( .A1(n643), .A2(n620), .A3(n600), .ZN(n753) );
  NAND2_X1 U691 ( .A1(n649), .A2(n754), .ZN(n752) );
  NAND2_X1 U692 ( .A1(n755), .A2(n756), .ZN(n754) );
  NAND2_X1 U693 ( .A1(n630), .A2(totalcoeffs_2_), .ZN(n756) );
  NAND4_X1 U694 ( .A1(n757), .A2(n644), .A3(totalcoeffs_2_), .A4(n612), .ZN(
        n749) );
  NAND2_X1 U695 ( .A1(n737), .A2(n758), .ZN(n757) );
  NAND2_X1 U696 ( .A1(n759), .A2(n679), .ZN(n758) );
  NAND2_X1 U697 ( .A1(n577), .A2(n760), .ZN(n748) );
  NAND3_X1 U698 ( .A1(n761), .A2(n762), .A3(n763), .ZN(n760) );
  NAND2_X1 U699 ( .A1(n764), .A2(n659), .ZN(n763) );
  NAND3_X1 U700 ( .A1(n765), .A2(n766), .A3(n767), .ZN(n762) );
  NAND2_X1 U701 ( .A1(n744), .A2(n631), .ZN(n765) );
  NAND3_X1 U702 ( .A1(n626), .A2(n586), .A3(n768), .ZN(n761) );
  NAND2_X1 U703 ( .A1(n769), .A2(n595), .ZN(n747) );
  NAND4_X1 U704 ( .A1(n770), .A2(n771), .A3(n772), .A4(n773), .ZN(n769) );
  NAND3_X1 U705 ( .A1(n635), .A2(n774), .A3(n775), .ZN(n773) );
  NAND3_X1 U706 ( .A1(n642), .A2(trailingones_0_), .A3(n603), .ZN(n772) );
  NAND2_X1 U707 ( .A1(n776), .A2(n678), .ZN(n771) );
  NAND2_X1 U708 ( .A1(totalcoeffs_1_), .A2(n777), .ZN(n770) );
  NAND2_X1 U709 ( .A1(n778), .A2(n779), .ZN(n777) );
  NAND2_X1 U710 ( .A1(n696), .A2(n780), .ZN(n779) );
  NAND2_X1 U711 ( .A1(n781), .A2(n782), .ZN(n780) );
  NAND2_X1 U712 ( .A1(n706), .A2(n620), .ZN(n782) );
  NAND2_X1 U713 ( .A1(n660), .A2(n783), .ZN(n778) );
  NOR2_X1 U714 ( .A1(n784), .A2(n785), .ZN(n725) );
  NOR2_X1 U715 ( .A1(n786), .A2(n787), .ZN(n784) );
  NOR2_X1 U716 ( .A1(ctable_0_), .A2(n788), .ZN(n787) );
  NOR2_X1 U717 ( .A1(n789), .A2(n790), .ZN(n788) );
  NOR3_X1 U718 ( .A1(n612), .A2(n630), .A3(n631), .ZN(n790) );
  AND3_X1 U719 ( .A1(n791), .A2(n792), .A3(n626), .Z(n789) );
  NOR4_X1 U720 ( .A1(n620), .A2(n588), .A3(n612), .A4(n793), .ZN(n786) );
  NOR3_X1 U721 ( .A1(n785), .A2(n794), .A3(n719), .ZN(n722) );
  NOR3_X1 U722 ( .A1(n795), .A2(n796), .A3(n797), .ZN(n794) );
  NOR3_X1 U723 ( .A1(n590), .A2(n715), .A3(n755), .ZN(n797) );
  NOR3_X1 U724 ( .A1(ctable_2_), .A2(n612), .A3(n644), .ZN(n796) );
  NOR2_X1 U725 ( .A1(n798), .A2(n620), .ZN(n795) );
  NOR2_X1 U726 ( .A1(n799), .A2(n800), .ZN(n798) );
  NOR2_X1 U727 ( .A1(n602), .A2(n715), .ZN(n800) );
  NOR2_X1 U728 ( .A1(n745), .A2(n801), .ZN(n799) );
  INV_X1 U729 ( .I(n802), .ZN(n785) );
  NOR4_X1 U730 ( .A1(n803), .A2(n804), .A3(n805), .A4(n806), .ZN(ctoken_len_0_) );
  NOR2_X1 U731 ( .A1(totalcoeffs_4_), .A2(n807), .ZN(n805) );
  NOR3_X1 U732 ( .A1(n808), .A2(n809), .A3(n810), .ZN(n807) );
  NOR2_X1 U733 ( .A1(n811), .A2(n812), .ZN(n810) );
  NOR4_X1 U734 ( .A1(n813), .A2(n814), .A3(n815), .A4(n816), .ZN(n811) );
  AND2_X1 U735 ( .A1(n657), .A2(n817), .Z(n816) );
  NOR3_X1 U736 ( .A1(n746), .A2(n679), .A3(n699), .ZN(n815) );
  INV_X1 U737 ( .I(n818), .ZN(n746) );
  NOR3_X1 U738 ( .A1(n595), .A2(n744), .A3(n774), .ZN(n814) );
  NAND2_X1 U739 ( .A1(n587), .A2(n819), .ZN(n774) );
  NAND2_X1 U740 ( .A1(trailingones_1_), .A2(n620), .ZN(n819) );
  INV_X1 U741 ( .I(n783), .ZN(n587) );
  NOR2_X1 U742 ( .A1(n630), .A2(n710), .ZN(n744) );
  NOR3_X1 U743 ( .A1(ctable_1_), .A2(n588), .A3(n820), .ZN(n813) );
  NOR2_X1 U744 ( .A1(n821), .A2(n822), .ZN(n809) );
  INV_X1 U745 ( .I(n619), .ZN(n822) );
  NOR2_X1 U746 ( .A1(n719), .A2(ctable_1_), .ZN(n619) );
  INV_X1 U747 ( .I(n649), .ZN(n719) );
  NOR3_X1 U748 ( .A1(n823), .A2(n824), .A3(n825), .ZN(n821) );
  NOR2_X1 U749 ( .A1(n826), .A2(n590), .ZN(n825) );
  NOR3_X1 U750 ( .A1(n827), .A2(n743), .A3(n828), .ZN(n826) );
  NOR3_X1 U751 ( .A1(n715), .A2(totalcoeffs_0_), .A3(n620), .ZN(n828) );
  NOR2_X1 U752 ( .A1(n699), .A2(n755), .ZN(n827) );
  INV_X1 U753 ( .I(n657), .ZN(n755) );
  NOR2_X1 U754 ( .A1(n745), .A2(n665), .ZN(n824) );
  NOR2_X1 U755 ( .A1(n766), .A2(n677), .ZN(n823) );
  NOR2_X1 U756 ( .A1(ctable_2_), .A2(n829), .ZN(n808) );
  NOR3_X1 U757 ( .A1(n830), .A2(n831), .A3(n832), .ZN(n829) );
  NOR3_X1 U758 ( .A1(n602), .A2(n634), .A3(n596), .ZN(n832) );
  NOR3_X1 U759 ( .A1(n702), .A2(n679), .A3(n715), .ZN(n831) );
  NOR2_X1 U760 ( .A1(n618), .A2(n645), .ZN(n830) );
  NOR2_X1 U761 ( .A1(n833), .A2(n834), .ZN(n804) );
  NOR4_X1 U762 ( .A1(n835), .A2(n836), .A3(n837), .A4(n838), .ZN(n833) );
  NOR2_X1 U763 ( .A1(n839), .A2(n595), .ZN(n838) );
  NOR2_X1 U764 ( .A1(n840), .A2(n841), .ZN(n839) );
  NOR2_X1 U765 ( .A1(n842), .A2(n699), .ZN(n840) );
  NOR2_X1 U766 ( .A1(n818), .A2(n660), .ZN(n842) );
  NOR2_X1 U767 ( .A1(n843), .A2(n586), .ZN(n837) );
  NOR4_X1 U768 ( .A1(n844), .A2(n845), .A3(n667), .A4(n846), .ZN(n843) );
  NOR3_X1 U769 ( .A1(n847), .A2(n848), .A3(n629), .ZN(n846) );
  NOR2_X1 U770 ( .A1(n849), .A2(n626), .ZN(n848) );
  NOR2_X1 U771 ( .A1(totalcoeffs_0_), .A2(n612), .ZN(n849) );
  NOR2_X1 U772 ( .A1(n699), .A2(n850), .ZN(n667) );
  NOR2_X1 U773 ( .A1(trailingones_0_), .A2(n820), .ZN(n845) );
  INV_X1 U774 ( .I(n689), .ZN(n820) );
  NAND4_X1 U775 ( .A1(n851), .A2(n852), .A3(n853), .A4(n854), .ZN(n844) );
  NAND3_X1 U776 ( .A1(n768), .A2(n781), .A3(n793), .ZN(n854) );
  NAND2_X1 U777 ( .A1(n791), .A2(n643), .ZN(n853) );
  NAND2_X1 U778 ( .A1(n657), .A2(n600), .ZN(n852) );
  NAND2_X1 U779 ( .A1(n775), .A2(n734), .ZN(n851) );
  NOR2_X1 U780 ( .A1(n662), .A2(n732), .ZN(n836) );
  NAND4_X1 U781 ( .A1(n855), .A2(n856), .A3(n857), .A4(n858), .ZN(n835) );
  NAND3_X1 U782 ( .A1(n768), .A2(n642), .A3(n679), .ZN(n858) );
  NAND3_X1 U783 ( .A1(n859), .A2(n860), .A3(ctable_0_), .ZN(n857) );
  NAND2_X1 U784 ( .A1(n689), .A2(n620), .ZN(n856) );
  NOR2_X1 U785 ( .A1(n715), .A2(n793), .ZN(n689) );
  INV_X1 U786 ( .I(n643), .ZN(n793) );
  NAND2_X1 U787 ( .A1(totalcoeffs_2_), .A2(n861), .ZN(n855) );
  NAND3_X1 U788 ( .A1(n862), .A2(n863), .A3(n864), .ZN(n861) );
  NAND2_X1 U789 ( .A1(n865), .A2(n626), .ZN(n864) );
  NAND3_X1 U790 ( .A1(n660), .A2(n679), .A3(n791), .ZN(n863) );
  NAND3_X1 U791 ( .A1(ctable_1_), .A2(n644), .A3(totalcoeffs_1_), .ZN(n862) );
  NOR2_X1 U792 ( .A1(n866), .A2(n589), .ZN(coeff_token_5_) );
  NOR2_X1 U793 ( .A1(n867), .A2(n803), .ZN(n866) );
  NOR3_X1 U794 ( .A1(n834), .A2(n650), .A3(n586), .ZN(n867) );
  INV_X1 U795 ( .I(n868), .ZN(n834) );
  NAND2_X1 U796 ( .A1(n869), .A2(n870), .ZN(coeff_token_4_) );
  NAND4_X1 U797 ( .A1(n806), .A2(n650), .A3(totalcoeffs_4_), .A4(n586), .ZN(
        n870) );
  NOR2_X1 U798 ( .A1(n589), .A2(ctable_2_), .ZN(n806) );
  NAND3_X1 U799 ( .A1(n868), .A2(n871), .A3(n872), .ZN(n869) );
  NAND2_X1 U800 ( .A1(n873), .A2(n874), .ZN(n871) );
  NAND2_X1 U801 ( .A1(totalcoeffs_2_), .A2(n745), .ZN(n874) );
  INV_X1 U802 ( .I(n584), .ZN(n745) );
  NAND2_X1 U803 ( .A1(n650), .A2(totalcoeffs_3_), .ZN(n873) );
  NAND3_X1 U804 ( .A1(n875), .A2(n876), .A3(n877), .ZN(coeff_token_3_) );
  NAND2_X1 U805 ( .A1(n872), .A2(n803), .ZN(n877) );
  NAND2_X1 U806 ( .A1(n721), .A2(n630), .ZN(n876) );
  NOR2_X1 U807 ( .A1(n878), .A2(n629), .ZN(n721) );
  NAND2_X1 U808 ( .A1(n679), .A2(n595), .ZN(n629) );
  NAND2_X1 U809 ( .A1(n879), .A2(n590), .ZN(n875) );
  NAND2_X1 U810 ( .A1(n880), .A2(n881), .ZN(n879) );
  NAND2_X1 U811 ( .A1(n802), .A2(n882), .ZN(n881) );
  NAND4_X1 U812 ( .A1(n883), .A2(n884), .A3(n885), .A4(n886), .ZN(n882) );
  NOR3_X1 U813 ( .A1(n887), .A2(n888), .A3(n889), .ZN(n886) );
  NOR3_X1 U814 ( .A1(n612), .A2(totalcoeffs_0_), .A3(n890), .ZN(n889) );
  NOR2_X1 U815 ( .A1(n891), .A2(n892), .ZN(n890) );
  NOR3_X1 U816 ( .A1(n706), .A2(n679), .A3(n620), .ZN(n891) );
  NOR2_X1 U817 ( .A1(totalcoeffs_1_), .A2(n720), .ZN(n888) );
  NOR2_X1 U818 ( .A1(n631), .A2(n676), .ZN(n887) );
  NAND2_X1 U819 ( .A1(totalcoeffs_3_), .A2(n893), .ZN(n885) );
  NAND2_X1 U820 ( .A1(n850), .A2(n894), .ZN(n893) );
  NAND2_X1 U821 ( .A1(n791), .A2(n618), .ZN(n894) );
  NAND3_X1 U822 ( .A1(n776), .A2(ctable_0_), .A3(n743), .ZN(n884) );
  NAND3_X1 U823 ( .A1(trailingones_0_), .A2(n618), .A3(n696), .ZN(n883) );
  NAND2_X1 U824 ( .A1(n895), .A2(n610), .ZN(n880) );
  NAND4_X1 U825 ( .A1(n896), .A2(n897), .A3(n898), .A4(n899), .ZN(n895) );
  NAND2_X1 U826 ( .A1(n900), .A2(n662), .ZN(n898) );
  NAND4_X1 U827 ( .A1(n901), .A2(n902), .A3(n903), .A4(n904), .ZN(n900) );
  NAND2_X1 U828 ( .A1(n767), .A2(ctable_1_), .ZN(n904) );
  NAND2_X1 U829 ( .A1(totalcoeffs_1_), .A2(n905), .ZN(n903) );
  NAND3_X1 U830 ( .A1(n906), .A2(n907), .A3(n908), .ZN(n905) );
  NAND2_X1 U831 ( .A1(totalcoeffs_3_), .A2(n679), .ZN(n908) );
  NAND2_X1 U832 ( .A1(n909), .A2(n634), .ZN(n907) );
  NAND2_X1 U833 ( .A1(n575), .A2(n588), .ZN(n906) );
  NAND2_X1 U834 ( .A1(n575), .A2(totalcoeffs_2_), .ZN(n902) );
  NAND2_X1 U835 ( .A1(n658), .A2(totalcoeffs_3_), .ZN(n901) );
  NAND2_X1 U836 ( .A1(n575), .A2(n910), .ZN(n897) );
  NAND4_X1 U837 ( .A1(n911), .A2(n912), .A3(n913), .A4(n914), .ZN(n910) );
  NAND2_X1 U838 ( .A1(n710), .A2(n612), .ZN(n914) );
  NAND2_X1 U839 ( .A1(n768), .A2(trailingones_0_), .ZN(n913) );
  NAND2_X1 U840 ( .A1(n915), .A2(n586), .ZN(n911) );
  NAND2_X1 U841 ( .A1(n775), .A2(n916), .ZN(n896) );
  NAND4_X1 U842 ( .A1(n917), .A2(n918), .A3(n919), .A4(n920), .ZN(n916) );
  NOR4_X1 U843 ( .A1(n872), .A2(n792), .A3(n627), .A4(n921), .ZN(n920) );
  NOR3_X1 U844 ( .A1(n666), .A2(trailingones_1_), .A3(n679), .ZN(n921) );
  NAND2_X1 U845 ( .A1(n696), .A2(n588), .ZN(n919) );
  NAND2_X1 U846 ( .A1(n783), .A2(n922), .ZN(n918) );
  NAND2_X1 U847 ( .A1(n923), .A2(n702), .ZN(n922) );
  NAND2_X1 U848 ( .A1(n859), .A2(n603), .ZN(n917) );
  NAND4_X1 U849 ( .A1(n924), .A2(n925), .A3(n926), .A4(n927), .ZN(
        coeff_token_2_) );
  NAND4_X1 U850 ( .A1(n735), .A2(trailingones_0_), .A3(n928), .A4(
        totalcoeffs_4_), .ZN(n927) );
  NOR2_X1 U851 ( .A1(ctable_2_), .A2(n608), .ZN(n928) );
  NAND2_X1 U852 ( .A1(n868), .A2(n929), .ZN(n926) );
  NAND2_X1 U853 ( .A1(n930), .A2(n931), .ZN(n929) );
  NAND2_X1 U854 ( .A1(n643), .A2(n932), .ZN(n931) );
  NAND4_X1 U855 ( .A1(n933), .A2(n934), .A3(n935), .A4(n936), .ZN(n932) );
  NOR2_X1 U856 ( .A1(n937), .A2(n938), .ZN(n936) );
  NOR2_X1 U857 ( .A1(n783), .A2(n695), .ZN(n938) );
  NOR2_X1 U858 ( .A1(n939), .A2(n595), .ZN(n937) );
  NOR3_X1 U859 ( .A1(n940), .A2(n941), .A3(n942), .ZN(n939) );
  NOR2_X1 U860 ( .A1(totalcoeffs_1_), .A2(n695), .ZN(n942) );
  NOR2_X1 U861 ( .A1(n865), .A2(n666), .ZN(n941) );
  NOR2_X1 U862 ( .A1(n631), .A2(n699), .ZN(n940) );
  INV_X1 U863 ( .I(n791), .ZN(n699) );
  NAND3_X1 U864 ( .A1(n847), .A2(n620), .A3(n759), .ZN(n935) );
  INV_X1 U865 ( .I(n712), .ZN(n847) );
  NOR2_X1 U866 ( .A1(n791), .A2(n658), .ZN(n712) );
  INV_X1 U867 ( .I(n678), .ZN(n933) );
  NOR2_X1 U868 ( .A1(n644), .A2(n631), .ZN(n678) );
  NAND2_X1 U869 ( .A1(n943), .A2(n662), .ZN(n930) );
  NAND4_X1 U870 ( .A1(n944), .A2(n945), .A3(n946), .A4(n947), .ZN(n943) );
  NOR3_X1 U871 ( .A1(n948), .A2(n949), .A3(n950), .ZN(n947) );
  NOR2_X1 U872 ( .A1(n951), .A2(n620), .ZN(n950) );
  NOR2_X1 U873 ( .A1(n952), .A2(n872), .ZN(n951) );
  NOR2_X1 U874 ( .A1(n677), .A2(n923), .ZN(n952) );
  INV_X1 U875 ( .I(n953), .ZN(n923) );
  NOR3_X1 U876 ( .A1(n702), .A2(n715), .A3(n737), .ZN(n949) );
  INV_X1 U877 ( .I(n575), .ZN(n737) );
  NOR2_X1 U878 ( .A1(n954), .A2(n586), .ZN(n948) );
  NOR2_X1 U879 ( .A1(n955), .A2(n956), .ZN(n954) );
  NOR3_X1 U880 ( .A1(n957), .A2(totalcoeffs_2_), .A3(n817), .ZN(n956) );
  NOR2_X1 U881 ( .A1(n588), .A2(n677), .ZN(n957) );
  NOR2_X1 U882 ( .A1(totalcoeffs_1_), .A2(n801), .ZN(n955) );
  NAND2_X1 U883 ( .A1(ctable_0_), .A2(n958), .ZN(n946) );
  NAND3_X1 U884 ( .A1(n959), .A2(n665), .A3(n960), .ZN(n958) );
  NAND2_X1 U885 ( .A1(n767), .A2(n850), .ZN(n960) );
  NOR2_X1 U886 ( .A1(n632), .A2(totalcoeffs_1_), .ZN(n767) );
  NAND3_X1 U887 ( .A1(n720), .A2(n631), .A3(n768), .ZN(n959) );
  NAND2_X1 U888 ( .A1(n764), .A2(n600), .ZN(n945) );
  NAND2_X1 U889 ( .A1(n768), .A2(n635), .ZN(n944) );
  NOR2_X1 U890 ( .A1(n588), .A2(totalcoeffs_3_), .ZN(n635) );
  NAND2_X1 U891 ( .A1(n803), .A2(n961), .ZN(n925) );
  NAND2_X1 U892 ( .A1(n679), .A2(n962), .ZN(n961) );
  NAND2_X1 U893 ( .A1(n595), .A2(n588), .ZN(n962) );
  NAND2_X1 U894 ( .A1(n802), .A2(n963), .ZN(n924) );
  NAND3_X1 U895 ( .A1(n964), .A2(n965), .A3(n966), .ZN(n963) );
  NAND2_X1 U896 ( .A1(n967), .A2(n590), .ZN(n966) );
  NAND4_X1 U897 ( .A1(n968), .A2(n969), .A3(n970), .A4(n971), .ZN(n967) );
  NOR4_X1 U898 ( .A1(n972), .A2(n973), .A3(n974), .A4(n975), .ZN(n971) );
  NOR3_X1 U899 ( .A1(n679), .A2(totalcoeffs_3_), .A3(n976), .ZN(n975) );
  NOR2_X1 U900 ( .A1(n977), .A2(n978), .ZN(n976) );
  NOR2_X1 U901 ( .A1(n612), .A2(n644), .ZN(n978) );
  NOR2_X1 U902 ( .A1(n706), .A2(n979), .ZN(n977) );
  INV_X1 U903 ( .I(n630), .ZN(n706) );
  NOR2_X1 U904 ( .A1(n980), .A2(n596), .ZN(n974) );
  NOR3_X1 U905 ( .A1(n981), .A2(n658), .A3(n734), .ZN(n980) );
  NOR2_X1 U906 ( .A1(trailingones_1_), .A2(n588), .ZN(n981) );
  NOR3_X1 U907 ( .A1(n662), .A2(n598), .A3(n644), .ZN(n973) );
  NAND2_X1 U908 ( .A1(n792), .A2(n612), .ZN(n598) );
  NOR3_X1 U909 ( .A1(totalcoeffs_0_), .A2(n586), .A3(n801), .ZN(n972) );
  INV_X1 U910 ( .I(n734), .ZN(n801) );
  NAND2_X1 U911 ( .A1(n743), .A2(n643), .ZN(n970) );
  NOR2_X1 U912 ( .A1(n644), .A2(totalcoeffs_2_), .ZN(n743) );
  NAND3_X1 U913 ( .A1(n630), .A2(n982), .A3(n776), .ZN(n969) );
  NAND3_X1 U914 ( .A1(n649), .A2(totalcoeffs_1_), .A3(n659), .ZN(n968) );
  NAND4_X1 U915 ( .A1(n915), .A2(n609), .A3(n679), .A4(n588), .ZN(n965) );
  NAND2_X1 U916 ( .A1(totalcoeffs_1_), .A2(n983), .ZN(n964) );
  NAND2_X1 U917 ( .A1(n984), .A2(n985), .ZN(n983) );
  NAND3_X1 U918 ( .A1(n630), .A2(n643), .A3(n986), .ZN(n985) );
  NOR2_X1 U919 ( .A1(n987), .A2(n588), .ZN(n630) );
  NAND2_X1 U920 ( .A1(n735), .A2(n988), .ZN(n984) );
  NAND2_X1 U921 ( .A1(n812), .A2(n989), .ZN(n988) );
  NAND2_X1 U922 ( .A1(n632), .A2(n679), .ZN(n989) );
  INV_X1 U923 ( .I(n990), .ZN(n812) );
  NAND3_X1 U924 ( .A1(n991), .A2(n992), .A3(n993), .ZN(coeff_token_1_) );
  NAND2_X1 U925 ( .A1(n868), .A2(n994), .ZN(n993) );
  NAND4_X1 U926 ( .A1(n995), .A2(n996), .A3(n997), .A4(n998), .ZN(n994) );
  NOR4_X1 U927 ( .A1(n999), .A2(n1000), .A3(n1001), .A4(n1002), .ZN(n998) );
  NOR2_X1 U928 ( .A1(ctable_1_), .A2(n1003), .ZN(n1002) );
  NOR3_X1 U929 ( .A1(n1004), .A2(n1005), .A3(n1006), .ZN(n1003) );
  NOR2_X1 U930 ( .A1(n1007), .A2(n677), .ZN(n1006) );
  NOR2_X1 U931 ( .A1(n643), .A2(n657), .ZN(n1007) );
  NOR2_X1 U932 ( .A1(n666), .A2(n662), .ZN(n657) );
  NOR2_X1 U933 ( .A1(n662), .A2(ctable_0_), .ZN(n643) );
  NOR4_X1 U934 ( .A1(n953), .A2(n759), .A3(n662), .A4(n715), .ZN(n1005) );
  NOR2_X1 U935 ( .A1(n1008), .A2(n1009), .ZN(n1004) );
  NOR2_X1 U936 ( .A1(n892), .A2(totalcoeffs_2_), .ZN(n1008) );
  AND2_X1 U937 ( .A1(n588), .A2(n1010), .Z(n1001) );
  NOR2_X1 U938 ( .A1(totalcoeffs_1_), .A2(n1011), .ZN(n1000) );
  NOR4_X1 U939 ( .A1(n1012), .A2(n1013), .A3(n1014), .A4(n1015), .ZN(n1011) );
  NOR2_X1 U940 ( .A1(totalcoeffs_3_), .A2(n1016), .ZN(n1015) );
  NOR2_X1 U941 ( .A1(n1017), .A2(n1018), .ZN(n1016) );
  NOR2_X1 U942 ( .A1(n616), .A2(n665), .ZN(n1018) );
  INV_X1 U943 ( .I(n909), .ZN(n665) );
  NOR2_X1 U944 ( .A1(n1019), .A2(n679), .ZN(n1017) );
  NOR2_X1 U945 ( .A1(n1020), .A2(n1021), .ZN(n1019) );
  NOR2_X1 U946 ( .A1(n850), .A2(n1009), .ZN(n1021) );
  AND2_X1 U947 ( .A1(n659), .A2(n818), .Z(n1020) );
  NOR2_X1 U948 ( .A1(n662), .A2(n588), .ZN(n818) );
  NOR2_X1 U949 ( .A1(n1022), .A2(n645), .ZN(n1014) );
  NOR2_X1 U950 ( .A1(n1023), .A2(n1024), .ZN(n1013) );
  NOR2_X1 U951 ( .A1(n1025), .A2(n1026), .ZN(n1023) );
  NOR3_X1 U952 ( .A1(n850), .A2(n586), .A3(n662), .ZN(n1025) );
  NOR3_X1 U953 ( .A1(n695), .A2(n595), .A3(n616), .ZN(n1012) );
  NOR2_X1 U954 ( .A1(n1027), .A2(n612), .ZN(n999) );
  NOR4_X1 U955 ( .A1(n1028), .A2(n1029), .A3(n1030), .A4(n1031), .ZN(n1027) );
  NOR2_X1 U956 ( .A1(n1032), .A2(n631), .ZN(n1031) );
  NOR2_X1 U957 ( .A1(n1033), .A2(n600), .ZN(n1032) );
  NOR2_X1 U958 ( .A1(trailingones_0_), .A2(n618), .ZN(n1033) );
  INV_X1 U959 ( .I(n603), .ZN(n618) );
  NOR2_X1 U960 ( .A1(n987), .A2(n679), .ZN(n603) );
  NOR2_X1 U961 ( .A1(n1034), .A2(n616), .ZN(n1030) );
  INV_X1 U962 ( .I(n634), .ZN(n616) );
  NOR2_X1 U963 ( .A1(n1035), .A2(n1026), .ZN(n1034) );
  NOR2_X1 U964 ( .A1(n588), .A2(n596), .ZN(n1026) );
  INV_X1 U965 ( .I(n617), .ZN(n596) );
  AND2_X1 U966 ( .A1(n626), .A2(n627), .Z(n1035) );
  NOR2_X1 U967 ( .A1(n595), .A2(totalcoeffs_3_), .ZN(n627) );
  NAND2_X1 U968 ( .A1(n1036), .A2(n899), .ZN(n1029) );
  NAND2_X1 U969 ( .A1(n634), .A2(n792), .ZN(n899) );
  NAND4_X1 U970 ( .A1(n734), .A2(n632), .A3(ctable_0_), .A4(n662), .ZN(n1036)
         );
  NOR3_X1 U971 ( .A1(n644), .A2(totalcoeffs_3_), .A3(ctable_1_), .ZN(n1028) );
  INV_X1 U972 ( .I(n710), .ZN(n644) );
  NAND2_X1 U973 ( .A1(n577), .A2(n1037), .ZN(n997) );
  NAND2_X1 U974 ( .A1(n732), .A2(n1038), .ZN(n1037) );
  NAND2_X1 U975 ( .A1(n768), .A2(n662), .ZN(n1038) );
  INV_X1 U976 ( .I(n841), .ZN(n732) );
  NOR2_X1 U977 ( .A1(n850), .A2(n715), .ZN(n841) );
  INV_X1 U978 ( .I(n658), .ZN(n715) );
  NAND3_X1 U979 ( .A1(ctable_0_), .A2(n1039), .A3(n600), .ZN(n996) );
  NAND2_X1 U980 ( .A1(n632), .A2(n979), .ZN(n1039) );
  NAND3_X1 U981 ( .A1(n1040), .A2(n620), .A3(n634), .ZN(n995) );
  NAND2_X1 U982 ( .A1(n695), .A2(n1041), .ZN(n1040) );
  NAND3_X1 U983 ( .A1(n979), .A2(n602), .A3(ctable_1_), .ZN(n1041) );
  INV_X1 U984 ( .I(n626), .ZN(n602) );
  INV_X1 U985 ( .I(n892), .ZN(n695) );
  NOR2_X1 U986 ( .A1(n588), .A2(n586), .ZN(n892) );
  NAND2_X1 U987 ( .A1(n802), .A2(n1042), .ZN(n992) );
  NAND2_X1 U988 ( .A1(n1043), .A2(n1044), .ZN(n1042) );
  NAND2_X1 U989 ( .A1(n1010), .A2(n590), .ZN(n1044) );
  NOR3_X1 U990 ( .A1(n982), .A2(n1022), .A3(n979), .ZN(n1010) );
  NOR2_X1 U991 ( .A1(n600), .A2(n953), .ZN(n1022) );
  NAND2_X1 U992 ( .A1(n649), .A2(n1045), .ZN(n1043) );
  NAND2_X1 U993 ( .A1(n1046), .A2(n1047), .ZN(n1045) );
  NAND2_X1 U994 ( .A1(ctable_2_), .A2(n1048), .ZN(n1047) );
  NAND2_X1 U995 ( .A1(n1049), .A2(n934), .ZN(n1048) );
  INV_X1 U996 ( .I(n738), .ZN(n934) );
  NOR2_X1 U997 ( .A1(n677), .A2(n666), .ZN(n738) );
  NAND2_X1 U998 ( .A1(trailingones_0_), .A2(n620), .ZN(n666) );
  NAND2_X1 U999 ( .A1(n1050), .A2(n1051), .ZN(n1049) );
  NAND3_X1 U1000 ( .A1(n694), .A2(n620), .A3(n979), .ZN(n1051) );
  INV_X1 U1001 ( .I(n775), .ZN(n979) );
  NAND2_X1 U1002 ( .A1(n1052), .A2(n850), .ZN(n1050) );
  NAND2_X1 U1003 ( .A1(n660), .A2(n612), .ZN(n1052) );
  NAND2_X1 U1004 ( .A1(n584), .A2(n783), .ZN(n1046) );
  NOR2_X1 U1005 ( .A1(totalcoeffs_0_), .A2(totalcoeffs_1_), .ZN(n584) );
  NAND2_X1 U1006 ( .A1(n990), .A2(n1053), .ZN(n991) );
  NAND2_X1 U1007 ( .A1(n1054), .A2(n1055), .ZN(n1053) );
  NAND3_X1 U1008 ( .A1(n783), .A2(trailingones_0_), .A3(n802), .ZN(n1055) );
  NAND2_X1 U1009 ( .A1(n650), .A2(n1056), .ZN(n1054) );
  NAND2_X1 U1010 ( .A1(n1057), .A2(n1058), .ZN(n1056) );
  NAND2_X1 U1011 ( .A1(totalcoeffs_4_), .A2(n1059), .ZN(n1058) );
  NAND2_X1 U1012 ( .A1(n1024), .A2(n1060), .ZN(n1059) );
  NAND2_X1 U1013 ( .A1(n817), .A2(trailingones_0_), .ZN(n1060) );
  NOR2_X1 U1014 ( .A1(ctable_1_), .A2(trailingones_1_), .ZN(n817) );
  INV_X1 U1015 ( .I(n600), .ZN(n1024) );
  NOR2_X1 U1016 ( .A1(n987), .A2(n595), .ZN(n600) );
  NAND2_X1 U1017 ( .A1(n577), .A2(n710), .ZN(n1057) );
  NOR2_X1 U1018 ( .A1(n766), .A2(totalcoeffs_1_), .ZN(n650) );
  NAND2_X1 U1019 ( .A1(n662), .A2(n620), .ZN(n766) );
  NOR2_X1 U1020 ( .A1(ctable_2_), .A2(totalcoeffs_3_), .ZN(n990) );
  NAND4_X1 U1021 ( .A1(n1061), .A2(n1062), .A3(n1063), .A4(n1064), .ZN(
        coeff_token_0_) );
  NAND3_X1 U1022 ( .A1(n1065), .A2(n590), .A3(n609), .ZN(n1064) );
  NAND2_X1 U1023 ( .A1(n1066), .A2(n1067), .ZN(n1065) );
  NAND3_X1 U1024 ( .A1(n1068), .A2(n662), .A3(n710), .ZN(n1067) );
  NOR2_X1 U1025 ( .A1(trailingones_0_), .A2(trailingones_1_), .ZN(n710) );
  NAND2_X1 U1026 ( .A1(n1069), .A2(n1070), .ZN(n1068) );
  NAND2_X1 U1027 ( .A1(ctable_1_), .A2(n589), .ZN(n1070) );
  INV_X1 U1028 ( .I(n577), .ZN(n1069) );
  NOR2_X1 U1029 ( .A1(n679), .A2(ctable_1_), .ZN(n577) );
  NAND3_X1 U1030 ( .A1(n626), .A2(totalcoeffs_4_), .A3(n872), .ZN(n1066) );
  NAND3_X1 U1031 ( .A1(n734), .A2(n589), .A3(n803), .ZN(n1063) );
  INV_X1 U1032 ( .I(n878), .ZN(n803) );
  NAND2_X1 U1033 ( .A1(n579), .A2(n590), .ZN(n878) );
  NOR3_X1 U1034 ( .A1(n608), .A2(totalcoeffs_0_), .A3(n610), .ZN(n579) );
  INV_X1 U1035 ( .I(totalcoeffs_4_), .ZN(n610) );
  INV_X1 U1036 ( .I(n609), .ZN(n608) );
  INV_X1 U1037 ( .I(n872), .ZN(n589) );
  NOR2_X1 U1038 ( .A1(n987), .A2(trailingones_0_), .ZN(n734) );
  NAND2_X1 U1039 ( .A1(n802), .A2(n1071), .ZN(n1062) );
  NAND4_X1 U1040 ( .A1(n1072), .A2(n1073), .A3(n1074), .A4(n1075), .ZN(n1071)
         );
  NAND3_X1 U1041 ( .A1(n953), .A2(n775), .A3(n986), .ZN(n1075) );
  NOR2_X1 U1042 ( .A1(n588), .A2(ctable_0_), .ZN(n953) );
  NAND3_X1 U1043 ( .A1(totalcoeffs_0_), .A2(n1076), .A3(n634), .ZN(n1074) );
  NOR2_X1 U1044 ( .A1(ctable_0_), .A2(trailingones_1_), .ZN(n634) );
  OR2_X1 U1045 ( .A1(n609), .A2(n986), .Z(n1076) );
  NOR2_X1 U1046 ( .A1(n590), .A2(n982), .ZN(n986) );
  NOR2_X1 U1047 ( .A1(n982), .A2(totalcoeffs_1_), .ZN(n609) );
  NAND2_X1 U1048 ( .A1(n649), .A2(n1077), .ZN(n1073) );
  NAND2_X1 U1049 ( .A1(n1078), .A2(n1079), .ZN(n1077) );
  NAND4_X1 U1050 ( .A1(n626), .A2(ctable_2_), .A3(n783), .A4(n612), .ZN(n1079)
         );
  NOR2_X1 U1051 ( .A1(n620), .A2(trailingones_1_), .ZN(n783) );
  NAND3_X1 U1052 ( .A1(n1080), .A2(n676), .A3(n859), .ZN(n1078) );
  NAND2_X1 U1053 ( .A1(totalcoeffs_1_), .A2(n1081), .ZN(n1080) );
  NAND2_X1 U1054 ( .A1(trailingones_1_), .A2(n662), .ZN(n1081) );
  NAND2_X1 U1055 ( .A1(n1082), .A2(n590), .ZN(n1072) );
  INV_X1 U1056 ( .I(ctable_2_), .ZN(n590) );
  NAND4_X1 U1057 ( .A1(n1083), .A2(n1084), .A3(n1085), .A4(n1086), .ZN(n1082)
         );
  NAND3_X1 U1058 ( .A1(trailingones_1_), .A2(n632), .A3(n775), .ZN(n1086) );
  NOR2_X1 U1059 ( .A1(n662), .A2(n612), .ZN(n775) );
  NOR2_X1 U1060 ( .A1(n764), .A2(n1087), .ZN(n1085) );
  NOR3_X1 U1061 ( .A1(n850), .A2(n768), .A3(n1088), .ZN(n1087) );
  NOR2_X1 U1062 ( .A1(n915), .A2(totalcoeffs_1_), .ZN(n1088) );
  INV_X1 U1063 ( .I(n859), .ZN(n850) );
  NOR2_X1 U1064 ( .A1(n702), .A2(n612), .ZN(n764) );
  INV_X1 U1065 ( .I(n759), .ZN(n702) );
  NOR2_X1 U1066 ( .A1(totalcoeffs_3_), .A2(trailingones_0_), .ZN(n759) );
  NAND2_X1 U1067 ( .A1(n909), .A2(n1089), .ZN(n1084) );
  NAND2_X1 U1068 ( .A1(n1009), .A2(n677), .ZN(n1089) );
  INV_X1 U1069 ( .I(n768), .ZN(n677) );
  INV_X1 U1070 ( .I(n735), .ZN(n1009) );
  NOR2_X1 U1071 ( .A1(n620), .A2(trailingones_0_), .ZN(n909) );
  NAND2_X1 U1072 ( .A1(n1090), .A2(n588), .ZN(n1083) );
  NAND3_X1 U1073 ( .A1(n912), .A2(n1091), .A3(n1092), .ZN(n1090) );
  NAND2_X1 U1074 ( .A1(n735), .A2(ctable_0_), .ZN(n1092) );
  NAND2_X1 U1075 ( .A1(n776), .A2(totalcoeffs_3_), .ZN(n1091) );
  NOR2_X1 U1076 ( .A1(n662), .A2(totalcoeffs_1_), .ZN(n776) );
  NAND2_X1 U1077 ( .A1(n865), .A2(n982), .ZN(n912) );
  INV_X1 U1078 ( .I(n632), .ZN(n982) );
  NOR2_X1 U1079 ( .A1(ctable_1_), .A2(totalcoeffs_4_), .ZN(n802) );
  NAND2_X1 U1080 ( .A1(n868), .A2(n1093), .ZN(n1061) );
  NAND4_X1 U1081 ( .A1(n1094), .A2(n1095), .A3(n1096), .A4(n1097), .ZN(n1093)
         );
  NAND3_X1 U1082 ( .A1(ctable_1_), .A2(n1098), .A3(n626), .ZN(n1097) );
  NOR2_X1 U1083 ( .A1(n588), .A2(totalcoeffs_0_), .ZN(n626) );
  NAND3_X1 U1084 ( .A1(n1099), .A2(n1100), .A3(n1101), .ZN(n1098) );
  NAND2_X1 U1085 ( .A1(n659), .A2(n586), .ZN(n1101) );
  NAND2_X1 U1086 ( .A1(n865), .A2(n792), .ZN(n1100) );
  NOR2_X1 U1087 ( .A1(n586), .A2(totalcoeffs_2_), .ZN(n792) );
  NAND2_X1 U1088 ( .A1(n768), .A2(n632), .ZN(n1099) );
  NOR2_X1 U1089 ( .A1(n612), .A2(trailingones_1_), .ZN(n768) );
  NAND2_X1 U1090 ( .A1(n658), .A2(n1102), .ZN(n1096) );
  NAND3_X1 U1091 ( .A1(n1103), .A2(n1104), .A3(n1105), .ZN(n1102) );
  NAND2_X1 U1092 ( .A1(n575), .A2(n859), .ZN(n1105) );
  NOR2_X1 U1093 ( .A1(totalcoeffs_2_), .A2(trailingones_0_), .ZN(n859) );
  NOR2_X1 U1094 ( .A1(n595), .A2(ctable_0_), .ZN(n575) );
  NAND2_X1 U1095 ( .A1(n660), .A2(n632), .ZN(n1104) );
  NAND2_X1 U1096 ( .A1(n649), .A2(n588), .ZN(n1103) );
  NOR2_X1 U1097 ( .A1(ctable_0_), .A2(totalcoeffs_3_), .ZN(n649) );
  NOR2_X1 U1098 ( .A1(totalcoeffs_1_), .A2(trailingones_1_), .ZN(n658) );
  NAND2_X1 U1099 ( .A1(trailingones_0_), .A2(n1106), .ZN(n1095) );
  NAND2_X1 U1100 ( .A1(n1107), .A2(n1108), .ZN(n1106) );
  NAND2_X1 U1101 ( .A1(n1109), .A2(n860), .ZN(n1108) );
  NAND2_X1 U1102 ( .A1(n1110), .A2(n1111), .ZN(n860) );
  NAND2_X1 U1103 ( .A1(n735), .A2(totalcoeffs_1_), .ZN(n1111) );
  NOR2_X1 U1104 ( .A1(totalcoeffs_0_), .A2(trailingones_1_), .ZN(n735) );
  NAND2_X1 U1105 ( .A1(n791), .A2(totalcoeffs_0_), .ZN(n1110) );
  NOR2_X1 U1106 ( .A1(n987), .A2(n612), .ZN(n791) );
  NAND2_X1 U1107 ( .A1(n1112), .A2(n1113), .ZN(n1109) );
  NAND2_X1 U1108 ( .A1(n696), .A2(totalcoeffs_2_), .ZN(n1113) );
  NOR2_X1 U1109 ( .A1(n586), .A2(n679), .ZN(n696) );
  NAND2_X1 U1110 ( .A1(n632), .A2(ctable_0_), .ZN(n1112) );
  NAND2_X1 U1111 ( .A1(n872), .A2(n1114), .ZN(n1107) );
  NAND2_X1 U1112 ( .A1(n632), .A2(n694), .ZN(n1114) );
  NOR2_X1 U1113 ( .A1(totalcoeffs_2_), .A2(totalcoeffs_3_), .ZN(n632) );
  NOR2_X1 U1114 ( .A1(n595), .A2(n679), .ZN(n872) );
  INV_X1 U1115 ( .I(ctable_1_), .ZN(n595) );
  NAND2_X1 U1116 ( .A1(n1115), .A2(n679), .ZN(n1094) );
  INV_X1 U1117 ( .I(ctable_0_), .ZN(n679) );
  NAND4_X1 U1118 ( .A1(n1116), .A2(n1117), .A3(n1118), .A4(n1119), .ZN(n1115)
         );
  NAND3_X1 U1119 ( .A1(trailingones_1_), .A2(totalcoeffs_3_), .A3(n660), .ZN(
        n1119) );
  OR2_X1 U1120 ( .A1(n645), .A2(n676), .Z(n1118) );
  INV_X1 U1121 ( .I(n865), .ZN(n676) );
  NOR2_X1 U1122 ( .A1(n987), .A2(totalcoeffs_1_), .ZN(n865) );
  NAND2_X1 U1123 ( .A1(n617), .A2(n662), .ZN(n645) );
  NOR2_X1 U1124 ( .A1(n620), .A2(totalcoeffs_3_), .ZN(n617) );
  NAND2_X1 U1125 ( .A1(n659), .A2(n588), .ZN(n1117) );
  NOR2_X1 U1126 ( .A1(n987), .A2(n620), .ZN(n659) );
  INV_X1 U1127 ( .I(trailingones_1_), .ZN(n987) );
  NOR2_X1 U1128 ( .A1(n1120), .A2(n1121), .ZN(n1116) );
  NOR3_X1 U1129 ( .A1(totalcoeffs_1_), .A2(n631), .A3(n694), .ZN(n1121) );
  INV_X1 U1130 ( .I(n915), .ZN(n694) );
  NOR2_X1 U1131 ( .A1(n662), .A2(trailingones_1_), .ZN(n915) );
  INV_X1 U1132 ( .I(totalcoeffs_0_), .ZN(n662) );
  INV_X1 U1133 ( .I(n642), .ZN(n631) );
  NOR2_X1 U1134 ( .A1(n586), .A2(n620), .ZN(n642) );
  INV_X1 U1135 ( .I(totalcoeffs_2_), .ZN(n620) );
  INV_X1 U1136 ( .I(totalcoeffs_3_), .ZN(n586) );
  NOR2_X1 U1137 ( .A1(n1122), .A2(n612), .ZN(n1120) );
  INV_X1 U1138 ( .I(totalcoeffs_1_), .ZN(n612) );
  AND2_X1 U1139 ( .A1(n720), .A2(n781), .Z(n1122) );
  INV_X1 U1140 ( .I(n660), .ZN(n781) );
  NOR2_X1 U1141 ( .A1(totalcoeffs_0_), .A2(trailingones_0_), .ZN(n660) );
  NAND2_X1 U1142 ( .A1(totalcoeffs_3_), .A2(n588), .ZN(n720) );
  INV_X1 U1143 ( .I(trailingones_0_), .ZN(n588) );
  NOR2_X1 U1144 ( .A1(ctable_2_), .A2(totalcoeffs_4_), .ZN(n868) );
endmodule

