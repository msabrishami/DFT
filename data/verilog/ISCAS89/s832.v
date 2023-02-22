//# 18 inputs
//# 19 outputs
//# 5 D-type flipflops
//# 25 inverters
//# 262 gates (78 ANDs + 54 NANDs + 64 ORs + 66 NORs)



module s832(GND,VDD,CK,G0,G1,G10,G11,G12,G13,G14,G15,G16,G18,G2,G288,G290,G292,
  G296,G298,
  G3,G300,G302,G310,G312,G315,G322,G325,G327,G4,G43,G45,G47,G49,G5,G53,G55,G6,
  G7,G8,G9);
input GND,VDD,CK,G0,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,G13,G14,G15,G16,G18;
output G327,G325,G300,G322,G45,G312,G53,G49,G47,G296,G290,G292,G298,G288,G315,
  G55,G43,G310,G302;

  wire G38,G90,G39,G93,G40,G96,G41,G99,G42,G102,G88,G91,G94,G97,G100,G112,G130,
    G168,G171,G172,G181,G198,G201,G202,G203,G245,G256,G267,G280,G281,G313,G317,
    G318,G323,G328,G89,G92,G95,G98,G101,G103,G117,G118,G120,G121,G127,G128,
    G129,G141,G140,G142,G143,G150,G147,G148,G149,G151,G153,G152,G154,G158,G157,
    G160,G161,G162,G163,G164,G166,G167,G169,G170,G174,G173,G175,G176,G185,G184,
    G187,G188,G189,G190,G191,G193,G194,G195,G197,G196,G199,G200,G210,G209,G211,
    G212,G213,G214,G215,G218,G216,G217,G219,G220,G223,G222,G226,G225,G230,G231,
    G232,G233,G234,G235,G249,G250,G251,G252,G258,G257,G259,G260,G263,G262,G264,
    G266,G265,G268,G271,G270,G272,G274,G273,G275,G276,G277,G278,G279,G282,G283,
    G294,G293,G52,G50,G62,G57,G58,G63,G59,G64,G60,G67,G177,G70,G65,G66,G71,G72,
    G68,G78,G73,G74,G79,G75,G80,G76,G85,G81,G86,G82,G87,G83,G155,G106,G105,
    G107,G108,G109,G110,G111,G113,G114,G115,G116,G124,G125,G126,G132,G133,G134,
    G135,G136,G139,G137,G144,G145,G180,G178,G182,G183,G207,G204,G205,G208,G228,
    G229,G236,G237,G238,G239,G240,G241,G242,G243,G244,G246,G247,G248,G255,G253,
    G285,G284,G286,G287,G307,G303,G308,G304,G309,G305,G320,G316,G321,G319,G44,
    G46,G122,G48,G51,G54,G56,G61,G146,G69,G179,G206,G84,G254,G77,G123,G156,
    G224,G227,G269,G289,G291,G131,G295,G297,G299,G301,G119,G306,G138,G311,G314,
    G326,G329,G159,G186,G221,G261,G104,G165,G192,G324;

  dff DFF_0(CK,G38,G90);
  dff DFF_1(CK,G39,G93);
  dff DFF_2(CK,G40,G96);
  dff DFF_3(CK,G41,G99);
  dff DFF_4(CK,G42,G102);
  not NOT_0(G88,G18);
  not NOT_1(G91,G18);
  not NOT_2(G94,G18);
  not NOT_3(G97,G18);
  not NOT_4(G100,G18);
  not NOT_5(G112,G8);
  not NOT_6(G130,G5);
  not NOT_7(G168,G12);
  not NOT_8(G171,G10);
  not NOT_9(G172,G11);
  not NOT_10(G181,G2);
  not NOT_11(G198,G9);
  not NOT_12(G201,G13);
  not NOT_13(G202,G7);
  not NOT_14(G203,G6);
  not NOT_15(G245,G0);
  not NOT_16(G256,G4);
  not NOT_17(G267,G15);
  not NOT_18(G280,G38);
  not NOT_19(G281,G16);
  not NOT_20(G313,G41);
  not NOT_21(G317,G40);
  not NOT_22(G318,G39);
  not NOT_23(G323,G1);
  not NOT_24(G328,G42);
  and AND2_0(G90,G89,G88);
  and AND2_1(G93,G92,G91);
  and AND2_2(G96,G95,G94);
  and AND2_3(G99,G98,G97);
  and AND2_4(G102,G101,G100);
  and AND2_5(G103,G313,G38);
  and AND4_0(G117,G1,G280,G39,G313);
  and AND3_0(G118,G245,G38,G39);
  and AND3_1(G120,G39,G40,G42);
  and AND3_2(G121,G318,G317,G328);
  and AND4_1(G127,G38,G39,G313,G328);
  and AND3_3(G128,G280,G318,G40);
  and AND2_6(G129,G39,G317);
  and AND4_2(G141,G317,G16,G323,G140);
  and AND2_7(G142,G40,G281);
  and AND2_8(G143,G40,G4);
  and AND4_3(G150,G256,G147,G148,G149);
  and AND4_4(G151,G38,G16,G256,G153);
  and AND4_5(G152,G313,G317,G318,G154);
  and AND2_9(G158,G280,G157);
  and AND3_4(G160,G5,G313,G328);
  and AND2_10(G161,G3,G42);
  and AND2_11(G162,G1,G42);
  and AND2_12(G163,G41,G42);
  and AND2_13(G164,G42,G313);
  and AND4_6(G166,G245,G38,G41,G42);
  and AND3_5(G167,G256,G38,G313);
  and AND2_14(G169,G172,G168);
  and AND2_15(G170,G171,G172);
  and AND4_7(G174,G41,G40,G15,G173);
  and AND2_16(G175,G317,G176);
  and AND2_17(G185,G280,G184);
  and AND3_6(G187,G5,G313,G328);
  and AND2_18(G188,G3,G42);
  and AND2_19(G189,G1,G42);
  and AND2_20(G190,G41,G42);
  and AND2_21(G191,G42,G313);
  and AND2_22(G193,G11,G328);
  and AND2_23(G194,G10,G328);
  and AND2_24(G195,G41,G42);
  and AND4_8(G197,G8,G7,G6,G196);
  and AND4_9(G199,G245,G38,G41,G42);
  and AND3_7(G200,G256,G38,G313);
  and AND4_10(G210,G39,G38,G245,G209);
  and AND4_11(G211,G317,G39,G256,G212);
  and AND3_8(G213,G16,G313,G328);
  and AND3_9(G214,G267,G16,G313);
  and AND2_25(G215,G41,G42);
  and AND4_12(G218,G2,G323,G216,G217);
  and AND2_26(G219,G318,G220);
  and AND2_27(G223,G16,G222);
  and AND2_28(G226,G318,G225);
  and AND3_10(G230,G15,G38,G328);
  and AND2_29(G231,G267,G313);
  and AND2_30(G232,G38,G318);
  and AND2_31(G233,G15,G318);
  and AND4_13(G234,G15,G40,G313,G42);
  and AND2_32(G235,G317,G328);
  and AND3_11(G249,G40,G41,G328);
  and AND3_12(G250,G39,G40,G42);
  and AND2_33(G251,G318,G313);
  and AND2_34(G252,G318,G317);
  and AND3_13(G258,G318,G280,G257);
  and AND2_35(G259,G41,G260);
  and AND3_14(G263,G39,G38,G262);
  and AND2_36(G264,G318,G266);
  and AND2_37(G265,G317,G267);
  and AND2_38(G268,G328,G267);
  and AND4_14(G271,G318,G15,G14,G270);
  and AND3_15(G272,G318,G4,G274);
  and AND3_16(G273,G40,G39,G275);
  and AND3_17(G276,G0,G38,G328);
  and AND3_18(G277,G323,G281,G280);
  and AND2_39(G278,G280,G42);
  and AND2_40(G279,G281,G42);
  and AND2_41(G282,G317,G328);
  and AND2_42(G283,G317,G313);
  and AND2_43(G294,G16,G293);
  or OR4_0(G52,G328,G313,G39,G50);
  or OR4_1(G62,G267,G4,G57,G58);
  or OR4_2(G63,G40,G318,G4,G59);
  or OR3_0(G64,G317,G318,G60);
  or OR3_1(G67,G174,G175,G177);
  or OR4_3(G70,G318,G4,G65,G66);
  or OR4_4(G71,G39,G281,G4,G67);
  or OR3_2(G72,G317,G318,G68);
  or OR4_5(G78,G39,G4,G73,G74);
  or OR4_6(G79,G40,G281,G4,G75);
  or OR2_0(G80,G38,G76);
  or OR4_7(G85,G328,G313,G317,G81);
  or OR2_1(G86,G38,G82);
  or OR2_2(G87,G281,G83);
  or OR4_8(G89,G150,G151,G152,G155);
  or OR4_9(G106,G8,G7,G203,G105);
  or OR3_3(G107,G41,G40,G1);
  or OR2_3(G108,G328,G15);
  or OR3_4(G109,G201,G267,G328);
  or OR2_4(G110,G280,G42);
  or OR2_5(G111,G15,G42);
  or OR4_10(G113,G203,G202,G112,G198);
  or OR3_5(G114,G267,G318,G328);
  or OR2_6(G115,G39,G42);
  or OR2_7(G116,G39,G313);
  or OR2_8(G124,G11,G12);
  or OR2_9(G125,G10,G12);
  or OR2_10(G126,G10,G11);
  or OR4_11(G132,G171,G11,G12,G42);
  or OR4_12(G133,G10,G172,G12,G42);
  or OR2_11(G134,G280,G42);
  or OR2_12(G135,G280,G40);
  or OR2_13(G136,G4,G281);
  or OR2_14(G139,G317,G137);
  or OR2_15(G144,G16,G42);
  or OR2_16(G145,G16,G41);
  or OR2_17(G180,G41,G178);
  or OR4_13(G182,G14,G267,G38,G39);
  or OR3_6(G183,G38,G39,G41);
  or OR4_14(G207,G202,G203,G204,G205);
  or OR2_18(G208,G42,G41);
  or OR2_19(G228,G38,G313);
  or OR2_20(G229,G15,G313);
  or OR3_7(G236,G318,G317,G328);
  or OR3_8(G237,G16,G39,G40);
  or OR4_15(G238,G14,G267,G40,G42);
  or OR3_9(G239,G40,G41,G42);
  or OR3_10(G240,G256,G313,G328);
  or OR2_21(G241,G256,G317);
  or OR2_22(G242,G41,G328);
  or OR2_23(G243,G5,G41);
  or OR2_24(G244,G281,G328);
  or OR2_25(G246,G4,G39);
  or OR2_26(G247,G38,G318);
  or OR2_27(G248,G245,G318);
  or OR2_28(G255,G317,G253);
  or OR4_16(G285,G3,G2,G1,G284);
  or OR2_29(G286,G42,G313);
  or OR2_30(G287,G42,G5);
  or OR4_17(G307,G328,G313,G39,G303);
  or OR4_18(G308,G40,G318,G16,G304);
  or OR3_11(G309,G39,G38,G305);
  or OR4_19(G320,G40,G39,G38,G316);
  or OR4_20(G321,G317,G318,G38,G319);
  nand NAND4_0(G44,G317,G318,G280,G15);
  nand NAND4_1(G46,G318,G280,G16,G122);
  nand NAND4_2(G48,G40,G39,G280,G130);
  nand NAND2_0(G49,G52,G51);
  nand NAND4_3(G54,G41,G317,G318,G280);
  nand NAND4_4(G56,G40,G39,G280,G5);
  nand NAND4_5(G57,G41,G40,G318,G16);
  nand NAND3_0(G58,G132,G133,G134);
  nand NAND2_1(G59,G144,G145);
  nand NAND4_6(G61,G328,G313,G317,G146);
  nand NAND3_1(G65,G42,G41,G317);
  nand NAND4_7(G69,G180,G328,G317,G179);
  nand NAND3_2(G73,G42,G41,G40);
  nand NAND3_3(G75,G207,G208,G206);
  nand NAND3_4(G81,G246,G247,G248);
  nand NAND2_2(G84,G255,G254);
  nand NAND4_8(G92,G62,G63,G64,G61);
  nand NAND4_9(G95,G70,G71,G72,G69);
  nand NAND4_10(G98,G78,G79,G80,G77);
  nand NAND4_11(G101,G85,G86,G87,G84);
  nand NAND4_12(G105,G328,G40,G15,G9);
  nand NAND4_13(G123,G124,G125,G126,G256);
  nand NAND3_5(G156,G318,G280,G281);
  nand NAND4_14(G176,G42,G41,G280,G15);
  nand NAND2_3(G179,G182,G183);
  nand NAND2_4(G204,G9,G8);
  nand NAND2_5(G205,G228,G229);
  nand NAND2_6(G217,G236,G237);
  nand NAND4_15(G224,G238,G239,G240,G241);
  nand NAND3_6(G225,G328,G41,G256);
  nand NAND4_16(G227,G242,G243,G244,G40);
  nand NAND3_7(G257,G106,G107,G108);
  nand NAND2_7(G262,G113,G317);
  nand NAND4_17(G266,G109,G110,G111,G40);
  nand NAND4_18(G269,G114,G115,G116,G317);
  nand NAND3_8(G275,G285,G286,G287);
  nand NAND2_8(G284,G42,G313);
  nand NAND4_19(G289,G313,G40,G39,G280);
  nand NAND4_20(G291,G313,G317,G39,G15);
  nand NAND4_21(G293,G8,G7,G6,G131);
  nand NAND4_22(G295,G41,G317,G39,G256);
  nand NAND4_23(G297,G41,G40,G39,G280);
  nand NAND4_24(G299,G318,G280,G15,G14);
  nand NAND4_25(G301,G281,G3,G323,G119);
  nand NAND4_26(G302,G307,G308,G309,G306);
  nand NAND2_9(G303,G135,G136);
  nand NAND2_10(G306,G139,G138);
  nand NAND4_27(G311,G313,G40,G39,G280);
  nand NAND4_28(G314,G40,G39,G280,G16);
  nand NAND2_11(G315,G320,G321);
  nand NAND2_12(G316,G328,G313);
  nand NAND2_13(G319,G42,G41);
  nand NAND4_29(G326,G313,G40,G39,G280);
  nand NAND4_30(G329,G313,G317,G39,G15);
  nor NOR3_0(G43,G42,G313,G44);
  nor NOR4_0(G45,G42,G313,G317,G46);
  nor NOR3_1(G47,G42,G41,G48);
  nor NOR2_0(G50,G40,G280);
  nor NOR3_2(G51,G127,G128,G129);
  nor NOR2_1(G53,G42,G54);
  nor NOR3_3(G55,G42,G41,G56);
  nor NOR2_2(G60,G158,G159);
  nor NOR2_3(G66,G197,G281);
  nor NOR2_4(G68,G185,G186);
  nor NOR3_4(G74,G281,G267,G201);
  nor NOR3_5(G76,G218,G219,G221);
  nor NOR2_5(G77,G210,G211);
  nor NOR3_6(G82,G271,G272,G273);
  nor NOR3_7(G83,G258,G259,G261);
  nor NOR2_6(G104,G117,G118);
  nor NOR2_7(G119,G39,G38);
  nor NOR2_8(G122,G267,G123);
  nor NOR3_8(G131,G280,G267,G198);
  nor NOR3_9(G137,G42,G41,G280);
  nor NOR2_9(G138,G318,G256);
  nor NOR2_10(G140,G42,G41);
  nor NOR4_1(G146,G3,G181,G1,G156);
  nor NOR3_10(G147,G38,G281,G267);
  nor NOR4_2(G148,G42,G313,G317,G39);
  nor NOR2_11(G149,G169,G170);
  nor NOR4_3(G153,G249,G250,G251,G252);
  nor NOR4_4(G154,G276,G277,G278,G279);
  nor NOR4_5(G155,G103,G328,G317,G104);
  nor NOR4_6(G157,G160,G161,G162,G163);
  nor NOR2_12(G159,G164,G165);
  nor NOR2_13(G165,G166,G167);
  nor NOR2_14(G173,G193,G194);
  nor NOR2_15(G177,G195,G280);
  nor NOR4_7(G178,G16,G3,G181,G1);
  nor NOR4_8(G184,G187,G188,G189,G190);
  nor NOR2_16(G186,G191,G192);
  nor NOR2_17(G192,G199,G200);
  nor NOR3_11(G196,G280,G267,G198);
  nor NOR4_9(G206,G230,G231,G232,G233);
  nor NOR3_12(G209,G328,G313,G317);
  nor NOR3_13(G212,G213,G214,G215);
  nor NOR2_18(G216,G41,G3);
  nor NOR2_19(G220,G223,G224);
  nor NOR2_20(G221,G226,G227);
  nor NOR2_21(G222,G234,G235);
  nor NOR3_14(G253,G42,G41,G280);
  nor NOR2_22(G254,G318,G256);
  nor NOR3_15(G260,G263,G264,G265);
  nor NOR2_23(G261,G268,G269);
  nor NOR3_16(G270,G42,G313,G40);
  nor NOR2_24(G274,G282,G283);
  nor NOR2_25(G288,G42,G289);
  nor NOR2_26(G290,G42,G291);
  nor NOR3_17(G292,G294,G328,G295);
  nor NOR2_27(G296,G42,G297);
  nor NOR4_10(G298,G42,G313,G40,G299);
  nor NOR4_11(G300,G42,G41,G40,G301);
  nor NOR2_28(G304,G328,G313);
  nor NOR3_18(G305,G141,G142,G143);
  nor NOR2_29(G310,G328,G311);
  nor NOR3_19(G312,G328,G313,G314);
  nor NOR4_12(G322,G41,G38,G323,G324);
  nor NOR2_30(G324,G120,G121);
  nor NOR2_31(G325,G328,G326);
  nor NOR2_32(G327,G328,G329);

endmodule