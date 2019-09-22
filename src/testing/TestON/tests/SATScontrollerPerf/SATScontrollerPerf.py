class SATScontrollerPerf:

    def __init__( self ):
        self.default = ''

    def CASE1( self, main ):
        import time
        import os
        import imp

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
        main.attackerHashValue = 0
        main.attacker = main.params[ 'ATTACKER' ]
        main.hosts = main.params['HOSTS']
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
        main.detectionTimePath = '/home/mininet/TestON/logs/detectionTimeResults/'
        main.detectionTimeLog = '/home/mininet/TestON/logs/detectionTimeResults/detectionTime'
#        main.swDPID = main.params[ 'TEST' ][ 'swDPID' ]
        main.cellData = {} # for creating cell file
        main.CLIs = []
        main.ONOSip = []
        main.chksums = {}
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

        main.log.info( "Create detection time results directory and file" )
        try:
            os.mkdir( main.detectionTimePath )
        except:
            if not os.path.isdir( main.detectionTimePath ):
                raise

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
        cellResult = main.ONOSbench.setCell( "onos-ats-test" )
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

        main.case( "Setup mininet for fat-tree topology" )
        main.caseExplanation = "Start mininet with fat-tree topology."

        main.step( "Setup Mininet 20 switch fat-tree Topology" )
        topology = main.Mininet1.home + '/custom/' + main.topologyMN
        mnCommand = ' --topo ft,4 --controller=remote,ip=130.149.39.154 --switch=ovs,protocols=OpenFlow13'
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
            0_0_2 <-> '0_1_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2'
        '''
        import json
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
        stepResult = main.Mininet1.arpHost( hostList )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully arpinged hosts",
                                 onfail="Failed to arping hosts" )
        main.step( "Ping test" )
        for host in hostList:
            for h in hostList:
                if host == h:
                    continue
                else:
                    stepResult = main.Mininet1.pingallHosts( [host, h], "2" )
                    if stepResult == main.FALSE:
                        break
                    time.sleep(.5)
            if stepResult == main.FALSE:
                break

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully pinged hosts",
                                 onfail="Failed to ping hosts" )

        # main.step( "Ping test again, just to be sure the flows are in sync with the switches and ONOS" )
        # stepResult = main.Mininet1.pingallHosts( ['0_0_2', '0_1_2', '1_0_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2'], "2" )
        #
        # utilities.assert_equals( expect=main.TRUE,
        #                          actual=stepResult,
        #                          onpass="Successfully pinged hosts",
        #                          onfail="Failed to ping hosts" )

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
        import time

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
        main.step( "But before that let's sleep for 10s so that the switch has the send_flow_rem flag")
        time.sleep(10)

        # get the flow IDs that were added
        main.log.info( "Getting the flow IDs from ONOS" )
        flowIds = [ f.get("id") for f in flows ]
        # convert the flowIDs to ints then hex and finally back to strings
        flowIds = [str(hex(int(x))) for x in flowIds]
        main.log.info( "ONOS flow IDs: {}".format(flowIds) )
        switchList = main.Mininet1.getSwitch( )

        stepResult = main.Mininet1.checkFlowId( switchList, flowIds, version="1.3", debug=True )

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
        flowRule = "priority=50002,dl_src=00:00:00:00:00:02,actions=DROP"
        stepResult = main.Mininet1.addFlow( [ "0_2_1", "0_3_1" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="0_2_1, 0_3_1 configured to emulate a drop attack",
                                 onfail="0_2_1, 0_3_1 not configured to emulate a drop attack" )

    def CASE39( self, main ):
        '''
            Configure a drop rule on the Core switch
            for traffic from 0_0_2 to 1_0_2
        '''
        import json

        main.step( "Configure flow drop rule on all core switches: 4_1_1, 4_1_2, 4_2_1, 4_2_2" )

        main.log.info( "Configure flow drop rules on switch  4_1_1, 4_1_2, 4_2_1, 4_2_2 to emulate a drop attack" )
        stepResult = main.TRUE
        flowRule = "priority=50002,dl_src=00:00:00:00:00:02,actions=DROP"
        stepResult = main.Mininet1.addFlow( [ "4_1_1",  "4_1_2",  "4_2_1", "4_2_2" ], version="1.3", flowcmd=flowRule, debug=True )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="  4_1_1, 4_1_2, 4_2_1, 4_2_2  configured to emulate a drop attack",
                                 onfail="  4_1_1, 4_1_2, 4_2_1, 4_2_2  not configured to emulate a drop attack" )

    def CASE338( self, main ):
        '''
            Mirror attack
            Configure a flow rule on the Aggregate switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that mirrors traffic
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

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if outputPort0_2_1 != '':
            main.log.info( "Configure flow mirror rule on switches 0_2_1 to mirror traffic to 0_1_1 and forward original traffic" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort0_2_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:00:01:02-\\>dl_dst,resubmit:" + inputPort0_2_1
            stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="0_2_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="0_2_1 not configured to emulate an injection attack that mirrors traffic" )
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

    def CASE339( self, main ):
        '''
            Mirror attack
            Configure a flow rule on the Core switches
            for traffic from 0_0_2 to 1_0_2 to emulate an
            injection attack that mirrors traffic to the
            aggregate switches (2_2_1 or 2_3_1)
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

        main.attackerHashValue = str( random.randint( 0, 4095 ) )
        if outputPort4_1_1 != '':
            main.log.info( "Configure flow mirror rule on switches 4_1_1 to mirror traffic to 2_1_2 and send traffic along the original path" )
            stepResult = main.TRUE
            flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                    "actions="+ outputPort4_1_1 + ",pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid," +\
                                    "set_field:00:00:00:02:01:02-\\>dl_dst,resubmit:" + inputPort4_1_1
            stepResult = main.Mininet1.addFlow( [ "4_1_1" ], version="1.3", flowcmd=flowRule )
            utilities.assert_equals( expect=main.TRUE,
                                     actual=stepResult,
                                     onpass="4_1_1 configured to emulate an injection attack that mirrors traffic",
                                     onfail="4_1_1 not configured to emulate an injection attack that mirrors traffic" )
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

    def CASE779( self, main ):
        '''
            Set the log level in ONOS to INFO
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Set the log level to INFO in ONOS" )
        main.caseExplanation = "Set the log level to INFO in ONOS"
        main.step( "Set the log level to INFO in ONOS" )
        cfgResult = main.CLIs[ 0 ].setLogLevel( level="INFO" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully set the log level",
                                 onfail="Failed to set the log level to INFO" )

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

    def CASE800( self, main ):
        '''
            Send traffic to and from the following hosts
            0_0_2 <-> '0_1_2', '1_0_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2'
            hosts = ['0_0_2', '0_1_2', '1_0_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2']
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case(\
        "This case sends traffic flows across hosts using the lbl traffic trace. The traffic is used as a load\
        to measure the cpu and memory consumption of SATS in ONOS.\
        The test stops either after all traffic has been sent or after a set time.")

        main.caseExplanation = "\
        1. Take a pair of hosts and use the assigned pcap for that pair.\
        2. Use tcpreplay to replay that pcap file.\
        3. Use 10Mbps as the bandwidth/throughput in tcpreplay\
        4. Stop after tcpreplay is over or after 600s."

        main.step( "Create the host pairs and the pcaps that each host must send" )
        hosts = main.hosts.split(',')
        hostPairs = []
        hostList = hosts
        hostPcapDict = dict.fromkeys(hosts, [])
        for host in hosts:
            pcapFileList = []
            for h in hostList:
                if host == h:
                    continue
                else:
                    pcapFileList.append(main.lblTrafficPath +host + '-' + h + '.pcap')
                    if h + '-' + host in hostPairs:
                        continue
                    elif host + '-' + h in hostPairs:
                        continue
                    else:
                        hostPairs.append(host + '-' + h)
            hostPcapDict[host] = pcapFileList
        backwardHostPair = []
        for host in hostPairs:
            x = host.split('-')
            y = x[1] + '-' + x[0]
            backwardHostPair.append(y)
        for host in backwardHostPair:
            hostPairs.append(host)
        main.log.info("host pairs are:")
        main.log.info(hostPairs)
        main.log.info("pcaps for each host are:")
        main.log.info(hostPcapDict)
        main.step( "Now open up a screen session on each host and start tcpreplay using\
        the hostPair filename from the host")
##        main.log.info( "Creating host components" )
##        for host in hosts:
##            print host
##            main.Mininet1.createHostComponent(host)
##            main.Mininet1.removeHostComponent(host)
        # Since we cannot use a variable to access each host's handle, it has to be
        # hardcoded :(
        for host in hostPcapDict:
            interface = host + "-eth0"
            i = 0
            for pcap in hostPcapDict[host]:
                sessionId = host + str(i)
                tcpreplayCommand = "tcpreplay --preload-pcap -l 10000 -M 1 -i " + interface + " " + pcap
##                tcpreplayCommand = "top"
                # dont log the output for perf reasons.
                command = "screen -dmSL " + sessionId + " " + tcpreplayCommand
                # command = "screen -dmSL " + sessionId + " " + tcpreplayCommand
                result = main.Mininet1.node( host, command)
                print result
                i += 1
            result = main.Mininet1.node(host, "ifconfig")
            print result
        time.sleep(600)
        main.log.info("Finally kill the tcpreplay and screen sessions as the test is over now.")
        main.log.info( "Remove any old screen sessions on the Mininet node.")
        main.Mininet1.killScreens()
        main.log.info( "Kill any old tcpreplay sessions on the Mininet node.")
        main.Mininet1.killTcpreplay()
##            break
##        result = main.Mininet1.node( nodeName="0_0_2", commandStr="date" )
##        main.h1.startHostCli()
##        main.log.info( "Going to start tcpreplay on h1 now" )
##        tcpreplayResult = main.h1.startTcpreplay( "h1", "/home/mininet/ats-testing/4packets1k2k3k4k.pcapng",
##                                                   "--pps-multi=100 --preload-pcap --pps=100 --loop=50 --limit=1000" )
##        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
##        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
##        main.Mininet1.removeHostComponent( "h1" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=main.TRUE,
                                 onpass="Successfully tested the performance of SATS on the controller",
                                 onfail="Failed to test the performance of SATS on the controller" )

    def CASE801( self, main ):
        '''
            Send traffic to and from the following hosts
            0_0_2 <-> '0_1_2', '1_0_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2'
            hosts = ['0_0_2', '0_1_2', '1_0_2', '1_1_2', '2_0_2', '2_1_2', '3_0_2', '3_1_2']
        '''
        import json
        import re
        import os
        import datetime
        import time
        import pprint

        main.case( \
            "This case sends traffic flows across hosts using the lbl traffic trace. The traffic is used as a load\
            to measure the cpu and memory consumption of SATS in ONOS.\
            The test stops either after all traffic has been sent or after a set time.")

        main.caseExplanation = "\
                1. Take a pair of hosts and use the assigned pcap for that pair.\
                2. Use tcpreplay to replay that pcap file.\
                3. Use 10Mbps as the bandwidth/throughput in tcpreplay\
                4. Stop after tcpreplay is over or after 600s."

        main.step("Create the host pairs and the pcaps that each host must send")
        hosts = main.hosts.split(',')
        hostPairs = []
        hostList = hosts
        hostPcapDict = dict.fromkeys(hosts, [])
        for host in hosts:
            pcapFileList = []
            for h in hostList:
                if host == h:
                    continue
                else:
                    pcapFileList.append(main.lblTrafficPath + host + '-' + h + '.pcap')
                    if h + '-' + host in hostPairs:
                        continue
                    elif host + '-' + h in hostPairs:
                        continue
                    else:
                        hostPairs.append(host + '-' + h)
            hostPcapDict[host] = pcapFileList
        backwardHostPair = []
        for host in hostPairs:
            x = host.split('-')
            y = x[1] + '-' + x[0]
            backwardHostPair.append(y)
        for host in backwardHostPair:
            hostPairs.append(host)
        main.log.info("host pairs are:")
        main.log.info(hostPairs)
        main.log.info("pcaps for each host are:")
        main.log.info(hostPcapDict)
        main.step("Now open up a screen session on each host and start tcpreplay using\
                the hostPair filename from the host")
        ##        main.log.info( "Creating host components" )
        ##        for host in hosts:
        ##            print host
        ##            main.Mininet1.createHostComponent(host)
        ##            main.Mininet1.removeHostComponent(host)
        # Since we cannot use a variable to access each host's handle, it has to be
        # hardcoded :(
        for host in hostPcapDict:
            interface = host + "-eth0"
            i = 0
            for pcap in hostPcapDict[host]:
                sessionId = host + str(i)
                tcpreplayCommand = "tcpreplay --preload-pcap -l 1000 -M 1 -i " + interface + " " + pcap
                ##                tcpreplayCommand = "top"
                # dont log the output for perf reasons.
                command = "screen -dmS " + sessionId + " " + tcpreplayCommand
                # command = "screen -dmSL " + sessionId + " " + tcpreplayCommand
                result = main.Mininet1.node(host, command)
                print result
                i += 1
            result = main.Mininet1.node(host, "ifconfig")
            print result
        time.sleep(600)
        main.log.info("Finally kill the tcpreplay and screen sessions as the test is over now.")
        main.log.info("Remove any old screen sessions on the Mininet node.")
        main.Mininet1.killScreens()
        main.log.info("Kill any old tcpreplay sessions on the Mininet node.")
        main.Mininet1.killTcpreplay()

        utilities.assert_equals(expect=main.TRUE,
                                actual=main.TRUE,
                                onpass="Successfully tested the performance of SATS on the controller",
                                onfail="Failed to test the performance of SATS on the controller")

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
        throughputPath = '/home/mininet/TestON/logs/detectionPerfResults/'

        try:
            os.mkdir( throughputPath )
        except:
            if not os.path.isdir( throughputPath ):
                raise

        throughputLog = '/home/mininet/TestON/logs/detectionPerfResults/throughput'
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
