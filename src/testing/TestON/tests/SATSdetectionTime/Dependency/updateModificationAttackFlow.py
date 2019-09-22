def __init__( self ):
    self.default = ''

def updateFlow( ):
        '''
            Helper routine to update the attacking flow rule on the attackers switch
        '''
        import json
        import random

        if main.attacker == "aggregate":
            outputPort0_2_1 = main.Mininet1.getFlowOutputPort( "0_2_1" )
            outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1" )
            main.attackerHashValue = str( random.randint( 0, 4095 ) )
            if outputPort0_2_1 != '':
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort0_2_1
                stepResult = main.Mininet1.addFlow( [ "0_2_1" ], version="1.3", flowcmd=flowRule )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="0_2_1 configured to emulate an injection attack that modifies traffic",
                                         onfail="0_2_1 not configured to emulate an injection attack that modifies traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" ) 
            else:
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort0_3_1
                stepResult = main.Mininet1.addFlow( [ "0_3_1" ], version="1.3", flowcmd=flowRule)
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="0_3_1 configured to emulate an injection attack that modifies traffic",
                                         onfail="0_3_1 not configured to emulate an injection attack that modifies traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "0_3_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "0_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" ) 
        elif main.attacker == "core":
            outputPort4_1_1 = main.Mininet1.getFlowOutputPort( "4_1_1" )
            outputPort4_1_2 = main.Mininet1.getFlowOutputPort( "4_1_2" )
            outputPort4_2_1 = main.Mininet1.getFlowOutputPort( "4_2_1" )
            outputPort4_2_2 = main.Mininet1.getFlowOutputPort( "4_2_2" )
            main.attackerHashValue = str( random.randint( 0, 4095 ) )
            if outputPort4_1_1 != '':
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_1_1
                stepResult = main.Mininet1.addFlow( [ "4_1_1" ], version="1.3", flowcmd=flowRule )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="4_1_1 configured to emulate an injection attack that modifies traffic",
                                         onfail="4_1_1 not configured to emulate an injection attack that modifies traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2", "4_2_1", "4_2_2" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )

            elif outputPort4_1_2 != '':
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_1_2
                stepResult = main.Mininet1.addFlow( [ "4_1_2" ], version="1.3", flowcmd=flowRule )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="4_1_2 configured to emulate an injection attack that modifiess traffic",
                                         onfail="4_1_2 not configured to emulate an injection attack that modifiess traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_2" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_2_1", "4_2_2" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" ) 
            elif outputPort4_2_1 != '':
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_2_1
                stepResult = main.Mininet1.addFlow( [ "4_2_1" ], version="1.3", flowcmd=flowRule )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="4_2_1 configured to emulate an injection attack that modifiess traffic",
                                         onfail="4_2_1 not configured to emulate an injection attack that modifiess traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_1_2", "4_2_2" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" ) 
            elif outputPort4_2_2 != '':
                main.log.info( "Configure flow rule that changes the Vlan ID and forwards the packet along the correct path." )
                stepResult = main.TRUE
                flowRule = "priority=40002,dl_type=0x0800,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02," +\
                                        "actions=pop_vlan,push_vlan:0x8100,set_field:" + main.attackerHashValue + "-\\>vlan_vid,output:" + outputPort4_2_2
                stepResult = main.Mininet1.addFlow( [ "4_2_2" ], version="1.3", flowcmd=flowRule )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="4_2_2 configured to emulate an injection attack that modifiess traffic",
                                         onfail="4_2_2 not configured to emulate an injection attack that modifiess traffic" )
                main.log.info( "Now to check if the flows are installed" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_2_2" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.TRUE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" )
                main.log.info( "Now to make sure that flows are not installed on other switches" )
                stepResult = main.Mininet1.checkAttackFlows( [ "4_1_1", "4_1_2", "4_2_1" ], "dl_src=00:00:00:00:00:02,dl_dst=00:00:00:01:00:02 actions=strip_vlan" )
                utilities.assert_equals( expect=main.FALSE,
                                         actual=stepResult,
                                         onpass="Successfully installed attack flows",
                                         onfail="Failed to install attack flows" ) 
