def __init__( self ):
    self.default = ''

def updateFlow( ):
        '''
            Helper routine to update the attacking flow rule on the attackers switch
        '''
        import json
        import random

        if main.attacker == "aggregate":
            inputPort0_2_1 = main.Mininet1.getFlowInputPort( "0_2_1" )
            inputPort0_3_1 = main.Mininet1.getFlowInputPort( "0_3_1" )
            outputPort0_2_1 = main.Mininet1.getFlowOutputPort( "0_2_1" )
            outputPort0_3_1 = main.Mininet1.getFlowOutputPort( "0_3_1" )
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
        elif main.attacker == "core":
            outputPort4_1_1 = main.Mininet1.getFlowOutputPort( "4_1_1" )
            outputPort4_1_2 = main.Mininet1.getFlowOutputPort( "4_1_2" )
            outputPort4_2_1 = main.Mininet1.getFlowOutputPort( "4_2_1" )
            outputPort4_2_2 = main.Mininet1.getFlowOutputPort( "4_2_2" )
            inputPort4_1_1 = main.Mininet1.getFlowInputPort( "4_1_1" )
            inputPort4_1_2 = main.Mininet1.getFlowInputPort( "4_1_2" )
            inputPort4_2_1 = main.Mininet1.getFlowInputPort( "4_2_1" )
            inputPort4_2_2 = main.Mininet1.getFlowInputPort( "4_2_2" )
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
