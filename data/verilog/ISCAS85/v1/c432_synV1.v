/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : P-2019.03-SP1-1
// Date      : Tue Nov 17 22:20:19 2020
/////////////////////////////////////////////////////////////


module c432 ( N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, N34, N37, N40, 
        N43, N47, N50, N53, N56, N60, N63, N66, N69, N73, N76, N79, N82, N86, 
        N89, N92, N95, N99, N102, N105, N108, N112, N115, N223, N329, N370, 
        N421, N430, N431, N432 );
  input N1, N4, N8, N11, N14, N17, N21, N24, N27, N30, N34, N37, N40, N43, N47,
         N50, N53, N56, N60, N63, N66, N69, N73, N76, N79, N82, N86, N89, N92,
         N95, N99, N102, N105, N108, N112, N115;
  output N223, N329, N370, N421, N430, N431, N432;
  wire   n172, n173, n174, n175, n176, n177, n178, n179, n180, n181, n182,
         n183, n184, n185, n186, n187, n188, n189, n190, n191, n192, n193,
         n194, n195, n196, n197, n198, n199, n200, n201, n202, n203, n204,
         n205, n206, n207, n208, n209, n210, n211, n212, n213, n214, n215,
         n216, n217, n218, n219, n220, n221, n222, n223, n224, n225, n226,
         n227, n228, n229, n230, n231, n232, n233, n234, n235, n236, n237,
         n238, n239, n240, n241, n242, n243, n244, n245, n246, n247, n248,
         n249, n250, n251, n252, n253, n254, n255, n256, n257, n258, n259,
         n260, n261, n262, n263, n264, n265, n266, n267, n268, n269, n270,
         n271, n272, n273, n274, n275, n276, n277, n278, n279, n280, n281,
         n282, n283, n284, n285, n286, n287, n288, n289, n290, n291, n292,
         n293, n294, n295, n296, n297, n298, n299, n300, n301, n302, n303,
         n304, n305, n306, n307, n308, n309, n310, n311, n312, n313, n314,
         n315, n316, n317, n318, n319, n320, n321, n322, n323, n324, n325,
         n326, n327, n328, n329, n330, n331, n332, n333, n334, n335, n336,
         n337, n338, n339, n340;

  NAND2_X1 U179 ( .A1(n172), .A2(n173), .ZN(N432) );
  NAND2_X1 U180 ( .A1(n174), .A2(n175), .ZN(n173) );
  NAND2_X1 U181 ( .A1(n176), .A2(n177), .ZN(n174) );
  OR2_X1 U182 ( .A1(n178), .A2(n179), .Z(n177) );
  NOR2_X1 U183 ( .A1(n180), .A2(n181), .ZN(n176) );
  NOR2_X1 U184 ( .A1(n182), .A2(n183), .ZN(n181) );
  NOR2_X1 U185 ( .A1(n184), .A2(n185), .ZN(n180) );
  NOR2_X1 U186 ( .A1(n186), .A2(n187), .ZN(n184) );
  NOR2_X1 U187 ( .A1(N329), .A2(n188), .ZN(n186) );
  NAND2_X1 U188 ( .A1(n189), .A2(n190), .ZN(N431) );
  NAND2_X1 U189 ( .A1(n191), .A2(n192), .ZN(n190) );
  NOR2_X1 U190 ( .A1(n179), .A2(n193), .ZN(n191) );
  NOR2_X1 U191 ( .A1(n194), .A2(n195), .ZN(n189) );
  NOR2_X1 U192 ( .A1(n196), .A2(n197), .ZN(N421) );
  NOR2_X1 U193 ( .A1(n198), .A2(n199), .ZN(n197) );
  NAND2_X1 U194 ( .A1(n200), .A2(n183), .ZN(n199) );
  NAND2_X1 U195 ( .A1(n201), .A2(n202), .ZN(n183) );
  NOR2_X1 U196 ( .A1(n203), .A2(n204), .ZN(n201) );
  NOR2_X1 U197 ( .A1(n205), .A2(n206), .ZN(n204) );
  NOR2_X1 U198 ( .A1(n207), .A2(n208), .ZN(n203) );
  INV_X1 U199 ( .I(n192), .ZN(n200) );
  NAND2_X1 U200 ( .A1(n178), .A2(n209), .ZN(n192) );
  INV_X1 U201 ( .I(n182), .ZN(n209) );
  NOR2_X1 U202 ( .A1(n210), .A2(n211), .ZN(n182) );
  OR2_X1 U203 ( .A1(n212), .A2(n213), .Z(n210) );
  NOR2_X1 U204 ( .A1(n205), .A2(n214), .ZN(n213) );
  AND2_X1 U205 ( .A1(N329), .A2(N86), .Z(n212) );
  NAND2_X1 U206 ( .A1(n215), .A2(n216), .ZN(n178) );
  NOR2_X1 U207 ( .A1(n217), .A2(n218), .ZN(n215) );
  AND2_X1 U208 ( .A1(N370), .A2(N79), .Z(n218) );
  NOR2_X1 U209 ( .A1(n207), .A2(n219), .ZN(n217) );
  OR2_X1 U210 ( .A1(N430), .A2(N108), .Z(n198) );
  NAND2_X1 U211 ( .A1(n220), .A2(n221), .ZN(N430) );
  NOR2_X1 U212 ( .A1(n179), .A2(n194), .ZN(n221) );
  INV_X1 U213 ( .I(n172), .ZN(n194) );
  NAND2_X1 U214 ( .A1(n222), .A2(n223), .ZN(n172) );
  NOR2_X1 U215 ( .A1(n224), .A2(n225), .ZN(n222) );
  AND2_X1 U216 ( .A1(N370), .A2(N27), .Z(n225) );
  NOR2_X1 U217 ( .A1(n207), .A2(n226), .ZN(n224) );
  AND2_X1 U218 ( .A1(n227), .A2(n228), .Z(n179) );
  NOR2_X1 U219 ( .A1(n229), .A2(n230), .ZN(n227) );
  NOR2_X1 U220 ( .A1(n207), .A2(n231), .ZN(n230) );
  AND2_X1 U221 ( .A1(N370), .A2(N66), .Z(n229) );
  NOR2_X1 U222 ( .A1(n195), .A2(n193), .ZN(n220) );
  AND2_X1 U223 ( .A1(n232), .A2(n233), .Z(n193) );
  NOR2_X1 U224 ( .A1(n234), .A2(n185), .ZN(n232) );
  NOR2_X1 U225 ( .A1(n205), .A2(n235), .ZN(n185) );
  INV_X1 U226 ( .I(N53), .ZN(n235) );
  INV_X1 U227 ( .I(N370), .ZN(n205) );
  AND2_X1 U228 ( .A1(N329), .A2(N47), .Z(n234) );
  INV_X1 U229 ( .I(n175), .ZN(n195) );
  NAND2_X1 U230 ( .A1(n236), .A2(n237), .ZN(n175) );
  NOR2_X1 U231 ( .A1(n238), .A2(n239), .ZN(n237) );
  AND2_X1 U232 ( .A1(N329), .A2(N34), .Z(n239) );
  NOR2_X1 U233 ( .A1(n240), .A2(n241), .ZN(n236) );
  AND2_X1 U234 ( .A1(N370), .A2(N40), .Z(n240) );
  NOR2_X1 U235 ( .A1(n242), .A2(n243), .ZN(n196) );
  NAND2_X1 U236 ( .A1(N4), .A2(n244), .ZN(n243) );
  NAND2_X1 U237 ( .A1(N14), .A2(N370), .ZN(n244) );
  NAND2_X1 U238 ( .A1(n245), .A2(n246), .ZN(n242) );
  NAND2_X1 U239 ( .A1(N8), .A2(N329), .ZN(n245) );
  NAND2_X1 U240 ( .A1(n247), .A2(n248), .ZN(N370) );
  NOR2_X1 U241 ( .A1(n249), .A2(n250), .ZN(n248) );
  NAND2_X1 U242 ( .A1(n251), .A2(n252), .ZN(n250) );
  NAND2_X1 U243 ( .A1(n253), .A2(n254), .ZN(n252) );
  INV_X1 U244 ( .I(n255), .ZN(n254) );
  NOR2_X1 U245 ( .A1(N115), .A2(n256), .ZN(n253) );
  NOR2_X1 U246 ( .A1(n257), .A2(n207), .ZN(n256) );
  NAND2_X1 U247 ( .A1(n258), .A2(n233), .ZN(n251) );
  INV_X1 U248 ( .I(n188), .ZN(n233) );
  NOR2_X1 U249 ( .A1(N53), .A2(n259), .ZN(n258) );
  NOR2_X1 U250 ( .A1(n187), .A2(n207), .ZN(n259) );
  NAND2_X1 U251 ( .A1(n260), .A2(n261), .ZN(n249) );
  NAND2_X1 U252 ( .A1(n262), .A2(n263), .ZN(n261) );
  NOR2_X1 U253 ( .A1(N14), .A2(n264), .ZN(n263) );
  NOR2_X1 U254 ( .A1(n265), .A2(n266), .ZN(n262) );
  AND2_X1 U255 ( .A1(N329), .A2(N8), .Z(n265) );
  NOR2_X1 U256 ( .A1(n267), .A2(n268), .ZN(n260) );
  NOR2_X1 U257 ( .A1(n211), .A2(n269), .ZN(n268) );
  NAND2_X1 U258 ( .A1(n270), .A2(n214), .ZN(n269) );
  INV_X1 U259 ( .I(N92), .ZN(n214) );
  OR2_X1 U260 ( .A1(n207), .A2(n271), .Z(n270) );
  NOR2_X1 U261 ( .A1(n272), .A2(n273), .ZN(n267) );
  NAND2_X1 U262 ( .A1(n274), .A2(n206), .ZN(n273) );
  INV_X1 U263 ( .I(N105), .ZN(n206) );
  NAND2_X1 U264 ( .A1(N329), .A2(n275), .ZN(n274) );
  NOR2_X1 U265 ( .A1(n276), .A2(n277), .ZN(n247) );
  NAND2_X1 U266 ( .A1(n278), .A2(n279), .ZN(n277) );
  NAND2_X1 U267 ( .A1(n280), .A2(n281), .ZN(n279) );
  NOR2_X1 U268 ( .A1(N27), .A2(n282), .ZN(n281) );
  AND2_X1 U269 ( .A1(n283), .A2(N329), .Z(n282) );
  NOR2_X1 U270 ( .A1(n284), .A2(n285), .ZN(n280) );
  INV_X1 U271 ( .I(N17), .ZN(n285) );
  NOR2_X1 U272 ( .A1(n286), .A2(n287), .ZN(n284) );
  NAND2_X1 U273 ( .A1(n288), .A2(n289), .ZN(n278) );
  NOR2_X1 U274 ( .A1(N40), .A2(n238), .ZN(n289) );
  NOR2_X1 U275 ( .A1(n290), .A2(n241), .ZN(n288) );
  AND2_X1 U276 ( .A1(n291), .A2(N329), .Z(n290) );
  NAND2_X1 U277 ( .A1(n292), .A2(n293), .ZN(n276) );
  NAND2_X1 U278 ( .A1(n294), .A2(n216), .ZN(n293) );
  NOR2_X1 U279 ( .A1(N79), .A2(n295), .ZN(n294) );
  NOR2_X1 U280 ( .A1(n296), .A2(n207), .ZN(n295) );
  INV_X1 U281 ( .I(N329), .ZN(n207) );
  NAND2_X1 U282 ( .A1(n297), .A2(n228), .ZN(n292) );
  NOR2_X1 U283 ( .A1(N66), .A2(n298), .ZN(n297) );
  AND2_X1 U284 ( .A1(n299), .A2(N329), .Z(n298) );
  NAND2_X1 U285 ( .A1(n300), .A2(n301), .ZN(N329) );
  NOR2_X1 U286 ( .A1(n302), .A2(n303), .ZN(n301) );
  NAND2_X1 U287 ( .A1(n283), .A2(n275), .ZN(n303) );
  NAND2_X1 U288 ( .A1(n202), .A2(n208), .ZN(n275) );
  INV_X1 U289 ( .I(N99), .ZN(n208) );
  INV_X1 U290 ( .I(n272), .ZN(n202) );
  NAND2_X1 U291 ( .A1(N95), .A2(n304), .ZN(n272) );
  NAND2_X1 U292 ( .A1(N89), .A2(N223), .ZN(n304) );
  NAND2_X1 U293 ( .A1(n223), .A2(n226), .ZN(n283) );
  INV_X1 U294 ( .I(N21), .ZN(n226) );
  AND2_X1 U295 ( .A1(N17), .A2(n305), .Z(n223) );
  NAND2_X1 U296 ( .A1(N11), .A2(N223), .ZN(n305) );
  NAND2_X1 U297 ( .A1(n306), .A2(n307), .ZN(n302) );
  INV_X1 U298 ( .I(n257), .ZN(n307) );
  NOR2_X1 U299 ( .A1(N112), .A2(n255), .ZN(n257) );
  NAND2_X1 U300 ( .A1(N108), .A2(n308), .ZN(n255) );
  NAND2_X1 U301 ( .A1(N102), .A2(N223), .ZN(n308) );
  NOR2_X1 U302 ( .A1(n271), .A2(n296), .ZN(n306) );
  AND2_X1 U303 ( .A1(n216), .A2(n219), .Z(n296) );
  INV_X1 U304 ( .I(N73), .ZN(n219) );
  AND2_X1 U305 ( .A1(N69), .A2(n309), .Z(n216) );
  NAND2_X1 U306 ( .A1(N63), .A2(N223), .ZN(n309) );
  NOR2_X1 U307 ( .A1(n211), .A2(N86), .ZN(n271) );
  NAND2_X1 U308 ( .A1(N82), .A2(n310), .ZN(n211) );
  NAND2_X1 U309 ( .A1(N76), .A2(N223), .ZN(n310) );
  NOR2_X1 U310 ( .A1(n311), .A2(n312), .ZN(n300) );
  NAND2_X1 U311 ( .A1(n313), .A2(n314), .ZN(n312) );
  INV_X1 U312 ( .I(n187), .ZN(n314) );
  NOR2_X1 U313 ( .A1(n188), .A2(N47), .ZN(n187) );
  NAND2_X1 U314 ( .A1(N43), .A2(n315), .ZN(n188) );
  NAND2_X1 U315 ( .A1(N37), .A2(N223), .ZN(n315) );
  NAND2_X1 U316 ( .A1(n316), .A2(N4), .ZN(n313) );
  NOR2_X1 U317 ( .A1(N8), .A2(n264), .ZN(n316) );
  INV_X1 U318 ( .I(n246), .ZN(n264) );
  NAND2_X1 U319 ( .A1(N1), .A2(N223), .ZN(n246) );
  NAND2_X1 U320 ( .A1(n299), .A2(n291), .ZN(n311) );
  NAND2_X1 U321 ( .A1(n317), .A2(N30), .ZN(n291) );
  NOR2_X1 U322 ( .A1(N34), .A2(n238), .ZN(n317) );
  NOR2_X1 U323 ( .A1(n286), .A2(n318), .ZN(n238) );
  INV_X1 U324 ( .I(N223), .ZN(n286) );
  NAND2_X1 U325 ( .A1(n228), .A2(n231), .ZN(n299) );
  INV_X1 U326 ( .I(N60), .ZN(n231) );
  AND2_X1 U327 ( .A1(N56), .A2(n319), .Z(n228) );
  NAND2_X1 U328 ( .A1(N50), .A2(N223), .ZN(n319) );
  NAND2_X1 U329 ( .A1(n320), .A2(n321), .ZN(N223) );
  NOR2_X1 U330 ( .A1(n322), .A2(n323), .ZN(n321) );
  NAND2_X1 U331 ( .A1(n324), .A2(n325), .ZN(n323) );
  NAND2_X1 U332 ( .A1(N17), .A2(n287), .ZN(n325) );
  INV_X1 U333 ( .I(N11), .ZN(n287) );
  NAND2_X1 U334 ( .A1(N43), .A2(n326), .ZN(n324) );
  INV_X1 U335 ( .I(N37), .ZN(n326) );
  NAND2_X1 U336 ( .A1(n327), .A2(n328), .ZN(n322) );
  NAND2_X1 U337 ( .A1(N108), .A2(n329), .ZN(n328) );
  INV_X1 U338 ( .I(N102), .ZN(n329) );
  NOR2_X1 U339 ( .A1(n318), .A2(n330), .ZN(n327) );
  NOR2_X1 U340 ( .A1(N1), .A2(n266), .ZN(n330) );
  INV_X1 U341 ( .I(N4), .ZN(n266) );
  NOR2_X1 U342 ( .A1(N24), .A2(n241), .ZN(n318) );
  INV_X1 U343 ( .I(N30), .ZN(n241) );
  NOR2_X1 U344 ( .A1(n331), .A2(n332), .ZN(n320) );
  NAND2_X1 U345 ( .A1(n333), .A2(n334), .ZN(n332) );
  NAND2_X1 U346 ( .A1(N82), .A2(n335), .ZN(n334) );
  INV_X1 U347 ( .I(N76), .ZN(n335) );
  NAND2_X1 U348 ( .A1(N95), .A2(n336), .ZN(n333) );
  INV_X1 U349 ( .I(N89), .ZN(n336) );
  NAND2_X1 U350 ( .A1(n337), .A2(n338), .ZN(n331) );
  NAND2_X1 U351 ( .A1(N56), .A2(n339), .ZN(n338) );
  INV_X1 U352 ( .I(N50), .ZN(n339) );
  NAND2_X1 U353 ( .A1(N69), .A2(n340), .ZN(n337) );
  INV_X1 U354 ( .I(N63), .ZN(n340) );
endmodule

