class SATSperf:

    def __init__( self ):
        self.default = ''

    def CASE1( self, main ):
        import json
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
        main.trajectoryThroughputPath = '/home/mininet/TestON/logs/detectionPerfResults/'
        main.trajectoryThroughputFile = main.trajectoryThroughputPath + 'trajectoryThroughput.json'
        main.detectors = ['1', '2', '4', '6', '8']
        main.currentDetector = ''
#        main.swDPID = main.params[ 'TEST' ][ 'swDPID' ]
        main.cellData = {} # for creating cell file
        main.CLIs = []
        main.ONOSip = []

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
        main.log.info( "Create trajectory through results directory and file" )
        try:
            os.mkdir( main.trajectoryThroughputPath )
        except:
            if not os.path.isdir( main.trajectoryThroughputPath ):
                raise
        if os.path.isfile(main.trajectoryThroughputFile) is True:
            main.log.info("trajectoryThroughput.json file exists")
        else:
            main.log.info("Need to create the trajectoryThroughput json file.")
            trajectoryThroughputDict = dict.fromkeys(main.detectors, [])
            with open(main.trajectoryThroughputFile, 'w') as fp:
                json.dump(trajectoryThroughputDict, fp, sort_keys=True, indent=4)


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
        import time

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

    def CASE35( self, main ):
        '''
            Start Mininet with 5switch topology
        '''
        import json

        main.case( "Setup mininet for 5switch topology" )
        main.caseExplanation = "Start mininet with 5switch topology."

        main.step( "Setup Mininet 5 switch Topology" )
        topology = main.Mininet1.home + '/custom/' + main.topology2
        #main.Mininet1.stopNet( )
        stepResult = main.Mininet1.startNet( topoFile=topology )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully loaded topology",
                                 onfail="Failed to load topology" )

    def CASE310( self, main ):
        '''
            Start Mininet with 10switch topology
        '''
        import json

        main.case( "Setup mininet for 10switch topology" )
        main.caseExplanation = "Start mininet with 10switch topology."

        main.step( "Setup Mininet 10 switch Topology" )
        topology = main.Mininet1.home + '/custom/' + main.topology3
        #main.Mininet1.stopNet( )
        stepResult = main.Mininet1.startNet( topoFile=topology )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully loaded topology",
                                 onfail="Failed to load topology" )

    def CASE36( self, main ):
        '''
            Ping hosts (h1<->h3) in Mininet topology
        '''
        import json

        main.case( "Ping hosts across the network to install flows." )
        main.caseExplanation = "Simple ping test between hosts across the network."

        main.step( "Ping test" )
        stepResult = main.Mininet1.pingallHosts( [ 'h1','h3' ], "4" )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=stepResult,
                                 onpass="Successfully pinged hosts",
                                 onfail="Failed to ping hosts" )

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

    def CASE51( self, main ):
        '''
            Configure 1 Detector
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure 1 detectors in  tsamp" )
        main.caseExplanation = "Set the number of detectors (threads) to 1."

        main.step( "Configure detectors in tsamp." )
        main.currentDetector = '1'
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "detectors", "1" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured 1 detector",
                                 onfail="Failed to configure 1 detector" )

    def CASE52( self, main ):
        '''
            Configure 2 Detectors
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure 2 detectors in  tsamp" )
        main.caseExplanation = "Set the number of detector (threads) to 2."

        main.step( "Configure detectors in tsamp." )
        main.currentDetector = '2'
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "detectors", "2" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured 2 detectors",
                                 onfail="Failed to configure 2 detectors" )

    def CASE54( self, main ):
        '''
            Configure 4 Detectors
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure 4 detectors in  tsamp" )
        main.caseExplanation = "Set the number of detector (threads) to 4."

        main.step( "Configure detectors in tsamp." )
        main.currentDetector = '4'
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "detectors", "4" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured 4 detectors",
                                 onfail="Failed to configure 4 detectors" )

    def CASE56( self, main ):
        '''
            Configure 6 Detectors
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure 6 detectors in  tsamp" )
        main.caseExplanation = "Set the number of detector (threads) to 6."

        main.step( "Configure detectors in tsamp." )
        main.currentDetector = '6'
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "detectors", "6" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured 6 detectors",
                                 onfail="Failed to configure 6 detectors" )

    def CASE58( self, main ):
        '''
            Configure 8 Detectors
        '''
        import json
        import time
        assert main.CLIs, "main.CLIs not defined"

        cfgResult = main.FALSE
        main.numCtrls = int( main.maxNodes )
        main.case( "Configure 8 detectors in  tsamp" )
        main.caseExplanation = "Set the number of detector (threads) to 8."

        main.step( "Configure detectors in tsamp." )
        main.currentDetector = '8'
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        cfgResult = main.CLIs[ 0 ].setCfg( "org.onosproject.tsamp.TrajectorySampling",
                                           "detectors", "8" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured 8 detectors",
                                 onfail="Failed to configure 8 detectors" )

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
                                           "flowTimeout", "3600" )
        utilities.assert_equals( expect=main.TRUE,
                                 actual=cfgResult,
                                 onpass="Successfully configured the flowTimeout",
                                 onfail="Failed to configure the flowTimeout in fwd" )

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
        main.step( "But first clear the logs on ONOS!" )
        clearLogResult = main.CLIs[ 0 ].clearLog( )
        utilities.assert_equals(expect=main.TRUE,
                                actual=clearLogResult,
                                onpass="Successfully cleared the logs on ONOS",
                                onfail="Failed to clear the logs on ONOS.")
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

    def CASE81( self, main ):
        '''
            Traffic generation for testing 1
            detector threads using
            20packetsPath5Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 1 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=500" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE82( self, main ):
        '''
            Traffic generation for testing 2
            detector threads using
            20packetsPath5Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 2 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=1000" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE84( self, main ):
        '''
            Traffic generation for testing 4
            detector threads using
            20packetsPath5Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 4 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=2000" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE86( self, main ):
        '''
            Traffic generation for testing 6
            detector threads using
            20packetsPath5Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 6 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.thread6Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=5000" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE88( self, main ):
        '''
            Traffic generation for testing 8
            detector threads using
            20packetsPath5Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 8 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.thread8Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=5000" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE101( self, main ):
        '''
            Traffic generation for testing 1
            detector threads using
            40packetsPath10Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 1 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.path10thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=25" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE102( self, main ):
        '''
            Traffic generation for testing 2
            detector threads using
            40packetsPath10Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 2 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.path10thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=50" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE104( self, main ):
        '''
            Traffic generation for testing 4
            detector threads using
            40packetsPath10Threads124.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 4 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.path10thread124Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=100" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE106( self, main ):
        '''
            Traffic generation for testing 6
            detector threads using
            30packetsPath10Threads6.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 6 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.path10thread6Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=200" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )

    def CASE108( self, main ):
        '''
            Traffic generation for testing 8
            detector threads using
            40packetsPath5Threads8.pcapng
        '''
        import json

        main.case( "h1 uses tcpreplay for traffic to h3." )
        main.caseExplanation = "Use tcpreplay from h1 to send to h3."

        main.step( "tcpreplay on h1 to test 8 threads" )
        main.log.info( "Creating host components" )
        main.Mininet1.createHostComponent( "h1" )
        main.h1.startHostCli()
        main.log.info( "Going to start tcpreplay on h1 now" )
        #tcpreplay -q --pps-multi=100 --preload-pcap --pps=100 --loop=1000 --limit=1000 --intf1=h1-eth0 8packets1k2k3k4k.pcapng
        tcpreplayResult = main.h1.startTcpreplay( "h1", main.dependencyPath + main.path10thread8Pcap,
                                                   "-q --pps-multi=100 --preload-pcap --pps=100 --loop=200" )
        main.log.info( main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" ) )
        #jsonFlowTable = main.Mininet1.getFlowTable( main.Mininet1.getSwitch ( ), "1.3" )
        main.Mininet1.removeHostComponent( "h1" )
        main.log.info( "Sleep for a bit so that the detector completes all detections" )
        time.sleep( main.tcpreplaySleep )

        utilities.assert_equals( expect=main.TRUE,
                                 actual=tcpreplayResult,
                                 onpass="Successfully started tcpreplay",
                                 onfail="Failed to start tcpreplay" )


    def CASE90( self, main ):
        '''
            Report Detection Rate
        '''
        import json
        import re

        main.log.info("Detection Statistics: \n" )
        # detectionResults = main.ONOSbench.detectionReport( main.ONOSip[ 0 ],
        #                           [ "\"Average Handling time\"",
        #                             "\"Average Detection time\"",
        #                             "\"The average thoughput\"" ] )
        main.CLIs[ 0 ].startOnosCli( main.ONOSip[ 0 ] )
        detectionResults = main.CLIs[0].getTrajectoryThroughput( ["\"Average Handling time\"",
                                    "\"Average Detection time\"",
                                    "\"The average thoughput\""])
        main.log.info( detectionResults )
        # throughputPath = '/home/mininet/TestON/logs/detectionPerfResults/'
        main.log.info("Now save the trajectory throughput results")
        # Structure of the trajectoryThroughputFile
        # {
        #     "1": { <-- Detectors
        #         [] <-- Trajectory Throughput
        #         }
        # }
        jsonData = json.loads(open(main.trajectoryThroughputFile).read())
        main.log.info("jsonData for trajectoryThroughput is:" + str(jsonData))
        temp = jsonData[main.currentDetector]
        main.log.info("existing detector throughputs are:" + str(temp))
        # throughputs = re.findall(r'^\d+\.?\d*$', detectionResults[2])
        # temp.append(throughputs[0])
        # temp.append(re.sub(r'/(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]/', '', throughput))
        throughput = detectionResults[2].partition('.')
        # throughput = throughput.rstrip('\\u001b[m')
        temp.append(throughput[0])
        jsonData[main.currentDetector] = temp
        with open(main.trajectoryThroughputFile, 'w') as fp:
            json.dump(jsonData, fp, sort_keys=True, indent=4)
        main.log.info("Trajectory throughput results saved.")


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
