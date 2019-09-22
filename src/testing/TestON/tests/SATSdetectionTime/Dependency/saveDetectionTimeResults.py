def __init__( self ):
    self.default = ''


def save( detectionResults, attackType, attackerPosition, assignmentType, hashFunction,
                       samplingRatio, updateRate='2', updateSize='2'):
    '''
        Save the detection time results in the json file using the provided
        parameters
    '''
    import os, pprint, json
    main.log.info("Now save the detection time results")
    attackPositionDict = dict.fromkeys(main.attackerPositions, dict.fromkeys(main.attackTypes, []))
    assignmentDict = dict.fromkeys(['dynamic'], None)
    assignmentDict['dynamic'] = dict.fromkeys(updateRate, dict.fromkeys(updateSize, attackPositionDict))
    dictForNewUpdateRate = assignmentDict['dynamic']
    # attackPositionDict = dict.fromkeys([u'aggregate', u'core'], dict.fromkeys([u'drop', u'inject'], []))
    # updateRateDict = dict.fromkeys(updateRate, dict.fromkeys(updateSize, attackPositionDict))
    # Structure of the detection time results
    # {
    #     "0.0046": { <-- Sampling Ratio
    #         "payload": { <-- Hash Function
    #             "dynamic": { <-- Assignment
    #                 "2": { <-- Update Rate
    #                     "2": { <-- Update Size
    #                         "aggregate": { <-- Attacker Position
    #                             "drop": [], <-- Attack Type: detectionResults = [timeStamp, packetsSent]
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
    # Need to traverse through the dictionary and append the results
    # to the apt (key, value).
    # begin by reading the existing detection time file
    # pprint.pprint(jsonData)
    jsonData = dict(json.loads(open(main.detectionTimeJsonFile).read()))
    if jsonData.has_key(samplingRatio) is False:
        # Create this dict based on the parameters passed to save()
        main.log.info("New sampling ratio introduced. Create the data structure for it.")
        attackPositionDict = dict.fromkeys(main.attackerPositions, dict.fromkeys(main.attackTypes, []))
        pprint.pprint(attackPositionDict)
        assignmentDict = dict.fromkeys(['static', 'dynamic'], None)
        for assignment in assignmentDict.keys():
            if assignment == 'static':
                assignmentDict[assignment] = attackPositionDict
            elif assignment == 'dynamic':
                updateRateDict = dict.fromkeys(updateRate, dict.fromkeys(updateSize, attackPositionDict))
                assignmentDict[assignment] = updateRateDict
        pprint.pprint(assignmentDict)
        detectionTimeDict = dict.fromkeys([samplingRatio], dict.fromkeys([hashFunction], assignmentDict))
        pprint.pprint(detectionTimeDict)
        jsonData[samplingRatio] = detectionTimeDict[samplingRatio]
        with open(main.detectionTimeJsonFile, 'w') as fp:
            json.dump(jsonData, fp, sort_keys=True, indent=4)
        main.log.info("Introduced the new sampling ratio into the detectionTime Results file.")
    else:
        main.log.info("Sampling ratio already exists in the detectionTime results file.")
    if assignmentType == 'static':
        jsonData = dict(json.loads(open(main.detectionTimeJsonFile).read()))
        temp = jsonData[samplingRatio][hashFunction][assignmentType][attackerPosition][attackType]
        temp.append(detectionResults)
        jsonData[samplingRatio][hashFunction][assignmentType][attackerPosition][attackType] = temp
        with open(main.detectionTimeJsonFile, 'w') as fp:
            json.dump(jsonData, fp, sort_keys=True, indent=4)
        main.log.info("Detection time results saved.")
    elif assignmentType == 'dynamic':
        jsonData = dict(json.loads(open(main.detectionTimeJsonFile).read()))
        if jsonData[samplingRatio][hashFunction][assignmentType].has_key(updateRate) is False:
            main.log.info("Need to introduce a new update rate to the detectionTime.json file.")
            jsonData[samplingRatio][hashFunction][assignmentType][updateRate] = dictForNewUpdateRate[updateRate]
            with open(main.detectionTimeJsonFile, 'w') as fp:
                json.dump(jsonData, fp, sort_keys=True, indent=4)
            main.log.info("Detection time results updated and saved with the new update rate.")
            jsonData = dict(json.loads(open(main.detectionTimeJsonFile).read()))
            temp = jsonData[samplingRatio][hashFunction][assignmentType][updateRate][updateSize][attackerPosition][attackType]
            temp.append(detectionResults)
            jsonData[samplingRatio][hashFunction][assignmentType][updateRate][updateSize][attackerPosition][attackType] = temp
            with open(main.detectionTimeJsonFile, 'w') as fp:
                json.dump(jsonData, fp, sort_keys=True, indent=4)
            main.log.info("Detection time results saved.")
        else:
            main.log.info("The update rate already exists")
            temp = jsonData[samplingRatio][hashFunction][assignmentType][updateRate][updateSize][attackerPosition][attackType]
            temp.append(detectionResults)
            jsonData[samplingRatio][hashFunction][assignmentType][updateRate][updateSize][attackerPosition][attackType] = temp
            with open(main.detectionTimeJsonFile, 'w') as fp:
                json.dump(jsonData, fp, sort_keys=True, indent=4)
            main.log.info("Detection time results saved.")