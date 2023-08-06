
# START: solvable by logic ###############################################

# requires only .solve_globally()
q1 =\
    '....2....' +\
    '83.714.96' +\
    '.6.9.54.8' +\
    '.9.3.1..4' +\
    '.1.4.2..7' +\
    '.75...21.' +\
    '..4...7..' +\
    '...5.7...' +\
    '...196...'
a1 =\
    '549628371' +\
    '832714596' +\
    '761935428' +\
    '298371654' +\
    '613452987' +\
    '475869213' +\
    '154283769' +\
    '986547132' +\
    '327196845'

# requires only .solve_locally(); .solve_globally() doesn't do anything
q2 =\
    '..3....2.' +\
    '...416..5' +\
    '6.8......' +\
    '.2.9.4.6.' +\
    '.6..8..7.' +\
    '.3.2.7.9.' +\
    '......6.4' +\
    '2..841...' +\
    '.5....9..'
a2 =\
    '543798126' +\
    '972416835' +\
    '618352749' +\
    '721934568' +\
    '469185273' +\
    '835267491' +\
    '387529614' +\
    '296841357' +\
    '154673982'

# .solve_by_pairs() not required
q3 =\
    '.....5.8.' +\
    '.2..7..46' +\
    '.5.9..3..' +\
    '.....7..9' +\
    '.4.....6.' +\
    '1..8.....' +\
    '..9..1.7.' +\
    '63..2..1.' +\
    '.7.5.....'
a3 =\
    '316245987' +\
    '928173546' +\
    '457968321' +\
    '863417259' +\
    '745392168' +\
    '192856734' +\
    '589631472' +\
    '634729815' +\
    '271584693'

# .solve_by_pairs() required, 
# but not the line "self.itemsets(candidates_global)" in .solve_by_pairs()
q4 =\
    '3.2....6.' +\
    '...7.81..' +\
    '.........' +\
    '58.4.....' +\
    '.......12' +\
    '...1.....' +\
    '.1....4..' +\
    '6...3....' +\
    '....2....'
a4 =\
    '342519867' +\
    '965748123' +\
    '178263945' +\
    '581472396' +\
    '496385712' +\
    '723196584' +\
    '219657438' +\
    '654831279' +\
    '837924651'

# not only .solve_by_pairs() required, 
# but also the line "self.itemsets(candidates_global)"
# and more than one iteration in while loop
q5 =\
    '...7.....' +\
    '1........' +\
    '...43.2..' +\
    '........6' +\
    '...5.9...' +\
    '......418' +\
    '....81...' +\
    '..2....5.' +\
    '.4....3..'
a5 =\
    '264715839' +\
    '137892645' +\
    '598436271' +\
    '423178596' +\
    '816549723' +\
    '759623418' +\
    '375281964' +\
    '982364157' +\
    '641957382'

q5_1 =\
    '...48..7.' +\
    '.61......' +\
    '.........' +\
    '.5.37....' +\
    '7.......2' +\
    '...6..1..' +\
    '4......5.' +\
    '3...9....' +\
    '......6..'
a5_1 =\
    '539486271' +\
    '861927345' +\
    '274513896' +\
    '652371489' +\
    '713849562' +\
    '948652137' +\
    '427168953' +\
    '386295714' +\
    '195734628' 
q5_2 =\
    '3.....61.' +\
    '...8.2...' +\
    '.........' +\
    '1......72' +\
    '45..6....' +\
    '...3.....' +\
    '.27...5..' +\
    '....1....' +\
    '..8......'
a5_2 =\
    '342579618' +\
    '761842953' +\
    '895136247' +\
    '186954372' +\
    '453267189' +\
    '279381465' +\
    '627498531' +\
    '934715826' +\
    '518623794'

# https://usatoday30.usatoday.com/news/offbeat/2006-11-06-sudoku_x.htm
q5_3 =\
    '85...24..' +\
    '72......9' +\
    '..4......' +\
    '...1.7..2' +\
    '3.5...9..' +\
    '.4.......' +\
    '....8..7.' +\
    '.17......' +\
    '....36.4.'
a5_3 =\
    '859612437' +\
    '723854169' +\
    '164379528' +\
    '986147352' +\
    '375268914' +\
    '241593786' +\
    '432981675' +\
    '617425893' +\
    '598736241'

# (2 ** 2)-by-(2 ** 2) sudoku
q6 =\
    '.3.4' +\
    '....' +\
    '..1.' +\
    '2...'
a6 =\
    '1324' +\
    '4231' +\
    '3412' +\
    '2143'
q_small =\
    '1.3.' +\
    '.2..' +\
    '....' +\
    '...4'
a_small =\
    '1432' +\
    '3241' +\
    '4123' +\
    '2314'

# (4 ** 2)-by-(4 ** 2) sudoku, or hexadoku
q7 =\
    '16F..........EG7' +\
    '..........D3AF8.' +\
    '.......EB5CG....' +\
    '.....G3DA1....C2' +\
    '398.........51BG' +\
    'B.........E6F2A.' +\
    '...C..9A87B2....' +\
    '.A1E.D6C53.....4' +\
    'FB48........17E3' +\
    'C..........8D4..' +\
    '.....1.G3D64....' +\
    '.....38F7C5...29' +\
    'G4DB........29F5' +\
    '.......4..7DE6..' +\
    '......25CG8E7...' +\
    '...2..A19F....38'
a7 =\
    '16FDCA5B48293EG7' +\
    '5CBG9742E6D3AF81' +\
    '732AF81EB5CG4D96' +\
    'E8946G3DA1F7B5C2' +\
    '39862FE7D4AC51BG' +\
    'BD5784G319E6F2AC' +\
    '4FGC159A87B263DE' +\
    '2A1EBD6C53GF9874' +\
    'FB485CD6G29A17E3' +\
    'CG35A279FE18D46B' +\
    'A279E1BG3D648C5F' +\
    'DE61438F7C5BGA29' +\
    'G4DB7EC86A3129F5' +\
    '85C3G9F42B7DE61A' +\
    '91AF3625CG8E7B4D' +\
    '67E2DBA19F45CG38'

# (5 ** 2)-by-(5 ** 2) sudoku, or alphadoku
q8 =\
    '..R.K.BC.T....XW.MN.YGE..' +\
    '......UQ.A.J.LK..CITHW...' +\
    '..T.PH.M..OWQ..Y.....DFS.' +\
    'JG.I.X.YD.MB.....K.....A.' +\
    'YX.....K.O...PC.....J.MRN' +\
    'MV.AC.....KHP......RD.I..' +\
    '..Y....DRW.N..U.TV......H' +\
    '.HUEJM.SB....FA.Y.DO.P.L.' +\
    '.L.F.O.AJ...Y.E..Q.HBT...' +\
    'KNDT...U...COBR.SGF...X.A' +\
    'IT..V.QX..FRK..BO.C.L..DY' +\
    'GD..Q..T..V....X..WK..RHU' +\
    '.BL..N.....TDQ.....U..JK.' +\
    'NCX..BM..Y....J..T..O..GE' +\
    'HO..E.L.FD..AUM..YQ.N..PC' +\
    'R.P...EIQ.CLMT...D...OKVX' +\
    '...CAV.P..U.W...BI.N.E.Q.' +\
    '.U.L.SX.K.NP....GO.WARHC.' +\
    'F......BT.Q..A.KER....U..' +\
    '..M.XU......IJD.....FN.WP' +\
    'VKA.T.....BD...R.E.....FW' +\
    '.M.....L.....OQ.NH.D.U.JR' +\
    '.SBO.....K..EXI..W.YQ.P..' +\
    '...QFEOG..AV.R.I.US......' +\
    '..CDW.TF.MH....O.JG.E.L..'
a8 =\
    'LQRUKFBCPTSAHDXWJMNVYGEIO' +\
    'DFNMORUQSAYJGLKEPCITHWVXB' +\
    'CATBPHNMEJOWQIVYXLRGUDFSK' +\
    'JGEIHXWYDVMBRNFUQKOSPLCAT' +\
    'YXVWSGIKLOTEUPCDHFABJQMRN' +\
    'MVOACTGENXKHPSWLUBJRDFIYQ' +\
    'QPYXBLFDRWGNJMUATVEICKSOH' +\
    'WHUEJMKSBCIQTFANYXDORPGLV' +\
    'SLGFROPAJIDXYVECWQKHBTNUM' +\
    'KNDTIQYUVHLCOBRPSGFMWJXEA' +\
    'ITJSVPQXGUFRKHNBOACELMWDY' +\
    'GDFPQAJTOEVYBCLXMNWKISRHU' +\
    'ABLYMNCWISETDQOGRPHUVXJKF' +\
    'NCXKUBMRHYPISWJVDTLFOAQGE' +\
    'HOWREKLVFDXGAUMSIYQJNBTPC' +\
    'RWPJGYEIQNCLMTBHFDUASOKVX' +\
    'OYKCAVHPMRUFWGSJBIXNTEDQL' +\
    'BUQLDSXJKFNPVEYMGOTWARHCI' +\
    'FISVNWDBTLQOXAHKERPCGYUMJ' +\
    'TEMHXUAOCGRKIJDQVSYLFNBWP' +\
    'VKANTJSHUQBDCYGRLEMPXIOFW' +\
    'EMIGYCVLXPWSFOQTNHBDKUAJR' +\
    'USBOLDRNAKJMEXIFCWVYQHPTG' +\
    'PJHQFEOGWBAVLRTIKUSXMCYND' +\
    'XRCDWITFYMHUNKPOAJGQEVLBS'

# END: solvable by logic #################################################


# START: expected to be solvable by logic ################################

# (5 ** 2)-by-(5 ** 2) sudoku, or alphadoku
q8_1 =\
    'CA....F..WG.D.P..YVOM.T.H' +\
    '..G....K.O.......X.BIEJUQ' +\
    '.BW.X.M.R..T..K.F..UGS.OA' +\
    '...NY.GUI.H...R.QSMC.K...' +\
    'JST..C..E..BMO....W.X.V.Y' +\
    '..PQBYK.C..OJ.MR.UT.F..IG' +\
    '..A..GIH..D..C.....X...PB' +\
    '.OFJCR..D.VW..N...A..HSX.' +\
    '...L....O.AE.I..D......Y.' +\
    '.....X.Q...YPK.FO..SL.N.J' +\
    '....O.S.AQ.XKD..Y.NHW...V' +\
    'QI.D.O..J....T....CVY..R.' +\
    'R.....T..IOAYUCQ..K.....X' +\
    '.V..NHU....F....X..M.G.TO' +\
    'T...SBR.K..HVG.PE.O.N....' +\
    'S.D.AU..TH.MWR...V.Y.....' +\
    '.U......M..S.NA.P....Q...' +\
    '.CQR..E...L..PX.H..ITOYS.' +\
    'NG...D.....I..O..QSE..X..' +\
    'IH..T.CA.SK.EF..M.RJVNL..' +\
    'A.O.L.D....CQY..J..K..PBF' +\
    '...I.PACL.T...E.GWQ.RV...' +\
    'FK.TME..G.W..J..S.U.C.IH.' +\
    'GXCSJN.T.......Y.P....Q..' +\
    'E.N.DSXV..R.A.BO..I....KU'
a8_1 =\
    'CAIEUJFLXWGQDSPKRYVOMBTNH' +\
    'LDGMRANKSOYVCWFHTXPBIEJUQ' +\
    'PBWHXQMYRVNTLEKIFJDUGSCOA' +\
    'OFVNYTGUIBHJXAREQSMCPKWLD' +\
    'JSTKQCHDEPIBMOULAGWNXRVFY' +\
    'HEPQBYKSCNXOJLMRVUTWFDAIG' +\
    'VTAUWGIHFEDRSCQJLNYXOMKPB' +\
    'YOFJCRLPDTVWGBNMIKAQUHSXE' +\
    'XNSLKVJMOUAEFIHGDCBPQWRYT' +\
    'DRMGIXWQBAUYPKTFOEHSLCNVJ' +\
    'ULEBOFSGAQJXKDITYRNHWPMCV' +\
    'QIXDGOPWJMENBTSAUFCVYLHRK' +\
    'RMHFPLTNVIOAYUCQWBKGSJDEX' +\
    'WVKCNHUEYDPFRQLSXIJMAGBTO' +\
    'TJYASBRXKCMHVGWPEDOLNFUQI' +\
    'SPDOAUBFTHQMWRJXNVLYKIEGC' +\
    'KULYEIVOMXCSHNAWPTGDBQFJR' +\
    'MCQRVKEJNGLDUPXBHAFITOYSW' +\
    'NGJWFDYRPLBITVOCKQSEHUXAM' +\
    'IHBXTWCAQSKGEFYUMORJVNLDP' +\
    'AWOVLMDIURSCQYGNJHXKETPBF' +\
    'BYUIHPACLJTKNXEDGWQFRVOMS' +\
    'FKRTMEQBGYWPOJDVSLUACXIHN' +\
    'GXCSJNOTHKFUIMVYBPERDAQWL' +\
    'EQNPDSXVWFRLAHBOCMITJYGKU'

# END: expected to be solvable by logic ##################################


# START: brute force required ############################################

# answer is not unique, but brute force finishes up very early.
q_sta410   =\
    '15764..8.' +\
    '.4.......' +\
    '.329..14.' +\
    '7.41.52..' +\
    '2..86..74' +\
    '....7...1' +\
    '.8..21...' +\
    '...3.4.19' +\
    '...5.682.' 
a_sta410_1 =\
    '157643982' +\
    '649218537' +\
    '832957146' +\
    '764135298' +\
    '215869374' +\
    '398472651' +\
    '983721465' +\
    '526384719' +\
    '471596823'
a_sta410_2 =\
    '157643982' +\
    '946218357' +\
    '832957146' +\
    '764135298' +\
    '213869574' +\
    '598472631' +\
    '389721465' +\
    '625384719' +\
    '471596823'
a_sta410_3 =\
    '157643982' +\
    '948217536' +\
    '632958147' +\
    '764135298' +\
    '215869374' +\
    '893472651' +\
    '389721465' +\
    '526384719' +\
    '471596823'

q_sta410_testing   =\
    '15764..8.' +\
    '84.......' +\
    '.329..14.' +\
    '7.41.52..' +\
    '2..86..74' +\
    '....7...1' +\
    '.8..21...' +\
    '...3.4.19' +\
    '...5.682.' 
a_sta410_4 =\
    '157643982' +\
    '849217536' +\
    '632958147' +\
    '764135298' +\
    '215869374' +\
    '398472651' +\
    '983721465' +\
    '526384719' +\
    '471596823'
a_sta410_5 =\
    '157643982' +\
    '849217635' +\
    '632958147' +\
    '794135268' +\
    '215869374' +\
    '368472591' +\
    '983721456' +\
    '526384719' +\
    '471596823'
a_sta410_6 =\
    '157643982' +\
    '849217635' +\
    '632958147' +\
    '764135298' +\
    '215869374' +\
    '398472561' +\
    '983721456' +\
    '526384719' +\
    '471596823'

# answer is not unique; the other answer includes a4
q4_ver2 =\
    '..2....6.' +\
    '...7.812.' +\
    '...2.....' +\
    '5814.2...' +\
    '.......12' +\
    '.2.1.....' +\
    '21....4..' +\
    '6...3.2..' +\
    '....2....'
a4_ver2 =\
    '132549768' +\
    '459768123' +\
    '768213549' +\
    '581492637' +\
    '946357812' +\
    '327186954' +\
    '213875496' +\
    '674931285' +\
    '895624371'

# https://www.telegraph.co.uk/news/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html
# not sure if the answer is unique; takes a long time to get the answer
q_telegraph =\
    '8........' +\
    '..36.....' +\
    '.7..9.2..' +\
    '.5...7...' +\
    '....457..' +\
    '...1...3.' +\
    '..1....68' +\
    '..85...1.' +\
    '.9....4..'
a_telegraph =\
    '812753649' +\
    '943682175' +\
    '675491283' +\
    '154237896' +\
    '369845721' +\
    '287169534' +\
    '521974368' +\
    '438526917' +\
    '796318452'

# https://www.mirror.co.uk/news/weird-news/worlds-hardest-sudoku-can-you-242294
q_mirror =\
    '..53.....' +\
    '8......2.' +\
    '.7..1.5..' +\
    '4....53..' +\
    '.1..7...6' +\
    '..32...8.' +\
    '.6.5....9' +\
    '..4....3.' +\
    '.....97..' 
a_mirror =\
    '145327698' +\
    '839654127' +\
    '672918543' +\
    '496185372' +\
    '218473956' +\
    '753296481' +\
    '367542819' +\
    '984761235' +\
    '521839764'

# from top95.txt and hardest.txt
q_top95_4 =\
    '48.3.....' +\
    '.......71' +\
    '.2.......' +\
    '7.5....6.' +\
    '...2..8..' +\
    '.........' +\
    '..1.76...' +\
    '3.....4..' +\
    '....5....'
q_top95_5 =\
    '....14...' +\
    '.3....2..' +\
    '.7.......' +\
    '...9...3.' +\
    '6.1......' +\
    '.......8.' +\
    '2.....1.4' +\
    '....5.6..' +\
    '...7.8...'
q_hardest_2 =\
    '..53.....' +\
    '8......2.' +\
    '.7..1.5..' +\
    '4....53..' +\
    '.1..7...6' +\
    '..32...8.' +\
    '.6.5....9' +\
    '..4....3.' +\
    '.....97..'
q_hardest_3 =\
    '12..4....' +\
    '..5.69.1.' +\
    '..9...5..' +\
    '.......7.' +\
    '7...52.9.' +\
    '.3......2' +\
    '.9.6...5.' +\
    '4..9..8.1' +\
    '..3...9.4'

# too few unique numbers given, answer unknown
q_boss =\
    '.....5.8.' +\
    '...6.1.43' +\
    '.........' +\
    '.1.5.....' +\
    '...1.6...' +\
    '3.......5' +\
    '53.....61' +\
    '........4' +\
    '.........'

# END: brute force required ##############################################
