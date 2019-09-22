class SATSdetectionTime:

    def __init__( self ):
        self.default = ''

    def CASE1( self, main ):
        import time
        import os
        import imp
        import json
        import pprint
        import re

        """
        - Construct tests variables
        - GIT ( optional )
            - Checkout ONOS master branch
            - Pull latest ONOS code
        - Building ONOS ( optional )
            - Install ONOS package
            - Build ONOS package
        """

        main.case( "Constructing test variables and building ONOS package" )
        main.step( "Constructing test variables" )
        stepResult = main.FALSE

        # Test variables
        main.testOnDirectory = os.path.dirname( os.getcwd ( ) )
        main.cellName = main.params[ 'ENV' ][ 'cellName' ]
        main.apps = main.params[ 'ENV' ][ 'cellApps' ]
        gitBranch = main.params[ 'GIT' ][ 'branch' ]
        gitPull = main.params[ 'GIT' ][ 'pull' ]
        main.ONOSport = main.params[ 'CTRL' ][ 'port' ]
        main.dependencyPath = main.testOnDirectory + \
                              main.params[ 'DEPENDENCY' ][ 'path' ]
        wrapperFile1 = main.params[ 'DEPENDENCY' ][ 'wrapper1' ]
        wrapperFile2 = main.params[ 'DEPENDENCY' ][ 'wrapper2' ]
        main.topology1 = main.params[ 'DEPENDENCY' ][ 'topology1' ]
        main.topology2 = main.params[ 'DEPENDENCY' ][ 'topology2' ]
        main.topology3 = main.params[ 'DEPENDENCY' ][ 'topology3' ]
        main.topologyMN = main.params[ 'DEPENDENCY' ][ 'topologyMN' ]
        main.dctopo = main.params[ 'DEPENDENCY' ][ 'dctopo' ]
        main.chksumFile1 = main.params[ 'DEPENDENCY' ][ 'chksumFile1' ]
        main.chksumFile2 = main.params[ 'DEPENDENCY' ][ 'chksumFile2' ]
        main.chksumFile3 = main.params[ 'DEPENDENCY' ][ 'chksumFile3' ]
        main.chksumFile4 = main.params[ 'DEPENDENCY' ][ 'chksumFile4' ]
        main.chksumFile5 = main.params[ 'DEPENDENCY' ][ 'chksumFile5' ]
        main.chksumFile6 = main.params[ 'DEPENDENCY' ][ 'chksumFile6' ]
        main.chksumFile7 = main.params[ 'DEPENDENCY' ][ 'chksumFile7' ]
        main.chksumFile8 = main.params[ 'DEPENDENCY' ][ 'chksumFile8' ]
        main.chksumFile9 = main.params[ 'DEPENDENCY' ][ 'chksumFile9' ]
        main.chksumFile10 = main.params[ 'DEPENDENCY' ][ 'chksumFile10' ]
        main.hashFunction = [main.params['DETECTIONPARAMETERS']['hashFunction']]
        main.samplingRatio = [main.params['DETECTIONPARAMETERS']['samplingRatio']]
        main.updateRate = main.params['DETECTIONPARAMETERS']['updateRate'].split(',')
        main.updateSize = main.params['DETECTIONPARAMETERS']['updateSize'].split(',')
        main.assignment = ['static', 'dynamic']
        main.attackerPositions = ['aggregate', 'core']
        main.attackTypes = ['drop', 'inject']
        main.attack = main.params['ATTACK']
        main.attackerHashValue = 0
        main.attacker = main.params[ 'ATTACKER' ]
        main.collusion = main.params[ 'COLLUSION']
        main.colludingSwitch1 = main.params[ 'COLLUDINGSWITCH1']
        main.colludingSwitch2 = main.params[ 'COLLUDINGSWITCH2']
        main.colludingPositions = ['colludingSwitch1_' + main.colludingSwitch1 + '_colludingSwitch2_' + main.colludingSwitch2]
        main.hosts = main.params['HOSTS']
        main.masterChksumFile = main.params[ 'DEPENDENCY' ][ 'masterChksumFile']
        main.lblTrafficPath = main.dependencyPath + main.params['DEPENDENCY']['lblTrafficPath']
        main.thread124Pcap = main.params[ 'DEPENDENCY' ][ 'thread124Pcap' ]
        main.thread6Pcap = main.params[ 'DEPENDENCY' ][ 'thread6Pcap' ]
        main.thread8Pcap = main.params[ 'DEPENDENCY' ][ 'thread8Pcap' ]
        main.path10thread124Pcap = main.params[ 'DEPENDENCY' ][ 'path10thread124Pcap' ]
        main.path10thread6Pcap = main.params[ 'DEPENDENCY' ][ 'path10thread6Pcap' ]
        main.path10thread8Pcap = main.params[ 'DEPENDENCY' ][ 'path10thread8Pcap' ]
        main.maxNodes = int( main.params[ 'SCALE' ][ 'max' ] )
        main.startUpSleep = int( main.params[ 'SLEEP' ][ 'startup' ] )
        main.startMNSleep = int( main.params[ 'SLEEP' ][ 'startMN' ] )
        main.addFlowSleep = int( main.params[ 'SLEEP' ][ 'addFlow' ] )
        main.delFlowSleep = int( main.params[ 'SLEEP' ][ 'delFlow' ] )
        main.activateSleep = int( main.params[ 'SLEEP' ][ 'activate' ] )
        main.deactivateSleep = int( main.params[ 'SLEEP' ][ 'deactivate' ] )
        main.tcpreplaySleep = int( main.params[ 'SLEEP' ][ 'tcpreplay' ] )
        main.debug = main.params['DEBUG']
        main.detectionTimePath = '/home/user/TestON/logs/detectionTimeResults/'
        main.detectionTimeLog = '/home/user/TestON/logs/detectionTimeResults/detectionTime'
        main.detectionTimeJsonFile = '/home/user/TestON/logs/detectionTimeResults/detectionTime.json'
        main.detectionTimeCollusionJsonFile = '/home/user/TestON/logs/detectionTimeResults/detectionTimeCollusion.json'
        # The name of the file that stores the used pcaps is main.pcapFilesUsed.
        main.pcapFilesUsed = main.detectionTimePath + 'pcapFilesUsed'
#        main.swDPID = main.params[ 'TEST' ][ 'swDPID' ]
        main.cellData = {} # for creating cell file
        main.CLIs = []
        main.ONOSip = []
        main.chksums = {}
        main.masterChksums = []
        main.seeds = dict.fromkeys(main.params['SEEDS'], None)
        main.currentSeeds = {}
        main.currentSeedsIndex = -1
        main.seedKeys = {}
        attackList = main.seeds.keys()
        main.injectSeeds = []
        main.currentInjectSeed = None
        main.currentInjectSeedsIndex = -1
        pprint.pprint(attackList)
        # pairwiseSeeds = []
        # hashMutationSeeds = []
        # switchMutationSeeds = []
        for attack in attackList:
            pairwiseSeeds = []
            hashMutationSeeds = []
            switchMutationSeeds = []
            pairwiseSeeds = main.params['SEEDS'][attack]['pairwiseSeeds'].split(',')
            # use the pairwiseSeeds as the seedKeys to obtain the currentSeeds
            main.seedKeys[attack] = main.params['SEEDS'][attack]['pairwiseSeeds'].split(',')
            # main.currentSeedsIndex = 0
            hashMutatorSeeds = main.params['SEEDS'][attack]['hashMutatorSeeds'].split(',')
            switchMutatorSeeds = main.params['SEEDS'][attack]['switchMutatorSeeds'].split(',')
            if attack == 'inject':
                main.injectSeeds = main.params['SEEDS'][attack]['injectSeeds'].split(',')
                main.log.info("injectSeeds is:" + str(main.injectSeeds))
            print pairwiseSeeds, hashMutatorSeeds, switchMutatorSeeds
            if len(pairwiseSeeds) != len(hashMutatorSeeds) != len(switchMutatorSeeds):
                main.log.error("Quantity of seeds are not the same for attack:" + str(attack))
                main.log.error("pairwiseSeeds=" + str(len(pairwiseSeeds)) + ", hashMutationSeeds="\
                               + str(len(hashMutatorSeeds)) + ", switchMutationSeeds=" + str(len(switchMutatorSeeds)))
                main.cleanup()
                main.exit()
            seedDict = dict.fromkeys(pairwiseSeeds, [])
            for i in range(0, len(pairwiseSeeds)):
                seedDict[pairwiseSeeds[i]] = [hashMutatorSeeds[i], switchMutatorSeeds[i]]
            main.seeds[attack] = seedDict

        main.log.info("Main.seeds is:")
        main.log.info(main.seeds)
        # main.log.info("Current seeds follows:")
        # main.attack = 'DROP'
        # if main.currentSeeds == {}:
        #     (key, value) = main.seeds[main.attack].popitem()
        #     main.currentSeeds[key] = value
        #main.chksums = { '0' : [], '1' : [], '2' : [], '3' : [], '4' : [], '5' : [],
        #                               '6' : [], '7' : [], '8' : [], '9' : [] }

        main.debug = True if "on" in main.debug else False

        main.ONOSip = main.ONOSbench.getOnosIps()

        # Assigning ONOS cli handles to a list
        for i in range( 1,  main.maxNodes + 1 ):
            main.CLIs.append( getattr( main, 'ONOScli' + str( 1 ) ) )

        # -- INIT SECTION, ONLY RUNS ONCE -- #
        main.startUp = imp.load_source( wrapperFile1,
                                        main.dependencyPath +
                                        wrapperFile1 +
                                        ".py" )

        main.topo = imp.load_source( wrapperFile2,
                                     main.dependencyPath +
                                     wrapperFile2 +
                                     ".py" )


        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.topology1,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.topology2,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.topology3,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.topologyMN,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.dctopo,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        copyResult = main.Mininet1.scp( main.Mininet1,
                                         main.dependencyPath+main.chksumFile1,
                                         main.Mininet1.home+'/custom/',
                                         direction="to" )

        chksumFiles = [ main.chksumFile1, main.chksumFile2, main.chksumFile3,
                                    main.chksumFile4, main.chksumFile5, main.chksumFile6,
                                    main.chksumFile7, main.chksumFile8, main.chksumFile8,
                                    main.chksumFile9, main.chksumFile10 ]

        key = 0
        for file in chksumFiles:
            chksumFile = main.dependencyPath+file
            chksums = []
            f = open( chksumFile, 'r' )
            for line in f:
                chksums.append( line.rstrip( os.linesep ) )
            f.close()
            main.chksums[ key ] = chksums
            key += 1
        #main.log.info( str( main.chksums ) )
##        for chksums in main.chksums.get( 0 ):
##            chksum = int( chksums ) & 4095
##            main.log.info( "chksum after & is:" + str( chksum ) )
        main.log.info("Create the masterChksum list from the masterChksumFile")
        f = open(main.dependencyPath + main.masterChksumFile, 'r')
        for line in f:
            line = line.strip('\n')
            main.masterChksums.append(line)

        main.log.info( "Create detection time results directory and file" )
        try:
            os.mkdir( main.detectionTimePath )
        except:
            if not os.path.isdir( main.detectionTimePath ):
                raise

        main.log.info( "Verify that the detection time json file exists")
        # Structure of the detection time results
        # {
        #     "0.0046": { <-- Sampling Ratio
        #         "payload": { <-- Hash Function
        #             "dynamic": { <-- Assignment
        #                 "2": { <-- Update Rate
        #                     "2": { <-- Update Size
        #                         "aggregate": { <-- Attacker Position
        #                             "drop": [], <-- Attack Type:detectionResults = [seeds, timeStamp, packetsSent, pcapsUsed]
        #                             "inject": []
        #                         },
        #                         "core": {
        #                             "drop": [],
        #                             "inject": []
        #                         }
        #                     }
        #                 }
        #             }
        #         }
        #     }
        # }
        if main.collusion == 'True':
            main.log.info("Collusion enabled. First check if collusion detection time json file exists.")
            if os.path.isfile(main.detectionTimeCollusionJsonFile) is True:
                main.log.info("Detection time json file for collusion exists")
            else:
                main.log.info("Does not exist! Need to create the collusion detection time json file.")
                attackPositionDict = dict.fromkeys(main.colludingPositions, dict.fromkeys(main.attackTypes, []))
                pprint.pprint(attackPositionDict)
                assignmentDict = dict.fromkeys(['static', 'dynamic'], None)
                for assignment in assignmentDict.keys():
                    if assignment == 'static':
                        assignmentDict[assignment] = attackPositionDict
                    elif assignment == 'dynamic':
                        updateRateDict = dict.fromkeys(main.updateRate,
                                                       dict.fromkeys(main.updateSize, attackPositionDict))
                        assignmentDict[assignment] = updateRateDict
                pprint.pprint(assignmentDict)
                detectionTimeDict = dict.fromkeys(main.samplingRatio, dict.fromkeys(main.hashFunction, assignmentDict))
                pprint.pprint(detectionTimeDict)
                with open(main.detectionTimeCollusionJsonFile, 'w') as fp:
                    json.dump(detectionTimeDict, fp, sort_keys=True, indent=4)
            try:
                fileName = "saveDetectionTimeCollusionResults"
                main.saveDetectionTimeCollusionResults = imp.load_source(fileName,
                                                                main.dependencyPath + fileName + ".py")
                # main.log.info("Test saving the detection time results")
                # detectionResults=["201294-8943",30, "jkfdljlfd"]
                # attackType = 'inject'
                # attackerPosition = 'pos1_of:0000000000000201_pos2_of:0000000000010201'
                # assignmentType = 'static'
                # hashFunction = 'payload'
                # samplingRatio = '0.0139'
                # updateRate = '1'
                # main.saveDetectionTimeCollusionResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio, updateRate=updateRate)
            except Exception as e:
                main.log.exception(e)
                main.cleanup()
                main.exit()
        elif main.collusion == 'False':
            if os.path.isfile(main.detectionTimeJsonFile) is True:
                main.log.info("Detection time json file exists")
            else:
                main.log.info("Need to create the detection time json file.")
                attackPositionDict = dict.fromkeys(main.attackerPositions, dict.fromkeys(main.attackTypes, []))
                pprint.pprint(attackPositionDict)
                assignmentDict = dict.fromkeys(['static', 'dynamic'], None)
                for assignment in assignmentDict.keys():
                    if assignment == 'static':
                        assignmentDict[assignment] = attackPositionDict
                    elif assignment == 'dynamic':
                        updateRateDict = dict.fromkeys(main.updateRate, dict.fromkeys(main.updateSize, attackPositionDict))
                        assignmentDict[assignment] = updateRateDict
                pprint.pprint(assignmentDict)
                detectionTimeDict = dict.fromkeys(main.samplingRatio, dict.fromkeys(main.hashFunction, assignmentDict))
                pprint.pprint(detectionTimeDict)
                with open(main.detectionTimeJsonFile, 'w') as fp:
                    json.dump(detectionTimeDict, fp, sort_keys=True, indent=4)

            try:
                fileName = "saveDetectionTimeResults"
                main.saveDetectionTimeResults = imp.load_source( fileName,
                                                 main.dependencyPath + fileName + ".py" )
                # main.log.info("Test saving the detection time results")
                # detectionResults=["201294-8943",30, "jkfdljlfd"]
                # attackType = 'inject'
                # attackerPosition = 'core'
                # assignmentType = 'dynamic'
                # hashFunction = 'payload'
                # samplingRatio = '0.0046'
                # updateRate = '1'
                # main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio, updateRate=updateRate)
            except Exception as e:
                main.log.exception( e )
                main.cleanup()
                main.exit()
        if os.path.isfile(main.pcapFilesUsed) is True:
            main.log.info("pcapFilesUsed exists")
        else:
            # mode=0664 = -rw-rw-r--
            os.mknod(main.pcapFilesUsed, 0664)
            main.log.info("pcapFilesUsed created.")
        try:
            fileName = "pcapFileHelper"
            main.pcapFileHelper = imp.load_source( fileName,
                                             main.dependencyPath + fileName + ".py" )
        except Exception as e:
            main.log.exception( e )
            main.cleanup()
            main.exit()
        # main.savePcapUsedFiles.save(['jkfd', '1234'])

        try:
            fileName = "updateMirrorAttackFlow"
            main.updateMirrorAttackFlow = imp.load_source( fileName,
                                             main.dependencyPath + fileName + ".py" )
        except Exception as e:
            main.log.exception( e )
            main.cleanup()
            main.exit()
        try:
            fileName = "updateRerouteAttackFlow"
            main.updateRerouteAttackFlow = imp.load_source( fileName,
                                             main.dependencyPath + fileName + ".py" )
        except Exception as e:
            main.log.exception( e )
            main.cleanup()
            main.exit()
        try:
            fileName = "updateModificationAttackFlow"
            main.updateModificationAttackFlow = imp.load_source( fileName,
                                             main.dependencyPath + fileName + ".py" )
        except Exception as e:
            main.log.exception( e )
            main.cleanup()
            main.exit()

        if main.CLIs:
            stepResult = main.TRUE
        else:
            main.log.error( "Did not properly created list of ONOS CLI handle" )
            stepResult = main.FALSE

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully construct " +
                                        "test variables ",
                                 onfail="Failed to construct test variables" )

        if gitPull == 'True':
            main.step( "Building ONOS in " + gitBranch + " branch" )
            onosBuildResult = main.startUp.onosBuild( main, gitBranch )
            stepResult = onosBuildResult
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully compiled " +
                                            "latest ONOS",
                                     onfail="Failed to compile " +
                                            "latest ONOS" )
        else:
            main.log.warn( "Did not pull new code so skipping mvn " +
                           "clean install" )
        # main.log.info("Debugging the usedPcapFileList")
        # lblTrafficPath = main.lblTrafficPath
        # pcapFilesUsedFile = main.pcapFilesUsed
        # orderedList = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath, fromJson=False)
        # main.log.info("Available pcapFiles for the tests cases are:")
        # main.log.info(orderedList)
        # pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(orderedList[0]))
        # print pcapNumber
        # pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath, fromJson=True, seedKey='1')
        # main.log.info("pcapsToUse from json file are:")
        # main.log.info(pcapsToUse)
        # pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath, fromJson=True, seedKey='21')
        # main.log.info(pcapsToUse)

    def CASE2( self, main ):
        """
        - Set up cell
            - Create cell file
            - Set cell file
            - Verify cell file
        - Kill ONOS process
        - Start ONOS process
        - Verify ONOS start up
        - Connect to cli
        """

        main.numCtrls = int( main.maxNodes )

        main.case( "Starting up " + str( main.numCtrls ) +
                   " node(s) ONOS cluster" )

        #kill off all onos processes
        main.log.info( "Safety check, killing all ONOS processes" +
                       " before initiating environment setup" )

        for i in range( main.maxNodes ):
            main.ONOSbench.onosDie( main.ONOSip[ i ] )

        print "NODE COUNT = ", main.numCtrls

        tempOnosIp = []
        for i in range( main.numCtrls ):
            tempOnosIp.append( main.ONOSip[i] )

        main.ONOSbench.createCellFile( main.ONOSbench.ip_address, "temp", main.Mininet1.ip_address, main.apps, tempOnosIp )

        main.step( "Apply local cell to environment" )
        #cellResult = main.ONOSbench.setCell( "temp" )
        cellResult = main.ONOSbench.setCell( "local" )
        # cellResult = main.ONOSbench.setCell( "onos-ats-test" )
        verifyResult = main.ONOSbench.verifyCell()
        stepResult = cellResult and verifyResult
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully applied cell to " + \
                                        "environment",
                                 onfail="Failed to apply cell to environment " )

        time.sleep( main.startUpSleep )
        main.step( "Starting ONOS service" )
        stopResult = main.TRUE
        startResult = main.TRUE
        onosIsUp = main.TRUE

        for i in range( main.numCtrls ):
            onosIsUp = onosIsUp and main.ONOSbench.isup( main.ONOSip[ i ] )
        if onosIsUp == main.TRUE:
            time.sleep( main.startUpSleep + 10 )
            main.log.report( "ONOS instance is up and ready" )
        else:
            main.log.report( "ONOS instance may not be up, stop and " +
                             "start ONOS again " )
            for i in range( main.numCtrls ):
                stopResult = stopResult and \
                        main.ONOSbench.onosStop( main.ONOSip[ i ] )
            for i in range( main.numCtrls ):
                startResult = startResult and \
                        main.ONOSbench.onosStart( main.ONOSip[ i ] )
        stepResult = onosIsUp and stopResult and startResult
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="ONOS service is ready",
                                 onfail="ONOS service did not start properly" )

        main.step( "Start ONOS cli" )
        cliResult = main.TRUE
        for i in range( main.numCtrls ):
            cliResult = cliResult and \
                        main.CLIs[ i ].startOnosCli( main.ONOSip[ i ] )
        stepResult = cliResult
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully start ONOS cli",
                                 onfail="Failed to start ONOS cli" )

    def CASE32( self, main ):
        '''
            Start Mininet with 2switch topology
        '''
        import json

        main.case( "Setup mininet for 2switch topology" )
        main.caseExplanation = "Start mininet with 2switch topology."

        main.step( "Setup Mininet 2 switch Topology" )
        topology = main.Mininet1.home + '/custom/' + main.topology1
        stepResult = main.Mininet1.startNet( topoFile=topology )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully loaded topology",
                                 onfail="Failed to load topology" )

    def CASE320( self, main ):
        '''
            Start Mininet with fat-tree topology
            20 switches.
        '''
        import json
        import time

        main.case( "Setup mininet for fat-tree topology" )
        main.caseExplanation = "Start mininet with fat-tree topology."

        main.step( "Setup Mininet 20 switch fat-tree Topology" )
        topology = main.Mininet1.home + '/custom/' + main.topologyMN
        mnCommand = ' --topo ft,4 --controller=remote,ip=127.0.0.1 --switch=ovs,protocols=OpenFlow13'
        #mnCommand = ' --topo ft,4 --controller=remote --switch=ovs,protocols=OpenFlow13'
        stepResult = main.Mininet1.startNet( topoFile=topology, args='',
                                                                    mnCmd='mn --custom ' + topology + mnCommand )
        main.log.info( "Sleep 10 seconds so that all switches connect to the controller")
        time.sleep ( 10 )
        main.log.info( "Remove any old screen sessions on the Mininet node.")
        main.Mininet1.killScreens()
        main.log.info( "Kill any old tcpreplay sessions on the Mininet node.")
        main.Mininet1.killTcpreplay()
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully loaded topology",
                                 onfail="Failed to load topology" )


    def CASE36( self, main ):
        '''
            Ping hosts (0_0_2<->1_0_2) in Mininet topology
        '''
        import json

        main.case( "Ping hosts across the network to install flows." )
        main.caseExplanation = "Simple ping test between hosts across the network."

        main.step( "First set static ARP entries on the hosts" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.staticArpEntries()

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully set static ARP entries on the hosts",
                                 onfail="Failed to set static ARP entries on the hosts" )

        main.step( "arp the host, so that ONOS discovers the host connect points." )
        hostList = main.hosts.split(',')
        # stepResult = main.Mininet1.arpHost( hostList )
        stepResult = main.Mininet1.arping(srcHost="0_0_2", dstHost="10.1.0.2", ethDevice="0_0_2-eth0")
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )
        stepResult = main.Mininet1.arping(srcHost="1_0_2", dstHost="10.0.0.2", ethDevice="1_0_2-eth0")
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )

        main.step( "Ping test" )
        stepResult = main.Mininet1.pingallHosts( [ '0_0_2','1_0_2' ], "2" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully pinged hosts",
                                 onfail="Failed to ping hosts" )

    def CASE336( self, main ):
        '''
            Ping hosts (0_0_2<->1_0_2) after the rerouting flows
            are installed. This will install the flows for rerouting.
        '''
        import json

        main.case( "Ping hosts across the network to install flows." )
        main.caseExplanation = "Simple ping test between hosts across the network."

        main.step( "arp the host, so that ONOS discovers the host connect points." )
        stepResult = main.Mininet1.arpHost( "0_1_2" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )
        stepResult = main.Mininet1.arpHost( "2_1_2" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )

        main.step( "Ping test" )
        stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

        utilities.assert_equals( expect=main.FALSE,
                                 actual=stepResult,
                                 onpass="Successfully pinged hosts",
                                 onfail="Failed to ping hosts" )
        main.log.info( main.Mininet1.checkFlows( "0_2_1" ) )
        main.log.info( main.Mininet1.checkFlows( "0_1_1" ) )
        main.log.info( main.Mininet1.checkFlows( "0_3_1" ) )

    def CASE3336( self, main ):
        '''
            Ping hosts (0_0_2<->2_0_2) in Mininet topology
        '''
        import time

        main.case( "Ping hosts across the network to install flows." )
        main.caseExplanation = "Simple ping test between hosts across the network."

        main.step( "First set static ARP entries on the hosts" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.staticArpEntries()

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully set static ARP entries on the hosts",
                                 onfail="Failed to set static ARP entries on the hosts" )

        main.step( "arp the host, so that ONOS discovers the host connect points." )
        hostList = main.hosts.split(',')
        # stepResult = main.Mininet1.arpHost( hostList )
        stepResult = main.Mininet1.arping(srcHost="0_0_2", dstHost="10.2.0.2", ethDevice="0_0_2-eth0")
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )

        stepResult = main.Mininet1.arping(srcHost="2_0_2", dstHost="10.0.0.2", ethDevice="2_0_2-eth0")
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )

        main.step( "Ping test" )
        stepResult = main.Mininet1.pingallHosts( [ '0_0_2','2_0_2' ], "2" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully pinged hosts",
                                 onfail="Failed to ping hosts" )

    def CASE35( self, main ):
        '''
            Verify sampling flows are installed on the switches
        '''
        import json

        main.step( "Check flows are in the switches" )

        # main.log.info( "Get the flows from every switch in the network" )
        # switchList = main.Mininet1.getSwitch()
        # samplesExist = main.Mininet1.checkSamplingFlows( switchList )
        main.step( "Check flows are in the ADDED state" )

        main.log.info( "Get the flows from ONOS" )
        flows = json.loads( main.ONOSrest.flows() )

        stepResult = main.TRUE
        for f in flows:
            if "rest" in f.get("appId"):
                if "ADDED" not in f.get("state"):
                    stepResult = main.FALSE
                    main.log.error( "Flow: %s in state: %s" % (f.get("id"), f.get("state")) )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="All flows are in the ADDED state",
                                 onfail="All flows are NOT in the ADDED state" )

        main.step( "Check flows are in Mininet's flow table" )

        # get the flow IDs that were added
        main.log.info( "Getting the flow IDs from ONOS" )
        flowIds = [ f.get("id") for f in flows ]
        # convert the flowIDs to ints then hex and finally back to strings
        flowIds = [str(hex(int(x))) for x in flowIds]
        main.log.info( "ONOS flow IDs: {}".format(flowIds) )
        switchList = main.Mininet1.getSwitch( )
        main.log.info("Now to check if the flowIds are in Mininet.")
        samplesExist = main.Mininet1.checkFlowId( switchList, flowIds, debug=False )
        print samplesExist
        if samplesExist == main.TRUE:
            main.log.info("Flows from SATS and Mininet match.")
            utilities.assert_equals( expect=main.TRUE,
                                 actual=samplesExist,
                                 onpass="All flows are in mininet",
                                 onfail="All flows are NOT in mininet" )
        else :
            attempts = 1
            samplesExist = main.FALSE
            while samplesExist == main.FALSE and attempts < 10:
                main.log.info( "Try to get them installed by disabling and enabling pair-wise" )
                main.step( "Disable pairAssignment" )
                main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
                cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                                   "pairAssignment", "false" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=cfgResult,
                                         onpass="Successfully disabled pairAssignment",
                                         onfail="Failed to disable pairAssignment" )
                main.step( "Deactivate tsamp." )
                main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
                deactivateResult = main.CLIs[ 0 ].app( "org.onosproject.tsamp", "deactivate" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=deactivateResult,
                                         onpass="Successfully deactivated tsamp",
                                         onfail="Failed to deactivate tsamp" )
                main.step( "Activate tsamp." )
                main.log.info( "Sleep 10 seconds before enabling" )
                time.sleep ( 10 )
                main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
                activateResult = main.CLIs[ 0 ].app( "org.onosproject.tsamp", "activate" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=activateResult,
                                         onpass="Successfully activated tsamp",
                                         onfail="Failed to activate tsamp" )

                main.log.info( "Sleep 10 seconds before enabling" )
                time.sleep ( 10 )
                main.step( "Configure pairAssignment" )
                main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
                cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                                   "pairAssignment", "true" )
                main.log.info( "Sleep for 10s so that the flows are actually installed" )
                time.sleep( main.activateSleep )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=cfgResult,
                                         onpass="Successfully configured pairAssignment",
                                         onfail="Failed to configure pairAssignment" )
                main.log.info( "Now check the flows again" )
                # main.log.info( "Get the flows from every switch in the network" )
                # switchList = main.Mininet1.getSwitch()
                # samplesExist = main.Mininet1.checkSamplingFlows( switchList )
                main.step("Check flows are in the ADDED state")

                main.log.info("Get the flows from ONOS")
                flows = json.loads(main.ONOSrest.flows())

                stepResult = main.TRUE
                for f in flows:
                    if "rest" in f.get("appId"):
                        if "ADDED" not in f.get("state"):
                            stepResult = main.FALSE
                            main.log.error("Flow: %s in state: %s" % (f.get("id"), f.get("state")))

                utilities.assert_equals(expect=main.TRUE,
                                        actual=stepResult,
                                        onpass="All flows are in the ADDED state",
                                        onfail="All flows are NOT in the ADDED state")

                main.step("Check flows are in Mininet's flow table")

                # get the flow IDs that were added
                main.log.info("Getting the flow IDs from ONOS")
                flowIds = [f.get("id") for f in flows]
                # convert the flowIDs to ints then hex and finally back to strings
                flowIds = [str(hex(int(x))) for x in flowIds]
                main.log.info("ONOS flow IDs: {}".format(flowIds))
                switchList = main.Mininet1.getSwitch()

                samplesExist = main.Mininet1.checkFlowId(switchList, flowIds, debug=False)
                attempts += 1

            utilities.assert_equals( expect=main.TRUE,
                                     actual=samplesExist,
                                     onpass="All samplings flows are in the ADDED state",
                                     onfail="All sampling flows are NOT in the ADDED state" )

    def CASE37( self, main ):
        '''
            Verify flows are installed in ONOS and Mininet
        '''
        import json

        main.step( "Check flows are in the ADDED state" )

        main.log.info( "Get the flows from ONOS" )
        flows = json.loads( main.ONOSrest.flows() )

        stepResult = main.TRUE
        for f in flows:
            if "rest" in f.get("appId"):
                if "ADDED" not in f.get("state"):
                    stepResult = main.FALSE
                    main.log.error( "Flow: %s in state: %s" % (f.get("id"), f.get("state")) )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="All flows are in the ADDED state",
                                 onfail="All flows are NOT in the ADDED state" )

        main.step( "Check flows are in Mininet's flow table" )

        # get the flow IDs that were added
        main.log.info( "Getting the flow IDs from ONOS" )
        flowIds = [ f.get("id") for f in flows ]
        # convert the flowIDs to ints then hex and finally back to strings
        flowIds = [str(hex(int(x))) for x in flowIds]
        main.log.info( "ONOS flow IDs: {}".format(flowIds) )
        switchList = main.Mininet1.getSwitch( )

        stepResult = main.Mininet1.checkFlowId( switchList, flowIds, debug=False )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="All flows are in mininet",
                                 onfail="All flows are NOT in mininet" )

    def CASE38( self, main ):
        '''
            Configure a drop rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Configure flow drop rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2" )

        main.log.info( "Configure flow drop rules on switch 0_2_1 and 0_3_1 to emulate a drop attack" )
        stepResult = main.TRUE
        flowRule = "send_flow_rem,table=1,priority=50002,dl_src=00:00:00:00:00:02,actions=DROP"
        stepResult = main.Mininet1.addFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 configured to emulate a drop attack",
                                 onfail="0_2_1, 0_3_1 not configured to emulate a drop attack" )

    def CASE380( self, main ):
        '''
            Delete the drop rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Delete flow drop rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2" )

        main.log.info( "Delete flow drop rules on switch 0_2_1 and 0_3_1 to emulate a drop attack" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_src=00:00:00:00:00:02"
        stepResult = main.Mininet1.delFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 have drop rules deleted to emulate a drop attack",
                                 onfail="0_2_1, 0_3_1 have drop rules not deleted to emulate a drop attack" )

    def CASE39( self, main ):
        '''
            Configure a drop rule on the Core switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Configure flow drop rule on all core switches: 4_1_1, 4_1_2, 4_2_1, 4_2_2" )
        main.log.info( "Configure flow drop rules on switch  4_1_1, 4_1_2, 4_2_1, 4_2_2 to emulate a drop attack" )
        stepResult = main.TRUE
        flowRule = "send_flow_rem,table=1,priority=50002,dl_src=00:00:00:00:00:02,actions=DROP"
        stepResult = main.Mininet1.addFlow( [ "4_1_1",  "4_1_2",  "4_2_1", "4_2_2" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="  4_1_1, 4_1_2, 4_2_1, 4_2_2  configured to emulate a drop attack",
                                 onfail="  4_1_1, 4_1_2, 4_2_1, 4_2_2  not configured to emulate a drop attack" )

    def CASE390( self, main ):
        '''
            Delete the drop rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Delete flow drop rule on switch 4_1_1, 4_1_2, 4_2_1, 4_2_2 for traffic from 0_0_2 to 1_0_2" )
        main.log.info( "Delete flow drop rules on switch 4_1_1, 4_1_2, 4_2_1, 4_2_2 to emulate a drop attack" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_src=00:00:00:00:00:02"
        stepResult = main.Mininet1.delFlow( [ "4_1_1",  "4_1_2",  "4_2_1", "4_2_2" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="4_1_1, 4_1_2, 4_2_1, 4_2_2 have drop rules deleted to emulate a drop attack",
                                 onfail="4_1_1, 4_1_2, 4_2_1, 4_2_2 have drop rules not deleted to emulate a drop attack" )

    def CASE338( self, main ):
        '''
            Mirror attack
            Configure a flow rule on the Aggregate switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that mirrors traffic along the
            same path of the flow. This is the correct injection
            as per discussion with Stefan on Oct 20, 2016. This
            has been modified to inject a differnt hash value
            each time.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2 that modifies the\
                            destination MAC address to mirror traffic to a different host and forward traffic to the original host." )
        main.step( "First get the installed input and output ports for 00:00:00:00:00:02 on switches 0_2_1 and 0_3_1" )
        inputPort0_2_1 = main.Mininet1.getFlowInputPort( "0_2_1" )
        inputPort0_3_1 = main.Mininet1.getFlowInputPort( "0_3_1" )
        outputPort0_2_1 = main.Mininet1.getFlowOutputPort( "0_2_1" )
        outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_1_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_1_1 flushed",
                                 onfail="0_1_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1 flushed",
                                 onfail="0_2_1 not flushed" )

        # main.attackerHashValue = str( random.randint( 0, 4095 ) ) which is 0<=attackerhashValue<=4095
        if main.currentInjectSeedsIndex == -1 and main.currentInjectSeed == None:
            main.log.info("In first inject seed config.")
            main.currentInjectSeedsIndex = 0
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        elif main.currentInjectSeedsIndex > -1 and main.currentInjectSeedsIndex < len(main.injectSeeds):
            main.log.info("In next inject seed config.")
            main.currentInjectSeedsIndex += 1
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        else:
            main.log.error("There are not enough inject seeds in the params file. GOing to use the last configured seed.")
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
            utilities.assert_equals(expect=main.TRUE,
                                    actual=main.FALSE,
                                    onpass="No. of inject seeds in the params file are sufficient.",
                                    onfail="Insufficient inject seeds in the params file.")

        if outputPort0_2_1 != '':
            main.log.info( "Configure flow mirror rule on switches 0_2_1 to mirror traffic to 0_1_1 and forward original traffic" )
            stepResult = main.TRUE
            # flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
            #                         "actions="+ outputPort0_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
            #                         "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit'(" + inputPort0_2_1 + ",0)'"
            # Simply mirror the traffic onto the same output port, this creates a copy of the packet along the same path for the flow.
            # flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
            #            "actions=" + outputPort0_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," + outputPort0_2_1
            flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
                       "actions=" + outputPort0_2_1 + "," + outputPort0_2_1
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that mirrors traffic" )
            # main.step( "arp the host, so that ONOS discovers the host connect points." )
            # stepResult = main.Mininet1.arpHost( ["0_1_2"] )
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully arpinged hosts",
            #                          onfail="Failed to arping hosts" )
            # main.step( "Ping test" )
            # stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )
            #
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully pinged hosts",
            #                          onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "actions=output:" + outputPort0_2_1 + ",output:" + outputPort0_2_1)
            # stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "strip_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "->vlan_vid,output:" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "actions=output:" + outputPort0_2_1 + ",output:" + outputPort0_2_1)
            # stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "strip_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "->vlan_vid,output:" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

        else:
            main.log.info( "Configure flow mirror rule on switches 0_3_1 to mirror traffic to 0_1_1 and forward original traffic" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort0_3_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit:" + inputPort0_3_1
            stepResult = main.Mininet1.addFlow( [ "0_3_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_3_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="0_3_1 not configured to emulate an injection attack that mirrors traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "0_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1", "0_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

    def CASE3380( self, main ):
        '''
            Delete the mirror rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Delete flow mirror rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2" )

        main.log.info( "Delete flow mirror rules on switch 0_2_1 and 0_3_1 to emulate an inject attack" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_type=0x0800,dl_src=00:00:00:00:00:02"
        stepResult = main.Mininet1.delFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 have mirror rules deleted to emulate an inject attack",
                                 onfail="0_2_1, 0_3_1 have mirror rules not deleted to emulate an inject attack" )

    def CASE3021221( self, main ):
        '''
            Collusion Mirror attack
            Normal traffic flows between 0_0_2 and 1_0_2
            via 001,021,411,121,101.
            021 and 221 are colluding switches along with
            host 202.
            0_2_1 mirrors traffic off path towards 2_2_1,
            who then forwards the packets to 2_0_2.
            The mirror flow rule, sends the original packet
            to port3, then rewrites the destination mac address
            and resubmits to port3.
            Ensure that flows for the mirrored traffic have
            already been installed on the required switches.
        '''
        import json
        import random

        main.case( "Configure mirror flow rule on switch 0_2_1 for traffic from 0_0_2 to 1_0_2 that modifies the \
        destination MAC address to mirror traffic to 2_0_2." )
        main.step( "First get the installed input and output ports for 00:00:00:00:00:02 to 00:00:00:02:00:02 on switches 0_2_1 and 0_3_1" )
        inputPort0_2_1 = main.Mininet1.getFlowInputPort( "0_2_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02" )
        inputPort0_3_1 = main.Mininet1.getFlowInputPort( "0_3_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02")
        outputPort0_2_1 = main.Mininet1.getFlowOutputPort( "0_2_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02")
        outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02" )
        forwardingTable = "1"

        # main.attackerHashValue = str( random.randint( 0, 4095 ) ) which is 0<=attackerhashValue<=4095
        if main.currentInjectSeedsIndex == -1 and main.currentInjectSeed == None:
            main.log.info("In first inject seed config.")
            main.currentInjectSeedsIndex = 0
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        elif main.currentInjectSeedsIndex > -1 and main.currentInjectSeedsIndex < len(main.injectSeeds):
            main.log.info("In next inject seed config.")
            main.currentInjectSeedsIndex += 1
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        else:
            main.log.error("There are not enough inject seeds in the params file. GOing to use the last configured seed.")
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
            utilities.assert_equals(expect=main.TRUE,
                                    actual=main.FALSE,
                                    onpass="No. of inject seeds in the params file are sufficient.",
                                    onfail="Insufficient inject seeds in the params file.")

        if outputPort0_2_1 != '':
            main.log.info( "Configure flow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )
            stepResult = main.TRUE
            # flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
            #                         "actions="+ outputPort0_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
            #                         "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit'(" + inputPort0_2_1 + ",0)'"
            # Simply mirror the traffic onto the same output port, this creates a copy of the packet along the same path for the flow.
            # flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
            #            "actions=" + outputPort0_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," + outputPort0_2_1
            flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
                       "actions=" + outputPort0_2_1 + "," + "set_field:00:00:00:02:00:02-\\>dl_dst,resubmit'(" + inputPort0_2_1 + "," + forwardingTable + ")'"
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that mirrors traffic" )
            # main.step( "arp the host, so that ONOS discovers the host connect points." )
            # stepResult = main.Mininet1.arpHost( ["0_1_2"] )
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully arpinged hosts",
            #                          onfail="Failed to arping hosts" )
            # main.step( "Ping test" )
            # stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )
            #
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully pinged hosts",
            #                          onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "actions=output:" + outputPort0_2_1 + ",set_field:00:00:00:02:00:02")
            # stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "strip_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "->vlan_vid,output:" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "actions=output:" + outputPort0_2_1 + ",set_field:00:00:00:02:00:02")
            # stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "strip_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "->vlan_vid,output:" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

            main.log.info( "Now Configure 2_2_1, to only forward traffic." )
            main.step( "Configure 2_2_1 to only forward traffic." )
            main.log.info( "Install a flow rule in table 0 pointing to table1" )
            stepResult = main.TRUE
            flowRule = "table=0,priority=50010,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02,actions=goto_table:1"
            stepResult = main.Mininet1.addFlow( [ "2_2_1"], version="1.3", flowcmd=flowRule )
            main.Mininet1.checkFlows("2_2_1")
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="2_2_1 now only forwards traffic. It does not sample.",
                                     onfail="2_2_1 does not only forward traffic. It samples too, bail!." )
        else:
            main.log.error( "Incorrect switch for testing! Bail!" )
            main.exit()

    def CASE30212210( self, main ):
        '''
            Delete the mirror rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Delete flow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )

        main.log.info( "Delete fflow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02"
        stepResult = main.Mininet1.delFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 have mirror rules deleted to emulate an inject attack",
                                 onfail="0_2_1, 0_3_1 have mirror rules not deleted to emulate an inject attack" )

        main.log.info( "Now Remove 2_2_1 to only forward traffic." )
        main.step( "Remove 2_2_1 to only forward traffic." )

        main.log.info( "Delete a flow rule in table 0 pointing to table1" )
        stepResult = main.TRUE
        flowRule = "table=0,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02"
        stepResult = main.Mininet1.delFlow( [ "2_2_1"], version="1.3", flowcmd=flowRule )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="2_2_1 now samples traffic.",
                                 onfail="2_2_1 does not sample traffic." )

    def CASE3021411221( self, main ):
        '''
            Collusion Mirror attack
            Normal traffic flows between 0_0_2 and 1_0_2
            via 001,021,411,121,101.
            021, 411 and 221 are colluding switches along with
            host 202.
            0_2_1 mirrors traffic off path towards 2_2_1,
            who then forwards the packets to 2_0_2.
            The mirror flow rule, sends the original packet
            to port3, then rewrites the destination mac address
            and resubmits to port3.
            Ensure that flows for the mirrored traffic have
            already been installed on the required switches.
        '''
        import json
        import random

        main.case( "Configure mirror flow rule on switch 0_2_1 for traffic from 0_0_2 to 1_0_2 that modifies the \
        destination MAC address to mirror traffic to 2_0_2." )
        main.step( "First get the installed input and output ports for 00:00:00:00:00:02 to 00:00:00:02:00:02 on switches 0_2_1 and 0_3_1" )
        inputPort0_2_1 = main.Mininet1.getFlowInputPort( "0_2_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02" )
        inputPort0_3_1 = main.Mininet1.getFlowInputPort( "0_3_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02")
        outputPort0_2_1 = main.Mininet1.getFlowOutputPort( "0_2_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02")
        outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1", matchOption="dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02" )
        forwardingTable = "1"

        # main.attackerHashValue = str( random.randint( 0, 4095 ) ) which is 0<=attackerhashValue<=4095
        if main.currentInjectSeedsIndex == -1 and main.currentInjectSeed == None:
            main.log.info("In first inject seed config.")
            main.currentInjectSeedsIndex = 0
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        elif main.currentInjectSeedsIndex > -1 and main.currentInjectSeedsIndex < len(main.injectSeeds):
            main.log.info("In next inject seed config.")
            main.currentInjectSeedsIndex += 1
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        else:
            main.log.error("There are not enough inject seeds in the params file. GOing to use the last configured seed.")
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
            utilities.assert_equals(expect=main.TRUE,
                                    actual=main.FALSE,
                                    onpass="No. of inject seeds in the params file are sufficient.",
                                    onfail="Insufficient inject seeds in the params file.")

        if outputPort0_2_1 != '':
            main.log.info( "Configure flow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )
            stepResult = main.TRUE
            flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
                       "actions=" + outputPort0_2_1 + "," + "set_field:00:00:00:02:00:02-\\>dl_dst,resubmit'(" + inputPort0_2_1 + "," + forwardingTable + ")'"
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that mirrors traffic" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "actions=output:" + outputPort0_2_1 + ",set_field:00:00:00:02:00:02")
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "actions=output:" + outputPort0_2_1 + ",set_field:00:00:00:02:00:02")
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

            main.log.info( "Now Configure 4_1_1, and 2_2_1, to only forward attack traffic." )
            main.step( "Configure 4_1_1, and 2_2_1 to only forward traffic." )
            main.log.info( "Install a flow rule in table 0 pointing to table1" )
            stepResult = main.TRUE
            flowRule = "table=0,priority=50010,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02,actions=goto_table:1"
            stepResult = main.Mininet1.addFlow( ["4_1_1", "2_2_1"], version="1.3", flowcmd=flowRule )
            main.Mininet1.checkFlows("4_1_1")
            main.Mininet1.checkFlows("2_2_1")
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_1, 2_2_1 now only forwards traffic. It does not sample.",
                                     onfail="4_1_1, 2_2_1 does not only forward traffic. It samples too, bail!." )
        else:
            main.log.error( "Incorrect switch for testing! Bail!" )
            main.exit()

    def CASE30214112210( self, main ):
        '''
            Delete the mirror rule on the Aggregate switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Delete flow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )

        main.log.info( "Delete fflow mirror rule on switch 0_2_1 to mirror traffic to switch 2_2_1 and forward original traffic" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02"
        stepResult = main.Mininet1.delFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 have mirror rules deleted to emulate an inject attack",
                                 onfail="0_2_1, 0_3_1 have mirror rules not deleted to emulate an inject attack" )

        main.log.info( "Now Remove 4_1_1, and 2_2_1 to only forward traffic." )
        main.step( "Remove 4_1_1, and 2_2_1 to only forward traffic." )

        main.log.info( "Delete a flow rule in table 0 pointing to table1" )
        stepResult = main.TRUE
        flowRule = "table=0,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02"
        stepResult = main.Mininet1.delFlow( [ "4_1_1", "2_2_1"], version="1.3", flowcmd=flowRule )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="4_1_1, 2_2_1 now samples traffic.",
                                 onfail="4_1_1, 2_2_1 does not sample traffic." )

    def CASE911( self, main ):
        '''
            Have switch 2_2_1, 4_1_1 not sample traffic, only forward.
            This is a debug test case to identify if the impl. of
            collusion is correct or not.
        '''
        import json

        main.step( "Configure 2_2_1, 4_1_1 to only forward traffic." )

        main.log.info( "Install a flow rule in table 0 pointing to table1" )
        stepResult = main.TRUE
        flowRule = "table=0,priority=50010,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02,actions=goto_table:1"
        stepResult = main.Mininet1.addFlow( [ "2_2_1", "4_1_1"], version="1.3", flowcmd=flowRule )
        main.Mininet1.checkFlows("2_2_1")
        main.Mininet1.checkFlows("4_1_1")
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="2_2_1, 4_1_1 now only forwards traffic. It does not sample.",
                                 onfail="2_2_1, 4_1_1 does not only forward traffic. It samples too, bail!." )

    def CASE9110( self, main ):
        '''
            Remove switch 2_2_1, 4_1_1 not sample traffic, only forward.
            This is a debug test case to identify if the impl. of
            collusion is correct or not.
        '''
        import json

        main.step( "Remove 2_2_1, 4_1_1 to only forward traffic." )

        main.log.info( "Delete a flow rule in table 0 pointing to table1" )
        stepResult = main.TRUE
        flowRule = "table=0,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:00:02"
        stepResult = main.Mininet1.delFlow( [ "2_2_1", "4_1_1"], version="1.3", flowcmd=flowRule )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="2_2_1, 4_1_1 now samples traffic.",
                                 onfail="2_2_1, 4_1_1 does not sample traffic." )


    def CASE339( self, main ):
        '''
            Mirror attack
            Configure a flow rule on the Core switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that mirrors traffic along the
            same path of the flow. This is the correct injection
            as per discussion with Stefan on Oct 20, 2016. This
            has been modified to inject a differnt hash value
            each time.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on \
                            The core switch that can be either 4_1_1, 4_1_2, 4_2_1 or 4_2_2.\
                            Modify the destination MAC address to mirror traffic to a different host and forward traffic to the original host." )

        main.step( "First get the installed output ports for 00:00:00:00:00:02 on the core switches 4_1_1, 4_1_2, 4_2_1 or 4_2_2" )
        outputPort4_1_1 = main.Mininet1.getFlowOutputPort( "4_1_1" )
        outputPort4_1_2 = main.Mininet1.getFlowOutputPort( "4_1_2" )
        outputPort4_2_1 = main.Mininet1.getFlowOutputPort( "4_2_1" )
        outputPort4_2_2 = main.Mininet1.getFlowOutputPort( "4_2_2" )
        inputPort4_1_1 = main.Mininet1.getFlowInputPort( "4_1_1" )
        inputPort4_1_2 = main.Mininet1.getFlowInputPort( "4_1_2" )
        inputPort4_2_1 = main.Mininet1.getFlowInputPort( "4_2_1" )
        inputPort4_2_2 = main.Mininet1.getFlowInputPort( "4_2_2" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "2_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="2_2_1 flushed",
                                 onfail="2_2_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "2_3_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="2_3_1 flushed",
                                 onfail="2_3_1 not flushed" )

        # main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if main.currentInjectSeedsIndex == -1 and main.currentInjectSeed == None:
            main.log.info("In first inject seed config.")
            main.currentInjectSeedsIndex = 0
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        elif main.currentInjectSeedsIndex > -1 and main.currentInjectSeedsIndex < len(main.injectSeeds):
            main.log.info("In next inject seed config.")
            main.currentInjectSeedsIndex += 1
            main.currentInjectSeed = main.injectSeeds[main.currentInjectSeedsIndex]
            random.seed(main.currentInjectSeed)
            main.attackerHashValue = str(random.randint(0, 4095))
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
        else:
            main.log.error("There are not enough inject seeds in the params file. GOing to use the last configured seed.")
            main.log.info("main.currentInjectSeed:" + str(main.currentInjectSeed))
            main.log.info("main.attackerHashValue:" + str(main.attackerHashValue))
            utilities.assert_equals(expect=main.TRUE,
                                    actual=main.FALSE,
                                    onpass="No. of inject seeds in the params file are sufficient.",
                                    onfail="Insufficient inject seeds in the params file.")
        if outputPort4_1_1 != '':
            main.log.info( "Configure flow mirror rule on switches 4_1_1 to mirror traffic to 2_1_2 and send traffic along the original path" )
            stepResult = main.TRUE
            flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort4_1_1 + "," + outputPort4_1_1
            # flowRule = "send_flow_rem,table=1,priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," + \
            #            "actions=" + outputPort4_1_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," + outputPort4_1_1
            stepResult = main.Mininet1.addFlow( [ "4_1_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="4_1_1 not configured to emulate an injection attack that mirrors traffic" )
            # main.step( "arp the host, so that ONOS discovers the host connect points." )
            # stepResult = main.Mininet1.arpHost( ["2_1_2"] )
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully arpinged hosts",
            #                          onfail="Failed to arping hosts" )
            # main.step( "Ping test" )
            # stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )
            #
            # utilities.assert_equals( expect=main.TRUE,
            #                          actual=stepResult,
            #                          onpass="Successfully pinged hosts",
            #                          onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1" ], "actions=output:" + outputPort4_1_1 + ",output:" + outputPort4_1_1)
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_2_1", "4_2_2", "2_3_1", "2_0_1" ], "actions=output:" + outputPort4_1_1 + ",output:" + outputPort4_1_1 )
            # stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_2_1", "4_2_2", "2_3_1", "2_0_1" ], "strip_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "->vlan_vid,output:" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        elif outputPort4_1_2 != '':
            main.log.info( "Configure flow mirror rule on switches 4_1_2 to mirror traffic to 2_1_2 and send traffic along the original path" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort4_1_2 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_1_2
            stepResult = main.Mininet1.addFlow( [ "4_1_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_2 configured to emulate an injection attack that mirrors traffic",
                                     onfail="4_1_2 not configured to emulate an injection attack that mirrors traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "2_2_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_2_1", "4_2_2", "2_3_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        elif outputPort4_2_1 != '':
            main.log.info( "Configure flow mirror rule on switches 4_2_1 to mirror traffic to 2_1_2 and send traffic along the original path" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort4_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_2_1
            stepResult = main.Mininet1.addFlow( [ "4_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="4_2_1 not configured to emulate an injection attack that mirrors traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_2_1", "2_3_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_1_1", "4_2_2", "2_2_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        elif outputPort4_2_2 != '':
            main.log.info( "Configure flow mirror rule on switches 4_2_2 to mirror traffic to 2_1_2 and send traffic along the original path" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort4_2_2 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_2_2
            stepResult = main.Mininet1.addFlow( [ "4_2_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_2 configured to emulate an injection attack that mirrors traffic",
                                     onfail="4_2_2 not configured to emulate an injection attack that mirrors traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_2_2", "2_3_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_1_1", "4_2_1", "2_2_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

    def CASE3390( self, main ):
        '''
            Delete the mirror rule on the Core switch
            for traffic from 0_0_2 to 2_1_2
        '''
        import json

        main.step( "Delete flow mirror rule on switch 4_1_1, 4_1_2, 4_2_1 or 4_2_2. for traffic from 0_0_2 to 2_1_2" )

        main.log.info( "Delete flow mirror rules on switch 4_1_1, 4_1_2, 4_2_1 or 4_2_2 to emulate an inject attack" )
        stepResult = main.TRUE
        flowRule = "table=1,dl_type=0x0800,dl_src=00:00:00:00:00:02"
        stepResult = main.Mininet1.delFlow( [ "4_1_1", "4_1_2", "4_2_1", "4_2_2" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="4_1_1, 4_1_2, 4_2_1 or 4_2_2 have mirror rules deleted to emulate an inject attack",
                                 onfail="4_1_1, 4_1_2, 4_2_1 or 4_2_2 have mirror rules not deleted to emulate an inject attack" )

    def CASE3338( self, main ):
        '''
            Configure a flow rule on the Aggregate switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that modifies the traffic.
            In this case it is simply the attacker chose hash value.
            The same hash is used for all packets during hte attack.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2 that modifies the vlan. Injection modification attack" )

        main.step( "First get the installed output ports for 00:00:00:00:00:02 on switches 0_2_1 and 0_3_1" )
        outputPort0_0_2 = main.Mininet1.getFlowOutputPort( "0_2_1" )
        outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_1_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_1_1 flushed",
                                 onfail="0_1_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1 flushed",
                                 onfail="0_2_1 not flushed" )

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if outputPort0_0_2 != '':
            main.log.info( "Configure flow rule that changes the Vlan on 0_0_2" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort0_0_2
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that modifies traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that modifies traffic" )

        else:
            main.log.info( "Configure flow rule that changes the source IP to 10.0.0.20 on 0_3_1" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort0_3_1
            stepResult = main.Mininet1.addFlow( [ "0_3_1" ], version="1.3", flowcmd=flowRule)
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_3_1 configured to emulate an injection attack that modifies traffic",
                                     onfail="0_3_1 not configured to emulate an injection attack that modifies traffic" )

    def CASE3339( self, main ):
        '''
            Configure a flow rule on the Core switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that modifies the traffic.
            In this case, the attacker chosen hash value.
            The same hash is used by the attacking switch during the attack.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on switch 4_1_1, 4_1_2, 4_2_1 or 4_2_2_1 for traffic from 0_0_2 to 1_0_2 that modifies the Vlan id" )

        main.step( "First get the installed output ports for 00:00:00:00:00:02 on the core switches 4_1_1, 4_1_2, 4_2_1 or 4_2_2" )
        outputPort4_1_1 = main.Mininet1.getFlowOutputPort( "4_1_1" )
        outputPort4_1_2 = main.Mininet1.getFlowOutputPort( "4_1_2" )
        outputPort4_2_1 = main.Mininet1.getFlowOutputPort( "4_2_1" )
        outputPort4_2_2 = main.Mininet1.getFlowOutputPort( "4_2_2" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_1_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_1_1 flushed",
                                 onfail="0_1_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1 flushed",
                                 onfail="0_2_1 not flushed" )

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if outputPort4_1_1 != '':
            main.log.info( "Configure flow rule that changes the source IP to 10.0.0.20 on 0_0_2" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_1_1
            stepResult = main.Mininet1.addFlow( [ "4_1_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_1 configured to emulate an injection attack that modifies traffic",
                                     onfail="4_1_1 not configured to emulate an injection attack that modifies traffic" )
        elif outputPort4_1_2 != '':
            main.log.info( "Configure flow rule that changes the source IP to 10.0.0.20 on 0_0_2" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_1_2
            stepResult = main.Mininet1.addFlow( [ "4_1_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_2 configured to emulate an injection attack that modifies traffic",
                                     onfail="4_1_2 not configured to emulate an injection attack that modifies traffic" )
        elif outputPort4_2_1 != '':
            main.log.info( "Configure flow rule that changes the source IP to 10.0.0.20 on 0_0_2" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_2_1
            stepResult = main.Mininet1.addFlow( [ "4_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_1 configured to emulate an injection attack that modifies traffic",
                                     onfail="4_2_1 not configured to emulate an injection attack that modifies traffic" )
        elif outputPort4_2_2 != '':
            main.log.info( "Configure flow rule that changes the source IP to 10.0.0.20 on 0_0_2" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_2_2
            stepResult = main.Mininet1.addFlow( [ "4_2_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_2 configured to emulate an injection attack that modifies traffic",
                                     onfail="4_2_2 not configured to emulate an injection attack that modifies traffic" )

    def CASE33338( self, main ):
        '''
            Reroute attack
            Configure a flow rule on the Aggregate switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that modifies the destination MAC address
            In this case, the malicious switch actually
            forwards traffic that it does not sample to
            a different destination.
            Also, send ping traffic so that flows are installed
            for the new path traffic.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on switch 0_2_1 and 0_3_1 for traffic from 0_0_2 to 1_0_2 that modifies the\
                            destination MAC address to forward traffic to a different host" )

        main.step( "First get the installed input ports for 00:00:00:00:00:02 on switches 0_2_1 and 0_3_1" )
        inputPort0_2_1 = main.Mininet1.getFlowInputPort( "0_2_1" )
        inputPort0_3_1 = main.Mininet1.getFlowInputPort( "0_3_1" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_1_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_1_1 flushed",
                                 onfail="0_1_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1 flushed",
                                 onfail="0_2_1 not flushed" )

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if inputPort0_2_1 != '':
            main.log.info( "Configure flow rule that changes the destination MAC address and resubmits the modified packets to the flow table" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit:" + inputPort0_2_1
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that reroutes traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that reroutes traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "0_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1", "0_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        else:
            main.log.info( "Configure flow rule that changes the destination MAC address and resubmits the modified packets to the flow table" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit:" + inputPort0_3_1
            stepResult = main.Mininet1.addFlow( [ "0_3_1" ], version="1.3", flowcmd=flowRule)
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_3_1 configured to emulate an injection attack that reroutes traffic",
                                     onfail="0_3_1 not configured to emulate an injection attack that reroutes traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "0_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1", "0_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
    def CASE33339( self, main ):
        '''
            Reroute attack
            Configure a flow rule on the Core switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that modifies the destination MAC address
            In this case, the malicious switch actually
            forwards traffic that it does not sample to
            a different destination.
            Also, send ping traffic so that flows are installed
            for the new path traffic.
        '''
        import json
        import random

        main.case( "Configure flow modifying rule on switch 4_1_1, 4_1_2, 4_2_1 or 4_2_2_1 for traffic from 0_0_2 to 1_0_2 that modifies the\
                            destination MAC address to reroute traffic that it does not sample" )

        main.step( "First get the installed input ports for 00:00:00:00:00:02 on the core switches 4_1_1, 4_1_2, 4_2_1 or 4_2_2" )
        inputPort4_1_1 = main.Mininet1.getFlowInputPort( "4_1_1" )
        inputPort4_1_2 = main.Mininet1.getFlowInputPort( "4_1_2" )
        inputPort4_2_1 = main.Mininet1.getFlowInputPort( "4_2_1" )
        inputPort4_2_2 = main.Mininet1.getFlowInputPort( "4_2_2" )

        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_1_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_1_1 flushed",
                                 onfail="0_1_1 not flushed" )
        stepResult = main.TRUE
        stepResult = main.Mininet1.flushIptablesDrop( "0_2_1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1 flushed",
                                 onfail="0_2_1 not flushed" )

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if inputPort4_1_1 != '':
            main.log.info( "Configure flow rule that changes the destination MAC address to 00:00:00:02:01:02" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_1_1
            stepResult = main.Mininet1.addFlow( [ "4_1_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_1 configured to emulate an injection attack that reroutes traffic",
                                     onfail="4_1_1 not configured to emulate an injection attack that reroutes traffic" )
            main.step( "arp the host, so that ONOS discovers the host connect points." )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "2_2_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_2_1", "4_2_2", "2_3_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )

        elif inputPort4_1_2 != '':
            main.log.info( "Configure flow rule that changes the destination MAC address to 00:00:00:02:01:02" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_1_2
            stepResult = main.Mininet1.addFlow( [ "4_1_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_2 configured to emulate an injection attack thatreroutes traffic",
                                     onfail="4_1_2 not configured to emulate an injection attack that reroutes traffic" )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "2_2_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_2_1", "4_2_2", "2_3_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        elif inputPort4_2_1 != '':
            main.log.info( "Configure flow rule that changes the destination MAC address to 00:00:00:02:01:02" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_2_1
            stepResult = main.Mininet1.addFlow( [ "4_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_1 configured to emulate an injection attack that reroutes traffic",
                                     onfail="4_2_1 not configured to emulate an injection attack that reroutes traffic" )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_2_1", "2_3_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_1_2", "4_2_2", "2_2_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
        elif inputPort4_2_2 != '':
            main.log.info( "Configure flow rule that changes the destination MAC address to 00:00:00:02:01:02" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_2_2
            stepResult = main.Mininet1.addFlow( [ "4_2_2" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_2_2 configured to emulate an injection attack that reroutes traffic",
                                     onfail="4_2_2 not configured to emulate an injection attack that reroutes traffic" )
            stepResult = main.Mininet1.arpHost( "2_1_2" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully arpinged hosts",
                                     onfail="Failed to arping hosts" )
            main.step( "Ping test" )
            stepResult = main.Mininet1.pingHost( src = "0_0_2", target = "1_0_2" )

            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully pinged hosts",
                                     onfail="Failed to ping hosts" )
            main.log.info( "Now to check if the flows are installed" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_2_2", "2_3_1", "2_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
            main.log.info( "Now to make sure that flows are not installed on other switches" )
            stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_1_2", "4_2_1", "2_2_1", "2_0_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:02:01:02" )
            utilities.assert_equals( expect=main.FALSE,
                                     actual=stepResult,
                                     onpass="Successfully installed attack flows",
                                     onfail="Failed to install attack flows" )
    def CASE41( self, main ):
        '''
            Activate the tsamp application
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        activateResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Activate tsamp" )
        main.caseExplanation = "Activate tsamp."

        main.step( "Activate tsamp." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        activateResult = main.CLIs[ 0 ].app( "org.onosproject.tsamp", "activate" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=activateResult,
                                 onpass="Successfully activated tsamp",
                                 onfail="Failed to activate tsamp" )

    def CASE42( self, main ):
        '''
            Deactivate the tsamp application
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        deactivateResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Deactivate tsamp" )
        main.caseExplanation = "Deactivate tsamp."

        main.step( "Deactivate tsamp." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        deactivateResult = main.CLIs[ 0 ].app( "org.onosproject.tsamp", "deactivate" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=deactivateResult,
                                 onpass="Successfully deactivated tsamp",
                                 onfail="Failed to deactivate tsamp" )

    def CASE50( self, main ):
        '''
            Configure pair-wise assignment
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure pair-wise assignment" )
        main.caseExplanation = "Configure pair-wise assignment in ATS"

        main.step( "Configure pairAssignment" )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "pairAssignment", "true" )
        main.log.info( "Sleep for 10s so that the flows are actually installed" )
        time.sleep( main.activateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured pairAssignment",
                                 onfail="Failed to configure pairAssignment" )

    def CASE500( self, main ):
        '''
            Disable pair-wise assignment
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Disable pair-wise assignment" )
        main.caseExplanation = "Disable pair-wise assignment in ATS"

        main.step( "Disable pairAssignment" )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "pairAssignment", "false" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully disabled pairAssignment",
                                 onfail="Failed to disable pairAssignment" )

    def CASE51( self, main ):
        '''
            Enable hash mutation
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Enable hash mutation" )
        main.caseExplanation = "Enable hash mutation in ATS"

        main.step( "Enable  hash mutation" )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "hashMutation", "true" )
        main.log.info( "Sleep for 5s so that the hash mutation begins" )
        time.sleep( 5 )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully Enabled pairAssignment",
                                 onfail="Failed to Enable pairAssignment" )

    def CASE52( self, main ):
        '''
            Disable hash mutation
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Disable hash mutation" )
        main.caseExplanation = "Disable hash mutation in ATS"

        main.step( "Disable  hash mutation" )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "hashMutation", "false" )
        main.log.info( "Sleep for 5s so that the hash mutation stops completely" )
        time.sleep( 5 )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully Disabled hash mutation",
                                 onfail="Failed to Disable hash mutation" )

    def CASE53( self, main ):
        '''
            Configure the currentSeeds for pair-wise assignment.
            This includes the pairwiseSeed, hashMutatorSeed and
            switchMutatorSeed. Make sure to call this before
            enabling pairwiseAssignment.
        '''
        import json
        import time
        import pprint
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure pairwiseSeed" )
        main.caseExplanation = "Configure pairwiseSeed in ATS"

        main.step( "Configure pairwiseSeed" )
        main.log.info("Attack type is:" + str(main.attack))
        # currentSeeds is simply the next seed popped from main.seeds
        # main.attack = 'DROP'
        # first handle the case where the first seed is to be taken
        if main.currentSeeds == {} and main.currentSeedsIndex == -1:
            main.log.info("In first seed config")
            main.currentSeedsIndex = 0
            main.currentSeeds[main.seedKeys[main.attack][main.currentSeedsIndex]] = main.seeds[main.attack][main.seedKeys[main.attack][main.currentSeedsIndex]]
            # (key, value) = main.seeds[main.attack].popitem()
            # main.currentSeeds[key] = value
        elif main.currentSeeds != {} and main.currentSeedsIndex >= 0 and main.currentSeedsIndex < len(main.seedKeys[main.attack]):
            main.log.info("In next seed config.")
            # Need to ensure that currentSeeds holds only the current seed.
            main.currentSeeds = {}
            main.currentSeedsIndex += 1
            main.currentSeeds[main.seedKeys[main.attack][main.currentSeedsIndex]] = main.seeds[main.attack][main.seedKeys[main.attack][main.currentSeedsIndex]]
            # (key, value) = main.seeds[main.attack].popitem()
            # main.currentSeeds[key] = value
        else :
            main.log.error("There are not enough seeds in the params file. Going to use the last configured seed..")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=main.FALSE,
                                    onpass="No. of seeds in the params file are sufficient.",
                                    onfail="Insufficient seeds in the params file.")
        main.log.info("currentSeeds is:" + str(main.currentSeeds))
        # pprint.pprint(main.currentSeeds)
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        for pairwiseSeed in main.currentSeeds:
            main.log.info("Going to set the pairwiseSeed to:" + str(pairwiseSeed))
            cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "pairwiseSeed", pairwiseSeed )
            main.log.info("main.currentSeeds[pairwiseSeed]:" + str(main.currentSeeds[pairwiseSeed]))
            main.log.info("Going to set the hashMutatorSeed to:" + str(main.currentSeeds[pairwiseSeed][0]))
            main.log.info("Going to set the switchMutatorSeed to:" + str(main.currentSeeds[pairwiseSeed][1]))
            hashCfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                       "hashMutatorSeed", main.currentSeeds[pairwiseSeed][0] )
            switchCfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                       "switchMutatorSeed", main.currentSeeds[pairwiseSeed][1] )
            break
        main.log.info( "Sleep for 10s so that the flows are actually installed" )
        time.sleep( main.activateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured pairwiseSeed",
                                 onfail="Failed to configure pairwiseSeed" )
        utilities.assert_equals(expect=main.TRUE,
                                actual=hashCfgResult,
                                onpass="Successfully configured hashMutatorSeed",
                                onfail="Failed to configure hashMutatorSeed")
        utilities.assert_equals(expect=main.TRUE,
                                actual=switchCfgResult,
                                onpass="Successfully configured switchMutatorSeed",
                                onfail="Failed to configure switchMutatorSeed")

    def CASE54( self, main ):
        '''
            Configure the sampling ratio from the params file.
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure the samplingRate." )
        main.caseExplanation = "Configure the samplingRate in ATS."

        main.step( "Configure the samplingRate." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        # The below needs to change to handle the different samplingRates better.
        samplingRate = main.samplingRatio[0]
        if samplingRate == '0.0046':
            samplingRate = '0.004638671875'
        elif samplingRate == '0.0092':
            samplingRate = '0.00927734375'
        elif samplingRate == '0.0139':
            samplingRate = '0.013916015625'
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "samplingRate", samplingRate )
        main.log.info( "Sleep for 2s so that the config is digested." )
        time.sleep( 2 )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured the samplingRate.",
                                 onfail="Failed to configure the samplingRate." )

    def CASE61( self, main ):
        '''
            Enable Trajectory Sampling
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Enable Trajectory Sampling" )
        main.caseExplanation = "Enabled Trajectory Sampling to commence sampling."

        main.step( "Configure trajectorySampling to true." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "trajectorySampling", "true" )
        main.log.info( "Sleep for 10s so that detectors settle down" )
        time.sleep( main.activateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully enabled Trajectory Sampling",
                                 onfail="Failed to enable Trajectory Sampling" )

    def CASE62( self, main ):
        '''
            Disable Trajectory Sampling
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Disable Trajectory Sampling" )
        main.caseExplanation = "Disabled Trajectory Sampling to stop sampling."

        main.step( "Configure trajectorySampling to false." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "trajectorySampling", "false" )
        main.log.info( "Sleep for 10s so that detectors settle down" )
        time.sleep( main.deactivateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully disabled Trajectory Sampling",
                                 onfail="Failed to disable Trajectory Sampling" )

    def CASE63( self, main ):
        '''
            Enable Collusion
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Enable Collusion" )
        main.caseExplanation = "Enabled Collusion."

        main.step( "Configure collusion to true." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "collusion", "true" )
        main.log.info( "Sleep for 10s so that detectors settle down" )
        time.sleep( main.activateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully enabled Collusion",
                                 onfail="Failed to enable Collusion" )
        main.step( "Now verify that colluding flow rules are installed." )
        main.step("Check flows are in the ADDED state")

        main.log.info("Get the flows from ONOS")
        flows = json.loads(main.ONOSrest.flows())

        stepResult = main.TRUE
        for f in flows:
            if "rest" in f.get("appId"):
                if "ADDED" not in f.get("state"):
                    stepResult = main.FALSE
                    main.log.error("Flow: %s in state: %s" % (f.get("id"), f.get("state")))

        utilities.assert_equals(expect=main.TRUE,
                                actual=stepResult,
                                onpass="All flows are in the ADDED state",
                                onfail="All flows are NOT in the ADDED state")

        main.step("Check flows are in Mininet's flow table")

        # get the flow IDs that were added
        main.log.info("Getting the flow IDs from ONOS")
        flowIds = [f.get("id") for f in flows]
        # convert the flowIDs to ints then hex and finally back to strings
        flowIds = [str(hex(int(x))) for x in flowIds]
        main.log.info("ONOS flow IDs: {}".format(flowIds))
        switchList = main.Mininet1.getSwitch()
        main.log.info("Now to check if the flowIds are in Mininet.")
        samplesExist = main.Mininet1.checkFlowId(switchList, flowIds, debug=False)
        print samplesExist
        if samplesExist == main.TRUE:
            main.log.info("Flows from SATS and Mininet match.")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=samplesExist,
                                    onpass="All flows are in mininet",
                                    onfail="All flows are NOT in mininet")
        else:
            attempts = 1
            samplesExist = main.FALSE
            while samplesExist == main.FALSE and attempts < 10:
                main.log.info("Try to get them installed by disabling and enabling collusion and pairAssignment resp.")
                main.step("Disable collusion")
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "collusion", "false")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully disabled collusion",
                                        onfail="Failed to disable collusion")
                main.step("Disable pairAssignment")
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "pairAssignment", "false")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully disabled pairAssignment",
                                        onfail="Failed to disable pairAssignment")
                main.step("Deactivate tsamp.")
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                deactivateResult = main.CLIs[0].app("org.onosproject.tsamp", "deactivate")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=deactivateResult,
                                        onpass="Successfully deactivated tsamp",
                                        onfail="Failed to deactivate tsamp")
                main.step("Activate tsamp.")
                main.log.info("Sleep 10 seconds before enabling")
                time.sleep(10)
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                activateResult = main.CLIs[0].app("org.onosproject.tsamp", "activate")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=activateResult,
                                        onpass="Successfully activated tsamp",
                                        onfail="Failed to activate tsamp")

                main.log.info("Sleep 10 seconds before enabling")
                time.sleep(10)
                main.step("Configure pairAssignment")
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "pairAssignment", "true")
                main.log.info("Sleep for 10s so that the flows are actually installed")
                time.sleep(main.activateSleep)
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully configured pairAssignment",
                                        onfail="Failed to configure pairAssignment")
                main.step("Configure collusion")
                main.CLIs[0].startOnosCli(main.ONOSip[0])
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "collusion", "true")
                main.log.info("Sleep for 10s so that the colluding flows are actually installed")
                time.sleep(main.activateSleep)
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully configured collusion",
                                        onfail="Failed to configure collusion")
                main.log.info("Now check the flows again")
                # main.log.info( "Get the flows from every switch in the network" )
                # switchList = main.Mininet1.getSwitch()
                # samplesExist = main.Mininet1.checkSamplingFlows( switchList )
                main.step("Check flows are in the ADDED state")

                main.log.info("Get the flows from ONOS")
                flows = json.loads(main.ONOSrest.flows())

                stepResult = main.TRUE
                for f in flows:
                    if "rest" in f.get("appId"):
                        if "ADDED" not in f.get("state"):
                            stepResult = main.FALSE
                            main.log.error("Flow: %s in state: %s" % (f.get("id"), f.get("state")))

                utilities.assert_equals(expect=main.TRUE,
                                        actual=stepResult,
                                        onpass="All flows are in the ADDED state",
                                        onfail="All flows are NOT in the ADDED state")

                main.step("Check flows are in Mininet's flow table")

                # get the flow IDs that were added
                main.log.info("Getting the flow IDs from ONOS")
                flowIds = [f.get("id") for f in flows]
                # convert the flowIDs to ints then hex and finally back to strings
                flowIds = [str(hex(int(x))) for x in flowIds]
                main.log.info("ONOS flow IDs: {}".format(flowIds))
                switchList = main.Mininet1.getSwitch()

                samplesExist = main.Mininet1.checkFlowId(switchList, flowIds, debug=False)
                attempts += 1

            utilities.assert_equals(expect=main.TRUE,
                                    actual=samplesExist,
                                    onpass="All samplings flows are in the ADDED state",
                                    onfail="All sampling flows are NOT in the ADDED state")

    def CASE64( self, main ):
        '''
            Disable Collusion
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Disable Collusion" )
        main.caseExplanation = "Disabled Collusion."

        main.step( "Configure collusion to false." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "collusion", "false" )
        main.log.info( "Sleep for 10s so that detectors settle down" )
        time.sleep( main.deactivateSleep )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully disabled Collusion",
                                 onfail="Failed to disable Collusion" )

    def CASE65( self, main ):
        '''
            Configure the colluding switches from the params file.
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure the colluding switches." )
        main.caseExplanation = "Configure the colluding switches in ATS."

        main.step( "Configure colludingSwitch1." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "colludingSwitch1", main.colludingSwitch1 )
        main.log.info( "Sleep for 2s so that the config is digested." )
        time.sleep( 2 )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured colludingSwitch1.",
                                 onfail="Failed to configure colludingSwitch1." )
        main.step( "Configure colludingSwitch2." )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "colludingSwitch2", main.colludingSwitch2 )
        main.log.info( "Sleep for 2s so that the config is digested." )
        time.sleep( 2 )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured colludingSwitch2.",
                                 onfail="Failed to configure colludingSwitch2." )

    def CASE71( self, main ):
        '''
            Set fwd Flow Timeout to 3600s
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure flow timeout to 3600s" )
        main.caseExplanation = "Configure flow timeout to 3600s."

        main.step( "Configure fwd.flowTimeout=3600s." )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.fwd.ReactiveForwarding",
                                           "flowTimeout", "60000" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured the flowTimeout",
                                 onfail="Failed to configure the flowTimeout in fwd" )

    def CASE72( self, main ):
        '''
            Allow extraneous flow rules
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Allow extraneous flow rules on switches" )
        main.caseExplanation = "Configure Flow Rule Manager to allow extraneous flow rules"
        main.step( "Configure org.onosproject.net.flow.impl.FlowRuleManage allowExtraneousRules=true " )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.net.flow.impl.FlowRuleManager",
                                           "allowExtraneousRules", "true" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured the allowExtraneousRules",
                                 onfail="Failed to configure the allowExtraneousRules" )

    def CASE77( self, main ):
        '''
            Start CPU and Memory sampling on the ONOS node
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Start sampling the CPU and Memory" )
        main.caseExplanation = "Start top for the ONOS process using the shell script."
        main.step( "Start top for the ONOS process using the shell script" )
        cfgResult = main.ONOSbench.startCpuMemSampling( main.ONOSip[ 0 ] )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully starting sampling the CPU and memory",
                                 onfail="Failed to start sampling the CPU and memory" )

    def CASE78( self, main ):
        '''
            Stop CPU and Memory sampling on the ONOS node
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Stop sampling the CPU and Memory" )
        main.caseExplanation = "Stop top for the ONOS process using the shell script."
        main.step( "Stop top for the ONOS process using the shell script" )
        cfgResult = main.ONOSbench.stopCpuMemSampling( main.ONOSip[ 0 ] )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully stopped sampling the CPU and memory",
                                 onfail="Failed to stop sampling the CPU and memory" )

    def CASE79( self, main ):
        '''
            Set the log level in ONOS to ERROR
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Set the log level to ERROR in ONOS" )
        main.caseExplanation = "Set the log level to ERROR in ONOS"
        main.step( "Set the log level to ERROR in ONOS" )
        cfgResult = main.CLIs[ 0 ].setLogLevel( level="ERROR" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully set the log level",
                                 onfail="Failed to set the log level to ERROR" )

    def CASE80( self, main ):
        '''
            h1 sends to h3 using tcpreplay
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay test" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        tcpreplayResult = main.h1.startTcpreplay( "h1", "/home/mininet/ats-testing/4packets1k2k3k4k.pcapng",
                                                   "--pps-multi=100 --preload-pcap --pps=100 --loop=50 --limit=1000" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE8800( self, main ):
        '''
            Measure detection time for a packet drop attack
            using tcpreplay instead of scapy.
            The testcase assumes that SATS has been configured with
            only the static assignment currently. This testcase will
            then switch it over to the dynamic assignment. Another
            testcase must take care of switching back to static assignment.
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 (Agg or Core switch) carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send 100 packets per second\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step("First generate the pcap file list to be used for traffic generation.")
        lblTrafficPath = main.lblTrafficPath
        pcapFilesUsedFile = main.pcapFilesUsed
        masterChksums = main.masterChksums
        pcapsToUse = []
        if main.attack == 'drop' and str(main.attacker) == 'aggregate':
            main.log.info("In drop attack at aggregate, therefore don't get results from json file.")
            orderedList = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath)
            pcapsToUse = orderedList
        else:
            main.log.info("Not in drop attack at aggregate, therefore first get results from json file.")
            seedKeys = main.currentSeeds.keys()
            seedKey = seedKeys[0]
            pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath,
                                                           fromJson=True, seedKey=seedKey)
        main.log.info("Got the following list of pcaps to use.")
        main.log.info(pcapsToUse)
        main.log.info("Now set the index for searching through the master checksum file")
        pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapsToUse[0]))
        masterChksumIndexStart = pcapNumber * 100
        main.log.info("Got the pcapNumber as:" + str(pcapNumber) + " and the masterChksumIndexStart as:" + str(masterChksumIndexStart))
        # Now for running the same traffic with the same seed.
        main.step("Now get the current seeds configured on ONOS/SATS.")
        allSeeds = main.seeds
        currentSeeds = main.currentSeeds
        # main.CLIs[0].startOnosCli(main.ONOSip[0])
        currentSeedsOnos = [main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling","pairwiseSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "hashMutatorSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "switchMutatorSeed", short=True)]
        main.log.info("currentSeedsOnos is:" + str(currentSeedsOnos))
        # if currentSeeds != currentSeedsOnos:
        #     main.log.error("currentSeeds:" + str(currentSeeds) + ", currentSeedsOnos:" + str(currentSeedsOnos))

        main.step( "Now clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog()

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )
        # Assume that only 0_0_2 is sending traffic to 1_0_2
        # Therefore the interface = 0_0_2-eth0
        host = '0_0_2'
        interface = host + "-eth0"
        # now first test the static assignment followed by the dynamic assignment.
        for assignment in ['static', 'dynamic']:
            main.log.info("Current assignment is:" + assignment)
            resultsSaved = False
            if assignment == 'dynamic':
                main.log.info("Need to switch on hash mutation now. Seed configuration is taken care of in testcase53.")
                main.step("Enable  hash mutation")
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "hashMutation", "true")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully Enabled pairAssignment",
                                        onfail="Failed to Enable pairAssignment")
                main.log.info("Start the traffic right away.")
            pcapFileList = []
            packetCounter = 0
            for pcapFile in pcapsToUse:
                # Append the pcapFile used for traffic generation in this round.
                pcapFileList.append(pcapFile)
                # start/endSearchIndex are used to keep of track of the range to search in the masterChksums
                tcpreplayCommand = "tcpreplay --preload-pcap -p 100 -i " + interface + " " + pcapFile
                result = main.Mininet1.node(host, tcpreplayCommand)
                print result
                # Sleep for 5 seconds for testing, can reduce to 2 I think.
                main.log.info("Sleep for 4s so that the last sample completes an RTT")
                time.sleep(4)
                packetCounter += 100
                main.log.info("Packets sent so far:" + str(packetCounter))
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapFile))
                    startSearchIndex = pcapNumber * 100
                    endSearchIndex = pcapNumber * 100 + 99
                    i = startSearchIndex
                    end = endSearchIndex
                    main.log.info("start and end SearchIndex are:" + str(startSearchIndex) + ", " + str(endSearchIndex))
                    while i <= end:
                        chksumValue = int(masterChksums[i]) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            # need to include the seeds used for this detection round.
                            seeds = main.currentSeeds
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( packetsToDetect ) )
                            # Now save the results in the json file.
                            # Data for the detection time json file are the following:
                            # [timestamp, packetsSent], attackType, attackerPosition, assignmentType, hashFunction, samplingRatio
                            timeStamp = time.strftime("%Y%m%d-%H%M%S")
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                            attackType = main.attack
                            attackerPosition = str(main.attacker)
                            assignmentType = assignment
                            # Using index 0 for main.hashFunction and main.samplingRatio, needs to change later.
                            hashFunction = main.hashFunction[0]
                            samplingRatio = main.samplingRatio[0]
                            # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                            main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio)
                            # Also save the pcap files used for this detection.
                            main.pcapFileHelper.save(pcapFileList)
                            resultsSaved = True
                            break
                        else:
                            i += 1
                    if resultsSaved is not True:
                        main.log.error("Could not save the detection results. Need to repeat this case!")
                    main.log.info("Finished testing assignmentType:" + str(assignment))
                    main.step("Clear the logs on ONOS before moving to the next assignment!")
                    clearLogResult = main.CLIs[0].clearLog()
                    utilities.assert_equals(expect=main.TRUE,
                                            actual=clearLogResult,
                                            onpass="Successfully cleared ONOS logs",
                                            onfail="Failed to clear ONOS logs")
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to find the no. of packets to detect the drop attack." )

    def CASE8880( self, main ):
        '''
            Measure detection time for a packet drop attack
            using tcpreplay instead of scapy.
            The testcase assumes that SATS has been configured with
            only the static assignment currently. This testcase will
            immediately switch it over to the dynamic assignment. It will
            also only carry out the experiment for different update rates.
            Another testcase must take care of switching back to static assignment.
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 (Agg or Core switch) carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector with different update rates.\
        The test stops when an alert is found.\
        1. Send 100 packets per second\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step("First generate the pcap file list to be used for traffic generation.")
        lblTrafficPath = main.lblTrafficPath
        pcapFilesUsedFile = main.pcapFilesUsed
        masterChksums = main.masterChksums
        pcapsToUse = []
        # In this case, we want to compare the performance of the dynamic assignment with
        # various update rates. Therefore, need to get the results from the reference attack
        # which is the agg/drop/static and sampling rate of .0046.
        assignments = ['dynamic']
        if main.attack == 'drop' and str(main.attacker) == 'aggregate' and assignments[0] == 'static':
            main.log.info("In drop attack at aggregate, therefore don't get results from json file.")
            orderedList = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath)
            pcapsToUse = orderedList
        else:
            main.log.info("Not in static drop attack at aggregate, therefore first get results from json file.")
            seedKeys = main.currentSeeds.keys()
            seedKey = seedKeys[0]
            pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath,
                                                           fromJson=True, seedKey=seedKey)
        main.log.info("Got the following list of pcaps to use.")
        main.log.info(pcapsToUse)
        main.log.info("Now set the index for searching through the master checksum file")
        pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapsToUse[0]))
        masterChksumIndexStart = pcapNumber * 100
        main.log.info("Got the pcapNumber as:" + str(pcapNumber) + " and the masterChksumIndexStart as:" + str(masterChksumIndexStart))
        # Now for running the same traffic with the same seed.
        main.step("Now get the current seeds configured on ONOS/SATS.")
        allSeeds = main.seeds
        currentSeeds = main.currentSeeds
        # main.CLIs[0].startOnosCli(main.ONOSip[0])
        currentSeedsOnos = [main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling","pairwiseSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "hashMutatorSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "switchMutatorSeed", short=True)]
        main.log.info("currentSeedsOnos is:" + str(currentSeedsOnos))
        # if currentSeeds != currentSeedsOnos:
        #     main.log.error("currentSeeds:" + str(currentSeeds) + ", currentSeedsOnos:" + str(currentSeedsOnos))

        main.step( "Now clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog()

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )
        # Assume that only 0_0_2 is sending traffic to 1_0_2
        # Therefore the interface = 0_0_2-eth0
        host = '0_0_2'
        interface = host + "-eth0"
        # Get the updateRates
        updateRates = main.updateRate
        main.log.info("Got the following updateRates from the params file:" + str(updateRates))
        for updateRate in updateRates:
            # Before starting, disable hashMutation, configure the updateRate and then enable it again.
            resultsSaved = False
            main.log.info("Need to switch OFF hash mutation now. Seed configuration is taken care of in testcase53.")
            main.step("Disable  hash mutation")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "hashMutation", "false")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully disabled the hashMutation",
                                    onfail="Failed to disable the hashMutation")
            main.log.info("Now configure the updateRate to:" + str(updateRate))
            main.step("Configure the update rate.")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "updateRate", updateRate)
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully configured the updateRate",
                                    onfail="Failed to configure the updateRate")
            main.log.info("Need to switch ON hash mutation now. Seed configuration is taken care of in testcase53.")
            main.step("Enable  hash mutation")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "hashMutation", "true")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully enabled the hashMutation",
                                    onfail="Failed to enable the hashMutation")
            main.log.info("Start the traffic right away.")
            pcapFileList = []
            packetCounter = 0
            for pcapFile in pcapsToUse:
                # Append the pcapFile used for traffic generation in this round.
                pcapFileList.append(pcapFile)
                # start/endSearchIndex are used to keep of track of the range to search in the masterChksums
                tcpreplayCommand = "tcpreplay --preload-pcap -p 100 -i " + interface + " " + pcapFile
                result = main.Mininet1.node(host, tcpreplayCommand)
                print result
                # Sleep for 5 seconds for testing, can reduce to 2 I think.
                main.log.info("Sleep for 4s so that the last sample completes an RTT")
                time.sleep(4)
                packetCounter += 100
                main.log.info("Packets sent so far:" + str(packetCounter))
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapFile))
                    startSearchIndex = pcapNumber * 100
                    endSearchIndex = pcapNumber * 100 + 99
                    i = startSearchIndex
                    end = endSearchIndex
                    main.log.info("start and end SearchIndex are:" + str(startSearchIndex) + ", " + str(endSearchIndex))
                    while i <= end:
                        chksumValue = int(masterChksums[i]) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            # need to include the seeds used for this detection round.
                            seeds = main.currentSeeds
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( packetsToDetect ) )
                            # Now save the results in the json file.
                            # Data for the detection time json file are the following:
                            # [timestamp, packetsSent], attackType, attackerPosition, assignmentType, hashFunction, samplingRatio
                            timeStamp = time.strftime("%Y%m%d-%H%M%S")
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                            attackType = main.attack
                            attackerPosition = str(main.attacker)
                            # assignments = ['dynamic']
                            assignmentType = assignments[0]
                            # Using index 0 for main.hashFunction and main.samplingRatio, needs to change later.
                            hashFunction = main.hashFunction[0]
                            samplingRatio = main.samplingRatio[0]
                            # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                            main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio, updateRate=updateRate)
                            # Also save the pcap files used for this detection.
                            main.pcapFileHelper.save(pcapFileList)
                            resultsSaved = True
                            break
                        else:
                            i += 1
                    if resultsSaved is not True:
                        main.log.error("Could not save the detection results. Need to repeat this case!")
                    main.log.info("Finished testing updateRate:" + str(updateRate))
                    main.step("Clear the logs on ONOS before moving to the next updateRate!")
                    clearLogResult = main.CLIs[0].clearLog()
                    utilities.assert_equals(expect=main.TRUE,
                                            actual=clearLogResult,
                                            onpass="Successfully cleared ONOS logs",
                                            onfail="Failed to clear ONOS logs")
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to find the no. of packets to detect the drop attack." )

    def CASE8900( self, main ):
        '''
            Measure detection time for a packet inject attack
            using tcpreplay instead of scapy.
            The testcase assumes that SATS has been configured with
            only the static assignment currently. This testcase will
            then switch it over to the dynamic assignment. Another
            testcase must take care of switching back to static assignment.
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case( "This case measures how many packets 0_0_2 sends until a packet inject attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 (Agg or Core switch) carry out an inject attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send 100 packets per second\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step("First generate the pcap file list to be used for traffic generation.")
        lblTrafficPath = main.lblTrafficPath
        pcapFilesUsedFile = main.pcapFilesUsed
        masterChksums = main.masterChksums
        pcapsToUse = []
        if main.attack == 'drop' and str(main.attacker) == 'aggregate':
            main.log.info("In drop attack at aggregate, therefore don't get results from json file.")
            orderedList = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath)
            pcapsToUse = orderedList
        else:
            main.log.info("Not in drop attack at aggregate, therefore first get results from json file.")
            seedKeys = main.currentSeeds.keys()
            seedKey = seedKeys[0]
            # if main.collusion == 'True':
            #     main.log.info("Use collusion based options.")
            #     pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath,
            #                                                attacker=str(main.colludingPositions[0]),
            #                                                attack='inject',
            #                                                jsonFile=main.detectionTimeCollusionJsonFile,
            #                                                fromJson=True, seedKey=seedKey)
            # else:
            pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath,
                                                           fromJson=True, seedKey=seedKey)
        main.log.info("Got the following list of pcaps to use.")
        main.log.info(pcapsToUse)
        main.log.info("Now set the index for searching through the master checksum file")
        pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapsToUse[0]))
        masterChksumIndexStart = pcapNumber * 100
        main.log.info("Got the pcapNumber as:" + str(pcapNumber) + " and the masterChksumIndexStart as:" + str(masterChksumIndexStart))
        # Now for running the same traffic with the same seed.
        main.step("Now get the current seeds configured on ONOS/SATS.")
        allSeeds = main.seeds
        currentSeeds = main.currentSeeds
        # main.CLIs[0].startOnosCli(main.ONOSip[0])
        currentSeedsOnos = [main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling","pairwiseSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "hashMutatorSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "switchMutatorSeed", short=True)]
        main.log.info("currentSeedsOnos is:" + str(currentSeedsOnos))
        # if currentSeeds != currentSeedsOnos:
        #     main.log.error("currentSeeds:" + str(currentSeeds) + ", currentSeedsOnos:" + str(currentSeedsOnos))

        main.step( "Now clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog()

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )
        # Assume that only 0_0_2 is sending traffic to 1_0_2
        # Therefore the interface = 0_0_2-eth0
        host = '0_0_2'
        interface = host + "-eth0"
        # now first test the static assignment followed by the dynamic assignment.
        for assignment in ['static', 'dynamic']:
            main.log.info("Current assignment is:" + assignment)
            resultsSaved = False
            injectStaticPacketLimit = 10000
            injectDynamicPacketLimit = 100000
            if assignment == 'dynamic':
                main.log.info("Need to switch on hash mutation now. Seed configuration is taken care of in testcase53.")
                main.step("Enable  hash mutation")
                cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                                "hashMutation", "true")
                utilities.assert_equals(expect=main.TRUE,
                                        actual=cfgResult,
                                        onpass="Successfully Enabled pairAssignment",
                                        onfail="Failed to Enable pairAssignment")
                main.log.info("Start the traffic right away.")
            pcapFileList = []
            packetCounter = 0
            for pcapFile in pcapsToUse:
                # Append the pcapFile used for traffic generation in this round.
                pcapFileList.append(pcapFile)
                # start/endSearchIndex are used to keep of track of the range to search in the masterChksums
                tcpreplayCommand = "tcpreplay --preload-pcap -p 100 -i " + interface + " " + pcapFile
                result = main.Mininet1.node(host, tcpreplayCommand)
                print result
                # Sleep for 5 seconds for testing, can reduce to 2 I think.
                main.log.info("Sleep for 4s so that the last sample completes an RTT")
                time.sleep(4)
                packetCounter += 100
                main.log.info("Packets sent so far:" + str(packetCounter))
                dropAttackFound = main.CLIs[0].isDropAttack()
                injectionAttackFound = main.CLIs[0].isInjectionAttack()
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapFile))
                    startSearchIndex = pcapNumber * 100
                    endSearchIndex = pcapNumber * 100 + 99
                    i = startSearchIndex
                    end = endSearchIndex
                    main.log.info("start and end SearchIndex are:" + str(startSearchIndex) + ", " + str(endSearchIndex))
                    while i <= end:
                        chksumValue = int(masterChksums[i]) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            # need to include the seeds used for this detection round.
                            seeds = main.currentSeeds
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( packetsToDetect ) )
                            # Now save the results in the json file.
                            # Data for the detection time json file are the following:
                            # [timestamp, packetsSent], attackType, attackerPosition, assignmentType, hashFunction, samplingRatio
                            timeStamp = time.strftime("%Y%m%d-%H%M%S")
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                            attackType = main.attack
                            attackerPosition = str(main.attacker)
                            assignmentType = assignment
                            # Using index 0 for main.hashFunction and main.samplingRatio, needs to change later.
                            hashFunction = main.hashFunction[0]
                            samplingRatio = main.samplingRatio[0]
                            if main.collusion == 'True':
                                main.log.info("Save collusion results.")
                                main.log.info("Set the attacker position to:" + main.colludingPositions[0])
                                attackerPosition = str(main.colludingPositions[0])
                                # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                                main.saveDetectionTimeCollusionResults.save(detectionResults, attackType, attackerPosition,
                                                                   assignmentType, hashFunction, samplingRatio)
                            else:
                                main.log.info("Save non-collusion results.")
                                # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                                main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio)
                            # Also save the pcap files used for this detection.
                            main.pcapFileHelper.save(pcapFileList)
                            resultsSaved = True
                            break
                        else:
                            i += 1
                    if resultsSaved is not True:
                        main.log.error("Could not save the detection results. Need to repeat this case!")
                    main.log.info("Finished testing assignmentType:" + str(assignment))
                    main.step("Clear the logs on ONOS before moving to the next assignment!")
                    clearLogResult = main.CLIs[0].clearLog()
                    utilities.assert_equals(expect=main.TRUE,
                                            actual=clearLogResult,
                                            onpass="Successfully cleared ONOS logs",
                                            onfail="Failed to clear ONOS logs")
                    break
                else:
                    if (packetCounter >= injectStaticPacketLimit and assignment == 'static' and main.attack == 'inject')\
                            or (packetCounter >= injectDynamicPacketLimit and assignment == 'dynamic' and main.attack == 'inject'):
                        seeds = main.currentSeeds
                        packetsToDetect = None
                        if (assignment == 'static'):
                            main.log.info("static assignment for the inject attack took more than 10000 packets, move on to the dynamic case.")
                        elif (assignment == 'dynamic'):
                            main.log.info("dynamic assignment for the inject attack took more than 100000 packets, move on to the next case.")
                        main.log.info("Save the seeds and pcaps used for this test though.")
                        timeStamp = time.strftime("%Y%m%d-%H%M%S")
                        detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                        attackType = main.attack
                        attackerPosition = str(main.attacker)
                        assignmentType = assignment
                        hashFunction = main.hashFunction[0]
                        samplingRatio = main.samplingRatio[0]
                        if main.collusion == 'True':
                            main.log.info("Save collusion results.")
                            main.log.info("Set the attacker position to:" + main.colludingPositions[0])
                            attackerPosition = str(main.colludingPositions[0])
                            # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                            main.saveDetectionTimeCollusionResults.save(detectionResults, attackType, attackerPosition,
                                                                        assignmentType, hashFunction, samplingRatio)
                        else:
                            main.log.info("Save non-collusion results.")
                            # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                            main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition,
                                                           assignmentType, hashFunction, samplingRatio)
                        # Also save the pcap files used for this detection.
                        main.pcapFileHelper.save(pcapFileList)
                        resultsSaved = True
                        break
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to find the no. of packets to detect the drop attack." )

    def CASE8990( self, main ):
        '''
            Measure detection time for a packet inject attack
            using tcpreplay instead of scapy.
            The testcase assumes that SATS has been configured with
            only the static assignment currently. This testcase will
            immediately switch over to the dynamic assignment. It will
            also only carry out the experiment for different update rates.
            Another testcase must take care of switching back to static assignment.
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case( "This case measures how many packets 0_0_2 sends until a packet inject attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 (Agg or Core switch) carry out an inject attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send 100 packets per second\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step("First generate the pcap file list to be used for traffic generation.")
        lblTrafficPath = main.lblTrafficPath
        pcapFilesUsedFile = main.pcapFilesUsed
        masterChksums = main.masterChksums
        pcapsToUse = []
        assignments = ['dynamic']
        if main.attack == 'drop' and str(main.attacker) == 'aggregate' and assignments[0] == 'static':
            main.log.info("In drop attack at aggregate, therefore don't get results from json file.")
            orderedList = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath)
            pcapsToUse = orderedList
        else:
            main.log.info("Not in drop attack at aggregate, therefore first get results from json file.")
            seedKeys = main.currentSeeds.keys()
            seedKey = seedKeys[0]
            pcapsToUse = main.pcapFileHelper.getPcapsToUse(pcapFilesUsedFile, lblTrafficPath,
                                                           fromJson=True, seedKey=seedKey)
        main.log.info("Got the following list of pcaps to use.")
        main.log.info(pcapsToUse)
        main.log.info("Now set the index for searching through the master checksum file")
        pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapsToUse[0]))
        masterChksumIndexStart = pcapNumber * 100
        main.log.info("Got the pcapNumber as:" + str(pcapNumber) + " and the masterChksumIndexStart as:" + str(masterChksumIndexStart))
        # Now for running the same traffic with the same seed.
        main.step("Now get the current seeds configured on ONOS/SATS.")
        allSeeds = main.seeds
        currentSeeds = main.currentSeeds
        # main.CLIs[0].startOnosCli(main.ONOSip[0])
        currentSeedsOnos = [main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling","pairwiseSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "hashMutatorSeed", short=True),
                            main.CLIs[0].getCfg("org.onosproject.tsamp.TrajectorySampling", "switchMutatorSeed", short=True)]
        main.log.info("currentSeedsOnos is:" + str(currentSeedsOnos))
        # if currentSeeds != currentSeedsOnos:
        #     main.log.error("currentSeeds:" + str(currentSeeds) + ", currentSeedsOnos:" + str(currentSeedsOnos))

        main.step( "Now clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog()

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )
        # Assume that only 0_0_2 is sending traffic to 1_0_2
        # Therefore the interface = 0_0_2-eth0
        host = '0_0_2'
        interface = host + "-eth0"
        # Get teh updateRates
        updateRates = main.updateRate
        main.log.info("Got the following updateRates from the params file:" + str(updateRates))
        # now first test the static assignment followed by the dynamic assignment.
        for updateRate in updateRates:
            # Before starting, disable hashMutation, configure the updateRate and then enable it again.
            resultsSaved = False
            injectStaticPacketLimit = 10000
            main.log.info("Need to switch OFF hash mutation now. Seed configuration is taken care of in testcase53.")
            main.step("Disable  hash mutation")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "hashMutation", "false")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully disabled the hashMutation",
                                    onfail="Failed to disable the hashMutation")
            main.log.info("Now configure the updateRate to:" + str(updateRate))
            main.step("Configure the update rate.")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "updateRate", updateRate)
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully configured the updateRate",
                                    onfail="Failed to configure the updateRate")
            main.log.info("Need to switch ON hash mutation now. Seed configuration is taken care of in testcase53.")
            main.step("Enable  hash mutation")
            cfgResult = main.CLIs[0].setCfg("org.onosproject.tsamp.TrajectorySampling",
                                            "hashMutation", "true")
            utilities.assert_equals(expect=main.TRUE,
                                    actual=cfgResult,
                                    onpass="Successfully enabled the hashMutation",
                                    onfail="Failed to enable the hashMutation")
            main.log.info("Start the traffic right away.")
            pcapFileList = []
            packetCounter = 0
            for pcapFile in pcapsToUse:
                # Append the pcapFile used for traffic generation in this round.
                pcapFileList.append(pcapFile)
                # start/endSearchIndex are used to keep of track of the range to search in the masterChksums
                tcpreplayCommand = "tcpreplay --preload-pcap -p 100 -i " + interface + " " + pcapFile
                result = main.Mininet1.node(host, tcpreplayCommand)
                print result
                # Sleep for 5 seconds for testing, can reduce to 2 I think.
                main.log.info("Sleep for 4s so that the last sample completes an RTT")
                time.sleep(4)
                packetCounter += 100
                main.log.info("Packets sent so far:" + str(packetCounter))
                dropAttackFound = main.CLIs[0].isDropAttack()
                injectionAttackFound = main.CLIs[0].isInjectionAttack()
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    pcapNumber = int(main.pcapFileHelper.getNumberFromPcapFileName(pcapFile))
                    startSearchIndex = pcapNumber * 100
                    endSearchIndex = pcapNumber * 100 + 99
                    i = startSearchIndex
                    end = endSearchIndex
                    main.log.info("start and end SearchIndex are:" + str(startSearchIndex) + ", " + str(endSearchIndex))
                    while i <= end:
                        chksumValue = int(masterChksums[i]) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            # need to include the seeds used for this detection round.
                            seeds = main.currentSeeds
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( packetsToDetect ) )
                            # Now save the results in the json file.
                            # Data for the detection time json file are the following:
                            # [timestamp, packetsSent], attackType, attackerPosition, assignmentType, hashFunction, samplingRatio
                            timeStamp = time.strftime("%Y%m%d-%H%M%S")
                            packetsToDetect = i + 1 - masterChksumIndexStart
                            detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                            attackType = main.attack
                            attackerPosition = str(main.attacker)
                            # assignmentType = assignment
                            assignmentType = assignments[0]
                            # Using index 0 for main.hashFunction and main.samplingRatio, needs to change later.
                            hashFunction = main.hashFunction[0]
                            samplingRatio = main.samplingRatio[0]
                            # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                            main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition, assignmentType, hashFunction, samplingRatio, updateRate=updateRate)
                            # Also save the pcap files used for this detection.
                            main.pcapFileHelper.save(pcapFileList)
                            resultsSaved = True
                            break
                        else:
                            i += 1
                    if resultsSaved is not True:
                        main.log.error("Could not save the detection results. Need to repeat this case!")
                    main.log.info("Finished testing assignmentType:" + str(assignments[0]))
                    main.step("Clear the logs on ONOS before moving to the next assignment!")
                    clearLogResult = main.CLIs[0].clearLog()
                    utilities.assert_equals(expect=main.TRUE,
                                            actual=clearLogResult,
                                            onpass="Successfully cleared ONOS logs",
                                            onfail="Failed to clear ONOS logs")
                    break
                else:
                    if packetCounter >= injectStaticPacketLimit and assignments[0] == 'static' and main.attack == 'inject':
                        seeds = main.currentSeeds
                        packetsToDetect = None
                        main.log.info("static assignment for the inject attack took more than 10000 packets, move on to the dynamic case.")
                        main.log.info("Save the seeds and pcaps used for this test though.")
                        timeStamp = time.strftime("%Y%m%d-%H%M%S")
                        detectionResults = [seeds, timeStamp, packetsToDetect, pcapFileList]
                        attackType = main.attack
                        attackerPosition = str(main.attacker)
                        # assignmentType = assignment
                        assignmentType = assignments[0]
                        hashFunction = main.hashFunction[0]
                        samplingRatio = main.samplingRatio[0]
                        # saveDetectionTimeResults.save takes care of getting the main.updateRate and main.updateSize.
                        main.saveDetectionTimeResults.save(detectionResults, attackType, attackerPosition,
                                                           assignmentType, hashFunction, samplingRatio, updateRate=updateRate)
                        # Also save the pcap files used for this detection.
                        main.pcapFileHelper.save(pcapFileList)
                        resultsSaved = True
                        break
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to find the no. of packets to detect the drop attack." )

    def CASE800(self, main):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case("This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS")
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send 100 packets per second\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        # main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )

        # main.CLIs[ 0 ].clearLog( )
        # attackFound = main.CLIs[ 0 ].isDropAttack( )

        ##        main.step( "First clear the logs on ONOS" )
        ##        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        ##        clearLogResult = main.CLIs[ 0 ].clearLog( )
        ##        utilities.assert_equals( expect=main.TRUE,
        ##                                 actual=clearLogResult,
        ##                                 onpass="Successfully cleared ONOS logs",
        ##                                 onfail="Failed to clear ONOS logs" )

        main.step("Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum")
        ##        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        ##        main.Mininet1.handle.expect( "mininet>" )
        ##        flowTable = main.Mininet1.handle.before
        ##        flowTable = flowTable.split( "\r\n" )
        ##        testChksums = []
        ##        for flow in flowTable:
        ##            main.log.info( "flow:" + str( flow ) )
        ##            if re.search( "dl_vlan", flow ):
        ##                chksumFlow = []
        ##                chksumAlmost = []
        ##                chksumFlow = flow.split( "dl_vlan=" )
        ##                chksumAlmost = chksumFlow[ 1 ].split( " " )
        ##                chksumUse = chksumAlmost[ 0 ]
        ##                main.log.info( "got:" + str( chksumUse ) )
        ##                testChksums.append( int( chksumUse ) )

        pktCounter = 0
        main.step("First clear the logs on ONOS!")
        clearLogResult = main.CLIs[0].clearLog()

        utilities.assert_equals(expect=main.TRUE,
                                actual=clearLogResult,
                                onpass="Successfully cleared ONOS logs",
                                onfail="Failed to clear ONOS logs")

        attackPackets = []
        attackedHashValue = 4096
        index = 0
        for chksum in main.chksums.get(0):
            index += 1
            if index > 1000:
                break
                # for chksum in testChksums:
            chksum = int(chksum) & 4095
            # main.log.info( "Going to send packet with checksum value:" + str( chksum ) )
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str(chksum)
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append(attackPacket)

            # main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
            # clearLogResult = main.CLIs[ 0 ].clearLog( )
            ##                utilities.assert_equals( expect=main.TRUE,
            ##                                 actual=clearLogResult,
            ##                                 onpass="Successfully cleared ONOS logs",
            ##                                 onfail="Failed to clear ONOS logs" )
            # main.log.info( "Attack Packet is:" + str( attackPacket) )
            if len(attackPackets) == 100:
                # if len( attackPackets ) == 100:
                main.step("Send attackPackets")
                scapyResult = main.Mininet1.startAtsScapy("0_0_2", attackPackets)
                utilities.assert_equals(expect=main.TRUE,
                                        actual=scapyResult,
                                        onpass="Successfully sent packets via Scapy",
                                        onfail="Failed to send packets via Scapy")
                # pktCounter += 100
                pktCounter += 100
                main.log.info("Total packets sent: " + str(pktCounter))
                attackPackets[:] = []
                main.log.info("Sleep for 20s so that the last sample completes an RTT")
                time.sleep(20)
                attackFound = main.FALSE
                ##                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info("Drop Attack detected")
                    attackedHashValue = main.CLIs[0].getDropHashValue()
                    main.log.info("Hash value attacked: " + str(attackedHashValue))
                    i = 0
                    # for chksumValue in testChksums:
                    for chksumValue in main.chksums.get(0):
                        i += 1
                        chksumValue = int(chksumValue) & 4095
                        if int(chksumValue) == int(attackedHashValue):
                            main.log.info("The no. of packets till the drop was detected is:" + str(i))
                            resultString = (datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str(i)
                            resultString += "\n"
                            mode = 'a' if os.path.exists(main.detectionTimeLog) else 'w'
                            with open(main.detectionTimeLog, mode) as f:
                                f.write(resultString)
                                break
                    break
                else:
                    main.step("Clear the logs on ONOS!")
                    clearLogResult = main.CLIs[0].clearLog()
                    utilities.assert_equals(expect=main.TRUE,
                                            actual=clearLogResult,
                                            onpass="Successfully cleared ONOS logs",
                                            onfail="Failed to clear ONOS logs")

                    ##        if attackedHashValue == 4096:
                    ##            main.log.error( "Did not find the attacked hash value" )
                    ##            utilities.assert_equals( expect=main.TRUE,
                    ##                             actual=main.FALSE,
                    ##                             onpass="Successfully found the no. of packets to detect the drop attack",
                    ##                             onfail="Failed to find the attacked hash value on a drop attack" )
                    ##        else:

        utilities.assert_equals(expect=main.TRUE,
                                actual=main.TRUE,
                                onpass="Successfully found the no. of packets to detect the drop attack",
                                onfail="Failed to start tcpreplay")

    def CASE801( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 1 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 1 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE802( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 2 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 2 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )


    def CASE803( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 3 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 3 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE804( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 4 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 4 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE805( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 5 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 5 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE806( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 6 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 6 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE807( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 7 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 7 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE808( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 8 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 8 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE809( self, main ):
        '''
            Measure detection time for a packet drop attack
        '''
        import json
        import re
        import os
        import datetime

        main.case( "This case measures how many packets 0_0_2 sends until a packet drop attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out a drop attack on all traffic from 0_0_2.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 9 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                attackFound = main.CLIs[ 0 ].isDropAttack( )
                if attackFound == main.TRUE:
                    main.log.info( "Drop Attack detected" )
                    attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 9 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the drop was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the drop attack",
                                 onfail="Failed to start tcpreplay" )

    def CASE900( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time
        import random

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        #main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )

        #main.CLIs[ 0 ].clearLog( )
        #attackFound = main.CLIs[ 0 ].isDropAttack( )

        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
##        main.step( "First clear the logs on ONOS" )
##        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
##        clearLogResult = main.CLIs[ 0 ].clearLog( )
##        utilities.assert_equals( expect=main.TRUE,
##                                 actual=clearLogResult,
##                                 onpass="Successfully cleared ONOS logs",
##                                 onfail="Failed to clear ONOS logs" )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
##        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
##        main.Mininet1.handle.expect( "mininet>" )
##        flowTable = main.Mininet1.handle.before
##        flowTable = flowTable.split( "\r\n" )
##        testChksums = []
##        for flow in flowTable:
##            main.log.info( "flow:" + str( flow ) )
##            if re.search( "dl_vlan", flow ):
##                chksumFlow = []
##                chksumAlmost = []
##                chksumFlow = flow.split( "dl_vlan=" )
##                chksumAlmost = chksumFlow[ 1 ].split( " " )
##                chksumUse = chksumAlmost[ 0 ]
##                main.log.info( "got:" + str( chksumUse ) )
##                testChksums.append( int( chksumUse ) )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 0 ):
        #for chksum in testChksums:
            chksum = int( chksum ) & 4095
            #main.log.info( "Going to send packet with checksum value:" + str( chksum ) )
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            #main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
            #clearLogResult = main.CLIs[ 0 ].clearLog( )
##                utilities.assert_equals( expect=main.TRUE,
##                                 actual=clearLogResult,
##                                 onpass="Successfully cleared ONOS logs",
##                                 onfail="Failed to clear ONOS logs" )
            #main.log.info( "Attack Packet is:" + str( attackPacket) )
            if len( attackPackets ) == 100:
            #if len( attackPackets ) == 19:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                #pktCounter += 19
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    #for chksumValue in testChksums:
                    for chksumValue in main.chksums.get( 0 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

##        if attackedHashValue == 4096:
##            main.log.error( "Did not find the attacked hash value" )
##            utilities.assert_equals( expect=main.TRUE,
##                             actual=main.FALSE,
##                             onpass="Successfully found the no. of packets to detect the drop attack",
##                             onfail="Failed to find the attacked hash value on a drop attack" )
##        else:

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE901( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 1 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 1 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE902( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 2 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 2 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE903( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 3 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 3 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE904( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 4 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 4 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE905( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 5 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 5 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE906( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 6 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 6 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE907( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 7 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 7 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE908( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 8 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 8 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE909( self, main ):
        '''
            Measure detection time for a packet injection mirror attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection mirror attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection mirror attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert is generated\
        3. If no alert goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the mirror rule with a new attacker hash value" )
        main.updateMirrorAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 9 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )

            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Mirror Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 9 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1000( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )
        testChksums = []
        for flow in flowTable:
            main.log.info( "flow:" + str( flow ) )
            if re.search( "dl_vlan", flow ):
                chksumFlow = []
                chksumAlmost = []
                chksumFlow = flow.split( "dl_vlan=" )
                chksumAlmost = chksumFlow[ 1 ].split( " " )
                chksumUse = chksumAlmost[ 0 ]
                main.log.info( "got:" + str( chksumUse ) )
                testChksums.append( int( chksumUse ) )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 0 ):
        #for chksum in testChksums:
            chksum = int( chksum ) & 4095
            #main.log.info( "Going to send packet with checksum value:" + str( chksum ) )
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
            #if len( attackPackets ) == 19:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                #pktCounter += 19
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    #for chksumValue in testChksums:
                    for chksumValue in main.chksums.get( 0 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1001( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 1 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 1 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1002( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 2 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 2 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1003( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 3 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 3 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1004( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 4 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 4 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1005( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 5 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 5 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1006( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 6 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 6 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1007( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 7 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 7 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1008( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 8 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 8 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

    def CASE1009( self, main ):
        '''
            Measure detection time for a packet injection modification attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet injection modification attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out an injection modification attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"
        main.step( "Before starting update the modification rule with a new attacker hash value" )
        main.updateModificationAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 9 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Injection Modification Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 9 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the injection modification was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the injection attack",
                                 onfail="Failed to find the no. of packets to detect the injection attack" )

###
    def CASE1100( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )
        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )
        main.Mininet1.handle.sendline( "sh ovs-ofctl -O OpenFlow13 dump-flows 0_0_1" )
        main.Mininet1.handle.expect( "mininet>" )
        flowTable = main.Mininet1.handle.before
        flowTable = flowTable.split( "\r\n" )
        testChksums = []
        for flow in flowTable:
            main.log.info( "flow:" + str( flow ) )
            if re.search( "dl_vlan", flow ):
                chksumFlow = []
                chksumAlmost = []
                chksumFlow = flow.split( "dl_vlan=" )
                chksumAlmost = chksumFlow[ 1 ].split( " " )
                chksumUse = chksumAlmost[ 0 ]
                main.log.info( "got:" + str( chksumUse ) )
                testChksums.append( int( chksumUse ) )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 0 ):
        #for chksum in testChksums:
            chksum = int( chksum ) & 4095
            #main.log.info( "Going to send packet with checksum value:" + str( chksum ) )
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
            #if len( attackPackets ) == 19:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                #pktCounter += 19
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    #for chksumValue in testChksums:
                    for chksumValue in main.chksums.get( 0 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1101( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 1 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 1 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1102( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 2 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 2 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1103( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 3 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 3 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1104( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 4 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 4 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1105( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 5 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 5 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1106( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 6 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 6 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1107( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 7 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 7 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1108( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 8 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 8 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )

    def CASE1109( self, main ):
        '''
            Measure detection time for a reroute attack
        '''
        import json
        import re
        import os
        import datetime
        import time

        main.case( "This case measures how many packets 0_0_2 sends until a packet reroute attack is detected by ATS" )
        main.caseExplanation = "0_2_1 or 0_3_1 carry out reroute attack on all traffic from 0_0_2 except what it samples.\
        We want to measure how many packets are sent by 0_0_2 before an alert is generated by the detector.\
        The test stops when an alert is found.\
        1. Send a packet\
        2. Check if an alert (drop + injection) is generated\
        3. If no alerts goto 1 else, stop and report the number of packets sent"

        main.step( "Before starting update the reroute rule with a new attacker hash value" )
        main.updateRerouteAttackFlow.updateFlow( )

        main.step( "Send a packet from 0_0_2 to 1_0_2 using scapy and vlan tag from the lbl traffic checksum" )

        pktCounter = 0
        main.step( "First clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )

        utilities.assert_equals( expect=main.TRUE,
             actual=clearLogResult,
             onpass="Successfully cleared ONOS logs",
             onfail="Failed to clear ONOS logs" )

        attackPackets = []
        attackedHashValue = 4096
        for chksum in main.chksums.get( 9 ):
            chksum = int( chksum ) & 4095
            attackPacket = "Ether(src=\"00:00:00:00:00:02\",dst=\"00:00:00:01:00:02\")/Dot1Q(vlan="
            attackPacket += str( chksum )
            attackPacket += ")/IP(dst=\"10.1.0.2\")/ICMP()"
            attackPackets.append( attackPacket )
            if len( attackPackets ) == 100:
                main.step( "Send attackPackets" )
                scapyResult = main.Mininet1.startAtsScapy( "0_0_2", attackPackets )
                utilities.assert_equals( expect=main.TRUE,
                    actual=scapyResult,
                    onpass="Successfully sent packets via Scapy",
                    onfail="Failed to send packets via Scapy" )
                pktCounter += 100
                main.log.info( "Total packets sent: " + str( pktCounter ) )
                attackPackets[ : ] = []
                main.log.info( "Sleep for 20s so that the last sample completes an RTT" )
                time.sleep( 20 )
                dropAttackFound = main.FALSE
                injectionAttackFound = main.FALSE
                dropAttackFound = main.CLIs[ 0 ].isDropAttack( )
                injectionAttackFound = main.CLIs[ 0 ].isInjectionAttack( )
                if dropAttackFound == main.TRUE or injectionAttackFound == main.TRUE:
                    main.log.info( "Reroute Attack detected" )
                    if injectionAttackFound == main.TRUE:
                        attackedHashValue = main.CLIs[ 0].getInjectionHashValue( )
                    else:
                        attackedHashValue = main.CLIs[ 0].getDropHashValue( )
                    main.log.info( "Hash value attacked: " + str( attackedHashValue ) )
                    i = 0
                    for chksumValue in main.chksums.get( 9 ):
                        i += 1
                        chksumValue = int( chksumValue ) & 4095
                        if int( chksumValue ) == int ( attackedHashValue ):
                            main.log.info( "The no. of packets till the reroute was detected is:" + str ( i ) )
                            resultString = ( datetime.datetime.now().isoformat() + "\n")
                            resultString += "Packets sent,"
                            resultString += str( i )
                            resultString += "\n"
                            mode = 'a' if os.path.exists( main.detectionTimeLog ) else 'w'
                            with open( main.detectionTimeLog, mode ) as f:
                                f.write( resultString )
                                break
                    break
                else:
                    main.step( "Clear the logs on ONOS!" )
                    clearLogResult = main.CLIs[ 0 ].clearLog( )
                    utilities.assert_equals( expect=main.TRUE,
                                     actual=clearLogResult,
                                     onpass="Successfully cleared ONOS logs",
                                     onfail="Failed to clear ONOS logs" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully found the no. of packets to detect the reroute attack",
                                 onfail="Failed to find the no. of packets to detect the reroute attack" )


###
    def CASE90( self, main ):
        '''
            Report Detection Rate
        '''
        import datetime
        import os

        main.log.info("Detection Statistics: \n" )
        detectionResults = main.ONOSbench.detectionReport( main.ONOSip[ 0 ],
                                  [ "\"Average Handling time\"",
                                    "\"Average Detection time\"",
                                    "\"The average thoughput\"" ] )
        main.log.info( detectionResults )

        resultString = ( datetime.datetime.now().isoformat() + "\n")
        resultString += ( "Detectors, " )
        resultString += ( str( detectionResults[ 3 ] ) )
        resultString += ( "\n" )
        resultString += ( "Average Throughput, " )
        resultString += ( detectionResults[ 2 ] )
        resultString += ( "\n" )
        throughputPath = '/home/user/TestON/logs/detectionPerfResults/'

        try:
            os.mkdir( throughputPath )
        except:
            if not os.path.isdir( throughputPath ):
                raise

        throughputLog = '/home/user/TestON/logs/detectionPerfResults/throughput'
        mode = 'a' if os.path.exists( throughputLog ) else 'w'
        with open( throughputLog, mode ) as f:
            f.write( resultString )
        #resultString += (str(clusterCount) + ",")
        #resultString += (str(n) + ",")
        #resultString += (str(avgTP) + "," + str(stdTP) + "\n")
        #resultsLog.write(resultString)
        #resultsLog.close()

    def CASE100( self, main ):
        '''
            Report errors/warnings/exceptions
        '''
        main.log.info("Error report: \n" )
        main.ONOSbench.logReport( main.ONOSip[ 0 ],
                                  [ "INFO",
                                    "FOLLOWER",
                                    "WARN",
                                    "flow",
                                    "ERROR",
                                    "Except" ],
                                  "s" )
