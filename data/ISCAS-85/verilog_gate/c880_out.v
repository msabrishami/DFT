// Benchmark "ISCAS-85/c880" written by ABC on Sun Jun 21 14:58:40 2020

module \ISCAS-85/c880  ( 
    G1gat, G8gat, G13gat, G17gat, G26gat, G29gat, G36gat, G42gat, G51gat,
    G55gat, G59gat, G68gat, G72gat, G73gat, G74gat, G75gat, G80gat, G85gat,
    G86gat, G87gat, G88gat, G89gat, G90gat, G91gat, G96gat, G101gat,
    G106gat, G111gat, G116gat, G121gat, G126gat, G130gat, G135gat, G138gat,
    G143gat, G146gat, G149gat, G152gat, G153gat, G156gat, G159gat, G165gat,
    G171gat, G177gat, G183gat, G189gat, G195gat, G201gat, G207gat, G210gat,
    G219gat, G228gat, G237gat, G246gat, G255gat, G259gat, G260gat, G261gat,
    G267gat, G268gat,
    G388gat, G389gat, G390gat, G391gat, G418gat, G419gat, G420gat, G421gat,
    G422gat, G423gat, G446gat, G447gat, G448gat, G449gat, G450gat, G767gat,
    G768gat, G850gat, G863gat, G864gat, G865gat, G866gat, G874gat, G878gat,
    G879gat, G880gat  );
  input  G1gat, G8gat, G13gat, G17gat, G26gat, G29gat, G36gat, G42gat,
    G51gat, G55gat, G59gat, G68gat, G72gat, G73gat, G74gat, G75gat, G80gat,
    G85gat, G86gat, G87gat, G88gat, G89gat, G90gat, G91gat, G96gat,
    G101gat, G106gat, G111gat, G116gat, G121gat, G126gat, G130gat, G135gat,
    G138gat, G143gat, G146gat, G149gat, G152gat, G153gat, G156gat, G159gat,
    G165gat, G171gat, G177gat, G183gat, G189gat, G195gat, G201gat, G207gat,
    G210gat, G219gat, G228gat, G237gat, G246gat, G255gat, G259gat, G260gat,
    G261gat, G267gat, G268gat;
  output G388gat, G389gat, G390gat, G391gat, G418gat, G419gat, G420gat,
    G421gat, G422gat, G423gat, G446gat, G447gat, G448gat, G449gat, G450gat,
    G767gat, G768gat, G850gat, G863gat, G864gat, G865gat, G866gat, G874gat,
    G878gat, G879gat, G880gat;
  wire new_n87_, new_n89_, new_n91_, new_n94_, new_n95_, new_n97_, new_n98_,
    new_n103_, new_n104_, new_n105_, new_n108_, new_n110_, new_n111_,
    new_n113_, new_n114_, new_n116_, new_n118_, new_n119_, new_n120_,
    new_n121_, new_n122_, new_n123_, new_n124_, new_n125_, new_n127_,
    new_n128_, new_n129_, new_n130_, new_n131_, new_n132_, new_n133_,
    new_n134_, new_n136_, new_n137_, new_n138_, new_n139_, new_n140_,
    new_n141_, new_n142_, new_n143_, new_n144_, new_n145_, new_n146_,
    new_n147_, new_n148_, new_n149_, new_n150_, new_n151_, new_n152_,
    new_n153_, new_n154_, new_n155_, new_n156_, new_n157_, new_n158_,
    new_n159_, new_n160_, new_n161_, new_n162_, new_n163_, new_n164_,
    new_n165_, new_n166_, new_n167_, new_n168_, new_n169_, new_n170_,
    new_n171_, new_n172_, new_n173_, new_n174_, new_n176_, new_n177_,
    new_n178_, new_n179_, new_n180_, new_n181_, new_n182_, new_n183_,
    new_n184_, new_n185_, new_n186_, new_n187_, new_n188_, new_n189_,
    new_n190_, new_n191_, new_n192_, new_n193_, new_n194_, new_n195_,
    new_n196_, new_n197_, new_n198_, new_n199_, new_n200_, new_n201_,
    new_n202_, new_n203_, new_n204_, new_n205_, new_n206_, new_n207_,
    new_n208_, new_n210_, new_n211_, new_n212_, new_n213_, new_n214_,
    new_n215_, new_n216_, new_n217_, new_n218_, new_n219_, new_n220_,
    new_n221_, new_n222_, new_n223_, new_n224_, new_n225_, new_n227_,
    new_n228_, new_n229_, new_n230_, new_n231_, new_n232_, new_n233_,
    new_n234_, new_n235_, new_n236_, new_n237_, new_n238_, new_n239_,
    new_n241_, new_n242_, new_n243_, new_n244_, new_n245_, new_n246_,
    new_n247_, new_n248_, new_n249_, new_n250_, new_n251_, new_n252_,
    new_n253_, new_n254_, new_n255_, new_n256_, new_n257_, new_n258_,
    new_n259_, new_n260_, new_n261_, new_n262_, new_n263_, new_n264_,
    new_n265_, new_n266_, new_n267_, new_n268_, new_n269_, new_n270_,
    new_n271_, new_n272_, new_n273_, new_n274_, new_n275_, new_n276_,
    new_n277_, new_n278_, new_n279_, new_n280_, new_n282_, new_n283_,
    new_n284_, new_n285_, new_n286_, new_n287_, new_n288_, new_n289_,
    new_n290_, new_n291_, new_n292_, new_n293_, new_n294_, new_n295_,
    new_n297_, new_n298_, new_n299_, new_n300_, new_n301_, new_n302_,
    new_n303_, new_n304_, new_n305_, new_n306_, new_n307_, new_n308_,
    new_n309_, new_n310_, new_n311_, new_n312_, new_n313_, new_n314_,
    new_n315_, new_n316_, new_n317_, new_n319_, new_n320_, new_n321_,
    new_n322_, new_n323_, new_n324_, new_n325_, new_n326_, new_n327_,
    new_n328_, new_n329_, new_n330_, new_n331_, new_n332_, new_n333_,
    new_n335_, new_n336_, new_n337_, new_n338_, new_n339_, new_n340_,
    new_n341_, new_n342_, new_n343_, new_n344_, new_n345_, new_n346_,
    new_n347_;
  nand3  g000(.a(G75gat), .b(G42gat), .c(G29gat), .O(new_n87_));
  inv1   g001(.a(new_n87_), .O(G388gat));
  nand3  g002(.a(G80gat), .b(G36gat), .c(G29gat), .O(new_n89_));
  inv1   g003(.a(new_n89_), .O(G389gat));
  nand3  g004(.a(G42gat), .b(G36gat), .c(G29gat), .O(new_n91_));
  inv1   g005(.a(new_n91_), .O(G390gat));
  and2   g006(.a(G86gat), .b(G85gat), .O(G391gat));
  and2   g007(.a(G8gat), .b(G1gat), .O(new_n94_));
  nand3  g008(.a(new_n94_), .b(G17gat), .c(G13gat), .O(new_n95_));
  inv1   g009(.a(new_n95_), .O(G418gat));
  nand4  g010(.a(G26gat), .b(G17gat), .c(G13gat), .d(G1gat), .O(new_n97_));
  inv1   g011(.a(new_n97_), .O(new_n98_));
  nand2  g012(.a(new_n98_), .b(new_n91_), .O(G419gat));
  nand3  g013(.a(G80gat), .b(G75gat), .c(G59gat), .O(G420gat));
  nand3  g014(.a(G80gat), .b(G59gat), .c(G36gat), .O(G421gat));
  nand3  g015(.a(G59gat), .b(G42gat), .c(G36gat), .O(G422gat));
  inv1   g016(.a(G87gat), .O(new_n103_));
  inv1   g017(.a(G88gat), .O(new_n104_));
  inv1   g018(.a(G90gat), .O(new_n105_));
  aoi21  g019(.a(new_n104_), .b(new_n103_), .c(new_n105_), .O(G423gat));
  nand2  g020(.a(new_n98_), .b(G390gat), .O(G446gat));
  nand3  g021(.a(G51gat), .b(G26gat), .c(G1gat), .O(new_n108_));
  inv1   g022(.a(new_n108_), .O(G447gat));
  nand3  g023(.a(new_n94_), .b(G55gat), .c(G13gat), .O(new_n110_));
  nand2  g024(.a(G68gat), .b(G29gat), .O(new_n111_));
  nor2   g025(.a(new_n111_), .b(new_n110_), .O(G448gat));
  nand2  g026(.a(G68gat), .b(G59gat), .O(new_n113_));
  nor2   g027(.a(new_n113_), .b(new_n110_), .O(new_n114_));
  and2   g028(.a(new_n114_), .b(G74gat), .O(G449gat));
  inv1   g029(.a(G89gat), .O(new_n116_));
  aoi21  g030(.a(new_n104_), .b(new_n103_), .c(new_n116_), .O(G450gat));
  xor2a  g031(.a(G96gat), .b(G91gat), .O(new_n118_));
  xor2a  g032(.a(G126gat), .b(G121gat), .O(new_n119_));
  xor2a  g033(.a(new_n119_), .b(new_n118_), .O(new_n120_));
  xor2a  g034(.a(G116gat), .b(G111gat), .O(new_n121_));
  xor2a  g035(.a(new_n121_), .b(G135gat), .O(new_n122_));
  xor2a  g036(.a(G106gat), .b(G101gat), .O(new_n123_));
  xor2a  g037(.a(new_n123_), .b(G130gat), .O(new_n124_));
  xor2a  g038(.a(new_n124_), .b(new_n122_), .O(new_n125_));
  xor2a  g039(.a(new_n125_), .b(new_n120_), .O(G767gat));
  xor2a  g040(.a(G165gat), .b(G159gat), .O(new_n127_));
  xor2a  g041(.a(G201gat), .b(G195gat), .O(new_n128_));
  xor2a  g042(.a(new_n128_), .b(new_n127_), .O(new_n129_));
  xor2a  g043(.a(G189gat), .b(G183gat), .O(new_n130_));
  xor2a  g044(.a(new_n130_), .b(G207gat), .O(new_n131_));
  xor2a  g045(.a(G177gat), .b(G171gat), .O(new_n132_));
  xor2a  g046(.a(new_n132_), .b(G130gat), .O(new_n133_));
  xor2a  g047(.a(new_n133_), .b(new_n131_), .O(new_n134_));
  xor2a  g048(.a(new_n134_), .b(new_n129_), .O(G768gat));
  inv1   g049(.a(G17gat), .O(new_n136_));
  nand2  g050(.a(G156gat), .b(G59gat), .O(new_n137_));
  nand4  g051(.a(new_n137_), .b(G51gat), .c(G26gat), .d(G1gat), .O(new_n138_));
  oai21  g052(.a(new_n138_), .b(new_n136_), .c(G1gat), .O(new_n139_));
  nand2  g053(.a(new_n139_), .b(G153gat), .O(new_n140_));
  nand3  g054(.a(G75gat), .b(G59gat), .c(G42gat), .O(new_n141_));
  and2   g055(.a(G51gat), .b(G17gat), .O(new_n142_));
  nand3  g056(.a(new_n142_), .b(new_n141_), .c(new_n94_), .O(new_n143_));
  inv1   g057(.a(new_n137_), .O(new_n144_));
  xor2a  g058(.a(G42gat), .b(G17gat), .O(new_n145_));
  nand3  g059(.a(new_n145_), .b(new_n144_), .c(G447gat), .O(new_n146_));
  nand2  g060(.a(new_n146_), .b(new_n143_), .O(new_n147_));
  nand2  g061(.a(new_n147_), .b(G126gat), .O(new_n148_));
  inv1   g062(.a(G268gat), .O(new_n149_));
  nand3  g063(.a(G80gat), .b(G75gat), .c(G29gat), .O(new_n150_));
  nor2   g064(.a(new_n150_), .b(new_n108_), .O(new_n151_));
  nand3  g065(.a(new_n151_), .b(new_n149_), .c(G55gat), .O(new_n152_));
  nand3  g066(.a(new_n152_), .b(new_n148_), .c(new_n140_), .O(new_n153_));
  nand2  g067(.a(new_n153_), .b(G201gat), .O(new_n154_));
  inv1   g068(.a(G201gat), .O(new_n155_));
  nand4  g069(.a(new_n152_), .b(new_n148_), .c(new_n140_), .d(new_n155_), .O(new_n156_));
  nand3  g070(.a(new_n156_), .b(new_n154_), .c(G261gat), .O(new_n157_));
  inv1   g071(.a(G261gat), .O(new_n158_));
  nand2  g072(.a(new_n156_), .b(new_n154_), .O(new_n159_));
  nand2  g073(.a(new_n159_), .b(new_n158_), .O(new_n160_));
  nand3  g074(.a(new_n160_), .b(new_n157_), .c(G219gat), .O(new_n161_));
  inv1   g075(.a(new_n159_), .O(new_n162_));
  nand3  g076(.a(new_n153_), .b(G237gat), .c(G201gat), .O(new_n163_));
  nand2  g077(.a(new_n153_), .b(G246gat), .O(new_n164_));
  nand3  g078(.a(G73gat), .b(G72gat), .c(G42gat), .O(new_n165_));
  inv1   g079(.a(new_n165_), .O(new_n166_));
  nand2  g080(.a(new_n166_), .b(new_n114_), .O(new_n167_));
  inv1   g081(.a(new_n167_), .O(new_n168_));
  nand2  g082(.a(G210gat), .b(G121gat), .O(new_n169_));
  nand2  g083(.a(G267gat), .b(G255gat), .O(new_n170_));
  nand2  g084(.a(new_n170_), .b(new_n169_), .O(new_n171_));
  aoi21  g085(.a(new_n168_), .b(G201gat), .c(new_n171_), .O(new_n172_));
  nand3  g086(.a(new_n172_), .b(new_n164_), .c(new_n163_), .O(new_n173_));
  aoi21  g087(.a(new_n162_), .b(G228gat), .c(new_n173_), .O(new_n174_));
  nand2  g088(.a(new_n174_), .b(new_n161_), .O(G850gat));
  nand2  g089(.a(new_n147_), .b(G111gat), .O(new_n176_));
  nand2  g090(.a(new_n139_), .b(G143gat), .O(new_n177_));
  nand3  g091(.a(new_n177_), .b(new_n176_), .c(new_n152_), .O(new_n178_));
  or2    g092(.a(new_n178_), .b(G183gat), .O(new_n179_));
  nand2  g093(.a(new_n178_), .b(G183gat), .O(new_n180_));
  nand2  g094(.a(new_n180_), .b(new_n179_), .O(new_n181_));
  nand2  g095(.a(new_n156_), .b(G261gat), .O(new_n182_));
  inv1   g096(.a(G189gat), .O(new_n183_));
  nand2  g097(.a(new_n147_), .b(G116gat), .O(new_n184_));
  nand2  g098(.a(new_n139_), .b(G146gat), .O(new_n185_));
  nand4  g099(.a(new_n185_), .b(new_n184_), .c(new_n152_), .d(new_n183_), .O(new_n186_));
  inv1   g100(.a(G195gat), .O(new_n187_));
  nand2  g101(.a(new_n147_), .b(G121gat), .O(new_n188_));
  nand2  g102(.a(new_n139_), .b(G149gat), .O(new_n189_));
  nand4  g103(.a(new_n189_), .b(new_n188_), .c(new_n152_), .d(new_n187_), .O(new_n190_));
  nand2  g104(.a(new_n190_), .b(new_n186_), .O(new_n191_));
  aoi21  g105(.a(new_n182_), .b(new_n154_), .c(new_n191_), .O(new_n192_));
  inv1   g106(.a(new_n186_), .O(new_n193_));
  nand3  g107(.a(new_n185_), .b(new_n184_), .c(new_n152_), .O(new_n194_));
  nand2  g108(.a(new_n194_), .b(G189gat), .O(new_n195_));
  nand3  g109(.a(new_n189_), .b(new_n188_), .c(new_n152_), .O(new_n196_));
  nand2  g110(.a(new_n196_), .b(G195gat), .O(new_n197_));
  oai21  g111(.a(new_n197_), .b(new_n193_), .c(new_n195_), .O(new_n198_));
  nor2   g112(.a(new_n198_), .b(new_n192_), .O(new_n199_));
  nor2   g113(.a(new_n199_), .b(new_n181_), .O(new_n200_));
  nand2  g114(.a(new_n199_), .b(new_n181_), .O(new_n201_));
  nand2  g115(.a(new_n201_), .b(G219gat), .O(new_n202_));
  inv1   g116(.a(new_n181_), .O(new_n203_));
  nand3  g117(.a(new_n178_), .b(G237gat), .c(G183gat), .O(new_n204_));
  nand2  g118(.a(new_n178_), .b(G246gat), .O(new_n205_));
  aoi22  g119(.a(new_n168_), .b(G183gat), .c(G210gat), .d(G106gat), .O(new_n206_));
  nand3  g120(.a(new_n206_), .b(new_n205_), .c(new_n204_), .O(new_n207_));
  aoi21  g121(.a(new_n203_), .b(G228gat), .c(new_n207_), .O(new_n208_));
  oai21  g122(.a(new_n202_), .b(new_n200_), .c(new_n208_), .O(G863gat));
  nand2  g123(.a(new_n195_), .b(new_n186_), .O(new_n210_));
  inv1   g124(.a(new_n210_), .O(new_n211_));
  and2   g125(.a(new_n182_), .b(new_n154_), .O(new_n212_));
  inv1   g126(.a(new_n190_), .O(new_n213_));
  oai21  g127(.a(new_n213_), .b(new_n212_), .c(new_n197_), .O(new_n214_));
  nor2   g128(.a(new_n214_), .b(new_n211_), .O(new_n215_));
  nand2  g129(.a(new_n214_), .b(new_n211_), .O(new_n216_));
  nand2  g130(.a(new_n216_), .b(G219gat), .O(new_n217_));
  nand3  g131(.a(new_n194_), .b(G237gat), .c(G189gat), .O(new_n218_));
  nand2  g132(.a(new_n194_), .b(G246gat), .O(new_n219_));
  nand2  g133(.a(G210gat), .b(G111gat), .O(new_n220_));
  nand2  g134(.a(G259gat), .b(G255gat), .O(new_n221_));
  nand2  g135(.a(new_n221_), .b(new_n220_), .O(new_n222_));
  aoi21  g136(.a(new_n168_), .b(G189gat), .c(new_n222_), .O(new_n223_));
  nand3  g137(.a(new_n223_), .b(new_n219_), .c(new_n218_), .O(new_n224_));
  aoi21  g138(.a(new_n211_), .b(G228gat), .c(new_n224_), .O(new_n225_));
  oai21  g139(.a(new_n217_), .b(new_n215_), .c(new_n225_), .O(G864gat));
  nand2  g140(.a(new_n197_), .b(new_n190_), .O(new_n227_));
  nor2   g141(.a(new_n227_), .b(new_n212_), .O(new_n228_));
  nand2  g142(.a(new_n227_), .b(new_n212_), .O(new_n229_));
  nand2  g143(.a(new_n229_), .b(G219gat), .O(new_n230_));
  inv1   g144(.a(new_n227_), .O(new_n231_));
  nand3  g145(.a(new_n196_), .b(G237gat), .c(G195gat), .O(new_n232_));
  nand2  g146(.a(new_n196_), .b(G246gat), .O(new_n233_));
  nand2  g147(.a(G210gat), .b(G116gat), .O(new_n234_));
  nand2  g148(.a(G260gat), .b(G255gat), .O(new_n235_));
  nand2  g149(.a(new_n235_), .b(new_n234_), .O(new_n236_));
  aoi21  g150(.a(new_n168_), .b(G195gat), .c(new_n236_), .O(new_n237_));
  nand3  g151(.a(new_n237_), .b(new_n233_), .c(new_n232_), .O(new_n238_));
  aoi21  g152(.a(new_n231_), .b(G228gat), .c(new_n238_), .O(new_n239_));
  oai21  g153(.a(new_n230_), .b(new_n228_), .c(new_n239_), .O(G865gat));
  inv1   g154(.a(G55gat), .O(new_n241_));
  nor2   g155(.a(new_n138_), .b(new_n241_), .O(new_n242_));
  nand2  g156(.a(new_n242_), .b(G143gat), .O(new_n243_));
  nand2  g157(.a(G138gat), .b(G8gat), .O(new_n244_));
  nand3  g158(.a(new_n151_), .b(new_n149_), .c(G17gat), .O(new_n245_));
  nand3  g159(.a(new_n245_), .b(new_n244_), .c(new_n243_), .O(new_n246_));
  aoi21  g160(.a(new_n147_), .b(G91gat), .c(new_n246_), .O(new_n247_));
  inv1   g161(.a(new_n247_), .O(new_n248_));
  nand2  g162(.a(new_n248_), .b(G159gat), .O(new_n249_));
  oai21  g163(.a(new_n198_), .b(new_n192_), .c(new_n179_), .O(new_n250_));
  inv1   g164(.a(G165gat), .O(new_n251_));
  nand2  g165(.a(new_n242_), .b(G146gat), .O(new_n252_));
  nand2  g166(.a(G138gat), .b(G51gat), .O(new_n253_));
  nand3  g167(.a(new_n253_), .b(new_n252_), .c(new_n245_), .O(new_n254_));
  aoi21  g168(.a(new_n147_), .b(G96gat), .c(new_n254_), .O(new_n255_));
  nand2  g169(.a(new_n255_), .b(new_n251_), .O(new_n256_));
  inv1   g170(.a(G171gat), .O(new_n257_));
  nand2  g171(.a(new_n242_), .b(G149gat), .O(new_n258_));
  nand2  g172(.a(G138gat), .b(G17gat), .O(new_n259_));
  nand3  g173(.a(new_n259_), .b(new_n258_), .c(new_n245_), .O(new_n260_));
  aoi21  g174(.a(new_n147_), .b(G101gat), .c(new_n260_), .O(new_n261_));
  nand2  g175(.a(new_n261_), .b(new_n257_), .O(new_n262_));
  inv1   g176(.a(G177gat), .O(new_n263_));
  nand2  g177(.a(new_n242_), .b(G153gat), .O(new_n264_));
  nand2  g178(.a(G152gat), .b(G138gat), .O(new_n265_));
  nand3  g179(.a(new_n265_), .b(new_n264_), .c(new_n245_), .O(new_n266_));
  aoi21  g180(.a(new_n147_), .b(G106gat), .c(new_n266_), .O(new_n267_));
  nand2  g181(.a(new_n267_), .b(new_n263_), .O(new_n268_));
  nand3  g182(.a(new_n268_), .b(new_n262_), .c(new_n256_), .O(new_n269_));
  aoi21  g183(.a(new_n250_), .b(new_n180_), .c(new_n269_), .O(new_n270_));
  inv1   g184(.a(new_n256_), .O(new_n271_));
  nor2   g185(.a(new_n255_), .b(new_n251_), .O(new_n272_));
  inv1   g186(.a(new_n272_), .O(new_n273_));
  nor2   g187(.a(new_n261_), .b(new_n257_), .O(new_n274_));
  nor2   g188(.a(new_n267_), .b(new_n263_), .O(new_n275_));
  aoi21  g189(.a(new_n275_), .b(new_n262_), .c(new_n274_), .O(new_n276_));
  oai21  g190(.a(new_n276_), .b(new_n271_), .c(new_n273_), .O(new_n277_));
  inv1   g191(.a(G159gat), .O(new_n278_));
  nand2  g192(.a(new_n247_), .b(new_n278_), .O(new_n279_));
  oai21  g193(.a(new_n277_), .b(new_n270_), .c(new_n279_), .O(new_n280_));
  nand2  g194(.a(new_n280_), .b(new_n249_), .O(G866gat));
  nand2  g195(.a(new_n250_), .b(new_n180_), .O(new_n282_));
  inv1   g196(.a(new_n268_), .O(new_n283_));
  nor2   g197(.a(new_n275_), .b(new_n283_), .O(new_n284_));
  and2   g198(.a(new_n284_), .b(new_n282_), .O(new_n285_));
  oai21  g199(.a(new_n284_), .b(new_n282_), .c(G219gat), .O(new_n286_));
  nand2  g200(.a(new_n284_), .b(G228gat), .O(new_n287_));
  nand2  g201(.a(new_n275_), .b(G237gat), .O(new_n288_));
  nand2  g202(.a(new_n147_), .b(G106gat), .O(new_n289_));
  inv1   g203(.a(new_n266_), .O(new_n290_));
  nand2  g204(.a(new_n290_), .b(new_n289_), .O(new_n291_));
  nand2  g205(.a(new_n291_), .b(G246gat), .O(new_n292_));
  aoi22  g206(.a(new_n168_), .b(G177gat), .c(G210gat), .d(G101gat), .O(new_n293_));
  nand4  g207(.a(new_n293_), .b(new_n292_), .c(new_n288_), .d(new_n287_), .O(new_n294_));
  inv1   g208(.a(new_n294_), .O(new_n295_));
  oai21  g209(.a(new_n286_), .b(new_n285_), .c(new_n295_), .O(G874gat));
  nand2  g210(.a(new_n279_), .b(new_n249_), .O(new_n297_));
  inv1   g211(.a(new_n297_), .O(new_n298_));
  oai21  g212(.a(new_n277_), .b(new_n270_), .c(new_n298_), .O(new_n299_));
  inv1   g213(.a(new_n269_), .O(new_n300_));
  nand2  g214(.a(new_n300_), .b(new_n282_), .O(new_n301_));
  inv1   g215(.a(new_n262_), .O(new_n302_));
  nand2  g216(.a(new_n147_), .b(G101gat), .O(new_n303_));
  inv1   g217(.a(new_n260_), .O(new_n304_));
  nand2  g218(.a(new_n304_), .b(new_n303_), .O(new_n305_));
  nand2  g219(.a(new_n305_), .b(G171gat), .O(new_n306_));
  nand2  g220(.a(new_n291_), .b(G177gat), .O(new_n307_));
  oai21  g221(.a(new_n307_), .b(new_n302_), .c(new_n306_), .O(new_n308_));
  aoi21  g222(.a(new_n308_), .b(new_n256_), .c(new_n272_), .O(new_n309_));
  nand3  g223(.a(new_n297_), .b(new_n309_), .c(new_n301_), .O(new_n310_));
  nand3  g224(.a(new_n310_), .b(new_n299_), .c(G219gat), .O(new_n311_));
  nand2  g225(.a(new_n298_), .b(G228gat), .O(new_n312_));
  nand3  g226(.a(new_n248_), .b(G237gat), .c(G159gat), .O(new_n313_));
  nand2  g227(.a(new_n248_), .b(G246gat), .O(new_n314_));
  aoi22  g228(.a(new_n168_), .b(G159gat), .c(G268gat), .d(G210gat), .O(new_n315_));
  nand4  g229(.a(new_n315_), .b(new_n314_), .c(new_n313_), .d(new_n312_), .O(new_n316_));
  inv1   g230(.a(new_n316_), .O(new_n317_));
  nand2  g231(.a(new_n317_), .b(new_n311_), .O(G878gat));
  nor2   g232(.a(new_n272_), .b(new_n271_), .O(new_n319_));
  inv1   g233(.a(new_n319_), .O(new_n320_));
  nand3  g234(.a(new_n268_), .b(new_n262_), .c(new_n282_), .O(new_n321_));
  nand3  g235(.a(new_n321_), .b(new_n320_), .c(new_n276_), .O(new_n322_));
  nand2  g236(.a(new_n268_), .b(new_n262_), .O(new_n323_));
  aoi21  g237(.a(new_n250_), .b(new_n180_), .c(new_n323_), .O(new_n324_));
  oai21  g238(.a(new_n324_), .b(new_n308_), .c(new_n319_), .O(new_n325_));
  nand3  g239(.a(new_n325_), .b(new_n322_), .c(G219gat), .O(new_n326_));
  nand2  g240(.a(new_n319_), .b(G228gat), .O(new_n327_));
  nand2  g241(.a(new_n272_), .b(G237gat), .O(new_n328_));
  inv1   g242(.a(new_n255_), .O(new_n329_));
  nand2  g243(.a(new_n329_), .b(G246gat), .O(new_n330_));
  aoi22  g244(.a(new_n168_), .b(G165gat), .c(G210gat), .d(G91gat), .O(new_n331_));
  nand4  g245(.a(new_n331_), .b(new_n330_), .c(new_n328_), .d(new_n327_), .O(new_n332_));
  inv1   g246(.a(new_n332_), .O(new_n333_));
  nand2  g247(.a(new_n333_), .b(new_n326_), .O(G879gat));
  nor2   g248(.a(new_n274_), .b(new_n302_), .O(new_n335_));
  inv1   g249(.a(new_n335_), .O(new_n336_));
  nand2  g250(.a(new_n268_), .b(new_n282_), .O(new_n337_));
  nand3  g251(.a(new_n337_), .b(new_n336_), .c(new_n307_), .O(new_n338_));
  aoi21  g252(.a(new_n250_), .b(new_n180_), .c(new_n283_), .O(new_n339_));
  oai21  g253(.a(new_n339_), .b(new_n275_), .c(new_n335_), .O(new_n340_));
  nand3  g254(.a(new_n340_), .b(new_n338_), .c(G219gat), .O(new_n341_));
  nand2  g255(.a(new_n335_), .b(G228gat), .O(new_n342_));
  nand2  g256(.a(new_n274_), .b(G237gat), .O(new_n343_));
  nand2  g257(.a(new_n305_), .b(G246gat), .O(new_n344_));
  aoi22  g258(.a(new_n168_), .b(G171gat), .c(G210gat), .d(G96gat), .O(new_n345_));
  nand4  g259(.a(new_n345_), .b(new_n344_), .c(new_n343_), .d(new_n342_), .O(new_n346_));
  inv1   g260(.a(new_n346_), .O(new_n347_));
  nand2  g261(.a(new_n347_), .b(new_n341_), .O(G880gat));
endmodule


