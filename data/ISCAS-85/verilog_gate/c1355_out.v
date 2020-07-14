// Benchmark "ISCAS-85/c1355" written by ABC on Sun Jun 21 14:59:19 2020

module \ISCAS-85/c1355  ( 
    G1gat, G8gat, G15gat, G22gat, G29gat, G36gat, G43gat, G50gat, G57gat,
    G64gat, G71gat, G78gat, G85gat, G92gat, G99gat, G106gat, G113gat,
    G120gat, G127gat, G134gat, G141gat, G148gat, G155gat, G162gat, G169gat,
    G176gat, G183gat, G190gat, G197gat, G204gat, G211gat, G218gat, G225gat,
    G226gat, G227gat, G228gat, G229gat, G230gat, G231gat, G232gat, G233gat,
    G1324gat, G1325gat, G1326gat, G1327gat, G1328gat, G1329gat, G1330gat,
    G1331gat, G1332gat, G1333gat, G1334gat, G1335gat, G1336gat, G1337gat,
    G1338gat, G1339gat, G1340gat, G1341gat, G1342gat, G1343gat, G1344gat,
    G1345gat, G1346gat, G1347gat, G1348gat, G1349gat, G1350gat, G1351gat,
    G1352gat, G1353gat, G1354gat, G1355gat  );
  input  G1gat, G8gat, G15gat, G22gat, G29gat, G36gat, G43gat, G50gat,
    G57gat, G64gat, G71gat, G78gat, G85gat, G92gat, G99gat, G106gat,
    G113gat, G120gat, G127gat, G134gat, G141gat, G148gat, G155gat, G162gat,
    G169gat, G176gat, G183gat, G190gat, G197gat, G204gat, G211gat, G218gat,
    G225gat, G226gat, G227gat, G228gat, G229gat, G230gat, G231gat, G232gat,
    G233gat;
  output G1324gat, G1325gat, G1326gat, G1327gat, G1328gat, G1329gat, G1330gat,
    G1331gat, G1332gat, G1333gat, G1334gat, G1335gat, G1336gat, G1337gat,
    G1338gat, G1339gat, G1340gat, G1341gat, G1342gat, G1343gat, G1344gat,
    G1345gat, G1346gat, G1347gat, G1348gat, G1349gat, G1350gat, G1351gat,
    G1352gat, G1353gat, G1354gat, G1355gat;
  wire new_n74_, new_n75_, new_n76_, new_n77_, new_n78_, new_n79_, new_n80_,
    new_n81_, new_n82_, new_n83_, new_n84_, new_n85_, new_n86_, new_n87_,
    new_n88_, new_n89_, new_n90_, new_n91_, new_n92_, new_n93_, new_n94_,
    new_n95_, new_n96_, new_n97_, new_n98_, new_n99_, new_n100_, new_n101_,
    new_n102_, new_n103_, new_n104_, new_n105_, new_n106_, new_n107_,
    new_n108_, new_n109_, new_n110_, new_n111_, new_n112_, new_n113_,
    new_n114_, new_n115_, new_n116_, new_n117_, new_n118_, new_n119_,
    new_n120_, new_n121_, new_n122_, new_n123_, new_n124_, new_n125_,
    new_n126_, new_n127_, new_n128_, new_n129_, new_n130_, new_n131_,
    new_n132_, new_n133_, new_n134_, new_n135_, new_n136_, new_n137_,
    new_n138_, new_n139_, new_n140_, new_n141_, new_n142_, new_n143_,
    new_n144_, new_n145_, new_n146_, new_n147_, new_n148_, new_n149_,
    new_n150_, new_n151_, new_n152_, new_n153_, new_n154_, new_n155_,
    new_n156_, new_n157_, new_n158_, new_n159_, new_n160_, new_n161_,
    new_n162_, new_n163_, new_n164_, new_n165_, new_n166_, new_n167_,
    new_n168_, new_n169_, new_n170_, new_n171_, new_n172_, new_n173_,
    new_n174_, new_n175_, new_n176_, new_n177_, new_n178_, new_n179_,
    new_n180_, new_n181_, new_n182_, new_n183_, new_n184_, new_n185_,
    new_n187_, new_n188_, new_n190_, new_n191_, new_n192_, new_n194_,
    new_n195_, new_n197_, new_n198_, new_n199_, new_n200_, new_n202_,
    new_n203_, new_n205_, new_n206_, new_n208_, new_n209_, new_n211_,
    new_n212_, new_n213_, new_n214_, new_n215_, new_n216_, new_n217_,
    new_n218_, new_n219_, new_n221_, new_n222_, new_n224_, new_n225_,
    new_n227_, new_n228_, new_n230_, new_n231_, new_n232_, new_n233_,
    new_n235_, new_n236_, new_n238_, new_n240_, new_n242_, new_n243_,
    new_n244_, new_n245_, new_n246_, new_n247_, new_n248_, new_n249_,
    new_n250_, new_n251_, new_n252_, new_n253_, new_n254_, new_n256_,
    new_n257_, new_n259_, new_n260_, new_n261_, new_n263_, new_n264_,
    new_n266_, new_n267_, new_n268_, new_n269_, new_n271_, new_n272_,
    new_n274_, new_n275_, new_n277_, new_n278_, new_n280_, new_n281_,
    new_n282_, new_n283_, new_n285_, new_n286_, new_n288_, new_n289_,
    new_n291_, new_n292_, new_n294_, new_n295_, new_n296_, new_n297_,
    new_n299_, new_n300_, new_n302_, new_n304_;
  inv1   g000(.a(G1gat), .O(new_n74_));
  xor2a  g001(.a(G134gat), .b(G113gat), .O(new_n75_));
  xor2a  g002(.a(G127gat), .b(G120gat), .O(new_n76_));
  xor2a  g003(.a(new_n76_), .b(new_n75_), .O(new_n77_));
  nand2  g004(.a(G233gat), .b(G225gat), .O(new_n78_));
  inv1   g005(.a(new_n78_), .O(new_n79_));
  xor2a  g006(.a(new_n79_), .b(new_n77_), .O(new_n80_));
  xor2a  g007(.a(G162gat), .b(G141gat), .O(new_n81_));
  xor2a  g008(.a(G155gat), .b(G148gat), .O(new_n82_));
  xor2a  g009(.a(new_n82_), .b(new_n81_), .O(new_n83_));
  xor2a  g010(.a(G85gat), .b(G1gat), .O(new_n84_));
  xor2a  g011(.a(G57gat), .b(G29gat), .O(new_n85_));
  xor2a  g012(.a(new_n85_), .b(new_n84_), .O(new_n86_));
  xor2a  g013(.a(new_n86_), .b(new_n83_), .O(new_n87_));
  xor2a  g014(.a(new_n87_), .b(new_n80_), .O(new_n88_));
  inv1   g015(.a(G106gat), .O(new_n89_));
  xor2a  g016(.a(G218gat), .b(G197gat), .O(new_n90_));
  xor2a  g017(.a(G211gat), .b(G204gat), .O(new_n91_));
  xor2a  g018(.a(new_n91_), .b(new_n90_), .O(new_n92_));
  xor2a  g019(.a(new_n92_), .b(G78gat), .O(new_n93_));
  xor2a  g020(.a(new_n93_), .b(new_n89_), .O(new_n94_));
  nand2  g021(.a(G233gat), .b(G228gat), .O(new_n95_));
  xor2a  g022(.a(G50gat), .b(G22gat), .O(new_n96_));
  xor2a  g023(.a(new_n96_), .b(new_n95_), .O(new_n97_));
  xor2a  g024(.a(new_n97_), .b(new_n83_), .O(new_n98_));
  xor2a  g025(.a(new_n98_), .b(new_n94_), .O(new_n99_));
  xor2a  g026(.a(G190gat), .b(G169gat), .O(new_n100_));
  xor2a  g027(.a(G183gat), .b(G176gat), .O(new_n101_));
  xor2a  g028(.a(new_n101_), .b(new_n100_), .O(new_n102_));
  xor2a  g029(.a(new_n102_), .b(G71gat), .O(new_n103_));
  xor2a  g030(.a(new_n103_), .b(G99gat), .O(new_n104_));
  nand2  g031(.a(G233gat), .b(G227gat), .O(new_n105_));
  xor2a  g032(.a(G43gat), .b(G15gat), .O(new_n106_));
  xnor2a g033(.a(new_n106_), .b(new_n105_), .O(new_n107_));
  xor2a  g034(.a(new_n107_), .b(new_n77_), .O(new_n108_));
  nand2  g035(.a(new_n108_), .b(new_n104_), .O(new_n109_));
  inv1   g036(.a(G99gat), .O(new_n110_));
  xor2a  g037(.a(new_n103_), .b(new_n110_), .O(new_n111_));
  inv1   g038(.a(new_n108_), .O(new_n112_));
  nand2  g039(.a(new_n112_), .b(new_n111_), .O(new_n113_));
  nand2  g040(.a(new_n113_), .b(new_n109_), .O(new_n114_));
  xor2a  g041(.a(new_n114_), .b(new_n99_), .O(new_n115_));
  xor2a  g042(.a(new_n78_), .b(new_n77_), .O(new_n116_));
  xor2a  g043(.a(new_n87_), .b(new_n116_), .O(new_n117_));
  nand2  g044(.a(G233gat), .b(G226gat), .O(new_n118_));
  xor2a  g045(.a(new_n118_), .b(new_n92_), .O(new_n119_));
  xor2a  g046(.a(G92gat), .b(G64gat), .O(new_n120_));
  xor2a  g047(.a(G36gat), .b(G8gat), .O(new_n121_));
  xor2a  g048(.a(new_n121_), .b(new_n120_), .O(new_n122_));
  xor2a  g049(.a(new_n122_), .b(new_n102_), .O(new_n123_));
  xor2a  g050(.a(new_n123_), .b(new_n119_), .O(new_n124_));
  nand2  g051(.a(new_n124_), .b(new_n117_), .O(new_n125_));
  inv1   g052(.a(new_n99_), .O(new_n126_));
  nand2  g053(.a(new_n124_), .b(new_n88_), .O(new_n127_));
  inv1   g054(.a(new_n118_), .O(new_n128_));
  xor2a  g055(.a(new_n128_), .b(new_n92_), .O(new_n129_));
  xor2a  g056(.a(new_n123_), .b(new_n129_), .O(new_n130_));
  nand2  g057(.a(new_n130_), .b(new_n117_), .O(new_n131_));
  aoi22  g058(.a(new_n131_), .b(new_n127_), .c(new_n113_), .d(new_n109_), .O(new_n132_));
  nand2  g059(.a(new_n132_), .b(new_n126_), .O(new_n133_));
  oai21  g060(.a(new_n125_), .b(new_n115_), .c(new_n133_), .O(new_n134_));
  nand2  g061(.a(G233gat), .b(G229gat), .O(new_n135_));
  inv1   g062(.a(new_n135_), .O(new_n136_));
  xor2a  g063(.a(G50gat), .b(G29gat), .O(new_n137_));
  xor2a  g064(.a(G43gat), .b(G36gat), .O(new_n138_));
  xor2a  g065(.a(new_n138_), .b(new_n137_), .O(new_n139_));
  xor2a  g066(.a(new_n139_), .b(new_n136_), .O(new_n140_));
  xor2a  g067(.a(G22gat), .b(G1gat), .O(new_n141_));
  xor2a  g068(.a(G15gat), .b(G8gat), .O(new_n142_));
  xor2a  g069(.a(new_n142_), .b(new_n141_), .O(new_n143_));
  xor2a  g070(.a(G197gat), .b(G169gat), .O(new_n144_));
  xor2a  g071(.a(G141gat), .b(G113gat), .O(new_n145_));
  xor2a  g072(.a(new_n145_), .b(new_n144_), .O(new_n146_));
  xor2a  g073(.a(new_n146_), .b(new_n143_), .O(new_n147_));
  xor2a  g074(.a(new_n147_), .b(new_n140_), .O(new_n148_));
  nand2  g075(.a(G233gat), .b(G230gat), .O(new_n149_));
  xor2a  g076(.a(G106gat), .b(G85gat), .O(new_n150_));
  xor2a  g077(.a(G99gat), .b(G92gat), .O(new_n151_));
  xor2a  g078(.a(new_n151_), .b(new_n150_), .O(new_n152_));
  xor2a  g079(.a(new_n152_), .b(new_n149_), .O(new_n153_));
  xor2a  g080(.a(G78gat), .b(G57gat), .O(new_n154_));
  xor2a  g081(.a(G71gat), .b(G64gat), .O(new_n155_));
  xor2a  g082(.a(new_n155_), .b(new_n154_), .O(new_n156_));
  xor2a  g083(.a(G204gat), .b(G176gat), .O(new_n157_));
  xor2a  g084(.a(G148gat), .b(G120gat), .O(new_n158_));
  xor2a  g085(.a(new_n158_), .b(new_n157_), .O(new_n159_));
  xor2a  g086(.a(new_n159_), .b(new_n156_), .O(new_n160_));
  xor2a  g087(.a(new_n160_), .b(new_n153_), .O(new_n161_));
  inv1   g088(.a(G218gat), .O(new_n162_));
  xor2a  g089(.a(new_n152_), .b(G190gat), .O(new_n163_));
  xor2a  g090(.a(new_n163_), .b(new_n162_), .O(new_n164_));
  nand2  g091(.a(G233gat), .b(G232gat), .O(new_n165_));
  xor2a  g092(.a(G162gat), .b(G134gat), .O(new_n166_));
  xor2a  g093(.a(new_n166_), .b(new_n165_), .O(new_n167_));
  xor2a  g094(.a(new_n167_), .b(new_n139_), .O(new_n168_));
  xor2a  g095(.a(new_n168_), .b(new_n164_), .O(new_n169_));
  xor2a  g096(.a(new_n156_), .b(G183gat), .O(new_n170_));
  xor2a  g097(.a(new_n170_), .b(G211gat), .O(new_n171_));
  nand2  g098(.a(G233gat), .b(G231gat), .O(new_n172_));
  xor2a  g099(.a(G155gat), .b(G127gat), .O(new_n173_));
  xnor2a g100(.a(new_n173_), .b(new_n172_), .O(new_n174_));
  xor2a  g101(.a(new_n174_), .b(new_n143_), .O(new_n175_));
  nand2  g102(.a(new_n175_), .b(new_n171_), .O(new_n176_));
  inv1   g103(.a(G211gat), .O(new_n177_));
  xor2a  g104(.a(new_n170_), .b(new_n177_), .O(new_n178_));
  inv1   g105(.a(new_n175_), .O(new_n179_));
  nand2  g106(.a(new_n179_), .b(new_n178_), .O(new_n180_));
  nand2  g107(.a(new_n180_), .b(new_n176_), .O(new_n181_));
  nor2   g108(.a(new_n181_), .b(new_n169_), .O(new_n182_));
  nand3  g109(.a(new_n182_), .b(new_n161_), .c(new_n148_), .O(new_n183_));
  inv1   g110(.a(new_n183_), .O(new_n184_));
  nand3  g111(.a(new_n184_), .b(new_n134_), .c(new_n88_), .O(new_n185_));
  xor2a  g112(.a(new_n185_), .b(new_n74_), .O(G1324gat));
  inv1   g113(.a(G8gat), .O(new_n187_));
  nand3  g114(.a(new_n184_), .b(new_n134_), .c(new_n130_), .O(new_n188_));
  xor2a  g115(.a(new_n188_), .b(new_n187_), .O(G1325gat));
  inv1   g116(.a(G15gat), .O(new_n190_));
  inv1   g117(.a(new_n114_), .O(new_n191_));
  nand3  g118(.a(new_n184_), .b(new_n134_), .c(new_n191_), .O(new_n192_));
  xor2a  g119(.a(new_n192_), .b(new_n190_), .O(G1326gat));
  inv1   g120(.a(G22gat), .O(new_n194_));
  nand3  g121(.a(new_n184_), .b(new_n134_), .c(new_n99_), .O(new_n195_));
  xor2a  g122(.a(new_n195_), .b(new_n194_), .O(G1327gat));
  inv1   g123(.a(G29gat), .O(new_n197_));
  nand4  g124(.a(new_n181_), .b(new_n169_), .c(new_n161_), .d(new_n148_), .O(new_n198_));
  inv1   g125(.a(new_n198_), .O(new_n199_));
  nand3  g126(.a(new_n199_), .b(new_n134_), .c(new_n88_), .O(new_n200_));
  xor2a  g127(.a(new_n200_), .b(new_n197_), .O(G1328gat));
  inv1   g128(.a(G36gat), .O(new_n202_));
  nand3  g129(.a(new_n199_), .b(new_n134_), .c(new_n130_), .O(new_n203_));
  xor2a  g130(.a(new_n203_), .b(new_n202_), .O(G1329gat));
  inv1   g131(.a(G43gat), .O(new_n205_));
  nand3  g132(.a(new_n199_), .b(new_n134_), .c(new_n191_), .O(new_n206_));
  xor2a  g133(.a(new_n206_), .b(new_n205_), .O(G1330gat));
  inv1   g134(.a(G50gat), .O(new_n208_));
  nand3  g135(.a(new_n199_), .b(new_n134_), .c(new_n99_), .O(new_n209_));
  xor2a  g136(.a(new_n209_), .b(new_n208_), .O(G1331gat));
  inv1   g137(.a(G57gat), .O(new_n211_));
  xor2a  g138(.a(new_n139_), .b(new_n135_), .O(new_n212_));
  xor2a  g139(.a(new_n147_), .b(new_n212_), .O(new_n213_));
  inv1   g140(.a(new_n149_), .O(new_n214_));
  xor2a  g141(.a(new_n152_), .b(new_n214_), .O(new_n215_));
  xor2a  g142(.a(new_n160_), .b(new_n215_), .O(new_n216_));
  nand3  g143(.a(new_n182_), .b(new_n216_), .c(new_n213_), .O(new_n217_));
  inv1   g144(.a(new_n217_), .O(new_n218_));
  nand3  g145(.a(new_n218_), .b(new_n134_), .c(new_n88_), .O(new_n219_));
  xor2a  g146(.a(new_n219_), .b(new_n211_), .O(G1332gat));
  inv1   g147(.a(G64gat), .O(new_n221_));
  nand3  g148(.a(new_n218_), .b(new_n134_), .c(new_n130_), .O(new_n222_));
  xor2a  g149(.a(new_n222_), .b(new_n221_), .O(G1333gat));
  inv1   g150(.a(G71gat), .O(new_n224_));
  nand3  g151(.a(new_n218_), .b(new_n134_), .c(new_n191_), .O(new_n225_));
  xor2a  g152(.a(new_n225_), .b(new_n224_), .O(G1334gat));
  inv1   g153(.a(G78gat), .O(new_n227_));
  nand3  g154(.a(new_n218_), .b(new_n134_), .c(new_n99_), .O(new_n228_));
  xor2a  g155(.a(new_n228_), .b(new_n227_), .O(G1335gat));
  inv1   g156(.a(G85gat), .O(new_n230_));
  nand4  g157(.a(new_n181_), .b(new_n169_), .c(new_n216_), .d(new_n213_), .O(new_n231_));
  inv1   g158(.a(new_n231_), .O(new_n232_));
  nand3  g159(.a(new_n232_), .b(new_n134_), .c(new_n88_), .O(new_n233_));
  xor2a  g160(.a(new_n233_), .b(new_n230_), .O(G1336gat));
  inv1   g161(.a(G92gat), .O(new_n235_));
  nand3  g162(.a(new_n232_), .b(new_n134_), .c(new_n130_), .O(new_n236_));
  xor2a  g163(.a(new_n236_), .b(new_n235_), .O(G1337gat));
  nand3  g164(.a(new_n232_), .b(new_n134_), .c(new_n191_), .O(new_n238_));
  xor2a  g165(.a(new_n238_), .b(new_n110_), .O(G1338gat));
  nand3  g166(.a(new_n232_), .b(new_n134_), .c(new_n99_), .O(new_n240_));
  xor2a  g167(.a(new_n240_), .b(new_n89_), .O(G1339gat));
  inv1   g168(.a(G113gat), .O(new_n242_));
  xor2a  g169(.a(new_n181_), .b(new_n169_), .O(new_n243_));
  nand2  g170(.a(new_n161_), .b(new_n213_), .O(new_n244_));
  inv1   g171(.a(new_n169_), .O(new_n245_));
  nand2  g172(.a(new_n161_), .b(new_n148_), .O(new_n246_));
  nand2  g173(.a(new_n216_), .b(new_n213_), .O(new_n247_));
  aoi22  g174(.a(new_n247_), .b(new_n246_), .c(new_n180_), .d(new_n176_), .O(new_n248_));
  nand2  g175(.a(new_n248_), .b(new_n245_), .O(new_n249_));
  oai21  g176(.a(new_n244_), .b(new_n243_), .c(new_n249_), .O(new_n250_));
  nor2   g177(.a(new_n114_), .b(new_n99_), .O(new_n251_));
  nand3  g178(.a(new_n124_), .b(new_n251_), .c(new_n88_), .O(new_n252_));
  inv1   g179(.a(new_n252_), .O(new_n253_));
  nand3  g180(.a(new_n253_), .b(new_n250_), .c(new_n148_), .O(new_n254_));
  xor2a  g181(.a(new_n254_), .b(new_n242_), .O(G1340gat));
  inv1   g182(.a(G120gat), .O(new_n256_));
  nand3  g183(.a(new_n253_), .b(new_n250_), .c(new_n216_), .O(new_n257_));
  xor2a  g184(.a(new_n257_), .b(new_n256_), .O(G1341gat));
  inv1   g185(.a(G127gat), .O(new_n259_));
  inv1   g186(.a(new_n181_), .O(new_n260_));
  nand3  g187(.a(new_n253_), .b(new_n250_), .c(new_n260_), .O(new_n261_));
  xor2a  g188(.a(new_n261_), .b(new_n259_), .O(G1342gat));
  inv1   g189(.a(G134gat), .O(new_n263_));
  nand3  g190(.a(new_n253_), .b(new_n250_), .c(new_n169_), .O(new_n264_));
  xor2a  g191(.a(new_n264_), .b(new_n263_), .O(G1343gat));
  inv1   g192(.a(G141gat), .O(new_n266_));
  nand4  g193(.a(new_n124_), .b(new_n114_), .c(new_n99_), .d(new_n88_), .O(new_n267_));
  inv1   g194(.a(new_n267_), .O(new_n268_));
  nand3  g195(.a(new_n268_), .b(new_n250_), .c(new_n148_), .O(new_n269_));
  xor2a  g196(.a(new_n269_), .b(new_n266_), .O(G1344gat));
  inv1   g197(.a(G148gat), .O(new_n271_));
  nand3  g198(.a(new_n268_), .b(new_n250_), .c(new_n216_), .O(new_n272_));
  xor2a  g199(.a(new_n272_), .b(new_n271_), .O(G1345gat));
  inv1   g200(.a(G155gat), .O(new_n274_));
  nand3  g201(.a(new_n268_), .b(new_n250_), .c(new_n260_), .O(new_n275_));
  xor2a  g202(.a(new_n275_), .b(new_n274_), .O(G1346gat));
  inv1   g203(.a(G162gat), .O(new_n277_));
  nand3  g204(.a(new_n268_), .b(new_n250_), .c(new_n169_), .O(new_n278_));
  xor2a  g205(.a(new_n278_), .b(new_n277_), .O(G1347gat));
  inv1   g206(.a(G169gat), .O(new_n280_));
  nand3  g207(.a(new_n130_), .b(new_n251_), .c(new_n117_), .O(new_n281_));
  inv1   g208(.a(new_n281_), .O(new_n282_));
  nand3  g209(.a(new_n282_), .b(new_n250_), .c(new_n148_), .O(new_n283_));
  xor2a  g210(.a(new_n283_), .b(new_n280_), .O(G1348gat));
  inv1   g211(.a(G176gat), .O(new_n285_));
  nand3  g212(.a(new_n282_), .b(new_n250_), .c(new_n216_), .O(new_n286_));
  xor2a  g213(.a(new_n286_), .b(new_n285_), .O(G1349gat));
  inv1   g214(.a(G183gat), .O(new_n288_));
  nand3  g215(.a(new_n282_), .b(new_n250_), .c(new_n260_), .O(new_n289_));
  xor2a  g216(.a(new_n289_), .b(new_n288_), .O(G1350gat));
  inv1   g217(.a(G190gat), .O(new_n291_));
  nand3  g218(.a(new_n282_), .b(new_n250_), .c(new_n169_), .O(new_n292_));
  xor2a  g219(.a(new_n292_), .b(new_n291_), .O(G1351gat));
  inv1   g220(.a(G197gat), .O(new_n294_));
  nand4  g221(.a(new_n130_), .b(new_n114_), .c(new_n99_), .d(new_n117_), .O(new_n295_));
  inv1   g222(.a(new_n295_), .O(new_n296_));
  nand3  g223(.a(new_n296_), .b(new_n250_), .c(new_n148_), .O(new_n297_));
  xor2a  g224(.a(new_n297_), .b(new_n294_), .O(G1352gat));
  inv1   g225(.a(G204gat), .O(new_n299_));
  nand3  g226(.a(new_n296_), .b(new_n250_), .c(new_n216_), .O(new_n300_));
  xor2a  g227(.a(new_n300_), .b(new_n299_), .O(G1353gat));
  nand3  g228(.a(new_n296_), .b(new_n250_), .c(new_n260_), .O(new_n302_));
  xor2a  g229(.a(new_n302_), .b(new_n177_), .O(G1354gat));
  nand3  g230(.a(new_n296_), .b(new_n250_), .c(new_n169_), .O(new_n304_));
  xor2a  g231(.a(new_n304_), .b(new_n162_), .O(G1355gat));
endmodule


