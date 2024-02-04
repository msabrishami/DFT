/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Wed Nov 18 17:32:47 2020
/////////////////////////////////////////////////////////////


module c1355 ( N1, N8, N15, N22, N29, N36, N43, N50, N57, N64, N71, N78, N85, 
        N92, N99, N106, N113, N120, N127, N134, N141, N148, N155, N162, N169, 
        N176, N183, N190, N197, N204, N211, N218, N225, N226, N227, N228, N229, 
        N230, N231, N232, N233, N1324, N1325, N1326, N1327, N1328, N1329, 
        N1330, N1331, N1332, N1333, N1334, N1335, N1336, N1337, N1338, N1339, 
        N1340, N1341, N1342, N1343, N1344, N1345, N1346, N1347, N1348, N1349, 
        N1350, N1351, N1352, N1353, N1354, N1355 );
  input N1, N8, N15, N22, N29, N36, N43, N50, N57, N64, N71, N78, N85, N92,
         N99, N106, N113, N120, N127, N134, N141, N148, N155, N162, N169, N176,
         N183, N190, N197, N204, N211, N218, N225, N226, N227, N228, N229,
         N230, N231, N232, N233;
  output N1324, N1325, N1326, N1327, N1328, N1329, N1330, N1331, N1332, N1333,
         N1334, N1335, N1336, N1337, N1338, N1339, N1340, N1341, N1342, N1343,
         N1344, N1345, N1346, N1347, N1348, N1349, N1350, N1351, N1352, N1353,
         N1354, N1355;
  wire   n287, n288, n289, n290, n291, n292, n293, n294, n295, n296, n297,
         n298, n299, n300, n301, n302, n303, n304, n305, n306, n307, n308,
         n309, n310, n311, n312, n313, n314, n315, n316, n317, n318, n319,
         n320, n321, n322, n323, n324, n325, n326, n327, n328, n329, n330,
         n331, n332, n333, n334, n335, n336, n337, n338, n339, n340, n341,
         n342, n343, n344, n345, n346, n347, n348, n349, n350, n351, n352,
         n353, n354, n355, n356, n357, n358, n359, n360, n361, n362, n363,
         n364, n365, n366, n367, n368, n369, n370, n371, n372, n373, n374,
         n375, n376, n377, n378, n379, n380, n381, n382, n383, n384, n385,
         n386, n387, n388, n389, n390, n391, n392, n393, n394, n395, n396,
         n397, n398, n399, n400, n401, n402, n403, n404, n405, n406, n407,
         n408, n409, n410, n411, n412, n413, n414, n415, n416, n417, n418,
         n419, n420, n421, n422, n423, n424, n425, n426, n427, n428, n429,
         n430, n431, n432, n433, n434, n435, n436, n437, n438, n439, n440,
         n441, n442, n443, n444, n445, n446, n447, n448, n449, n450, n451,
         n452, n453, n454, n455, n456, n457, n458, n459, n460, n461, n462;

  XOR2_X1 U319 ( .A1(N218), .A2(n287), .Z(N1355) );
  NOR2_X1 U320 ( .A1(n288), .A2(n289), .ZN(n287) );
  XOR2_X1 U321 ( .A1(N211), .A2(n290), .Z(N1354) );
  NOR2_X1 U322 ( .A1(n291), .A2(n289), .ZN(n290) );
  XOR2_X1 U323 ( .A1(N204), .A2(n292), .Z(N1353) );
  NOR2_X1 U324 ( .A1(n293), .A2(n289), .ZN(n292) );
  XOR2_X1 U325 ( .A1(N197), .A2(n294), .Z(N1352) );
  NOR2_X1 U326 ( .A1(n295), .A2(n289), .ZN(n294) );
  NAND4_X1 U327 ( .A1(n296), .A2(n297), .A3(n298), .A4(n299), .ZN(n289) );
  XOR2_X1 U328 ( .A1(N190), .A2(n300), .Z(N1351) );
  NOR2_X1 U329 ( .A1(n288), .A2(n301), .ZN(n300) );
  XOR2_X1 U330 ( .A1(N183), .A2(n302), .Z(N1350) );
  NOR2_X1 U331 ( .A1(n291), .A2(n301), .ZN(n302) );
  XOR2_X1 U332 ( .A1(N176), .A2(n303), .Z(N1349) );
  NOR2_X1 U333 ( .A1(n293), .A2(n301), .ZN(n303) );
  XOR2_X1 U334 ( .A1(N169), .A2(n304), .Z(N1348) );
  NOR2_X1 U335 ( .A1(n295), .A2(n301), .ZN(n304) );
  NAND4_X1 U336 ( .A1(n305), .A2(n299), .A3(n306), .A4(n307), .ZN(n301) );
  NOR2_X1 U337 ( .A1(n308), .A2(n309), .ZN(n307) );
  XOR2_X1 U338 ( .A1(N162), .A2(n310), .Z(N1347) );
  NOR2_X1 U339 ( .A1(n288), .A2(n311), .ZN(n310) );
  XOR2_X1 U340 ( .A1(N155), .A2(n312), .Z(N1346) );
  NOR2_X1 U341 ( .A1(n291), .A2(n311), .ZN(n312) );
  XOR2_X1 U342 ( .A1(N148), .A2(n313), .Z(N1345) );
  NOR2_X1 U343 ( .A1(n293), .A2(n311), .ZN(n313) );
  XOR2_X1 U344 ( .A1(N141), .A2(n314), .Z(N1344) );
  NOR2_X1 U345 ( .A1(n295), .A2(n311), .ZN(n314) );
  NAND4_X1 U346 ( .A1(n308), .A2(n299), .A3(n309), .A4(n315), .ZN(n311) );
  NOR2_X1 U347 ( .A1(n306), .A2(n305), .ZN(n315) );
  XOR2_X1 U348 ( .A1(N134), .A2(n316), .Z(N1343) );
  NOR2_X1 U349 ( .A1(n288), .A2(n317), .ZN(n316) );
  XOR2_X1 U350 ( .A1(N127), .A2(n318), .Z(N1342) );
  NOR2_X1 U351 ( .A1(n291), .A2(n317), .ZN(n318) );
  XOR2_X1 U352 ( .A1(N120), .A2(n319), .Z(N1341) );
  NOR2_X1 U353 ( .A1(n293), .A2(n317), .ZN(n319) );
  XOR2_X1 U354 ( .A1(N113), .A2(n320), .Z(N1340) );
  NOR2_X1 U355 ( .A1(n295), .A2(n317), .ZN(n320) );
  NAND4_X1 U356 ( .A1(n321), .A2(n322), .A3(n323), .A4(n299), .ZN(n317) );
  NAND2_X1 U357 ( .A1(n324), .A2(n325), .ZN(n299) );
  OR3_X1 U358 ( .A1(n326), .A2(n327), .A3(n328), .Z(n325) );
  OR3_X1 U359 ( .A1(n329), .A2(n330), .A3(n331), .Z(n324) );
  XOR2_X1 U360 ( .A1(N106), .A2(n332), .Z(N1339) );
  NOR2_X1 U361 ( .A1(n323), .A2(n333), .ZN(n332) );
  XOR2_X1 U362 ( .A1(N99), .A2(n334), .Z(N1338) );
  NOR2_X1 U363 ( .A1(n296), .A2(n333), .ZN(n334) );
  XOR2_X1 U364 ( .A1(N92), .A2(n335), .Z(N1337) );
  NOR2_X1 U365 ( .A1(n321), .A2(n333), .ZN(n335) );
  XOR2_X1 U366 ( .A1(N85), .A2(n336), .Z(N1336) );
  NOR2_X1 U367 ( .A1(n298), .A2(n333), .ZN(n336) );
  NAND4_X1 U368 ( .A1(n291), .A2(n330), .A3(n295), .A4(n337), .ZN(n333) );
  NOR2_X1 U369 ( .A1(n288), .A2(n293), .ZN(n330) );
  XOR2_X1 U370 ( .A1(N78), .A2(n338), .Z(N1335) );
  NOR2_X1 U371 ( .A1(n323), .A2(n339), .ZN(n338) );
  XOR2_X1 U372 ( .A1(N71), .A2(n340), .Z(N1334) );
  NOR2_X1 U373 ( .A1(n296), .A2(n339), .ZN(n340) );
  XOR2_X1 U374 ( .A1(N64), .A2(n341), .Z(N1333) );
  NOR2_X1 U375 ( .A1(n321), .A2(n339), .ZN(n341) );
  XNOR2_X1 U376 ( .A1(n342), .A2(n343), .ZN(N1332) );
  NOR2_X1 U377 ( .A1(n298), .A2(n339), .ZN(n343) );
  NAND4_X1 U378 ( .A1(n331), .A2(n337), .A3(n328), .A4(n344), .ZN(n339) );
  NOR2_X1 U379 ( .A1(n326), .A2(n329), .ZN(n344) );
  XOR2_X1 U380 ( .A1(N50), .A2(n345), .Z(N1331) );
  NOR2_X1 U381 ( .A1(n323), .A2(n346), .ZN(n345) );
  XOR2_X1 U382 ( .A1(N43), .A2(n347), .Z(N1330) );
  NOR2_X1 U383 ( .A1(n296), .A2(n346), .ZN(n347) );
  XOR2_X1 U384 ( .A1(N36), .A2(n348), .Z(N1329) );
  NOR2_X1 U385 ( .A1(n321), .A2(n346), .ZN(n348) );
  XOR2_X1 U386 ( .A1(N29), .A2(n349), .Z(N1328) );
  NOR2_X1 U387 ( .A1(n298), .A2(n346), .ZN(n349) );
  NAND4_X1 U388 ( .A1(n329), .A2(n337), .A3(n326), .A4(n350), .ZN(n346) );
  NOR2_X1 U389 ( .A1(n331), .A2(n328), .ZN(n350) );
  XOR2_X1 U390 ( .A1(N22), .A2(n351), .Z(N1327) );
  NOR2_X1 U391 ( .A1(n323), .A2(n352), .ZN(n351) );
  XOR2_X1 U392 ( .A1(N15), .A2(n353), .Z(N1326) );
  NOR2_X1 U393 ( .A1(n296), .A2(n352), .ZN(n353) );
  XOR2_X1 U394 ( .A1(N8), .A2(n354), .Z(N1325) );
  NOR2_X1 U395 ( .A1(n321), .A2(n352), .ZN(n354) );
  XOR2_X1 U396 ( .A1(N1), .A2(n355), .Z(N1324) );
  NOR2_X1 U397 ( .A1(n298), .A2(n352), .ZN(n355) );
  NAND4_X1 U398 ( .A1(n293), .A2(n327), .A3(n288), .A4(n337), .ZN(n352) );
  NAND2_X1 U399 ( .A1(n356), .A2(n357), .ZN(n337) );
  OR3_X1 U400 ( .A1(n308), .A2(n322), .A3(n305), .Z(n357) );
  NOR2_X1 U401 ( .A1(n298), .A2(n296), .ZN(n322) );
  INV_X1 U402 ( .I(n306), .ZN(n296) );
  OR3_X1 U403 ( .A1(n309), .A2(n297), .A3(n306), .Z(n356) );
  XNOR2_X1 U404 ( .A1(n358), .A2(n359), .ZN(n306) );
  XOR2_X1 U405 ( .A1(N43), .A2(n360), .Z(n359) );
  XOR2_X1 U406 ( .A1(N99), .A2(N71), .Z(n360) );
  XOR2_X1 U407 ( .A1(n361), .A2(N15), .Z(n358) );
  NAND2_X1 U408 ( .A1(n362), .A2(n363), .ZN(n361) );
  NAND3_X1 U409 ( .A1(N233), .A2(n364), .A3(N227), .ZN(n363) );
  XNOR2_X1 U410 ( .A1(n365), .A2(n366), .ZN(n364) );
  NAND2_X1 U411 ( .A1(n367), .A2(n368), .ZN(n362) );
  NAND2_X1 U412 ( .A1(N227), .A2(N233), .ZN(n368) );
  XNOR2_X1 U413 ( .A1(n366), .A2(n369), .ZN(n367) );
  NOR2_X1 U414 ( .A1(n321), .A2(n323), .ZN(n297) );
  INV_X1 U415 ( .I(n308), .ZN(n323) );
  XNOR2_X1 U416 ( .A1(n370), .A2(n371), .ZN(n308) );
  XOR2_X1 U417 ( .A1(N22), .A2(n372), .Z(n371) );
  XOR2_X1 U418 ( .A1(N78), .A2(N50), .Z(n372) );
  XOR2_X1 U419 ( .A1(n373), .A2(N106), .Z(n370) );
  NAND2_X1 U420 ( .A1(n374), .A2(n375), .ZN(n373) );
  NAND3_X1 U421 ( .A1(N233), .A2(n376), .A3(N228), .ZN(n375) );
  XNOR2_X1 U422 ( .A1(n377), .A2(n378), .ZN(n376) );
  NAND2_X1 U423 ( .A1(n379), .A2(n380), .ZN(n374) );
  NAND2_X1 U424 ( .A1(N228), .A2(N233), .ZN(n380) );
  XNOR2_X1 U425 ( .A1(n381), .A2(n377), .ZN(n379) );
  INV_X1 U426 ( .I(n305), .ZN(n321) );
  XNOR2_X1 U427 ( .A1(n382), .A2(n383), .ZN(n305) );
  XOR2_X1 U428 ( .A1(N64), .A2(n384), .Z(n383) );
  XOR2_X1 U429 ( .A1(N92), .A2(N8), .Z(n384) );
  XOR2_X1 U430 ( .A1(n385), .A2(N36), .Z(n382) );
  NAND2_X1 U431 ( .A1(n386), .A2(n387), .ZN(n385) );
  NAND3_X1 U432 ( .A1(N233), .A2(n388), .A3(N226), .ZN(n387) );
  XNOR2_X1 U433 ( .A1(n366), .A2(n378), .ZN(n388) );
  INV_X1 U434 ( .I(n381), .ZN(n378) );
  NAND2_X1 U435 ( .A1(n389), .A2(n390), .ZN(n386) );
  NAND2_X1 U436 ( .A1(N226), .A2(N233), .ZN(n390) );
  XNOR2_X1 U437 ( .A1(n381), .A2(n366), .ZN(n389) );
  XNOR2_X1 U438 ( .A1(n391), .A2(n392), .ZN(n366) );
  XOR2_X1 U439 ( .A1(N190), .A2(N183), .Z(n392) );
  XNOR2_X1 U440 ( .A1(N169), .A2(N176), .ZN(n391) );
  XNOR2_X1 U441 ( .A1(n393), .A2(n394), .ZN(n381) );
  XOR2_X1 U442 ( .A1(N218), .A2(N211), .Z(n394) );
  XNOR2_X1 U443 ( .A1(N197), .A2(N204), .ZN(n393) );
  INV_X1 U444 ( .I(n326), .ZN(n288) );
  XNOR2_X1 U445 ( .A1(n395), .A2(n396), .ZN(n326) );
  XOR2_X1 U446 ( .A1(N162), .A2(n397), .Z(n396) );
  XOR2_X1 U447 ( .A1(N218), .A2(N190), .Z(n397) );
  XOR2_X1 U448 ( .A1(n398), .A2(N134), .Z(n395) );
  NAND2_X1 U449 ( .A1(n399), .A2(n400), .ZN(n398) );
  NAND3_X1 U450 ( .A1(N233), .A2(n401), .A3(N232), .ZN(n400) );
  XOR2_X1 U451 ( .A1(n402), .A2(n403), .Z(n401) );
  NAND2_X1 U452 ( .A1(n404), .A2(n405), .ZN(n399) );
  NAND2_X1 U453 ( .A1(N232), .A2(N233), .ZN(n405) );
  XNOR2_X1 U454 ( .A1(n403), .A2(n402), .ZN(n404) );
  NOR2_X1 U455 ( .A1(n295), .A2(n291), .ZN(n327) );
  INV_X1 U456 ( .I(n331), .ZN(n291) );
  XNOR2_X1 U457 ( .A1(n406), .A2(n407), .ZN(n331) );
  XOR2_X1 U458 ( .A1(N155), .A2(n408), .Z(n407) );
  XOR2_X1 U459 ( .A1(N211), .A2(N183), .Z(n408) );
  XOR2_X1 U460 ( .A1(n409), .A2(N127), .Z(n406) );
  NAND2_X1 U461 ( .A1(n410), .A2(n411), .ZN(n409) );
  NAND3_X1 U462 ( .A1(N231), .A2(n412), .A3(N233), .ZN(n411) );
  XNOR2_X1 U463 ( .A1(n413), .A2(n414), .ZN(n412) );
  NAND2_X1 U464 ( .A1(n415), .A2(n416), .ZN(n410) );
  NAND2_X1 U465 ( .A1(N233), .A2(N231), .ZN(n416) );
  XNOR2_X1 U466 ( .A1(n417), .A2(n413), .ZN(n415) );
  INV_X1 U467 ( .I(n329), .ZN(n295) );
  NAND2_X1 U468 ( .A1(n418), .A2(n419), .ZN(n329) );
  NAND2_X1 U469 ( .A1(n420), .A2(n421), .ZN(n419) );
  NAND2_X1 U470 ( .A1(n422), .A2(n423), .ZN(n421) );
  NAND3_X1 U471 ( .A1(n422), .A2(n423), .A3(n424), .ZN(n418) );
  INV_X1 U472 ( .I(n420), .ZN(n424) );
  XNOR2_X1 U473 ( .A1(n425), .A2(n426), .ZN(n420) );
  XOR2_X1 U474 ( .A1(N197), .A2(N169), .Z(n426) );
  XNOR2_X1 U475 ( .A1(N113), .A2(N141), .ZN(n425) );
  NAND2_X1 U476 ( .A1(n427), .A2(n428), .ZN(n423) );
  NAND2_X1 U477 ( .A1(N229), .A2(N233), .ZN(n428) );
  XNOR2_X1 U478 ( .A1(n417), .A2(n403), .ZN(n427) );
  NAND3_X1 U479 ( .A1(N233), .A2(n429), .A3(N229), .ZN(n422) );
  XNOR2_X1 U480 ( .A1(n403), .A2(n414), .ZN(n429) );
  INV_X1 U481 ( .I(n417), .ZN(n414) );
  XNOR2_X1 U482 ( .A1(n430), .A2(n431), .ZN(n417) );
  XOR2_X1 U483 ( .A1(N8), .A2(N22), .Z(n431) );
  XNOR2_X1 U484 ( .A1(N1), .A2(N15), .ZN(n430) );
  XNOR2_X1 U485 ( .A1(n432), .A2(n433), .ZN(n403) );
  XOR2_X1 U486 ( .A1(N50), .A2(N43), .Z(n433) );
  XNOR2_X1 U487 ( .A1(N29), .A2(N36), .ZN(n432) );
  INV_X1 U488 ( .I(n328), .ZN(n293) );
  XNOR2_X1 U489 ( .A1(n434), .A2(n435), .ZN(n328) );
  XOR2_X1 U490 ( .A1(N148), .A2(n436), .Z(n435) );
  XOR2_X1 U491 ( .A1(N204), .A2(N176), .Z(n436) );
  XOR2_X1 U492 ( .A1(n437), .A2(N120), .Z(n434) );
  NAND2_X1 U493 ( .A1(n438), .A2(n439), .ZN(n437) );
  NAND3_X1 U494 ( .A1(N233), .A2(n440), .A3(N230), .ZN(n439) );
  XOR2_X1 U495 ( .A1(n402), .A2(n413), .Z(n440) );
  NAND2_X1 U496 ( .A1(n441), .A2(n442), .ZN(n438) );
  NAND2_X1 U497 ( .A1(N230), .A2(N233), .ZN(n442) );
  XNOR2_X1 U498 ( .A1(n413), .A2(n402), .ZN(n441) );
  XNOR2_X1 U499 ( .A1(n443), .A2(n444), .ZN(n402) );
  XOR2_X1 U500 ( .A1(N99), .A2(N92), .Z(n444) );
  XNOR2_X1 U501 ( .A1(N106), .A2(N85), .ZN(n443) );
  XNOR2_X1 U502 ( .A1(n445), .A2(n446), .ZN(n413) );
  XOR2_X1 U503 ( .A1(N78), .A2(N71), .Z(n446) );
  XNOR2_X1 U504 ( .A1(N57), .A2(N64), .ZN(n445) );
  INV_X1 U505 ( .I(n309), .ZN(n298) );
  NAND2_X1 U506 ( .A1(n447), .A2(n448), .ZN(n309) );
  NAND2_X1 U507 ( .A1(n449), .A2(n450), .ZN(n448) );
  NAND2_X1 U508 ( .A1(n451), .A2(n452), .ZN(n450) );
  NAND3_X1 U509 ( .A1(n451), .A2(n452), .A3(n453), .ZN(n447) );
  INV_X1 U510 ( .I(n449), .ZN(n453) );
  XNOR2_X1 U511 ( .A1(n454), .A2(n455), .ZN(n449) );
  XNOR2_X1 U512 ( .A1(N85), .A2(n342), .ZN(n455) );
  INV_X1 U513 ( .I(N57), .ZN(n342) );
  XNOR2_X1 U514 ( .A1(N1), .A2(N29), .ZN(n454) );
  NAND2_X1 U515 ( .A1(n456), .A2(n457), .ZN(n452) );
  NAND2_X1 U516 ( .A1(N225), .A2(N233), .ZN(n457) );
  XNOR2_X1 U517 ( .A1(n369), .A2(n377), .ZN(n456) );
  NAND3_X1 U518 ( .A1(N233), .A2(n458), .A3(N225), .ZN(n451) );
  XNOR2_X1 U519 ( .A1(n377), .A2(n365), .ZN(n458) );
  INV_X1 U520 ( .I(n369), .ZN(n365) );
  XNOR2_X1 U521 ( .A1(n459), .A2(n460), .ZN(n369) );
  XOR2_X1 U522 ( .A1(N134), .A2(N127), .Z(n460) );
  XNOR2_X1 U523 ( .A1(N113), .A2(N120), .ZN(n459) );
  XNOR2_X1 U524 ( .A1(n461), .A2(n462), .ZN(n377) );
  XOR2_X1 U525 ( .A1(N162), .A2(N155), .Z(n462) );
  XNOR2_X1 U526 ( .A1(N141), .A2(N148), .ZN(n461) );
endmodule

