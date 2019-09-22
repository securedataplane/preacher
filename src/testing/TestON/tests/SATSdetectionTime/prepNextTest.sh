#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo 'detectionTime json file or archive file name not provided. e.g.,: psamp2AggInjectDetectionTime.json psamp2AggInject.tar.gz'
    exit 1
fi
if [[ $# -eq 1 ]] ; then
    echo 'detectionTime json file or archive file Archive name not provided. e.g.,: psamp2AggInjectDetectionTime.json psamp2AggInject.tar.gz'
    exit 1
fi
echo "first make a copy of detection time results"
cp /home/user/TestON/logs/detectionTimeResults/detectionTime.json /home/user/SATSresults/pureIndependentPairAssignmentDontAttackSamples/$1
#cp /home/user/TestON/logs/detectionTimeResults/detectionTime.json /tmp/$1
echo "next archive the detection results"
echo "Save archive as:"
echo $2
#
#if tar -czf /tmp/$1 /tmp/foo; then
if tar -czf /home/user/SATSresults/pureIndependentPairAssignmentDontAttackSamples/$2 /home/user/TestON/logs/SATS* /home/user/TestON/logs/detectionTimeResults/; then
    echo "Now replace the detectionTime.json with the baseline"
    cp /home/user/SATSresults/pureIndependentPairAssignmentDontAttackSamples/baselineAggDropDetectionTime.json /home/user/TestON/logs/detectionTimeResults/detectionTime.json
    #cp /home/user/SATSresults/pureIndependentPairAssignmentDontAttackSamples/baselineAggDropDetectionTime.json /tmp/detectionTime.json
fi
echo "done"
