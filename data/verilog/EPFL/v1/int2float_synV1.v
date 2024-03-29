/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Tue Nov 17 18:47:53 2020
/////////////////////////////////////////////////////////////


module top ( B_0_, B_1_, B_2_, B_3_, B_4_, B_5_, B_6_, B_7_, B_8_, B_9_, B_10_, 
        M_0_, M_1_, M_2_, M_3_, E_0_, E_1_, E_2_ );
  input B_0_, B_1_, B_2_, B_3_, B_4_, B_5_, B_6_, B_7_, B_8_, B_9_, B_10_;
  output M_0_, M_1_, M_2_, M_3_, E_0_, E_1_, E_2_;
  wire   n223, n224, n225, n226, n227, n228, n229, n230, n231, n232, n233,
         n234, n235, n236, n237, n238, n239, n240, n241, n242, n243, n244,
         n245, n246, n247, n248, n249, n250, n251, n252, n253, n254, n255,
         n256, n257, n258, n259, n260, n261, n262, n263, n264, n265, n266,
         n267, n268, n269, n270, n271, n272, n273, n274, n275, n276, n277,
         n278, n279, n280, n281, n282, n283, n284, n285, n286, n287, n288,
         n289, n290, n291, n292, n293, n294, n295, n296, n297, n298, n299,
         n300, n301, n302, n303, n304, n305, n306, n307, n308, n309, n310,
         n311, n312, n313, n314, n315, n316, n317, n318, n319, n320, n321,
         n322, n323, n324, n325, n326, n327, n328, n329, n330, n331, n332,
         n333, n334, n335, n336, n337, n338, n339, n340, n341, n342, n343,
         n344, n345, n346, n347, n348, n349, n350, n351, n352, n353, n354,
         n355, n356, n357, n358, n359, n360, n361, n362, n363, n364, n365,
         n366, n367, n368, n369, n370, n371, n372, n373, n374, n375, n376,
         n377, n378, n379, n380, n381, n382, n383, n384, n385, n386, n387,
         n388, n389, n390, n391, n392, n393, n394, n395, n396, n397, n398,
         n399, n400, n401, n402, n403, n404, n405, n406, n407, n408, n409,
         n410, n411, n412, n413, n414, n415, n416, n417, n418, n419, n420,
         n421, n422, n423, n424, n425, n426, n427, n428, n429, n430, n431,
         n432, n433, n434, n435, n436, n437, n438, n439, n440, n441, n442,
         n443, n444;

  NAND2_X1 U230 ( .A1(n223), .A2(n224), .ZN(M_3_) );
  NOR2_X1 U231 ( .A1(B_3_), .A2(n225), .ZN(n223) );
  NOR2_X1 U232 ( .A1(n226), .A2(n227), .ZN(n225) );
  NOR2_X1 U233 ( .A1(n228), .A2(n229), .ZN(n227) );
  NAND2_X1 U234 ( .A1(n230), .A2(n231), .ZN(n229) );
  INV_X1 U235 ( .I(n232), .ZN(n226) );
  NAND2_X1 U236 ( .A1(n233), .A2(n234), .ZN(M_2_) );
  NOR2_X1 U237 ( .A1(n235), .A2(n236), .ZN(n234) );
  NOR2_X1 U238 ( .A1(n237), .A2(n238), .ZN(n236) );
  NOR2_X1 U239 ( .A1(n239), .A2(n240), .ZN(n237) );
  NAND2_X1 U240 ( .A1(n241), .A2(n242), .ZN(n240) );
  NAND2_X1 U241 ( .A1(n243), .A2(n244), .ZN(n242) );
  NOR2_X1 U242 ( .A1(n245), .A2(n246), .ZN(n243) );
  NAND2_X1 U243 ( .A1(n247), .A2(n231), .ZN(n241) );
  NOR2_X1 U244 ( .A1(B_8_), .A2(n248), .ZN(n239) );
  NOR2_X1 U245 ( .A1(n249), .A2(n250), .ZN(n248) );
  NAND2_X1 U246 ( .A1(n251), .A2(n252), .ZN(n250) );
  NAND2_X1 U247 ( .A1(B_5_), .A2(n253), .ZN(n252) );
  NAND2_X1 U248 ( .A1(n254), .A2(n255), .ZN(n253) );
  OR2_X1 U249 ( .A1(n256), .A2(B_7_), .Z(n255) );
  NAND2_X1 U250 ( .A1(B_6_), .A2(n246), .ZN(n254) );
  NAND2_X1 U251 ( .A1(B_2_), .A2(n257), .ZN(n251) );
  NOR2_X1 U252 ( .A1(n258), .A2(n259), .ZN(n249) );
  NOR2_X1 U253 ( .A1(n260), .A2(n261), .ZN(n258) );
  NAND2_X1 U254 ( .A1(n262), .A2(n263), .ZN(n261) );
  NAND2_X1 U255 ( .A1(n264), .A2(n245), .ZN(n263) );
  NOR2_X1 U256 ( .A1(n265), .A2(n266), .ZN(n264) );
  NOR2_X1 U257 ( .A1(n267), .A2(B_6_), .ZN(n265) );
  NOR2_X1 U258 ( .A1(B_7_), .A2(n268), .ZN(n267) );
  NAND2_X1 U259 ( .A1(n269), .A2(B_5_), .ZN(n262) );
  NAND2_X1 U260 ( .A1(n270), .A2(n271), .ZN(n269) );
  NAND2_X1 U261 ( .A1(n272), .A2(n273), .ZN(n271) );
  NAND2_X1 U262 ( .A1(n274), .A2(B_3_), .ZN(n270) );
  NOR2_X1 U263 ( .A1(B_6_), .A2(B_1_), .ZN(n274) );
  NOR2_X1 U264 ( .A1(n275), .A2(n276), .ZN(n260) );
  NAND2_X1 U265 ( .A1(n277), .A2(n278), .ZN(n276) );
  NAND2_X1 U266 ( .A1(B_2_), .A2(n279), .ZN(n277) );
  NAND2_X1 U267 ( .A1(n268), .A2(n272), .ZN(n279) );
  NOR2_X1 U268 ( .A1(n273), .A2(n280), .ZN(n235) );
  NAND2_X1 U269 ( .A1(B_6_), .A2(n281), .ZN(n280) );
  NAND2_X1 U270 ( .A1(n282), .A2(n283), .ZN(n281) );
  NAND2_X1 U271 ( .A1(n224), .A2(n284), .ZN(n283) );
  NAND2_X1 U272 ( .A1(B_5_), .A2(B_4_), .ZN(n284) );
  NOR2_X1 U273 ( .A1(n285), .A2(n286), .ZN(n282) );
  NOR2_X1 U274 ( .A1(n287), .A2(n288), .ZN(n286) );
  NOR2_X1 U275 ( .A1(B_8_), .A2(n289), .ZN(n285) );
  NAND2_X1 U276 ( .A1(B_9_), .A2(B_5_), .ZN(n289) );
  NOR2_X1 U277 ( .A1(n290), .A2(n291), .ZN(n233) );
  NOR2_X1 U278 ( .A1(n288), .A2(n292), .ZN(n291) );
  NOR2_X1 U279 ( .A1(n293), .A2(n287), .ZN(n290) );
  NOR2_X1 U280 ( .A1(n294), .A2(n295), .ZN(n293) );
  NAND2_X1 U281 ( .A1(n296), .A2(n297), .ZN(n295) );
  NAND2_X1 U282 ( .A1(n298), .A2(n288), .ZN(n296) );
  OR2_X1 U283 ( .A1(n244), .A2(n247), .Z(n298) );
  NOR2_X1 U284 ( .A1(B_5_), .A2(n292), .ZN(n294) );
  NOR2_X1 U285 ( .A1(n299), .A2(n300), .ZN(M_1_) );
  NAND2_X1 U286 ( .A1(n301), .A2(n302), .ZN(n300) );
  NAND2_X1 U287 ( .A1(n303), .A2(n288), .ZN(n302) );
  NAND2_X1 U288 ( .A1(n304), .A2(n305), .ZN(n303) );
  NOR2_X1 U289 ( .A1(n306), .A2(n307), .ZN(n305) );
  NOR2_X1 U290 ( .A1(n275), .A2(n292), .ZN(n307) );
  NOR2_X1 U291 ( .A1(B_9_), .A2(n308), .ZN(n306) );
  NAND2_X1 U292 ( .A1(n309), .A2(B_8_), .ZN(n308) );
  NOR2_X1 U293 ( .A1(B_6_), .A2(B_4_), .ZN(n309) );
  NOR2_X1 U294 ( .A1(n310), .A2(n311), .ZN(n304) );
  NOR2_X1 U295 ( .A1(n312), .A2(n245), .ZN(n311) );
  NOR2_X1 U296 ( .A1(n313), .A2(n314), .ZN(n312) );
  NAND2_X1 U297 ( .A1(n315), .A2(n316), .ZN(n314) );
  NAND2_X1 U298 ( .A1(n317), .A2(n318), .ZN(n316) );
  NOR2_X1 U299 ( .A1(n319), .A2(n320), .ZN(n317) );
  NAND2_X1 U300 ( .A1(n321), .A2(n297), .ZN(n320) );
  NAND2_X1 U301 ( .A1(n259), .A2(n292), .ZN(n321) );
  NAND2_X1 U302 ( .A1(n322), .A2(n323), .ZN(n315) );
  NOR2_X1 U303 ( .A1(n324), .A2(n259), .ZN(n322) );
  NOR2_X1 U304 ( .A1(n325), .A2(n326), .ZN(n324) );
  NOR2_X1 U305 ( .A1(n273), .A2(n272), .ZN(n326) );
  NOR2_X1 U306 ( .A1(n266), .A2(n327), .ZN(n325) );
  NOR2_X1 U307 ( .A1(n275), .A2(n256), .ZN(n313) );
  NAND2_X1 U308 ( .A1(n328), .A2(B_1_), .ZN(n256) );
  NOR2_X1 U309 ( .A1(B_5_), .A2(n329), .ZN(n310) );
  NOR2_X1 U310 ( .A1(n330), .A2(n331), .ZN(n329) );
  NAND2_X1 U311 ( .A1(n332), .A2(n333), .ZN(n331) );
  NAND2_X1 U312 ( .A1(n334), .A2(n335), .ZN(n333) );
  NAND2_X1 U313 ( .A1(n287), .A2(n336), .ZN(n335) );
  NAND2_X1 U314 ( .A1(n327), .A2(n259), .ZN(n336) );
  NOR2_X1 U315 ( .A1(B_9_), .A2(B_6_), .ZN(n334) );
  NAND2_X1 U316 ( .A1(n337), .A2(n338), .ZN(n332) );
  NAND2_X1 U317 ( .A1(n339), .A2(n340), .ZN(n338) );
  NAND2_X1 U318 ( .A1(n341), .A2(B_4_), .ZN(n340) );
  NOR2_X1 U319 ( .A1(n342), .A2(n343), .ZN(n341) );
  NOR2_X1 U320 ( .A1(n268), .A2(n231), .ZN(n343) );
  NOR2_X1 U321 ( .A1(B_2_), .A2(n344), .ZN(n342) );
  NAND2_X1 U322 ( .A1(n327), .A2(n231), .ZN(n339) );
  NAND2_X1 U323 ( .A1(n345), .A2(n297), .ZN(n330) );
  NAND2_X1 U324 ( .A1(B_9_), .A2(n273), .ZN(n297) );
  NAND2_X1 U325 ( .A1(n346), .A2(n323), .ZN(n345) );
  INV_X1 U326 ( .I(n318), .ZN(n323) );
  NAND2_X1 U327 ( .A1(n287), .A2(n292), .ZN(n318) );
  AND2_X1 U328 ( .A1(n246), .A2(B_7_), .Z(n346) );
  NAND2_X1 U329 ( .A1(B_3_), .A2(B_4_), .ZN(n246) );
  NAND2_X1 U330 ( .A1(n347), .A2(B_10_), .ZN(n301) );
  NOR2_X1 U331 ( .A1(n348), .A2(n349), .ZN(n347) );
  NAND2_X1 U332 ( .A1(B_6_), .A2(n292), .ZN(n349) );
  NOR2_X1 U333 ( .A1(B_8_), .A2(n350), .ZN(n299) );
  NOR2_X1 U334 ( .A1(n351), .A2(n352), .ZN(n350) );
  NAND2_X1 U335 ( .A1(n353), .A2(n354), .ZN(n352) );
  NAND2_X1 U336 ( .A1(n355), .A2(n356), .ZN(n354) );
  NOR2_X1 U337 ( .A1(B_3_), .A2(n357), .ZN(n356) );
  NOR2_X1 U338 ( .A1(n231), .A2(n327), .ZN(n357) );
  NAND2_X1 U339 ( .A1(n358), .A2(n359), .ZN(n353) );
  INV_X1 U340 ( .I(n360), .ZN(n359) );
  NOR2_X1 U341 ( .A1(n361), .A2(n328), .ZN(n358) );
  NOR2_X1 U342 ( .A1(B_4_), .A2(n266), .ZN(n328) );
  NOR2_X1 U343 ( .A1(n362), .A2(n259), .ZN(n361) );
  NOR2_X1 U344 ( .A1(n363), .A2(n288), .ZN(n351) );
  NOR2_X1 U345 ( .A1(n319), .A2(n273), .ZN(n363) );
  NAND2_X1 U346 ( .A1(n364), .A2(n365), .ZN(M_0_) );
  NOR2_X1 U347 ( .A1(n366), .A2(n367), .ZN(n365) );
  NOR2_X1 U348 ( .A1(n368), .A2(n238), .ZN(n367) );
  NOR2_X1 U349 ( .A1(n369), .A2(n370), .ZN(n368) );
  NAND2_X1 U350 ( .A1(n371), .A2(n372), .ZN(n370) );
  NAND2_X1 U351 ( .A1(n373), .A2(n245), .ZN(n372) );
  NOR2_X1 U352 ( .A1(n374), .A2(n259), .ZN(n373) );
  NOR2_X1 U353 ( .A1(n375), .A2(B_8_), .ZN(n374) );
  NOR2_X1 U354 ( .A1(n376), .A2(n275), .ZN(n375) );
  NOR2_X1 U355 ( .A1(n377), .A2(n378), .ZN(n376) );
  NOR2_X1 U356 ( .A1(B_1_), .A2(n344), .ZN(n378) );
  NOR2_X1 U357 ( .A1(B_0_), .A2(n327), .ZN(n377) );
  NAND2_X1 U358 ( .A1(n379), .A2(B_5_), .ZN(n371) );
  NOR2_X1 U359 ( .A1(B_4_), .A2(n287), .ZN(n379) );
  NOR2_X1 U360 ( .A1(n344), .A2(n232), .ZN(n369) );
  NAND2_X1 U361 ( .A1(n257), .A2(n287), .ZN(n232) );
  AND2_X1 U362 ( .A1(n380), .A2(n337), .Z(n257) );
  INV_X1 U363 ( .I(n275), .ZN(n337) );
  NOR2_X1 U364 ( .A1(B_5_), .A2(B_4_), .ZN(n380) );
  NOR2_X1 U365 ( .A1(n381), .A2(n319), .ZN(n366) );
  NOR2_X1 U366 ( .A1(n382), .A2(n383), .ZN(n381) );
  NOR2_X1 U367 ( .A1(B_7_), .A2(n288), .ZN(n383) );
  NOR2_X1 U368 ( .A1(n292), .A2(n384), .ZN(n382) );
  NAND2_X1 U369 ( .A1(n385), .A2(n386), .ZN(n384) );
  NAND2_X1 U370 ( .A1(B_10_), .A2(n287), .ZN(n386) );
  NAND2_X1 U371 ( .A1(B_5_), .A2(n288), .ZN(n385) );
  NOR2_X1 U372 ( .A1(n387), .A2(n388), .ZN(n364) );
  NAND2_X1 U373 ( .A1(n389), .A2(n390), .ZN(n388) );
  NAND2_X1 U374 ( .A1(n391), .A2(n288), .ZN(n390) );
  AND2_X1 U375 ( .A1(B_5_), .A2(n392), .Z(n391) );
  NAND2_X1 U376 ( .A1(n244), .A2(B_10_), .ZN(n389) );
  NOR2_X1 U377 ( .A1(n273), .A2(B_6_), .ZN(n244) );
  NOR2_X1 U378 ( .A1(B_8_), .A2(n393), .ZN(n387) );
  NOR2_X1 U379 ( .A1(n394), .A2(n395), .ZN(n393) );
  NAND2_X1 U380 ( .A1(n396), .A2(n397), .ZN(n395) );
  NAND2_X1 U381 ( .A1(n355), .A2(n398), .ZN(n397) );
  NOR2_X1 U382 ( .A1(B_10_), .A2(n399), .ZN(n398) );
  NOR2_X1 U383 ( .A1(n400), .A2(n401), .ZN(n399) );
  NOR2_X1 U384 ( .A1(B_2_), .A2(n327), .ZN(n401) );
  NOR2_X1 U385 ( .A1(B_1_), .A2(n231), .ZN(n400) );
  NOR2_X1 U386 ( .A1(n275), .A2(n245), .ZN(n355) );
  NAND2_X1 U387 ( .A1(n273), .A2(n319), .ZN(n275) );
  INV_X1 U388 ( .I(B_6_), .ZN(n319) );
  NAND2_X1 U389 ( .A1(n402), .A2(n224), .ZN(n396) );
  NOR2_X1 U390 ( .A1(n403), .A2(n273), .ZN(n402) );
  NOR2_X1 U391 ( .A1(n404), .A2(n405), .ZN(n403) );
  NOR2_X1 U392 ( .A1(B_4_), .A2(n272), .ZN(n405) );
  NOR2_X1 U393 ( .A1(B_3_), .A2(n259), .ZN(n404) );
  NOR2_X1 U394 ( .A1(n406), .A2(n360), .ZN(n394) );
  NAND2_X1 U395 ( .A1(n407), .A2(B_6_), .ZN(n360) );
  NOR2_X1 U396 ( .A1(B_9_), .A2(B_7_), .ZN(n407) );
  NOR2_X1 U397 ( .A1(n408), .A2(n409), .ZN(n406) );
  NOR2_X1 U398 ( .A1(B_3_), .A2(n231), .ZN(n409) );
  NOR2_X1 U399 ( .A1(B_2_), .A2(n272), .ZN(n408) );
  NAND2_X1 U400 ( .A1(n410), .A2(n411), .ZN(E_2_) );
  NOR2_X1 U401 ( .A1(B_8_), .A2(B_7_), .ZN(n411) );
  NOR2_X1 U402 ( .A1(n412), .A2(n238), .ZN(n410) );
  NAND2_X1 U403 ( .A1(n413), .A2(n224), .ZN(E_1_) );
  INV_X1 U404 ( .I(n238), .ZN(n224) );
  NAND2_X1 U405 ( .A1(n292), .A2(n288), .ZN(n238) );
  NOR2_X1 U406 ( .A1(n414), .A2(n415), .ZN(n413) );
  NOR2_X1 U407 ( .A1(n416), .A2(n417), .ZN(n415) );
  NAND2_X1 U408 ( .A1(n273), .A2(n287), .ZN(n417) );
  INV_X1 U409 ( .I(B_7_), .ZN(n273) );
  NOR2_X1 U410 ( .A1(n418), .A2(n419), .ZN(n416) );
  NOR2_X1 U411 ( .A1(n259), .A2(n420), .ZN(n419) );
  NOR2_X1 U412 ( .A1(n421), .A2(n412), .ZN(n418) );
  NOR2_X1 U413 ( .A1(n228), .A2(n266), .ZN(n412) );
  NOR2_X1 U414 ( .A1(B_5_), .A2(B_6_), .ZN(n421) );
  NOR2_X1 U415 ( .A1(n228), .A2(n422), .ZN(n414) );
  NAND2_X1 U416 ( .A1(n230), .A2(n278), .ZN(n422) );
  NAND2_X1 U417 ( .A1(n288), .A2(n423), .ZN(E_0_) );
  NAND2_X1 U418 ( .A1(n424), .A2(n425), .ZN(n423) );
  NAND2_X1 U419 ( .A1(n426), .A2(n427), .ZN(n425) );
  NAND2_X1 U420 ( .A1(n230), .A2(B_5_), .ZN(n427) );
  NAND2_X1 U421 ( .A1(n428), .A2(n292), .ZN(n426) );
  NAND2_X1 U422 ( .A1(n287), .A2(n429), .ZN(n428) );
  NAND2_X1 U423 ( .A1(n430), .A2(n431), .ZN(n429) );
  NAND2_X1 U424 ( .A1(B_7_), .A2(n432), .ZN(n431) );
  NAND2_X1 U425 ( .A1(B_3_), .A2(n433), .ZN(n432) );
  NOR2_X1 U426 ( .A1(n434), .A2(n435), .ZN(n430) );
  NOR2_X1 U427 ( .A1(B_6_), .A2(n436), .ZN(n435) );
  NOR2_X1 U428 ( .A1(n259), .A2(n437), .ZN(n436) );
  NAND2_X1 U429 ( .A1(n438), .A2(n420), .ZN(n437) );
  NAND2_X1 U430 ( .A1(n439), .A2(n268), .ZN(n420) );
  NOR2_X1 U431 ( .A1(n344), .A2(n327), .ZN(n268) );
  INV_X1 U432 ( .I(B_1_), .ZN(n327) );
  INV_X1 U433 ( .I(B_0_), .ZN(n344) );
  NOR2_X1 U434 ( .A1(B_5_), .A2(n266), .ZN(n439) );
  NAND2_X1 U435 ( .A1(B_5_), .A2(n440), .ZN(n438) );
  NAND2_X1 U436 ( .A1(B_1_), .A2(n362), .ZN(n440) );
  AND2_X1 U437 ( .A1(n247), .A2(n362), .Z(n434) );
  INV_X1 U438 ( .I(n266), .ZN(n362) );
  NAND2_X1 U439 ( .A1(B_2_), .A2(B_3_), .ZN(n266) );
  NOR2_X1 U440 ( .A1(n228), .A2(B_7_), .ZN(n247) );
  INV_X1 U441 ( .I(B_8_), .ZN(n287) );
  NOR2_X1 U442 ( .A1(n441), .A2(n392), .ZN(n424) );
  NOR2_X1 U443 ( .A1(n292), .A2(B_6_), .ZN(n392) );
  NOR2_X1 U444 ( .A1(n442), .A2(n443), .ZN(n441) );
  NAND2_X1 U445 ( .A1(n433), .A2(n230), .ZN(n443) );
  INV_X1 U446 ( .I(n348), .ZN(n230) );
  NAND2_X1 U447 ( .A1(B_8_), .A2(B_7_), .ZN(n348) );
  INV_X1 U448 ( .I(n228), .ZN(n433) );
  NAND2_X1 U449 ( .A1(n444), .A2(B_6_), .ZN(n228) );
  NOR2_X1 U450 ( .A1(n259), .A2(n245), .ZN(n444) );
  INV_X1 U451 ( .I(B_5_), .ZN(n245) );
  INV_X1 U452 ( .I(B_4_), .ZN(n259) );
  NAND2_X1 U453 ( .A1(n278), .A2(n292), .ZN(n442) );
  INV_X1 U454 ( .I(B_9_), .ZN(n292) );
  NAND2_X1 U455 ( .A1(n272), .A2(n231), .ZN(n278) );
  INV_X1 U456 ( .I(B_2_), .ZN(n231) );
  INV_X1 U457 ( .I(B_3_), .ZN(n272) );
  INV_X1 U458 ( .I(B_10_), .ZN(n288) );
endmodule

