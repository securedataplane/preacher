def __init__( self ):
    self.default = ''

# pcapFileListUsed is a list of the pcap files used.
def save( pcapFileListUsed ):
    main.log.info("Giong to save the pcap files used in the pcapFilesUsed file.")
    with open(main.pcapFilesUsed, 'a') as fp:
        for line in pcapFileListUsed:
            fp.write(line + '\n')

def getLblPcapFileList (lblTrafficPath):
    import os
    fileList = []
    for root, directories, filenames in os.walk(lblTrafficPath, 'r'):
        for filename in filenames:
            fileList.append(os.path.join(root, filename))
    return fileList

def getUsedPcapFileList(pcapFilesUsedFile):
    usedPcapList = []
    with open(pcapFilesUsedFile, 'r') as fp:
        pcapFilesUsed = fp.readlines()
    for pcapUsed in pcapFilesUsed:
        pcapUsed = pcapUsed.strip('\n')
        usedPcapList.append(pcapUsed)
    return usedPcapList

# To fetch data from the json file, the default values are as per the parameters.
def getPcapsToUse(pcapFilesUsedFile, lblTrafficPath, fromJson=False,
                  jsonFile=main.detectionTimeJsonFile,
                  assignment='static', attacker='aggregate', attack='drop',
                  seedKey='1'):
    import json
    if fromJson is False:
        usedPcapList = getUsedPcapFileList(pcapFilesUsedFile)
        lblPcapFileList = getLblPcapFileList(lblTrafficPath)
        pcapsToUse =  list(set(lblPcapFileList) - set(usedPcapList))
        i = 0
        end = len(lblPcapFileList)
        orderedList = []
        while i < end:
            # print i
            fileToSearch = lblTrafficPath + '0_0_2-1_0_2-' + str(i) + '.pcap'
            if fileToSearch in set(pcapsToUse):
                orderedList.append(fileToSearch)
            # else:
            #     main.log.warn("Already used pcap file:" + fileToSearch + ", in the lblTrafficpath.")
            i += 1
        return orderedList
    elif fromJson is True:
        # All repetitions are relative to the agg/static/drop attack. Therefore,
        # we need to return the pcaps starting from where that attack started.
        main.log.info("Going to get the pcaps used from the json file:" + str(jsonFile))
        jsonFileData = dict(json.loads(open(jsonFile).read()))
        # Changed the sampling ratio to always point to the baseline sampling ratio of 0.0046.
        detectionResults = jsonFileData[u'0.0046'][main.hashFunction[0]][assignment][attacker][attack]
        # detectionResults = jsonFileData[main.samplingRatio[0]][main.hashFunction[0]][assignment][attacker][attack]
        pcapsFromAttackDetectResult = []
        for result in detectionResults:
            if result[0].has_key(seedKey) is True:
                print "seedKey in result[0]"
                pcapsFromAttackDetectResult = result[3]
                break
        if pcapsFromAttackDetectResult == []:
            main.log.warn("Did not find the appropriate list of pcaps that were run. Check the usedPcapFiles instead.")
            return getPcapsToUse(pcapFilesUsedFile, lblTrafficPath, fromJson=False)
        else:
            pcapNumber = getNumberFromPcapFileName(pcapsFromAttackDetectResult[0])
            lblPcapFileList = getLblPcapFileList(lblTrafficPath)
            pcapsToUse = []
            i = int(pcapNumber)
            end = len(lblPcapFileList)
            while i < end:
                fileToSearch = lblTrafficPath + '0_0_2-1_0_2-' + str(i) + '.pcap'
                if fileToSearch in set(lblPcapFileList):
                    pcapsToUse.append(fileToSearch)
                else:
                    main.log.warn("pcap file missing:" + fileToSearch + ", in the lblTrafficpath.")
                i += 1
            return pcapsToUse



# E.g. pcapFileName
# /home/mininet/OnosSystemTest/TestON/tests/SATSdetectionTime/Dependency/lblTraffic/0_0_2-1_0_2-45.pcap
# This function returns 45 for the above filename
def getNumberFromPcapFileName(pcapFileName):
    x = pcapFileName.split('/')
    y = x[-1].strip('.pcap')
    z = y.split('-')
    pcapNumber = z[-1]
    return pcapNumber