// Benchmark "ISCAS-85/c499" written by ABC on Sun Jun 21 14:57:33 2020

module \ISCAS-85/c499  ( 
    Gid0, Gid1, Gid2, Gid3, Gid4, Gid5, Gid6, Gid7, Gid8, Gid9, Gid10,
    Gid11, Gid12, Gid13, Gid14, Gid15, Gid16, Gid17, Gid18, Gid19, Gid20,
    Gid21, Gid22, Gid23, Gid24, Gid25, Gid26, Gid27, Gid28, Gid29, Gid30,
    Gid31, Gic0, Gic1, Gic2, Gic3, Gic4, Gic5, Gic6, Gic7, Gr,
    God0, God1, God2, God3, God4, God5, God6, God7, God8, God9, God10,
    God11, God12, God13, God14, God15, God16, God17, God18, God19, God20,
    God21, God22, God23, God24, God25, God26, God27, God28, God29, God30,
    God31  );
  input  Gid0, Gid1, Gid2, Gid3, Gid4, Gid5, Gid6, Gid7, Gid8, Gid9,
    Gid10, Gid11, Gid12, Gid13, Gid14, Gid15, Gid16, Gid17, Gid18, Gid19,
    Gid20, Gid21, Gid22, Gid23, Gid24, Gid25, Gid26, Gid27, Gid28, Gid29,
    Gid30, Gid31, Gic0, Gic1, Gic2, Gic3, Gic4, Gic5, Gic6, Gic7, Gr;
  output God0, God1, God2, God3, God4, God5, God6, God7, God8, God9, God10,
    God11, God12, God13, God14, God15, God16, God17, God18, God19, God20,
    God21, God22, God23, God24, God25, God26, God27, God28, God29, God30,
    God31;
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
    new_n162_, new_n163_, new_n164_, new_n165_, new_n166_, new_n168_,
    new_n169_, new_n171_, new_n172_, new_n173_, new_n175_, new_n176_,
    new_n178_, new_n179_, new_n180_, new_n181_, new_n183_, new_n184_,
    new_n186_, new_n187_, new_n189_, new_n190_, new_n192_, new_n193_,
    new_n194_, new_n196_, new_n198_, new_n200_, new_n202_, new_n203_,
    new_n204_, new_n206_, new_n208_, new_n210_, new_n212_, new_n213_,
    new_n214_, new_n215_, new_n216_, new_n217_, new_n218_, new_n219_,
    new_n220_, new_n221_, new_n222_, new_n224_, new_n225_, new_n227_,
    new_n228_, new_n230_, new_n231_, new_n233_, new_n234_, new_n235_,
    new_n237_, new_n238_, new_n240_, new_n241_, new_n243_, new_n244_,
    new_n246_, new_n247_, new_n248_, new_n250_, new_n251_, new_n253_,
    new_n254_, new_n256_, new_n257_, new_n259_, new_n260_, new_n262_,
    new_n263_, new_n265_, new_n266_, new_n268_, new_n269_;
  inv1   g000(.a(Gid0), .O(new_n74_));
  nand2  g001(.a(Gr), .b(Gic0), .O(new_n75_));
  xor2a  g002(.a(Gid19), .b(Gid16), .O(new_n76_));
  xor2a  g003(.a(Gid18), .b(Gid17), .O(new_n77_));
  xor2a  g004(.a(new_n77_), .b(new_n76_), .O(new_n78_));
  xor2a  g005(.a(new_n78_), .b(new_n75_), .O(new_n79_));
  xor2a  g006(.a(Gid12), .b(Gid0), .O(new_n80_));
  xor2a  g007(.a(Gid8), .b(Gid4), .O(new_n81_));
  xor2a  g008(.a(new_n81_), .b(new_n80_), .O(new_n82_));
  xor2a  g009(.a(Gid23), .b(Gid20), .O(new_n83_));
  xor2a  g010(.a(Gid22), .b(Gid21), .O(new_n84_));
  xor2a  g011(.a(new_n84_), .b(new_n83_), .O(new_n85_));
  xor2a  g012(.a(new_n85_), .b(new_n82_), .O(new_n86_));
  xor2a  g013(.a(new_n86_), .b(new_n79_), .O(new_n87_));
  inv1   g014(.a(new_n87_), .O(new_n88_));
  nand2  g015(.a(Gr), .b(Gic7), .O(new_n89_));
  xor2a  g016(.a(Gid7), .b(Gid4), .O(new_n90_));
  xor2a  g017(.a(Gid6), .b(Gid5), .O(new_n91_));
  xor2a  g018(.a(new_n91_), .b(new_n90_), .O(new_n92_));
  xor2a  g019(.a(new_n92_), .b(new_n89_), .O(new_n93_));
  xor2a  g020(.a(Gid15), .b(Gid12), .O(new_n94_));
  xor2a  g021(.a(Gid14), .b(Gid13), .O(new_n95_));
  xor2a  g022(.a(new_n95_), .b(new_n94_), .O(new_n96_));
  xor2a  g023(.a(Gid31), .b(Gid19), .O(new_n97_));
  xor2a  g024(.a(Gid27), .b(Gid23), .O(new_n98_));
  xor2a  g025(.a(new_n98_), .b(new_n97_), .O(new_n99_));
  xor2a  g026(.a(new_n99_), .b(new_n96_), .O(new_n100_));
  xor2a  g027(.a(new_n100_), .b(new_n93_), .O(new_n101_));
  inv1   g028(.a(new_n101_), .O(new_n102_));
  and2   g029(.a(Gr), .b(Gic6), .O(new_n103_));
  xor2a  g030(.a(Gid3), .b(Gid0), .O(new_n104_));
  xor2a  g031(.a(Gid2), .b(Gid1), .O(new_n105_));
  xor2a  g032(.a(new_n105_), .b(new_n104_), .O(new_n106_));
  xor2a  g033(.a(new_n106_), .b(new_n103_), .O(new_n107_));
  xor2a  g034(.a(Gid11), .b(Gid8), .O(new_n108_));
  xor2a  g035(.a(Gid10), .b(Gid9), .O(new_n109_));
  xor2a  g036(.a(new_n109_), .b(new_n108_), .O(new_n110_));
  xor2a  g037(.a(Gid30), .b(Gid18), .O(new_n111_));
  xor2a  g038(.a(Gid26), .b(Gid22), .O(new_n112_));
  xor2a  g039(.a(new_n112_), .b(new_n111_), .O(new_n113_));
  xor2a  g040(.a(new_n113_), .b(new_n110_), .O(new_n114_));
  xnor2a g041(.a(new_n114_), .b(new_n107_), .O(new_n115_));
  nor2   g042(.a(new_n115_), .b(new_n102_), .O(new_n116_));
  nand2  g043(.a(Gr), .b(Gic4), .O(new_n117_));
  xor2a  g044(.a(new_n117_), .b(new_n92_), .O(new_n118_));
  xor2a  g045(.a(Gid28), .b(Gid16), .O(new_n119_));
  xor2a  g046(.a(Gid24), .b(Gid20), .O(new_n120_));
  xor2a  g047(.a(new_n120_), .b(new_n119_), .O(new_n121_));
  xor2a  g048(.a(new_n121_), .b(new_n106_), .O(new_n122_));
  xor2a  g049(.a(new_n122_), .b(new_n118_), .O(new_n123_));
  and2   g050(.a(Gr), .b(Gic5), .O(new_n124_));
  xor2a  g051(.a(new_n124_), .b(new_n96_), .O(new_n125_));
  xor2a  g052(.a(Gid29), .b(Gid17), .O(new_n126_));
  xor2a  g053(.a(Gid25), .b(Gid21), .O(new_n127_));
  xor2a  g054(.a(new_n127_), .b(new_n126_), .O(new_n128_));
  xor2a  g055(.a(new_n128_), .b(new_n110_), .O(new_n129_));
  xor2a  g056(.a(new_n129_), .b(new_n125_), .O(new_n130_));
  nor2   g057(.a(new_n130_), .b(new_n123_), .O(new_n131_));
  and2   g058(.a(Gr), .b(Gic1), .O(new_n132_));
  xor2a  g059(.a(Gid31), .b(Gid28), .O(new_n133_));
  xor2a  g060(.a(Gid30), .b(Gid29), .O(new_n134_));
  xor2a  g061(.a(new_n134_), .b(new_n133_), .O(new_n135_));
  xor2a  g062(.a(new_n135_), .b(new_n132_), .O(new_n136_));
  xor2a  g063(.a(Gid13), .b(Gid1), .O(new_n137_));
  xor2a  g064(.a(Gid9), .b(Gid5), .O(new_n138_));
  xor2a  g065(.a(new_n138_), .b(new_n137_), .O(new_n139_));
  xor2a  g066(.a(Gid27), .b(Gid24), .O(new_n140_));
  xor2a  g067(.a(Gid26), .b(Gid25), .O(new_n141_));
  xor2a  g068(.a(new_n141_), .b(new_n140_), .O(new_n142_));
  xor2a  g069(.a(new_n142_), .b(new_n139_), .O(new_n143_));
  xor2a  g070(.a(new_n143_), .b(new_n136_), .O(new_n144_));
  xor2a  g071(.a(new_n144_), .b(new_n87_), .O(new_n145_));
  nand2  g072(.a(Gr), .b(Gic2), .O(new_n146_));
  xor2a  g073(.a(new_n146_), .b(new_n78_), .O(new_n147_));
  xor2a  g074(.a(Gid14), .b(Gid2), .O(new_n148_));
  xor2a  g075(.a(Gid10), .b(Gid6), .O(new_n149_));
  xor2a  g076(.a(new_n149_), .b(new_n148_), .O(new_n150_));
  xor2a  g077(.a(new_n150_), .b(new_n142_), .O(new_n151_));
  xor2a  g078(.a(new_n151_), .b(new_n147_), .O(new_n152_));
  and2   g079(.a(Gr), .b(Gic3), .O(new_n153_));
  xor2a  g080(.a(new_n153_), .b(new_n85_), .O(new_n154_));
  xor2a  g081(.a(Gid15), .b(Gid3), .O(new_n155_));
  xor2a  g082(.a(Gid11), .b(Gid7), .O(new_n156_));
  xor2a  g083(.a(new_n156_), .b(new_n155_), .O(new_n157_));
  xor2a  g084(.a(new_n157_), .b(new_n135_), .O(new_n158_));
  xnor2a g085(.a(new_n158_), .b(new_n154_), .O(new_n159_));
  nand2  g086(.a(new_n159_), .b(new_n152_), .O(new_n160_));
  xor2a  g087(.a(new_n158_), .b(new_n154_), .O(new_n161_));
  xor2a  g088(.a(new_n161_), .b(new_n152_), .O(new_n162_));
  xnor2a g089(.a(new_n143_), .b(new_n136_), .O(new_n163_));
  nand2  g090(.a(new_n163_), .b(new_n87_), .O(new_n164_));
  oai22  g091(.a(new_n164_), .b(new_n162_), .c(new_n160_), .d(new_n145_), .O(new_n165_));
  nand4  g092(.a(new_n165_), .b(new_n131_), .c(new_n116_), .d(new_n88_), .O(new_n166_));
  xor2a  g093(.a(new_n166_), .b(new_n74_), .O(God0));
  inv1   g094(.a(Gid1), .O(new_n168_));
  nand4  g095(.a(new_n165_), .b(new_n144_), .c(new_n131_), .d(new_n116_), .O(new_n169_));
  xor2a  g096(.a(new_n169_), .b(new_n168_), .O(God1));
  inv1   g097(.a(Gid2), .O(new_n171_));
  inv1   g098(.a(new_n152_), .O(new_n172_));
  nand4  g099(.a(new_n165_), .b(new_n172_), .c(new_n131_), .d(new_n116_), .O(new_n173_));
  xor2a  g100(.a(new_n173_), .b(new_n171_), .O(God2));
  inv1   g101(.a(Gid3), .O(new_n175_));
  nand4  g102(.a(new_n165_), .b(new_n161_), .c(new_n131_), .d(new_n116_), .O(new_n176_));
  xor2a  g103(.a(new_n176_), .b(new_n175_), .O(God3));
  inv1   g104(.a(Gid4), .O(new_n178_));
  xor2a  g105(.a(new_n114_), .b(new_n107_), .O(new_n179_));
  nor2   g106(.a(new_n179_), .b(new_n101_), .O(new_n180_));
  nand4  g107(.a(new_n180_), .b(new_n165_), .c(new_n131_), .d(new_n88_), .O(new_n181_));
  xor2a  g108(.a(new_n181_), .b(new_n178_), .O(God4));
  inv1   g109(.a(Gid5), .O(new_n183_));
  nand4  g110(.a(new_n180_), .b(new_n165_), .c(new_n144_), .d(new_n131_), .O(new_n184_));
  xor2a  g111(.a(new_n184_), .b(new_n183_), .O(God5));
  inv1   g112(.a(Gid6), .O(new_n186_));
  nand4  g113(.a(new_n180_), .b(new_n165_), .c(new_n172_), .d(new_n131_), .O(new_n187_));
  xor2a  g114(.a(new_n187_), .b(new_n186_), .O(God6));
  inv1   g115(.a(Gid7), .O(new_n189_));
  nand4  g116(.a(new_n180_), .b(new_n165_), .c(new_n161_), .d(new_n131_), .O(new_n190_));
  xor2a  g117(.a(new_n190_), .b(new_n189_), .O(God7));
  nand4  g118(.a(new_n130_), .b(new_n123_), .c(new_n179_), .d(new_n101_), .O(new_n192_));
  inv1   g119(.a(new_n192_), .O(new_n193_));
  nand3  g120(.a(new_n193_), .b(new_n165_), .c(new_n88_), .O(new_n194_));
  xnor2a g121(.a(new_n194_), .b(Gid8), .O(God8));
  nand3  g122(.a(new_n193_), .b(new_n165_), .c(new_n144_), .O(new_n196_));
  xnor2a g123(.a(new_n196_), .b(Gid9), .O(God9));
  nand3  g124(.a(new_n193_), .b(new_n165_), .c(new_n172_), .O(new_n198_));
  xnor2a g125(.a(new_n198_), .b(Gid10), .O(God10));
  nand3  g126(.a(new_n193_), .b(new_n165_), .c(new_n161_), .O(new_n200_));
  xnor2a g127(.a(new_n200_), .b(Gid11), .O(God11));
  nand3  g128(.a(new_n180_), .b(new_n130_), .c(new_n123_), .O(new_n202_));
  inv1   g129(.a(new_n202_), .O(new_n203_));
  nand3  g130(.a(new_n203_), .b(new_n165_), .c(new_n88_), .O(new_n204_));
  xnor2a g131(.a(new_n204_), .b(Gid12), .O(God12));
  nand3  g132(.a(new_n203_), .b(new_n165_), .c(new_n144_), .O(new_n206_));
  xnor2a g133(.a(new_n206_), .b(Gid13), .O(God13));
  nand3  g134(.a(new_n203_), .b(new_n165_), .c(new_n172_), .O(new_n208_));
  xnor2a g135(.a(new_n208_), .b(Gid14), .O(God14));
  nand3  g136(.a(new_n203_), .b(new_n165_), .c(new_n161_), .O(new_n210_));
  xnor2a g137(.a(new_n210_), .b(Gid15), .O(God15));
  inv1   g138(.a(Gid16), .O(new_n212_));
  inv1   g139(.a(new_n123_), .O(new_n213_));
  nor2   g140(.a(new_n144_), .b(new_n87_), .O(new_n214_));
  nor2   g141(.a(new_n161_), .b(new_n152_), .O(new_n215_));
  xor2a  g142(.a(new_n179_), .b(new_n101_), .O(new_n216_));
  xnor2a g143(.a(new_n129_), .b(new_n125_), .O(new_n217_));
  nand2  g144(.a(new_n217_), .b(new_n123_), .O(new_n218_));
  xor2a  g145(.a(new_n130_), .b(new_n123_), .O(new_n219_));
  nand2  g146(.a(new_n115_), .b(new_n101_), .O(new_n220_));
  oai22  g147(.a(new_n220_), .b(new_n219_), .c(new_n218_), .d(new_n216_), .O(new_n221_));
  nand4  g148(.a(new_n221_), .b(new_n215_), .c(new_n214_), .d(new_n213_), .O(new_n222_));
  xor2a  g149(.a(new_n222_), .b(new_n212_), .O(God16));
  inv1   g150(.a(Gid17), .O(new_n224_));
  nand4  g151(.a(new_n221_), .b(new_n215_), .c(new_n214_), .d(new_n130_), .O(new_n225_));
  xor2a  g152(.a(new_n225_), .b(new_n224_), .O(God17));
  inv1   g153(.a(Gid18), .O(new_n227_));
  nand4  g154(.a(new_n221_), .b(new_n215_), .c(new_n214_), .d(new_n179_), .O(new_n228_));
  xor2a  g155(.a(new_n228_), .b(new_n227_), .O(God18));
  inv1   g156(.a(Gid19), .O(new_n230_));
  nand4  g157(.a(new_n221_), .b(new_n215_), .c(new_n214_), .d(new_n102_), .O(new_n231_));
  xor2a  g158(.a(new_n231_), .b(new_n230_), .O(God19));
  inv1   g159(.a(Gid20), .O(new_n233_));
  nor2   g160(.a(new_n159_), .b(new_n172_), .O(new_n234_));
  nand4  g161(.a(new_n221_), .b(new_n234_), .c(new_n214_), .d(new_n213_), .O(new_n235_));
  xor2a  g162(.a(new_n235_), .b(new_n233_), .O(God20));
  inv1   g163(.a(Gid21), .O(new_n237_));
  nand4  g164(.a(new_n221_), .b(new_n234_), .c(new_n214_), .d(new_n130_), .O(new_n238_));
  xor2a  g165(.a(new_n238_), .b(new_n237_), .O(God21));
  inv1   g166(.a(Gid22), .O(new_n240_));
  nand4  g167(.a(new_n221_), .b(new_n234_), .c(new_n214_), .d(new_n179_), .O(new_n241_));
  xor2a  g168(.a(new_n241_), .b(new_n240_), .O(God22));
  inv1   g169(.a(Gid23), .O(new_n243_));
  nand4  g170(.a(new_n221_), .b(new_n234_), .c(new_n214_), .d(new_n102_), .O(new_n244_));
  xor2a  g171(.a(new_n244_), .b(new_n243_), .O(God23));
  inv1   g172(.a(Gid24), .O(new_n246_));
  nor2   g173(.a(new_n163_), .b(new_n88_), .O(new_n247_));
  nand4  g174(.a(new_n221_), .b(new_n215_), .c(new_n247_), .d(new_n213_), .O(new_n248_));
  xor2a  g175(.a(new_n248_), .b(new_n246_), .O(God24));
  inv1   g176(.a(Gid25), .O(new_n250_));
  nand4  g177(.a(new_n221_), .b(new_n215_), .c(new_n247_), .d(new_n130_), .O(new_n251_));
  xor2a  g178(.a(new_n251_), .b(new_n250_), .O(God25));
  inv1   g179(.a(Gid26), .O(new_n253_));
  nand4  g180(.a(new_n221_), .b(new_n215_), .c(new_n247_), .d(new_n179_), .O(new_n254_));
  xor2a  g181(.a(new_n254_), .b(new_n253_), .O(God26));
  inv1   g182(.a(Gid27), .O(new_n256_));
  nand4  g183(.a(new_n221_), .b(new_n215_), .c(new_n247_), .d(new_n102_), .O(new_n257_));
  xor2a  g184(.a(new_n257_), .b(new_n256_), .O(God27));
  inv1   g185(.a(Gid28), .O(new_n259_));
  nand4  g186(.a(new_n221_), .b(new_n234_), .c(new_n247_), .d(new_n213_), .O(new_n260_));
  xor2a  g187(.a(new_n260_), .b(new_n259_), .O(God28));
  inv1   g188(.a(Gid29), .O(new_n262_));
  nand4  g189(.a(new_n221_), .b(new_n234_), .c(new_n247_), .d(new_n130_), .O(new_n263_));
  xor2a  g190(.a(new_n263_), .b(new_n262_), .O(God29));
  inv1   g191(.a(Gid30), .O(new_n265_));
  nand4  g192(.a(new_n221_), .b(new_n234_), .c(new_n247_), .d(new_n179_), .O(new_n266_));
  xor2a  g193(.a(new_n266_), .b(new_n265_), .O(God30));
  inv1   g194(.a(Gid31), .O(new_n268_));
  nand4  g195(.a(new_n221_), .b(new_n234_), .c(new_n247_), .d(new_n102_), .O(new_n269_));
  xor2a  g196(.a(new_n269_), .b(new_n268_), .O(God31));
endmodule


