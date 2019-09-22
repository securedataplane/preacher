/*
 * Copyright 2014-2015 Open Networking Laboratory
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * author: Kashyap Thimmaraju
 * email: kashyap.thimmaraju@sect.tu-berlin.de
 */
package org.onosproject.tsamp;

import org.apache.commons.lang.math.RandomUtils;
import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Modified;
import org.apache.felix.scr.annotations.Property;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;
import org.onlab.packet.Ethernet;
import org.onlab.packet.IPv4;
import org.onlab.packet.VlanId;
import org.onosproject.cfg.ComponentConfigService;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.Device;
import org.onosproject.net.DeviceId;
import org.onosproject.net.Host;
import org.onosproject.net.HostId;
import org.onosproject.net.Link;
import org.onosproject.net.Path;
import org.onosproject.net.PortNumber;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.FlowEntry;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.TrafficTreatment;
import org.onosproject.net.flow.criteria.Criterion;
import org.onosproject.net.flow.criteria.EthCriterion;
import org.onosproject.net.flow.criteria.PortCriterion;
import org.onosproject.net.flow.criteria.VlanIdCriterion;
import org.onosproject.net.flow.instructions.Instruction;
import org.onosproject.net.flowobjective.DefaultForwardingObjective;
import org.onosproject.net.flowobjective.FlowObjectiveService;
import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.group.GroupService;
import org.onosproject.net.group.GroupBucket;
import org.onosproject.net.group.GroupBuckets;
import org.onosproject.net.group.GroupKey;
import org.onosproject.net.group.DefaultGroupKey;
import org.onosproject.net.group.GroupDescription;
import org.onosproject.net.group.DefaultGroupBucket;
import org.onosproject.net.group.DefaultGroupDescription;
import org.onosproject.net.flow.TrafficTreatment.Builder;
import org.onosproject.net.host.HostService;
import org.onosproject.net.packet.InboundPacket;
import org.onosproject.net.packet.PacketContext;
import org.onosproject.net.packet.PacketProcessor;
import org.onosproject.net.packet.PacketService;
import org.onosproject.net.topology.PathService;
import org.onosproject.net.topology.TopologyService;
import org.osgi.service.component.ComponentContext;
import org.slf4j.Logger;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Dictionary;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;
import java.util.TreeMap;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;
import java.time.Duration;
import java.time.Instant;

import static com.google.common.base.Strings.isNullOrEmpty;
import static java.util.concurrent.Executors.newSingleThreadScheduledExecutor;
import static org.onlab.util.Tools.groupedThreads;
import static org.slf4j.LoggerFactory.getLogger;

/**
 * Preacher: Network policy checker for adversarial environments.
 * From the SRDS'19 paper.
 * Also known as Adversarial Trajectory Sampling (ATS) in this code.
 * t0 is the start time for ATS.
 * timestamp = LocalDateTime.now().
 * switchIterator iterates over the available switches,
 * and stores them in availableSwitchesList.
 * histortList is an ordered list of History events,
 * see History.java for the fields and methods.
 */
@Component(immediate = true)
public class TrajectorySampling {

    //t0 is the time sampling begins/configured.
    private static Instant t0 = null;
    private static long timeStamp = 0;
    private static final double DEFAULT_SAMPLING_RATE = 0.004638671875;
    private static final double HASH_TOTAL = 4096;
    private static final int DEFAULT_SAMPLING_SIZE = 4;
    private static final int DETECTORS = 1;
    private static Iterator<Device> switchIterator;
    private static final long DEFAULT_RTT = 2;
    private static final long PERIOD = 30;
    //Poisson distribution lambda value
    private static final double DEFAULT_POISSON_LAMBDA = 2.0;
    private static final int DEFAULT_PAIRWISE_SEED = 0;
    private static final int DEFAULT_HASHMUTATOR_SEED = 0;
    private static final int DEFAULT_SWITCHMUTATOR_SEED = 0;
    private static final String DEFAULT_COLLUDING_SWITCH_1 = "of:0000000000000201";
    private static final String DEFAULT_COLLUDING_SWITCH_2 = "of:0000000000010201";
    //private static List<History> historyList = Collections.synchronizedList(new ArrayList<History>());
    /*
     * The idea now is to create historyLists based
     * on the hash space. While using VLANs, each
     * historyList is assigned 4096/4 = 1024 hashes.
     * historyList0: 0-1022, historyList1: 1023-2046,
     * historyList2: 2047-3071, historyList3: 3072-4095
     */
    private static List<History> historyList0 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList1 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList2 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList3 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList4 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList5 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList6 = Collections.synchronizedList(new ArrayList<History>());
    private static List<History> historyList7 = Collections.synchronizedList(new ArrayList<History>());
    //A list of the detectorExecutors to execute as per user-configuration.
    private static List<ScheduledExecutorService> detectorExecutors = new ArrayList<ScheduledExecutorService>();
    public static Map<Integer, List<Double>> profileTable =
            new HashMap<Integer, List<Double>>();
    //A list to keep track of the handlingTime for every sample received
    public static List<Double> handlingTime = Collections.synchronizedList(new ArrayList<Double>());
    public static int samplesReceived = 0;
    //private static List<DeviceId> availableSwitchesList = new ArrayList<DeviceId>();
    //A HashMap of each switch and its assigned hash values timestamped
    //stored as a TreeMap for identifying the period of usage.
    private static Map<DeviceId, TreeMap<Long, List<Short>>> timeStampedHashesAssigned =
            new HashMap<DeviceId, TreeMap<Long, List<Short>>>();
    // {DeviceId, {TimeStamp, {DeviceId, [VlanId]}}}
    private static HashMap<DeviceId, TreeMap<Long, HashMap<DeviceId, List<Short>>>> timeStampedHashesDevicePairHashMap =
    		new HashMap<DeviceId, TreeMap<Long, HashMap<DeviceId, List<Short>>>>();

    private final Logger log = getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected TopologyService topologyService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected PacketService packetService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected HostService hostService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected FlowRuleService flowRuleService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected FlowObjectiveService flowObjectiveService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected ComponentConfigService cfgService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected PathService pathService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected GroupService groupService;

    private ScheduledExecutorService executor;

    private TrajectorySamplingProcessor processor = new TrajectorySamplingProcessor();

    private ApplicationId appId;

    @Property(name = "detectors", intValue = DETECTORS,
            label = "The number of detectors; " +
                    "default is 1")
    private int atsDetectors = DETECTORS;

    @Property(name = "samplingRate", doubleValue = DEFAULT_SAMPLING_RATE,
            label = "Sampling rate (p=Nrouter/Ntotal) for each switch; " +
                    "default is 0.004638671875")
    private Double samplingRate = DEFAULT_SAMPLING_RATE;

    @Property(name = "roundTripTime", longValue = DEFAULT_RTT,
            label = "Maximum round-trip-time for a packet in the network; " +
                    "default is 1s")
    private long roundTripTime = DEFAULT_RTT;

    @Property(name = "hashMutation", boolValue = false,
            label = "Enable random hash mutation; " +
                    "default is false")
    private boolean hashMutation = false;

    @Property(name = "pairAssignment", boolValue = false,
            label = "Enable pair assigment of sampling rules; " +
                    "default is Independent@Random (false)")
    private boolean pairAssignment = false;

    @Property(name = "samplingSize", intValue = DEFAULT_SAMPLING_SIZE,
            label = "The number of sampling flow rules to install; " +
                    "default is 40")
    private int samplingSize = DEFAULT_SAMPLING_SIZE;

    @Property(name = "trajectorySampling", boolValue = false,
            label = "Enable Adversarial Trajectory Sampling; default is false")
    private boolean trajectorySampling = false;

    @Property(name = "pairwiseSeed", intValue = DEFAULT_PAIRWISE_SEED,
            label = "The seed for generating the pairwise sampling rules; default is 0.")
    private int pairwiseSeed = DEFAULT_PAIRWISE_SEED;
    @Property(name = "hashMutatorSeed", intValue = DEFAULT_HASHMUTATOR_SEED,
            label = "The seed for the hashmutator to generate sampling rules; default is 0.")
    private int hashMutatorSeed = DEFAULT_HASHMUTATOR_SEED;
    @Property(name = "switchMutatorSeed", intValue = DEFAULT_SWITCHMUTATOR_SEED,
            label = "The seed for the switchMutatorSeed to generate sampling rules; default is 0.")
    private int switchMutatorSeed = DEFAULT_SWITCHMUTATOR_SEED;
    @Property(name = "collusion", boolValue = false,
    		label = "Enable Collusion among switches; default is false")
    private boolean collusion = false;
    @Property(name = "updateRate", doubleValue = DEFAULT_POISSON_LAMBDA,
            label = "The average update rate to generate a new sampling rule; default is 2(s).")
    private double updateRate = DEFAULT_POISSON_LAMBDA;
    @Property(name = "colludingSwitch1", value = DEFAULT_COLLUDING_SWITCH_1,
            label = "Enable Collusion among switches; default is of:0000000000000201")
    private String colludingSwitch1 = DEFAULT_COLLUDING_SWITCH_1;
    @Property(name = "colludingSwitch2", value = DEFAULT_COLLUDING_SWITCH_2,
            label = "Enable Collusion among switches; default is of:0000000000010201")
    private String colludingSwitch2 = DEFAULT_COLLUDING_SWITCH_2;

    /**
     * @return the start time of adversarial trajectory sampling.
    */
    public static Instant getStartTime() {
        return TrajectorySampling.t0;
    }

    /**
     * Sets the timestamp for a received packet.
    */
    public static void setTimeStamp() {
        TrajectorySampling.timeStamp = Duration.between(t0, Instant.now()).getSeconds();
    }

    /**
     * Sets the start time of adversarial trajectory sampling.
    */
    public static void setStartTime() {
        TrajectorySampling.t0 = Instant.now();
    }

    @Activate
    public void activate(ComponentContext context) {
        cfgService.registerProperties(getClass());
        appId = coreService.registerApplication("org.onosproject.tsamp");
        //advisor(2) so that we read the packet before most apps.
        packetService.addProcessor(processor, PacketProcessor.advisor(2));
        readComponentConfiguration(context);
        //requestIntercepts();
        log.info("Activated the Adversarial Trajectory Sampling application." +
            "You still need to enable sampling via the cfg command.", appId.id());
        /*
         * Set t0 to record the start time of ATS.
         * This is necessary to keep track of what
         * time hashes were assigned to respective
         * switches.
         */
        setStartTime();
        log.info("ATS started at: {}", t0.toString());
        if (!profileTable.isEmpty()) {
            log.info("ProfileTable has been cleaned for new detection stats");
            profileTable.clear();
        }
        if (!handlingTime.isEmpty()) {
            log.info("handlingTime list has been cleaned up for new detection stats");
            handlingTime.clear();
        }
        //requestGroupIntercepts();
        requestFlowIntercepts();
    }

     /*
     * This method should configure the groupTable
     * for each switch in the network based on the
     * random hash assignment algorithm for ATS.
     */
    private void requestGroupIntercepts() {
        log.info("In requestGroupIntercepts()");
        int groupId = 1;
        GroupKey key = new DefaultGroupKey(appId.toString().getBytes());
        VlanId vlanId = VlanId.ANY;
        Iterator<Device> switchIterator = deviceService.getAvailableDevices(
                Device.Type.SWITCH).iterator();
        while (switchIterator.hasNext()) {
            List<GroupBucket> buckets = new ArrayList<GroupBucket>();
            for (int i = 0; i < 10; i++) {
                vlanId = VlanId.vlanId((short) i);
                Builder bucketBuilder = DefaultTrafficTreatment.builder();
                bucketBuilder.pushVlan();
                bucketBuilder.setVlanId(vlanId);
                bucketBuilder.setOutput(PortNumber.CONTROLLER);
                GroupBucket bucket = DefaultGroupBucket.createSelectGroupBucket(bucketBuilder.build());
                buckets.add(i, bucket);
            }
            /*DeviceId deviceId,
            GroupDescription.Type type,
            GroupBuckets buckets,
            GroupKey appCookie,
            Integer groupId,
            ApplicationId appId*/
            GroupDescription groupDescription = new DefaultGroupDescription(switchIterator.next().id(),
                    GroupDescription.Type.SELECT,
                    new GroupBuckets(buckets),
                    key,
                    groupId,
                    appId);
            groupService.addGroup(groupDescription);
        }
    }

    /*
     * Method to remove the installed GroupIds
     * on all the switches.
     */
    private void withdrawGroupIntercepts() {
        GroupKey key = new DefaultGroupKey(appId.toString().getBytes());
        Iterator<Device> switchIterator = deviceService.getAvailableDevices(
                Device.Type.SWITCH).iterator();
        while (switchIterator.hasNext()) {
            groupService.removeGroup(switchIterator.next().id(), key, appId);
        }
    }

    /*
     * This method installs flows on available switches
     * in order to sample packets based on the VlanId.
     * This is a workaround the groupBuckets.
     * The number of sampling rules installed on each
     * switch is 10 as of now. We limit the random numbers
     * to 4096 as thats the maximum VlanId value.
     * This is Algorithm 1 for ATS i.e.,
     * Random Hash Assignment.
     * The ability to configure the hash value has been
     * deprecated.
     */
    private void requestFlowIntercepts() {
        setTimeStamp();
        if (deviceService.getDeviceCount() == 0) {
            log.info("No available devices yet");
            return;
        }
        Iterator<Device> switchIterator = getSortedDeviceIds().iterator();
        int switchCounter = 0;
        boolean singleSwitch = false;
        if (deviceService.getDeviceCount() == 1) {
            log.info("Single device only, must be for measurements?");
            singleSwitch = true;
        }
        while (switchIterator.hasNext()) {
            DeviceId deviceId = switchIterator.next().id();
            TreeMap<Long, List<Short>> timeStampedHashes =
                    new TreeMap<Long, List<Short>>();
            List<Short> switchHashAssignment = new ArrayList<Short>();
            //TODO: change the 10 to a user configured value.
            for (int i = 1; i < samplingSize + 1; i++) {
                TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
                int hashValue = 0;
                //int hashValue = i * 500 + 48;
                if (atsDetectors <= 4) {
                    if (singleSwitch) {
                        hashValue = 1000 + i;
                    } else {
                        switch (i) {
                        case 1:
                            hashValue = 1000 + switchCounter;
                            break;
                        case 2:
                            hashValue = 2000 + switchCounter;
                            break;
                        case 3:
                            hashValue = 3000 + switchCounter;
                            break;
                        case 4:
                            hashValue = 4000 + switchCounter;
                            break;
                        default:
                            hashValue = 4094;
                            break;
                        }
                    }
                } else if (atsDetectors == 6) {
                    if (deviceId.toString().compareTo("of:0000000000000201") == 0 ||
                            deviceId.toString().compareTo("of:0000000000010201") == 0) {
                        log.info("Going to install odd based sampling rules for an even numbered switch.");
                        switch (i) {
                        case 1:
                            hashValue = 2500 + switchCounter;
                            break;
                        case 2:
                            hashValue = 3000 + switchCounter;
                            break;
                        case 3:
                            hashValue = 3500 + switchCounter;
                            break;
                        case 4:
                            hashValue = switchCounter;
                            break;
                        default:
                            hashValue = 4094;
                            break;
                        }
                    } else {
                        switch (switchCounter) {
                        case 0: case 2: case 4: case 6: case 8: case 10: case 12: case 14: case 16: case 18: case 20:
                            switch (i) {
                            case 1:
                                hashValue = 500 + switchCounter;
                                break;
                            case 2:
                                hashValue = 1000 + switchCounter;
                                break;
                            case 3:
                                hashValue = 1500 + switchCounter;
                                break;
                            case 4:
                                hashValue = switchCounter;
                                break;
                            default:
                                hashValue = 4094;
                                break;
                            }
                            break;
                        case 1: case 3: case 5: case 7: case 9: case 11: case 13: case 15: case 17: case 19: case 21:
                            switch (i) {
                            case 1:
                                hashValue = 2500 + switchCounter;
                                break;
                            case 2:
                                hashValue = 3000 + switchCounter;
                                break;
                            case 3:
                                hashValue = 3500 + switchCounter;
                                break;
                            case 4:
                                hashValue = switchCounter;
                                break;
                            default:
                                hashValue = 4094;
                                break;
                            }
                            break;
                        default:
                            break;
                        }
                    }
                } else if (atsDetectors == 8) {
                    if (deviceId.toString().compareTo("of:0000000000000201") == 0 ||
                            deviceId.toString().compareTo("of:0000000000010201") == 0) {
                        log.info("Going to install odd based sampling rules for an even numbered switch.");
                        switch (i) {
                        case 1:
                            hashValue = 2500 + switchCounter;
                            break;
                        case 2:
                            hashValue = 3000 + switchCounter;
                            break;
                        case 3:
                            hashValue = 3500 + switchCounter;
                            break;
                        case 4:
                            hashValue = 4000 + switchCounter;
                            break;
                        default:
                            hashValue = 4094;
                            break;
                        }
                    } else {
                        switch (switchCounter) {
                        case 0: case 2: case 4: case 6: case 8: case 10: case 12: case 14: case 16: case 18: case 20:
                            switch (i) {
                            case 1:
                                hashValue = 500 + switchCounter;
                                break;
                            case 2:
                                hashValue = 1000 + switchCounter;
                                break;
                            case 3:
                                hashValue = 1500 + switchCounter;
                                break;
                            case 4:
                                hashValue = 2000 + switchCounter;
                                break;
                            default:
                                hashValue = 4094;
                                break;
                            }
                            break;
                        case 1: case 3: case 5: case 7: case 9: case 11: case 13: case 15: case 17: case 19: case 21:
                            switch (i) {
                            case 1:
                                hashValue = 2500 + switchCounter;
                                break;
                            case 2:
                                hashValue = 3000 + switchCounter;
                                break;
                            case 3:
                                hashValue = 3500 + switchCounter;
                                break;
                            case 4:
                                hashValue = 4000 + switchCounter;
                                break;
                            default:
                                hashValue = 4094;
                                break;
                            }
                            break;
                        default:
                            break;
                        }
                    }
                }

                VlanId vlanId = VlanId.vlanId((short) hashValue);
                //VlanId vlanId = VlanId.vlanId((short) RandomUtils.nextInt(1022));
                switchHashAssignment.add(vlanId.toShort());
                selector.matchVlanId(vlanId);

                TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                        .setOutput(PortNumber.CONTROLLER)
                        .transition(2)
                        .build();

                ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                        .withSelector(selector.build())
                        .withTreatment(treatment)
                        .withPriority(50001)
                        .withFlag(ForwardingObjective.Flag.VERSATILE)
                        .fromApp(appId)
                        .makePermanent()
                        .add();

                flowObjectiveService.forward(deviceId,
                        forwardingObjective);
            }
            /*
             * Save the timestamp of when the hashes were assigned.
             * This is used to identify the switch sampler for
             * the appropriate timestamp.
             */
            timeStampedHashes.put(timeStamp, switchHashAssignment);
            timeStampedHashesAssigned.put(deviceId, timeStampedHashes);
            switchCounter++;
        }
        log.info("The Random timestampedhashesassigned are: {}", timeStampedHashesAssigned.toString());
    }

    @Deactivate
    public void deactivate() {
        cfgService.unregisterProperties(getClass(), false);
        //withdrawGroupIntercepts();
        /*
         * Shutdown the hashmutator
         * if it was enabled.
         */
        if (executor != null) {
            executor.shutdownNow();
        }
        /*
         * Shutdown the detector threads
         * if it was enabled
         */
        for (int i = 0; i < atsDetectors; i++) {
            if (detectorExecutors.isEmpty()) {
                break;
            }
            if (detectorExecutors.get(i) != null) {
                detectorExecutors.get(i).shutdown();
                log.info("Shutdown detector{}.", i);
            }
        }
        //remove old detectors.
        detectorExecutors.clear();
        //if (!profileTable.isEmpty() && !handlingTime.isEmpty()) {
        //computeTrajectoryThroughput();
        //}
        //Clean up the profile table?
        if (!profileTable.isEmpty()) {
            for (int detectorId : profileTable.keySet()) {
                log.info("Detector Id: {}", detectorId);
                log.info("Total Trajectories: {}", profileTable.get(detectorId).size());
                log.info("Trajectories/s for all detections: {}", profileTable.get(detectorId).toString());
            }
            profileTable.clear();
        }
        if (!handlingTime.isEmpty()) {
            log.info("Total samples received: {}", handlingTime.size());
            handlingTime.clear();
        }
        flowRuleService.removeFlowRulesById(appId);
        packetService.removeProcessor(processor);
        processor = null;
        log.info("Stopped Adversarial Trajectory Sampling.");
    }

    public void computeTrajectoryThroughput() {
        double totalHandlingTime = 0;
        for (Double handledTime : handlingTime) {
            totalHandlingTime += handledTime;
        }
        //avgTotalHandlingTime (ms).
        double avgTotalHandlingTime = totalHandlingTime / handlingTime.size();
        log.info("Average Handling time(s) is: {}",
                String.format("%.4f", avgTotalHandlingTime / 1000));
        //log.info(String.format("%.4f", avgTotalHandlingTime / 1000));
        int totalDetections = 0;
        //totalDetectionTime (ms)
        double totalDetectionTime = 0;
        // The detectionTimeList has times from index=1 as index=0 is always 0.
        for (int detectorId : profileTable.keySet()) {
            int detectorsDetections = profileTable.get(detectorId).size() - 1;
            for (int i = 1; i <= detectorsDetections; i++) {
                totalDetectionTime += profileTable.get(detectorId).get(i);
                totalDetections++;
            }
        }
        if (totalDetections != handlingTime.size()) {
            log.error("totalDetections != handlingTime.size()");
            log.error("totalDetections - handlingTime.size() is:{}", totalDetections - handlingTime.size());
        }
        //avgDetectionTime (ms)
        double avgDetectionTime = (totalDetectionTime / totalDetections);
        log.info("Average Detection time(s) is: {}", avgDetectionTime / 1000);
        double totalAverageTime = avgTotalHandlingTime + avgDetectionTime;
        //totalThroughput (trajectories per second)
        double totalThroughput = (atsDetectors / totalAverageTime) * 1000;
        log.info("The average thoughput for {} threads is: {}",
                atsDetectors, String.format("%.4f", totalThroughput));
        //log.info(String.format("%.4f", totalThroughput));
    }

    @Modified
    public void modified(ComponentContext context) {
        readComponentConfiguration(context);
        //requestIntercepts();
    }

    /**
     * Extracts properties from the component configuration context.
     *
     * @param context the component context
     */
    private void readComponentConfiguration(ComponentContext context) {
        Dictionary<?, ?> properties = context.getProperties();
        // Configure the number of detectors
        Integer detectorsConfigured =
                getIntegerProperty(properties, "detectors");
        if (detectorsConfigured == null) {
            log.info("Detectors is not configured, default value is {}",
                     DETECTORS);
        } else {
            atsDetectors = detectorsConfigured;
            log.info("Configured. No. of Detectors is configured to {}", atsDetectors);
        }
        // Get the user configured sampling value size
        Integer samplingSizeConfigured =
                getIntegerProperty(properties, "samplingSize");
        if (samplingSizeConfigured == null) {
            log.info("Sampling size is not configured, default value is {}",
                     DEFAULT_SAMPLING_SIZE);
        } else {
            samplingSize = samplingSizeConfigured;
            log.info("Configured. Sampling size is configured to {}", samplingSize);
        }
        Integer hashMutatorSeedConfigured =
                getIntegerProperty(properties, "hashMutatorSeed");
        if (hashMutatorSeedConfigured == null) {
            hashMutatorSeed = DEFAULT_HASHMUTATOR_SEED;
            log.info("hashMutatorSeed is not configured, default value is {}", DEFAULT_HASHMUTATOR_SEED);
        } else {
            hashMutatorSeed = hashMutatorSeedConfigured;
            log.info("Configured. hashMutatorSeed is configured to {}.", hashMutatorSeed);
        }
        Integer switchMutatorSeedConfigured =
                getIntegerProperty(properties, "switchMutatorSeed");
        if (switchMutatorSeedConfigured == null) {
            switchMutatorSeed = DEFAULT_SWITCHMUTATOR_SEED;
            log.info("switchMutatorSeed is not configured, default value is {}", DEFAULT_SWITCHMUTATOR_SEED);
        } else {
            switchMutatorSeed = switchMutatorSeedConfigured;
            log.info("Configured. switchMutatorSeed is configured to {}.", switchMutatorSeed);
        }
        Double updateRateConfigured =
                getDoubleProperty(properties, "updateRate");
        if (updateRateConfigured == null) {
            updateRate = DEFAULT_POISSON_LAMBDA;
            log.info("updateRate is not configured, default value is {}", DEFAULT_POISSON_LAMBDA);
        } else {
            updateRate = updateRateConfigured;
            log.info("Configured. updateRate is configured to {}.", updateRate);
        }
        Double samplingRateConfigured =
                getDoubleProperty(properties, "samplingRate");
        if (samplingRateConfigured == null) {
            samplingRate = DEFAULT_SAMPLING_RATE;
            log.info("SAMPLINGRate is not configured, default value is {}", DEFAULT_SAMPLING_RATE);
        } else {
            samplingRate = samplingRateConfigured;
            log.info("Configured. samplingRate is configured to {}.", samplingRate);
        }
        // Alg. 2: Enable random hash mutation.
        boolean hashMutationEnabled =
                isPropertyEnabled(properties, "hashMutation");
        if (hashMutation != hashMutationEnabled) {
            hashMutation = hashMutationEnabled;
            if (!hashMutation) {
                if (executor != null) {
                    executor.shutdownNow();
                    log.info("Stopped hash mutation.");
                }
            } else if (hashMutation) {
                log.info("Configured Random hash mutation.");
                executor = newSingleThreadScheduledExecutor(groupedThreads("onos/ats", "hash-mutator-%d"));
                log.info("Executor for hashMutator has been assgined thread factory.");
                HashMutator hashMutator = new HashMutator(hashMutatorSeed, switchMutatorSeed);
                executor.schedule(hashMutator, 5, TimeUnit.SECONDS);
                log.info("executor is scheduled for periodic mutation");
            }
        }
        // Get the seed for pairwise sampling rule generation.
        Integer pairwiseSeedConfigured =
                getIntegerProperty(properties, "pairwiseSeed");
        if (pairwiseSeedConfigured == null) {
            log.info("Sampling size is not configured, default value is {}",
                    DEFAULT_PAIRWISE_SEED);
            pairwiseSeed = DEFAULT_PAIRWISE_SEED;
        } else {
            if (pairwiseSeedConfigured == pairwiseSeed) {
                log.info("Pairwise seed has not changed.");
            } else {
                pairwiseSeed = pairwiseSeedConfigured;
                log.info("Pairwise seed has changed. call requestPairWiseIntercepts(seed) if pairAssignmentEnabled");
                if (pairAssignment) {
                    requestPairWiseIntercepts(pairwiseSeed);
                }
                log.info("Configured. pairwiseSeed is configured to {}.", pairwiseSeed);
            }
        }
        // Get the names (DPID) of the colluding switches.
        // Note that collusion MUST be deactivated before changing
        // the colluding switches.
        String colludingSwitch1Configured =
                getStringProperty(properties, "colludingSwitch1");
        if (colludingSwitch1Configured == null) {
            colludingSwitch1 = DEFAULT_COLLUDING_SWITCH_1;
            log.info("colludingSwitch1 is not configured, default value is {}", DEFAULT_COLLUDING_SWITCH_1);
        } else {
            colludingSwitch1 = colludingSwitch1Configured;
            log.info("Configured. colludingSwitch1 is configured to {}.", colludingSwitch1);
        }
        String colludingSwitch2Configured =
                getStringProperty(properties, "colludingSwitch2");
        if (colludingSwitch2Configured == null) {
            colludingSwitch2 = DEFAULT_COLLUDING_SWITCH_2;
            log.info("colludingSwitch2 is not configured, default value is {}", DEFAULT_COLLUDING_SWITCH_2);
        } else {
            colludingSwitch2 = colludingSwitch2Configured;
            log.info("Configured. colludingSwitch2 is configured to {}.", colludingSwitch2);
        }

        // Need to disable and enable collusion when the malicious switches
        // are changed.
        boolean collusionEnabled =
                isPropertyEnabled(properties, "collusion");
        if (collusion != collusionEnabled) {
            collusion = collusionEnabled;
            if (collusion) {
                log.info("Collusion enabled.");
                // Need to install colluding sampling flow rules
                activateCollusion(colludingSwitch1, colludingSwitch2);
            } else if (!collusion) {
                log.info("Collusion disabled");
                // Need to disable the colluding sampling flow rules
                deactivateCollusion(colludingSwitch1, colludingSwitch2);
            }
        }
        boolean pairAssignmentEnabled =
                isPropertyEnabled(properties, "pairAssignment");
        if (pairAssignment != pairAssignmentEnabled) {
            pairAssignment = pairAssignmentEnabled;
            if (pairAssignment) {
                log.info("Pair-wise assignment enabled.");
                //First withdraw old hash values
                flowRuleService.removeFlowRulesById(appId);
                requestPairWiseIntercepts(pairwiseSeed);
            } else if (!pairAssignment) {
                //First withdraw old hash values
                flowRuleService.removeFlowRulesById(appId);
                requestFlowIntercepts();
            }
        }
        boolean trajectorySamplingEnabled =
                isPropertyEnabled(properties, "trajectorySampling");
        if (trajectorySampling != trajectorySamplingEnabled) {
            trajectorySampling = trajectorySamplingEnabled;
            log.info("Configured. Adversarial Trajectory Sampling is {}",
                     trajectorySampling ? "enabled" : "disabled");
            /*
             * Handle multi-threaded detection.
             * the packetProcessor process() is the
             * dispatcher. When trajectorySampling
             * is enabled, create n threads that
             * handle detection.
             */
            if (!trajectorySampling) {
                if (!profileTable.isEmpty() && !handlingTime.isEmpty()) {
                    computeTrajectoryThroughput();
                }
                for (int i = 0; i < atsDetectors; i++) {
                    if (detectorExecutors.get(i) != null) {
                        detectorExecutors.get(i).shutdown();
                        log.info("Shutdown detector{}.", i);
                    }
                }
                //remove old detectors.
                detectorExecutors.clear();
            } else if (trajectorySampling) {
                for (int i = 0; i < atsDetectors; i++) {
                    detectorExecutors.add(i, newSingleThreadScheduledExecutor(
                            groupedThreads("onos/ats", "ATS-Detector-" + i + "-%d")));
                    switch (i) {
                    case 0:
                        Detector detector0 = new Detector(historyList0, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector0, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 1:
                        Detector detector1 = new Detector(historyList1, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector1, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 2:
                        Detector detector2 = new Detector(historyList2, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector2, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 3:
                        Detector detector3 = new Detector(historyList3, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector3, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 4:
                        Detector detector4 = new Detector(historyList4, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector4, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 5:
                        Detector detector5 = new Detector(historyList5, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector5, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 6:
                        Detector detector6 = new Detector(historyList6, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector6, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    case 7:
                        Detector detector7 = new Detector(historyList7, i);
                        detectorExecutors.get(i).scheduleWithFixedDelay(detector7, 1, 2, TimeUnit.SECONDS);
                        log.info("Started detector{}.", i);
                        break;
                    default:
                        log.info("Maximum allowed detectors is 8.");
                        break;
                    }
                }
            }
        }
    }

    /**
     * Check property name is defined and set to true.
     *
     * @param properties   properties to be looked up
     * @param propertyName the name of the property to look up
     * @return true when the propertyName is defined and set to true
     */
    private static boolean isPropertyEnabled(Dictionary<?, ?> properties,
                                             String propertyName) {
        boolean enabled = false;
        try {
            String flag = (String) properties.get(propertyName);
            if (flag != null) {
                enabled = flag.trim().equals("true");
            }
        } catch (ClassCastException e) {
            // No propertyName defined.
            enabled = false;
        }
        return enabled;
    }

    /**
     * Get Integer property from the propertyName
     * Return null if propertyName is not found.
     *
     * @param properties   properties to be looked up
     * @param propertyName the name of the property to look up
     * @return value when the propertyName is defined or return null
     */
    private static Integer getIntegerProperty(Dictionary<?, ?> properties,
                                              String propertyName) {
        Integer value = null;
        try {
            String s = (String) properties.get(propertyName);
            value = isNullOrEmpty(s) ? value : Integer.parseInt(s.trim());
        } catch (NumberFormatException | ClassCastException e) {
            value = null;
        }
        return value;
    }

    private static Double getDoubleProperty(Dictionary<?, ?> properties,
                    String propertyName) {
        Double value = null;
        try {
        String s = (String) properties.get(propertyName);
        value = isNullOrEmpty(s) ? value : Double.parseDouble(s.trim());
        } catch (NumberFormatException | ClassCastException e) {
            value = null;
        }
        return value;
    }

    private static String getStringProperty(Dictionary<?, ?> properties, String propertyName) {
        String stringValue = null;
        try {
            String value = (String) properties.get(propertyName);
            if (value != null) {
                stringValue = value.trim();
            }
        } catch (ClassCastException e) {
            // No property defined.
            stringValue = null;
        }
        return stringValue;
    }

    // Helper method to return a sorted list of the available devices based on Ids.
    private List<Device> getSortedDeviceIds() {
        Iterator<Device> switchIterator = deviceService.getAvailableDevices(
                Device.Type.SWITCH).iterator();
        List<Device> deviceList = new ArrayList<Device>();
        List<String> deviceIdList = new ArrayList<String>();
        List<Device> sortedDeviceList = new ArrayList<Device>();
        while (switchIterator.hasNext()) {
            Device device = switchIterator.next();
            deviceList.add(device);
            deviceIdList.add(device.id().toString());
        }
        // compareDeviceId sorts the devices Ids in ascending order.
        Comparator<String> compareDeviceId = (id1, id2) -> id1.compareTo(id2);
        Collections.sort(deviceIdList, compareDeviceId);
        for (String d : deviceIdList) {
            for (Device device : deviceList) {
                if (device.id().toString() == d) {
                    sortedDeviceList.add(device);
                    break;
                }
            }
        }
        return sortedDeviceList;
    }
    // Calling this rewrites timeStampedHashesAssigned i.e., it's like starting from scratch.
    private void requestPairWiseIntercepts(int seed) {
        int nRouter = deviceService.getDeviceCount();
        int nPrimeSmall = nRouter - 1;
        if (nRouter < 2) {
            log.info("pair-wise Assignment requires at least 2 switches.");
            return;
        }
        int nTotal = (int) ((double) nPrimeSmall / samplingRate);
        int nSmall = (int) ((double) nTotal * samplingRate);
        int hashesPerSwitch = (int) (samplingRate * HASH_TOTAL);
        short totalHashesForNetwork = (short) (hashesPerSwitch * nRouter);
        // Note: hashesPerPair are used to determine the sampling rate/ratio.
        int hashesPerPair = hashesPerSwitch / nPrimeSmall;
        // Get the sortedDeviceList
        List<Device> deviceList = getSortedDeviceIds();
        // Initialize the devicePairHashMap that is used for random pair random hash assignment.
        HashMap<Device, HashMap<Device, List<Short>>> devicePairHashMap =
                new HashMap<Device, HashMap<Device, List<Short>>>();
        for (Device firstKey : deviceList) {
            HashMap<Device, List<Short>> secondKeyMap = new HashMap<Device, List<Short>>();
            for (Device secondKey : deviceList) {
                List<Short> hashList = new ArrayList<Short>();
                // The firstKey->firstKey:Value is used for counting hashes assigned for firstKey switch.
                if (secondKey.id().equals(firstKey.id())) {
                    hashList.add((short) 0);
                    secondKeyMap.put(secondKey, hashList);
                } else {
                    // The other values are used to store the hashes that are assigned for the respective pair.
                    secondKeyMap.put(secondKey, hashList);
                }
            }
            devicePairHashMap.put(firstKey, secondKeyMap);
        }
        // Use an random number generator to pick random pairs.
        Random rng2 = new Random();
        rng2.setSeed(seed);
        short hashValue = (short) 4096;
        short totalAssignedHashes = (short) 0;
        setTimeStamp();
        // Loop until all pairs have been assigned the appropriate no. of hashes
        while (totalAssignedHashes < totalHashesForNetwork) {
            for (int firstKey = 0; firstKey < deviceList.size(); firstKey++) {
                log.info("Go through each device.");
                for (int secondKey = 0; secondKey < deviceList.size(); secondKey++) {
                    log.info("Go through the pairs formed with the previous device.");
                    if (firstKey != secondKey) {
                        if (devicePairHashMap.get(deviceList.get(firstKey))
                                .get(deviceList.get(secondKey)).size() < hashesPerPair && devicePairHashMap
                                .get(deviceList.get(secondKey)).get(deviceList.get(firstKey)).size() < hashesPerPair) {
                            hashValue = (short) rng2.nextInt(4096);
                            log.info("Going to assign a hashValue {} to a new random pair:{}, {}",
                                    hashValue, deviceList.get(firstKey).id(), deviceList.get(secondKey).id());
                            TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
                            VlanId vlanId = VlanId.vlanId((short) hashValue);
                            // Initialize lists for adding the assigned hashValue and for the counter.
                            List<Short> hashListFirstKeySecondKey = new ArrayList<Short>();
                            List<Short> hashListSecondKeyFirstKey = new ArrayList<Short>();
                            List<Short> hashCountList1 = new ArrayList<Short>();
                            List<Short> hashCountList2 = new ArrayList<Short>();
                            hashListFirstKeySecondKey = devicePairHashMap.get(deviceList.get(firstKey))
                                    .get(deviceList.get(secondKey));
                            hashListSecondKeyFirstKey = devicePairHashMap.get(deviceList.get(secondKey))
                                    .get(deviceList.get(firstKey));
                            // Append the new hashValue to the appropriate pair.
                            hashListFirstKeySecondKey.add(hashValue);
                            hashListSecondKeyFirstKey.add(hashValue);
                            devicePairHashMap.get(deviceList.get(firstKey)).put(deviceList.get(secondKey),
                                    hashListFirstKeySecondKey);
                            devicePairHashMap.get(deviceList.get(secondKey)).put(deviceList.get(firstKey),
                                    hashListSecondKeyFirstKey);
                            // Increment the counters for the pair chosen.
                            hashCountList1 = devicePairHashMap.get(deviceList.get(firstKey))
                                    .get(deviceList.get(firstKey));
                            short hashCounter = (short) (hashCountList1.get(0) + 1);
                            hashCountList1.clear();
                            hashCountList1.add(0, hashCounter);
                            log.info("hashCount for {} is:{}", deviceList.get(firstKey).id(), hashCountList1.get(0));
                            devicePairHashMap.get(deviceList.get(firstKey)).put(deviceList.get(firstKey), hashCountList1);
                            hashCountList2 = devicePairHashMap.get(deviceList.get(secondKey))
                                    .get(deviceList.get(secondKey));
                            hashCounter = (short) (hashCountList2.get(0) + 1);
                            hashCountList2.clear();
                            hashCountList2.add(0, hashCounter);
                            log.info("hashCount for {} is:{}", deviceList.get(secondKey).id(), hashCountList2.get(0));
                            devicePairHashMap.get(deviceList.get(secondKey)).put(deviceList.get(secondKey), hashCountList2);
                            // Increment the totalAssignedHashes by 2 as we introduce the same hash for 2 switches.
                            totalAssignedHashes = (short) (totalAssignedHashes + 2);
                            log.info("totalAssignedHashes so far:{}", totalAssignedHashes);
                            // Install the flow rule onto the switches.
                            selector.matchVlanId(vlanId);
                            TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                                    .setOutput(PortNumber.CONTROLLER)
                                    .transition(2)
                                    .build();
                            ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                                    .withSelector(selector.build())
                                    .withTreatment(treatment)
                                    .withPriority(50001)
                                    .withFlag(ForwardingObjective.Flag.VERSATILE)
                                    .fromApp(appId)
                                    .makePermanent()
                                    .add();
                            flowObjectiveService.forward(deviceList.get(firstKey).id(),
                                    forwardingObjective);
                            flowObjectiveService.forward(deviceList.get(secondKey).id(),
                                    forwardingObjective);
                        }
                    }
                    log.info("Check if all assignments are complete.");
                    if (totalAssignedHashes == totalHashesForNetwork) {
                        log.info("All assignments complete");
                        break;
                    }
                }
            }
        }
        /*
         * Save the timestamp of when the hashes were assigned.
         * This is used to identify the switch sampler for the appropriate timestamp.
         */
        for (int i = 0; i < deviceList.size(); i++) {
            HashMap<Device, List<Short>> tempDeviceHashList =
                    new HashMap<Device, List<Short>>();
            // Store the HashMap of DeviceId and List of Hashes
            HashMap<DeviceId, List<Short>> tempDeviceIdHashList =
                    new HashMap<DeviceId, List<Short>>();
            // Get the keys for the 2nd level of the HashMap and covert it to DeviceId
            tempDeviceHashList = devicePairHashMap.get(deviceList.get(i));
            // Now iterate through the keySet: Store the key as DeviceId, and value as the HashList
            for (Device d : tempDeviceHashList.keySet()) {
                tempDeviceIdHashList.put(d.id(), tempDeviceHashList.get(d));
            }
            // Now, create a HashMap with the timestamp as the key, and the {deviceIds, HashList} as values.
            TreeMap<Long, HashMap<DeviceId, List<Short>>> timeStampedDeviceIdHashValues =
                    new TreeMap<Long, HashMap<DeviceId, List<Short>>>();
            timeStampedDeviceIdHashValues.put(timeStamp, tempDeviceIdHashList);
            // Finally, put the DeviceId as the key and the timeStamped DeviceIds HashValues as the values.
            timeStampedHashesDevicePairHashMap.put(deviceList.get(i).id(), timeStampedDeviceIdHashValues);
        }
        log.info("timeStampedHashesDevicePairHashMap:{}", timeStampedHashesDevicePairHashMap);
    }

    // Method to activate collusion.
    // @param: maliciousSwitch1, maliciousSwitch2
    // are string values of the switches/devices that need to collude.
    private void activateCollusion(String switch1, String switch2) {
    	log.info("In activateCollusion()");
    	// First convert the String switches to Devices
    	Iterator<Device> devices = deviceService.getAvailableDevices(
    			Device.Type.SWITCH).iterator();
        List<Device> maliciousDeviceList = new ArrayList<Device>();
    	while (devices.hasNext()) {
    		Device device = devices.next();
            if (device.id().toString().compareTo(switch1) == 0) {
                maliciousDeviceList.add(device);
    		}
            if (device.id().toString().compareTo(switch2) == 0) {
                maliciousDeviceList.add(device);
    		}
    	}
        if (maliciousDeviceList.isEmpty() || maliciousDeviceList.size() < 2) {
    		log.error("Did not find the malicious devices: {} and {}, in the available devices", switch1, switch2);
    		return;
    	}
        // Now get the hash values for those devices. It's sufficient to just get it from one.
        HashMap<DeviceId, List<Short>> deviceIdHashList = new HashMap<DeviceId, List<Short>>();
        deviceIdHashList = getSwitchHashAssignmentTable(maliciousDeviceList.get(0).id(), timeStamp);
        List<FlowEntry> oldFlows = new ArrayList<FlowEntry>();
        List<ForwardingObjective> newFlows = new ArrayList<ForwardingObjective>();
        List<Short> colludingHashList = new ArrayList<Short>();
        colludingHashList = deviceIdHashList.get(maliciousDeviceList.get(1).id());
        log.info("colludingHashList:{}", colludingHashList);
        //Get the associate flow rule
        for (Device maliciousDevice : maliciousDeviceList) {
            for (Short hashValue : colludingHashList) {
                for (FlowEntry flowEntry : flowRuleService.getFlowEntries(maliciousDevice.id())) {
                    for (Criterion crSwitch : flowEntry.selector().criteria()) {
                        if (crSwitch.type() == Criterion.Type.VLAN_VID) {
                            if (((VlanIdCriterion) crSwitch).vlanId().toShort() == hashValue) {
                                oldFlows.add(flowEntry);
                                //Create a copy of it with action: goto_table only
                                TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
                                selector.matchVlanId(VlanId.vlanId(hashValue));
                                TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                                        .transition(2)
                                        .build();
                                ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                                        .withSelector(selector.build())
                                        .withTreatment(treatment)
                                        .withPriority(50001)
                                        .withFlag(ForwardingObjective.Flag.VERSATILE)
                                        .fromApp(appId)
                                        .makePermanent()
                                        .add();
                                newFlows.add(forwardingObjective);
                            }
                        }
                    }
                }
            }
        }
        //Remove the old flow rule
        for (FlowEntry oldFlow : oldFlows) {
            flowRuleService.removeFlowRules((FlowRule) oldFlow);
        }
        for (Device d : maliciousDeviceList) {
            for (ForwardingObjective f : newFlows) {
                flowObjectiveService.forward(d.id(), f);
            }
        }
        log.info("Collusion activated.");
    }

    private void deactivateCollusion(String switch1, String switch2) {
        log.info("deactiveCollusion()");
        // First convert the String switches to Devices
        Iterator<Device> devices = deviceService.getAvailableDevices(
                Device.Type.SWITCH).iterator();
        List<Device> maliciousDeviceList = new ArrayList<Device>();
        while (devices.hasNext()) {
            Device device = devices.next();
            if (device.id().toString().compareTo(switch1) == 0) {
                maliciousDeviceList.add(device);
            }
            else if (device.id().toString().compareTo(switch2) == 0) {
                maliciousDeviceList.add(device);
            }
        }
        if (maliciousDeviceList.isEmpty()) {
            log.error("Did not find the malicious devices: {} and {}, in the available devices", switch1, switch2);
            return;
        }
        // Now get the hash values for those devices. It's sufficient to just get it from one.
        HashMap<DeviceId, List<Short>> deviceIdHashList = new HashMap<DeviceId, List<Short>>();
        deviceIdHashList = getSwitchHashAssignmentTable(maliciousDeviceList.get(0).id(), timeStamp);
        List<FlowEntry> oldFlows = new ArrayList<FlowEntry>();
        List<ForwardingObjective> newFlows = new ArrayList<ForwardingObjective>();
        List<Short> colludingHashList = new ArrayList<Short>();
        colludingHashList = deviceIdHashList.get(maliciousDeviceList.get(1).id());
        log.info("colludingHashList:{}", colludingHashList);
        //Get the associate flow rule
        for (Device maliciousDevice : maliciousDeviceList) {
            for (Short hashValue : colludingHashList) {
                for (FlowEntry flowEntry : flowRuleService.getFlowEntries(maliciousDevice.id())) {
                    for (Criterion crSwitch : flowEntry.selector().criteria()) {
                        if (crSwitch.type() == Criterion.Type.VLAN_VID) {
                            if (((VlanIdCriterion) crSwitch).vlanId().toShort() == hashValue) {
                                oldFlows.add(flowEntry);
                                //Create a copy of it with action: goto_table only
                                TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
                                selector.matchVlanId(VlanId.vlanId(hashValue));
                                TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                                        .setOutput(PortNumber.CONTROLLER)
                                        .transition(2)
                                        .build();
                                ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                                        .withSelector(selector.build())
                                        .withTreatment(treatment)
                                        .withPriority(50001)
                                        .withFlag(ForwardingObjective.Flag.VERSATILE)
                                        .fromApp(appId)
                                        .makePermanent()
                                        .add();
                                newFlows.add(forwardingObjective);
                            }
                        }
                    }
                }
            }
        }
        //Remove the old flow rule
        for (FlowEntry oldFlow : oldFlows) {
            flowRuleService.removeFlowRules((FlowRule) oldFlow);
        }
        for (Device d : maliciousDeviceList) {
            for (ForwardingObjective f : newFlows) {
                flowObjectiveService.forward(d.id(), f);
            }
        }
        // Need to introduce something like this in the hashMutator thread too.
        log.info("Collusion deactivated.");
    }

    /**
     * Packet processor responsible for adversarial trajectory sampling.
     */
    private class TrajectorySamplingProcessor implements PacketProcessor {

        @Override
        public synchronized void process(PacketContext context) {
            // Stop processing if the packet has been handled, since we
            // can't do any more to it.

            if (context.isHandled()) {
                return;
            }

            InboundPacket pkt = context.inPacket();
            Ethernet ethPkt = pkt.parsed();

            if (ethPkt == null) {
                return;
            }
            if (deviceService.getDeviceCount() == 1) {
                log.info("Single device only, must be for measurements?");
                log.info("Going to drop sampled packets even if trajectorySampling is false.");
                context.block();
                return;
            }

            // Bail if this is deemed to be a control packet.
            if (isControlPacket(ethPkt)) {
                return;
            }

            // For testing, only consider ICMP/TCP traffic for ATS.
            if (isUnwantedPacket(ethPkt)) {
                return;
            }

            if (trajectorySampling) {
                log.info("I just got a packet. Let's add it to the List<History>");
                Instant sampleReceivedStart = Instant.now();

                /*
                 * We just received a packet to sample.
                 * Create a historyEvent using the
                 * Ethernet packet,
                 * the Switch that sampled this packet and
                 * the Port it came from.
                 * Then, append to appropriate historyList.
                 */
                History historyEvent = new History();
                setTimeStamp();
                historyEvent.addEvent(timeStamp, ethPkt, pkt.receivedFrom().deviceId(), pkt.receivedFrom().port());
                /*
                 * Based on the number of detectors configured, dispatch the historyEvent
                 * to the appropriate historyList.
                 * TODO: create historyLists based on number of detectors instead of
                 * statically configured lists.
                 */
                switch (atsDetectors) {
                case 1:
                    log.info("historyList0 added");
                    synchronized (historyList0) {
                        historyList0.add(historyEvent);
                    }
                    break;
                case 2:
                    if (ethPkt.getVlanID() <= 2047) {
                        log.info("historyList0 added");
                        synchronized (historyList0) {
                            historyList0.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2048 && ethPkt.getVlanID() <= 4095) {
                        log.info("historyList1 added");
                        synchronized (historyList1) {
                            historyList1.add(historyEvent);
                        }
                    }
                    break;
                case 3:
                    if (ethPkt.getVlanID() <= 1365) {
                        log.info("historyList0 added");
                        synchronized (historyList0) {
                            historyList0.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 1366 && ethPkt.getVlanID() <= 2731) {
                        log.info("historyList1 added");
                        synchronized (historyList1) {
                            historyList1.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2731 && ethPkt.getVlanID() <= 4095) {
                        synchronized (historyList2) {
                            log.info("historyList2 added");
                            historyList2.add(historyEvent);
                        }
                    }
                    break;
                case 4:
                    if (ethPkt.getVlanID() <= 1022) {
                        log.info("historyList0 added");
                        synchronized (historyList0) {
                            historyList0.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 1023 && ethPkt.getVlanID() <= 2046) {
                        log.info("historyList1 added");
                        synchronized (historyList1) {
                            historyList1.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2047 && ethPkt.getVlanID() <= 3071) {
                        synchronized (historyList2) {
                            log.info("historyList2 added");
                            historyList2.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 3072) {
                        synchronized (historyList3) {
                            log.info("historyList3 added");
                            historyList3.add(historyEvent);
                        }
                    }
                    break;
                case 6:
                    if (ethPkt.getVlanID() <= 681) {
                        log.info("historyList0 added");
                        synchronized (historyList0) {
                            historyList0.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 682 && ethPkt.getVlanID() <= 1363) {
                        log.info("historyList1 added");
                        synchronized (historyList1) {
                            historyList1.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 1364 && ethPkt.getVlanID() <= 2045) {
                        synchronized (historyList2) {
                            log.info("historyList2 added");
                            historyList2.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2046 && ethPkt.getVlanID() <= 2727) {
                        synchronized (historyList3) {
                            log.info("historyList3 added");
                            historyList3.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2728 && ethPkt.getVlanID() <= 3409) {
                        synchronized (historyList4) {
                            log.info("historyList4 added");
                            historyList4.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 3410) {
                        synchronized (historyList5) {
                            log.info("historyList5 added");
                            historyList5.add(historyEvent);
                        }
                    }
                    break;
                case 8:
                    if (ethPkt.getVlanID() <= 511) {
                        log.info("historyList0 added");
                        synchronized (historyList0) {
                            historyList0.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 512 && ethPkt.getVlanID() <= 1023) {
                        log.info("historyList1 added");
                        synchronized (historyList1) {
                            historyList1.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 1024 && ethPkt.getVlanID() <= 1535) {
                        synchronized (historyList2) {
                            log.info("historyList2 added");
                            historyList2.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 1536 && ethPkt.getVlanID() <= 2047) {
                        synchronized (historyList3) {
                            log.info("historyList3 added");
                            historyList3.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2048 && ethPkt.getVlanID() <= 2559) {
                        synchronized (historyList4) {
                            log.info("historyList4 added");
                            historyList4.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 2560 && ethPkt.getVlanID() <= 3071) {
                        synchronized (historyList5) {
                            log.info("historyList5 added");
                            historyList5.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 3072 && ethPkt.getVlanID() <= 3583) {
                        synchronized (historyList6) {
                            log.info("historyList6 added");
                            historyList6.add(historyEvent);
                        }
                    } else if (ethPkt.getVlanID() >= 3583) {
                        synchronized (historyList7) {
                            log.info("historyList7 added");
                            historyList7.add(historyEvent);
                        }
                    }
                    break;
                default:
                    break;
                }
                Instant sampleReceivedStop = Instant.now();
                synchronized (handlingTime) {
                    handlingTime.add((double) Duration.between(sampleReceivedStart,
                            sampleReceivedStop).toMillis());
                }
                // Block the sampled packet.
                context.block();
                return;
            } else {
                log.info("ATS is not yet enabled to detect attacks.");
            }
            return;
        }

    }

    private boolean isPacketInjectionAttack(History historyEvent, List<History> historyList) {
        Path pathPrefix = getPathPrefix(historyEvent);
        if (pathPrefix == null) {

            /*
             * Handle the case where pathPrefix is null as the
             * source and destination switch the same.
             */
            return false;
        }
        List<DeviceId> pathPrefixDeviceIds = new ArrayList<DeviceId>();
        log.info("In isPacketInjectionAttack.");
        pathPrefixDeviceIds = getPathDeviceIds(pathPrefix);
        /*
         * Remove the last switch. We are interested only in switches before
         * it.
         */
        log.info("pathPrefixDeviceIds.size() is: {}",
                pathPrefixDeviceIds.size());
        log.info("pathPrefixDeviceIds is: {}",
                pathPrefixDeviceIds.toString());
        pathPrefixDeviceIds.remove(pathPrefixDeviceIds.size() - 1);
        log.info("Removed the last switch. pathPrefixDeviceIds is: {}",
                pathPrefixDeviceIds.toString());

        for (int i = 0; i < pathPrefixDeviceIds.size(); i = i + 1) {
            /*
             * Check if the packet was meant to be sampled by
             * this switch and check if this packet was not
             * sampled by this switch in the
             * historyList. If both are true, then ATS has
             * detected a packet injection.
             */
            if (isSwitchSampler(pathPrefixDeviceIds.get(i),
                    historyEvent.getHistoryBucketId(),
                    historyEvent.getHistoryTimeStamp())
                    && !isPacketInHistory(historyList,
                            historyEvent.getHistoryBucketId(),
                            pathPrefixDeviceIds.get(i),
                            historyEvent.getHistoryEthPacketHash())) {
                log.error("Packet: {}, was injected between"
                        + "{} switch and {} switch.",
                        historyEvent.getHistoryEthPacket()
                                .toString(),
                        pathPrefixDeviceIds.get(i).toString(),
                        historyEvent.getHistorySrcSwitch()
                                .toString());
                /*
                 * Need to clean up the events that were sampled
                 * by other switches to prevent false positives
                 * in future checks.
                 */
                for (int j = i + 1; j < pathPrefixDeviceIds.size(); j++) {
                    if (isSwitchSampler(pathPrefixDeviceIds.get(j),
                            historyEvent.getHistoryBucketId(),
                            historyEvent.getHistoryTimeStamp())) {
                            isPacketInHistory(historyList,
                                    historyEvent.getHistoryBucketId(),
                                    pathPrefixDeviceIds.get(j),
                                    historyEvent.getHistoryEthPacketHash());
                    }
                }
                return true;
            }
        }
        return false;
    }

    public boolean isUnwantedPacket(Ethernet ethPkt) {
        if (ethPkt.getEtherType() != Ethernet.TYPE_IPV4) {
            log.info("Not an IPv4 packet");
            return true;
        } else if (ethPkt.getEtherType() == Ethernet.TYPE_IPV4) {
            IPv4 ipv4Packet = (IPv4) ethPkt.getPayload();
            if (ipv4Packet.getProtocol() == IPv4.PROTOCOL_UDP) {
                log.info("Not an ICMP/TCP packet, got: {}", ipv4Packet.getProtocol());
                return true;
            }
        }
        return false;
    }

    /*
     * This method must check the pathSuffix for
     * samples matching the oldestEvent.
     */
    private boolean isPacketDropAttack(History oldestEvent, List<History> historyList) {
        Path pathSuffix = getPathSuffix(oldestEvent);
        if (pathSuffix == null) {

            /*
             * Handle the case where pathSuffix is null as
             * the source and destination switch are the
             * same.
             */
            return false;
        }
        List<DeviceId> pathSuffixDeviceIds = getPathDeviceIds(pathSuffix);
        log.info("In isPacketDropAttack.");
        /*
         * Remove the first switch from the
         * pathSuffixDeviceIds. We are only interested in
         * switches after the one that reported the sample.
         */
        log.info("The length of pathSuffixDeviceIds is: {}",
                pathSuffixDeviceIds.size());
        log.info("The pathSuffixDeviceId is: {}",
                pathSuffixDeviceIds.toString());
        pathSuffixDeviceIds.remove(0);
        log.info("Removed the first switch. pathSuffixDeviceIds is: {}",
                pathSuffixDeviceIds.toString());
        for (int i = 0; i < pathSuffixDeviceIds.size(); i = i + 1) {

            /*
             * Check if the packet is meant to be sampled by
             * this switch and check if this packet has not
             * been sampled by another switch in the
             * historyList. If both are true, then ATS has
             * detected a packet drop.
             */
            if (isSwitchSampler(pathSuffixDeviceIds.get(i),
                    oldestEvent.getHistoryBucketId(),
                    oldestEvent.getHistoryTimeStamp())
                    && !isPacketInHistory(historyList,
                            oldestEvent.getHistoryBucketId(),
                            pathSuffixDeviceIds.get(i),
                            oldestEvent.getHistoryEthPacketHash())) {
                log.error("Packet: {}, was dropped between"
                        + "{} switch and {} switch.",
                        oldestEvent.getHistoryEthPacket()
                                .toString(), oldestEvent
                                .getHistorySrcSwitch()
                                .toString(),
                        pathSuffixDeviceIds.get(i));
                /*
                 * Need to clean up the events that were sampled
                 * by other switches to prevent false positives
                 * in future checks.
                 */
                for (int j = i + 1; j < pathSuffixDeviceIds.size(); j++) {
                    if (isSwitchSampler(pathSuffixDeviceIds.get(j),
                            oldestEvent.getHistoryBucketId(),
                            oldestEvent.getHistoryTimeStamp())) {
                            isPacketInHistory(historyList,
                                    oldestEvent.getHistoryBucketId(),
                                    pathSuffixDeviceIds.get(j),
                                    oldestEvent.getHistoryEthPacketHash());
                    }
                }
                return true;
            }
        }
        return false;
    }

    /*
     * This method should check if this packet
     * has been sampled already i.e., does it
     * exist in the historyList. If true, remove
     * it from the historyList
     */
    /*
     * Also need to check the packet here, the bucketId
     * and deviceId are not enough.
     */
    private boolean isPacketInHistory(List<History> historyList, Short bucketId,
            DeviceId deviceId, int ethPacketHash) {
        log.info("In isPacketInHistory. historyList.size(): {}", historyList.size());
        for (int i = 0; i < historyList.size(); i++) {
            if (historyList.get(i).getHistoryBucketId() == bucketId &&
                    historyList.get(i).getHistorySrcSwitch().equals(deviceId) &&
                    historyList.get(i).getHistoryEthPacketHash() ==
                    ethPacketHash) {
                log.info("Found a packet sample in the historyList.");
                log.info("Remove the matched packet sample from the historyList.");
                historyList.remove(i);
                i--;
                return true;
            }
        }
        log.info("Did not find a packet sample in the historyList.");
        return false;
    }

    /*
     * This method should check if this switch
     * is meant to sample this packet. The timeStamp
     * of the event is used to identify the hashes
     * assigned for the respective sampling interval.
     */
    private boolean isSwitchSampler(DeviceId deviceId, Short bucketId, Long timeStamp) {
        List<Short> switchHashList = new ArrayList<Short>();
        log.info("In isSwitchSampler()");
        switchHashList = getSwitchHashAssignment(deviceId, timeStamp);
        if (!switchHashList.isEmpty()) {
            for (short hashAssigned : switchHashList) {
                if (hashAssigned == bucketId) {
                    log.info("Found hash: {} assigned to switch: {} for bucketId: {}",
                            hashAssigned, deviceId.toString(), bucketId);
                    return true;
                }
            }
        }
        log.info("Did not find a hash assigned for switch: {} and bucketId: {}",
                deviceId.toString(), bucketId);
        return false;
    }

    /*
     * This method should return the hash values assigned
     * to a switch for the correct sampling interval.
     * This uses the new data structure timeStampedHashesDevicePairHashMap
     */
    private List<Short> getSwitchHashAssignment(DeviceId deviceId, Long timeStamp) {
        TreeMap<Long, HashMap<DeviceId, List<Short>>> timeStampDeviceIdHashList =
                new TreeMap<Long, HashMap<DeviceId, List<Short>>>();
        timeStampDeviceIdHashList = timeStampedHashesDevicePairHashMap.get(deviceId);
        List<Short> hashAssignment = new ArrayList<>();
        /*
         * Use the timeStamp as the initial matchedKey
         * to find the hashAssignment for the sampled interval.
         */
        if (timeStampDeviceIdHashList == null) {
            return null;
        }
        Long matchedKey = timeStamp;
        for (Long searchKey : timeStampDeviceIdHashList.descendingKeySet()) {
            if (matchedKey >= searchKey) {
                matchedKey = searchKey;
                break;
            }
        }
        for (DeviceId d : timeStampDeviceIdHashList.get(matchedKey).keySet()) {
            if (d == deviceId) {
                continue;
            } else {
                List<Short> hashList = timeStampDeviceIdHashList.get(matchedKey).get(d);
                for (Short hash : hashList) {
                    hashAssignment.add(hash);
                }
            }
        }
        log.info("Found the assigned hashes: {} for the installed timestamp: {}",
                hashAssignment, matchedKey);
        return hashAssignment;
    }

    private HashMap<DeviceId, List<Short>> getSwitchHashAssignmentTable(DeviceId deviceId, Long timeStamp) {
        TreeMap<Long, HashMap<DeviceId, List<Short>>> timeStampDeviceIdHashList =
                new TreeMap<Long, HashMap<DeviceId, List<Short>>>();
        timeStampDeviceIdHashList = timeStampedHashesDevicePairHashMap.get(deviceId);
        HashMap<DeviceId, List<Short>> hashAssignment = new HashMap<DeviceId, List<Short>>();
        /*
         * Use the timeStamp as the initial matchedKey
         * to find the hashAssignment for the sampled interval.
         */
        if (timeStampDeviceIdHashList == null) {
            return null;
        }
        Long matchedKey = timeStamp;
        for (Long searchKey : timeStampDeviceIdHashList.descendingKeySet()) {
            if (matchedKey >= searchKey) {
                matchedKey = searchKey;
                break;
            }
        }
        hashAssignment = timeStampedHashesDevicePairHashMap.get(deviceId).get(matchedKey);
        log.info("Found the assigned hashes: {} for the installed timestamp: {}",
                hashAssignment, matchedKey);
        return hashAssignment;
    }

    /*
     * This method should return the DeviceIds of
     * a path made up of links.
     * It is painful that pathSuffix is made up
     * of links. As of now, this is the only way
     * I know of getting to the DeviceId of the
     * switch.
     */
    private List<DeviceId> getPathDeviceIds(Path pathDevices) {
        List<DeviceId> pathDeviceIds = new ArrayList<DeviceId>();
        List<Link> pathLinks = pathDevices.links();
        log.info("Traverse the switches and return their DeviceIds");
        log.info("pathLinks.size() = {}", pathLinks.size());
        /*
         * Handle the case where there are only 2
         * switches i.e. h1---s1---s2---h2.
         */
        if (pathLinks.size() >= 1) {
            //Link curLink = pathLinks.get(0);
            //DeviceId curDevice = curLink.src().deviceId();
            //log.info("getPathDeviceIds: DeviceId: {}", curDevice.toString());
            pathDeviceIds.add(pathLinks.get(0).src().deviceId());
            pathDeviceIds.add(pathLinks.get(0).dst().deviceId());
        }
        for (int i = 1; i < pathLinks.size(); i = i + 1) {
            Link curLink = pathLinks.get(i);
            DeviceId curDevice = curLink.dst().deviceId();
            log.info("getPathDeviceIds: DeviceId: {}", curDevice.toString());
            pathDeviceIds.add(curDevice);
        }
        if (pathDeviceIds.isEmpty()) {
           return null;
        } else {
            return pathDeviceIds;
        }
    }

    /*
     * This method should return the Path of
     * links before the switch that sampled
     * the given historyEvent. This includes
     * the switch that sampled the historyEvent.
     */
    private Path getPathPrefix(History historyEvent) {
        Host srcHost = hostService.getHost(HostId.hostId(historyEvent
                .getHistoryEthPacket()
                .getSourceMAC()));
        Host dstHost = hostService.getHost(HostId.hostId(historyEvent
                .getHistoryEthPacket()
                .getDestinationMAC()));
        DeviceId srcSwitch = srcHost.location().deviceId();
        Set<Path> paths =
                topologyService.getPaths(topologyService.currentTopology(),
                                         srcSwitch,
                                         historyEvent.getHistorySrcSwitch());
        Path pathPrefixInstalled = null;

        /*
         * Handle the case if this packet is completely
         * spurious i.e., no path exists for this packet
         * in the historyList.
         * If the 2 hosts are on the same
         * switch. The paths.isEmpty() will be true.
         * This needs to be handled elegantly.
         * Another case that needs to be handled
         * is when the edge is one of
         * the first to sample.
         */
        if (paths.isEmpty()) {
            log.warn("It could be that the source and destination are on the same switch.");
            log.warn("Wait, how did we get this packet if there is no path?!");
            log.warn("Adversarial Trajectory Sampling detected the following" +
               "switch {} to have sampled a packet that may not have a path.",
               historyEvent.getHistorySrcSwitch().toString());
            return null;
        }
        /*
         * After we get the paths, we need to find
         * the path that exists on the switches. Therefore,
         * the flowRuleService is queried.
         * Link = srcSwitch-outPort--dstSwitch-inPort
         * 1. Iterate through the paths.
         * 2. Iterate through each link in the path.
         * 3. Iterate through all flows on the destination
         * switch of the link
         * 4. Match the flow's inPort of the dstSwitch.
         * 5. Match the flow's srcMac and dstMac with
         * the packets src/dstMac.
         * 6. If the 3 conditions match, then we are on
         * the right links of the path. Otherwise, get
         * the next path and re-iterate.
         */
        boolean matchesOutPort = false;
        boolean matchesSrcHost = false;
        boolean matchesDstHost = false;
        for (Path pathPrefix : paths) {
            //Get the links from the pathSuffix.
            List<Link> pathLinks = pathPrefix.links();
            matchesOutPort = false;
            matchesSrcHost = false;
            matchesDstHost = false;
            for (Link linkInPath : pathLinks) {
                log.info("getPathPrefix:The link is: {}", linkInPath.toString());
                DeviceId dstDevice = linkInPath.dst().deviceId();
                PortNumber dstPort = linkInPath.dst().port();
                matchesOutPort = false;
                matchesSrcHost = false;
                matchesDstHost = false;
                log.debug("In pathPrefix: iterating over the links. Before checking flows.");

                for (FlowEntry r : flowRuleService.getFlowEntries(dstDevice)) {
                    log.debug("getPathPrefix: Inside flowEntry r: {}", r.toString());
                    for (Instruction i : r.treatment().allInstructions()) {
                        //Interested in only the sampling rules?
                        if (i.type() == Instruction.Type.OUTPUT) {
                            for (Criterion cr : r.selector().criteria()) {
                                log.debug("criterion for this flow is: {}", cr.toString());
                                if (cr.type() == Criterion.Type.IN_PORT) {
                                    if (((PortCriterion) cr).port().equals(dstPort)) {
                                        log.debug("matchesOutPort = true");
                                        log.debug("Flow_InPort: {}, Link_InPort: {}",
                                                ((PortCriterion) cr).port().toString(),
                                                dstPort);
                                        matchesOutPort = true;
                                    }
                                } else if (cr.type() == Criterion.Type.ETH_SRC) {
                                    if (((EthCriterion) cr).mac().equals(srcHost.mac())) {
                                        log.debug("matchesSrcMac = true");
                                        log.debug("Flow_SrcMac: {}, Link_SrcMac: {}",
                                                ((EthCriterion) cr).mac().toString(),
                                                srcHost.toString());
                                        matchesSrcHost = true;
                                    }
                                } else if (cr.type() == Criterion.Type.ETH_DST) {
                                    if (((EthCriterion) cr).mac().equals(dstHost.mac())) {
                                        log.debug("matchesDstMac = true");
                                        log.debug("Flow_DstMac: {}, Link_DstMac: {}",
                                                ((EthCriterion) cr).mac().toString(),
                                                dstHost.toString());
                                        matchesDstHost = true;
                                    }
                                }
                            }
                        }
                    }
                    if (matchesOutPort && matchesSrcHost && matchesDstHost) {
                        log.debug("Found the exact flow on the switch. Check the next switch in the path.");
                        break;
                    }
                }
                if (matchesOutPort && matchesSrcHost && matchesDstHost) {
                    log.debug("On the right path, continue checking flow entries.");
                    //continue;
                } else {
                    log.debug("Not on the installed path, check the next available path.");
                    break;
                }
            }
            if (matchesOutPort && matchesSrcHost && matchesDstHost) {
                pathPrefixInstalled = pathPrefix;
                log.info("Found the installed path. pathPrefixInstalled: {}", pathPrefixInstalled.toString());
                break;
            }
        }
        return pathPrefixInstalled;
    }

    /*
     * This method should return the Path of
     * links after the switch that sampled
     * this historyEvent. This includes
     * the switch that sampled the historyEvent.
     */
    private Path getPathSuffix(History oldestEvent) {
        Host destHost = hostService.getHost(HostId.hostId(oldestEvent
                .getHistoryEthPacket()
                .getDestinationMAC()));
        Host srcHost = hostService.getHost(HostId.hostId(oldestEvent
                .getHistoryEthPacket()
                .getSourceMAC()));
        DeviceId destSwitch = destHost.location().deviceId();
        Set<Path> paths =
                topologyService.getPaths(topologyService.currentTopology(),
                                         oldestEvent.getHistorySrcSwitch(),
                                         destSwitch);
        Path pathSuffixInstalled = null;

        /*
         * Handling below is similar to the getPathPrefix method.
         */
        if (paths.isEmpty()) {
            log.warn("getPathSuffix:It could be that the source and destination are on the same switch.");
            log.warn("getPathSuffix:Wait, how did we get this packet if there is no path?!");
            log.warn("getPathSuffix:Adversarial Trajectory Sampling detected the following" +
               "switch {} to have sampled a packet that may not have a path.",
               oldestEvent.getHistorySrcSwitch().toString());
            return null;
        }
        boolean matchesOutPort = false;
        boolean matchesSrcHost = false;
        boolean matchesDestHost = false;
        for (Path pathSuffix : paths) {
            //Get the links from the pathSuffix.
            List<Link> pathLinks = pathSuffix.links();
            matchesOutPort = false;
            matchesSrcHost = false;
            matchesDestHost = false;
            for (Link linkInPath : pathLinks) {
                log.debug("getPathSuffix:The link is: {}", linkInPath.toString());
                DeviceId dstDevice = linkInPath.dst().deviceId();
                PortNumber dstPort = linkInPath.dst().port();
                matchesOutPort = false;
                matchesSrcHost = false;
                matchesDestHost = false;
                log.debug("In pathSuffix: iterating over the links. Before checking flows.");

                for (FlowEntry r : flowRuleService.getFlowEntries(dstDevice)) {
                    log.debug("getPathSuffix: Inside flowEntry r: {}", r.toString());
                    for (Instruction i : r.treatment().allInstructions()) {
                        //Interested in only the sampling rules?
                        if (i.type() == Instruction.Type.OUTPUT) {
                            for (Criterion cr : r.selector().criteria()) {
                                log.debug("criterion for this flow is: {}", cr.toString());
                                if (cr.type() == Criterion.Type.IN_PORT) {
                                    if (((PortCriterion) cr).port().equals(dstPort)) {
                                        log.debug("matchesOutPort = true");
                                        log.debug("Flow_InPort: {}, Link_InPort: {}",
                                                ((PortCriterion) cr).port().toString(),
                                                dstPort);
                                        matchesOutPort = true;
                                    }
                                } else if (cr.type() == Criterion.Type.ETH_SRC) {
                                    if (((EthCriterion) cr).mac().equals(srcHost.mac())) {
                                        log.debug("matchesSrcMac = true");
                                        log.debug("Flow_SrcMac: {}, Link_SrcMac: {}",
                                                ((EthCriterion) cr).mac().toString(),
                                                srcHost.toString());
                                        matchesSrcHost = true;
                                    }
                                } else if (cr.type() == Criterion.Type.ETH_DST) {
                                    if (((EthCriterion) cr).mac().equals(destHost.mac())) {
                                        log.debug("matchesDestMac = true");
                                        log.debug("Flow_DstMac: {}, Link_DstMac: {}",
                                                ((EthCriterion) cr).mac().toString(),
                                                destHost.toString());
                                        matchesDestHost = true;
                                    }
                                }
                            }
                        }
                    }
                    if (matchesOutPort && matchesSrcHost && matchesDestHost) {
                        log.debug("Found the exact flow on the switch. Check the next switch in the path.");
                        break;
                    }
                }
                if (matchesOutPort && matchesSrcHost && matchesDestHost) {
                    log.debug("On the right path, continue checking flow entries.");
                    //continue;
                } else {
                    log.debug("Not on the installed path, check the next available path.");
                    break;
                }
            }
            if (matchesOutPort && matchesSrcHost && matchesDestHost) {
                pathSuffixInstalled = pathSuffix;
                log.info("Found the installed path. pathSuffixInstalled: {}", pathSuffixInstalled.toString());
                break;
            }
        }
        return pathSuffixInstalled;
    }

    // Indicates whether this is a control packet, e.g. LLDP, BDDP
    private boolean isControlPacket(Ethernet eth) {
        short type = eth.getEtherType();
        return type == Ethernet.TYPE_LLDP || type == Ethernet.TYPE_BSN;
    }

    /*
     * Algorithm 2: This task periodically installs new sampling
     * rules on a random switch. Auxiliary task to update flow
     * rules with new hashes on the switches.
     */
    private final class HashMutator implements Runnable {
        Random hashMutator = new Random();
        Random switchMutator = new Random();
        Random oldHashRemover = new Random();
        int mutations = 0;
        private HashMutator(int hashMutatorSeed, int switchMutatorSeed) {
            this.hashMutator.setSeed(hashMutatorSeed);
            this.switchMutator.setSeed(switchMutatorSeed);
            this.oldHashRemover.setSeed(switchMutatorSeed);
        }
        //Use PoissonDistribution for random sleep time between mutations.
        PoissonDistribution poissonDistribution = new PoissonDistribution();
        @Override
        public void run() {
            while (hashMutation) {
                try {
                    int sleepTime = poissonDistribution.nextPoisson(updateRate) * 1000;
                    if (pairAssignment) {
                        mutatePairsOnSwitch(hashMutator, switchMutator, oldHashRemover);
                        //Added another pair-mutation for faster detection
                        mutatePairsOnSwitch(hashMutator, switchMutator, oldHashRemover);
                        this.mutations += 2;
                    } else {
                        mutateHashesOnSwitch();
                    }
                    log.info("Mutated hashes on a switch. Total Mutations: {}", this.mutations);
                    Thread.sleep(sleepTime);
                } catch (InterruptedException e) {
                    if (Thread.currentThread().isInterrupted()) {
                        log.info("Hash update Interrupted, quitting");
                        return;
                    }
                } catch (Exception e) {
                    // Catch all exceptions to avoid task being suppressed
                    log.error("Exception thrown during synchronization process", e);
                }
            }
        }
    }

    private final class Detector implements Runnable {

        List<History> detectorList;
        AtsProfiler detectorProfiler;

        private Detector(List<History> historyList, int id) {
            this.detectorList = historyList;
            this.detectorProfiler = new AtsProfiler(id);
        }
        @Override
        /*
         * This thread performs the actual
         * detection.
         * In the paper this is known as verifying
         * the sample's requirements.
         */
        public void run() {
            //boolean done = false;
            if (Thread.currentThread().isInterrupted()) {
                log.info("Detector interrupted, quitting");
                return;
            }
            try {
                //while (!done) {
                synchronized (detectorList) {
                    if (detectorList.size() == 0) {
                        return;
                    }
                    if (Duration.between(t0, Instant.now()).getSeconds() < DEFAULT_RTT) {
                        //log.info("The oldestEvent has not yet completed an RTT.");
                        return;
                    }
                    while (detectorList.size() > 0 &&
                            detectorList.get(0).getHistoryTimeStamp() <
                            Duration.between(t0, Instant.now()).getSeconds()
                            - DEFAULT_RTT) {
                        detectorProfiler.setStartTime(Instant.now());
                        History oldestEvent = detectorList.remove(0);
                        log.info("After pop oldestEvent, detectorList.size: {}",
                                detectorList.size());
                        log.info("oldestEvent timestamp {}, timestamp: {}, RTT:{}",
                                oldestEvent.getHistoryTimeStamp(), timeStamp,
                                DEFAULT_RTT);
                        log.info("oldestEvent hash: {}, oldestEvent srcSwitch: {}",
                                oldestEvent.getHistoryEthPacketHash(),
                                oldestEvent.getHistorySrcSwitch().toString());
                        /*
                         * If it has at least reached its RTT, then find out
                         * the path the packet should have taken.
                         */
                        log.info("First look for packet drop attacks.");
                        if (isPacketDropAttack(oldestEvent, detectorList)) {
                            log.error("ATS found a packet drop attack! hash_value:{}.",
                                    oldestEvent.getHistoryBucketId());
                        }

                        /*
                         * In order to handle the case where the second
                         * sample arrives before the first, we need to
                         * check the pathPrefix only after the pathSuffix
                         * and not outside of it.
                         * Now check the past i.e., where was the packet
                         * supposed to have come from. Get the pathPrefix of
                         * switches. Check if this packet was supposed to be
                         * sampled by a switch in the pathPrefix and check if
                         * this packet is not in the historyList. If both are
                         * true, then ATS has detected a packet injection.
                         */
                        log.info("Now look for packet injection attacks.");
                        /*
                         * Check for packet injections for the oldestEvent
                         * and not the historyEvent (earliest).
                         */
                        if (isPacketInjectionAttack(oldestEvent, detectorList)) {
                            log.error("ATS found a packet injection attack! hash_value:{}.",
                                    oldestEvent.getHistoryBucketId());
                        }
                        detectorProfiler.setStopTime(Instant.now());
                        detectorProfiler.computeDetectionRate();
                        detectorProfiler.addToProfileTable(profileTable);
                        log.info("The oldestEvent has been checked and removed.");
                    }
                }
                //}
            } catch (Exception e) {
                log.error("Exception thrown during detection", e);
            }
        }
    }

    /*
     * Algorithm 2:
     * This method picks an available switch at random.
     * Then removes the old sampling rules.
     * Selects hash values at random and installs them
     * on the switch as flow rules.
     */
    public void mutateHashesOnSwitch() {
        /*
         * Pick a switch at random
         */
        if (deviceService.getDeviceCount() == 0) {
            log.info("No available devices yet.");
            return;
        }
        List<Short> switchHashAssignment = new ArrayList<Short>();
        List<FlowEntry> oldFlows = new ArrayList<FlowEntry>();
        Iterator<Device> switchIterator = deviceService.getAvailableDevices(
                Device.Type.SWITCH).iterator();
        List<DeviceId> deviceIdList = new ArrayList<DeviceId>();
        while (switchIterator.hasNext()) {
            deviceIdList.add(switchIterator.next().id());
        }
        DeviceId randomSwitch = deviceIdList.get(RandomUtils.nextInt(deviceService.getDeviceCount()));
        for (FlowEntry flowEntry : flowRuleService.getFlowEntries(randomSwitch)) {
            if (flowEntry.priority() == 50001) {
                oldFlows.add(flowEntry);
            }
        }

        /*
         * Then select random hash values for the switch
         * and install them as flows.
         */
        //set the seed to 0 for same random sequence
        //Random randomSequence = new Random(1);
        int[] firstSeq = {1, 2, 3, 4};
        int[] secSeq = {1023, 1024, 1025, 1026};
        for (int i = 0; i < samplingSize; i++) {
            TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
            VlanId vlanId = VlanId.NONE;
            if (i % 2 == 0) {
                vlanId = VlanId.vlanId((short) firstSeq[i]);
            } else {
                vlanId = VlanId.vlanId((short) secSeq[i]);
            }
            //VlanId vlanId = VlanId.vlanId((short) RandomUtils.nextInt(1022));
            switchHashAssignment.add(vlanId.toShort());
            selector.matchVlanId(vlanId);

            TrafficTreatment treatment = DefaultTrafficTreatment.builder()
                    .setOutput(PortNumber.CONTROLLER)
                    .transition(2)
                    .build();

            ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                    .withSelector(selector.build())
                    .withTreatment(treatment)
                    .withPriority(50001)
                    .withFlag(ForwardingObjective.Flag.VERSATILE)
                    .fromApp(appId)
                    .makePermanent()
                    .add();

            flowObjectiveService.forward(randomSwitch,
                    forwardingObjective);
        }
        //Set the timestamp for the new hashes
        setTimeStamp();
        TreeMap<Long, List<Short>> timeStampedHashes = timeStampedHashesAssigned.get(randomSwitch);
        /*
         * Handle the case if a switch was not
         * available previously but is available
         * now.
         */
        if (timeStampedHashes != null) {
            timeStampedHashes.put(timeStamp, switchHashAssignment);
            timeStampedHashesAssigned.replace(randomSwitch, timeStampedHashes);
        } else {
            TreeMap<Long, List<Short>> newTimeStampedHashes = new TreeMap<Long, List<Short>>();
            newTimeStampedHashes.put(timeStamp, switchHashAssignment);
            timeStampedHashesAssigned.put(randomSwitch, newTimeStampedHashes);
        }
        /*switchesHashesAssigned.replace(randomSwitch, switchHashAssignment);
        log.info("Assigned the Random switch: {} with the following values: {}",
                randomSwitch.toString(), switchesHashesAssigned.get(randomSwitch));*/
        log.info("timeStampedHashesAssigned: {}", timeStampedHashesAssigned.toString());
        /*
         * Now remove the old sampling rules
         */
        for (FlowEntry oldFlow : oldFlows) {
            flowRuleService.removeFlowRules((FlowRule) oldFlow);
        }
    }
    /*
     * Algorithm 2:
     * This method picks an available switch pair at random.
     * Changes this pairs assignment and installs them
     * on the switches as flow rules.
     */
    public void mutatePairsOnSwitch(Random hashMutator, Random switchMutator, Random oldHashRemover) {
        //Pick a random switch pair.
        if (deviceService.getDeviceCount() == 0) {
            log.info("No available devices yet.");
            return;
        }
        int deviceCount = deviceService.getDeviceCount();
        List<FlowEntry> oldFlows = new ArrayList<FlowEntry>();
        short oldVlanId = 0;
        List<Short> oldVlanIdsFromHashMap = new ArrayList<Short>();
        List<Device> deviceIdList = getSortedDeviceIds();
        DeviceId randomSwitch1 = deviceIdList.get(switchMutator.nextInt(deviceCount)).id();
        DeviceId randomSwitch2 = deviceIdList.get(switchMutator.nextInt(deviceCount)).id();
        boolean foundPair = false;
        // Set the timeStamp now, to get the latest assignment.
        setTimeStamp();
        while (!foundPair) {
            if (randomSwitch1 != randomSwitch2) {
                foundPair = true;
            } else {
                randomSwitch2 = deviceIdList.get(switchMutator.nextInt(deviceCount)).id();
            }
        }
        log.info("Going to mutate the switch pair:{},{}", randomSwitch1, randomSwitch2);
        /*
         * Now find the hash assigned for this switch pair
         */
        // First in timeStampedHashesDevicePairHashMap, then as flow rules.
        log.info("New implementation of finding the old flow rules.");
        oldVlanIdsFromHashMap = getSwitchHashAssignmentTable(randomSwitch1, timeStamp).get(randomSwitch2);
        oldFlows = new ArrayList<FlowEntry>();
        for (FlowEntry flowEntrySwitch1 : flowRuleService.getFlowEntries(randomSwitch1)) {
            for (Criterion crSwitch1 : flowEntrySwitch1.selector().criteria()) {
                if (crSwitch1.type() == Criterion.Type.VLAN_VID) {
                    for (Short vlandId : oldVlanIdsFromHashMap) {
                        if (((VlanIdCriterion) crSwitch1).vlanId().toShort() == vlandId) {
                            oldFlows.add(flowEntrySwitch1);
                        }
                    }
                }
            }
        }
        for (FlowEntry flowEntrySwitch2 : flowRuleService.getFlowEntries(randomSwitch2)) {
            for (Criterion crSwitch2 : flowEntrySwitch2.selector().criteria()) {
                if (crSwitch2.type() == Criterion.Type.VLAN_VID) {
                    for (Short vlandId : oldVlanIdsFromHashMap) {
                        if (((VlanIdCriterion) crSwitch2).vlanId().toShort() == vlandId) {
                            oldFlows.add(flowEntrySwitch2);
                        }
                    }
                }
            }
        }
        /*
         * Then select a random hash value for the switch pair
         * and install them as flows.
         */
        TrafficSelector.Builder selector = DefaultTrafficSelector.builder();
        VlanId newVlanId = VlanId.vlanId((short) hashMutator.nextInt(4096));
        log.info("New VlanId is:{}", newVlanId);
        selector.matchVlanId(newVlanId);
        TrafficTreatment treatment = DefaultTrafficTreatment.emptyTreatment();
        if (collusion &&
                randomSwitch1.toString().compareTo(colludingSwitch1) == 0 &&
                randomSwitch2.toString().compareTo(colludingSwitch2) == 0 ||
                randomSwitch1.toString().compareTo(colludingSwitch2) == 0 &&
                randomSwitch2.toString().compareTo(colludingSwitch1) == 0) {
                //randomSwitch1=colludingSwitch1; randomSwitch2=colludingSwitch2
                //randomSwitch1=colludingSwitch2; randomSwitch2=colludingSwitch1
            treatment = DefaultTrafficTreatment.builder()
                    .transition(2)
                    .build();
        } else {
            treatment = DefaultTrafficTreatment.builder()
                    .setOutput(PortNumber.CONTROLLER)
                    .transition(2)
                    .build();
        }
        ForwardingObjective forwardingObjective = DefaultForwardingObjective.builder()
                .withSelector(selector.build())
                .withTreatment(treatment)
                .withPriority(50001)
                .withFlag(ForwardingObjective.Flag.VERSATILE)
                .fromApp(appId)
                .makePermanent()
                .add();
        //Set the timestamp for the new hashes
        setTimeStamp();
        flowObjectiveService.forward(randomSwitch1,
                    forwardingObjective);
        flowObjectiveService.forward(randomSwitch2,
                forwardingObjective);
        /*
         * Replace the old hash value with a new one.
         * Make sure the new timestamp has hash values
         * that did not change too.
         */
        // Add the random switches to a List
        List<DeviceId> randomSwitchList = new ArrayList<DeviceId>();
        randomSwitchList.add(randomSwitch1);
        randomSwitchList.add(randomSwitch2);
        // Iterate forward and backwards over that list
        // to update the global assignment.
        for (int i = 0; i < randomSwitchList.size(); i++) {
            for (int j=randomSwitchList.size() - 1; j >= 0; j--) {
                if (i == j) {
                    continue;
                } else {
                    TreeMap<Long, HashMap<DeviceId, List<Short>>> timeStampDeviceIdHashList =
                            new TreeMap<Long, HashMap<DeviceId, List<Short>>>();
                    // First duplicate the existing assignment
                    timeStampDeviceIdHashList.putAll(timeStampedHashesDevicePairHashMap.get(randomSwitchList.get(i)));
                    // Then insert a new timestamp key with the old values for both switches.
                    // Now insert a hard copy for the new timestamp
                    HashMap<DeviceId, List<Short>> refToCurrentAssignment =
                            new HashMap<DeviceId, List<Short>>(getSwitchHashAssignmentTable(randomSwitchList.get(i), timeStamp));
                    HashMap<DeviceId, List<Short>> copyOfCurrentAssignment =
                            new HashMap<DeviceId, List<Short>>();
                    for (DeviceId d : refToCurrentAssignment.keySet()) {
                        List<Short> hashValues = new ArrayList<Short>();
                        for (Short s : refToCurrentAssignment.get(d)) {
                            hashValues.add(s);
                        }
                        copyOfCurrentAssignment.put(d, hashValues);
                    }
                    timeStampDeviceIdHashList.put(timeStamp, copyOfCurrentAssignment);
                    HashMap<DeviceId, List<Short>> deviceIdHashList = timeStampDeviceIdHashList.get(timeStamp);
                    // Now randomly select the old hash value to remove
                    List<Short> oldVlans = new ArrayList<Short>();
                    List<Short> newVlans = new ArrayList<Short>();
                    for (Short vlan : deviceIdHashList.get(randomSwitchList.get(j))) {
                        oldVlans.add(vlan);
                    }
                    if (oldVlans.size() == 1) {
                        oldVlanId = oldVlans.get(0);
                    } else if (oldVlans.size() > 1) {
                        oldVlanId = oldVlans.get(oldHashRemover.nextInt(oldVlans.size()));
                    } else {
                        log.warn("oldVlans.size() is empty! Won't remove anything");
                    }
                    // Now remove that vlanId
                    log.info("OldVlanId is:{}", oldVlanId);
                    for (int k = 0; k < oldVlans.size(); k++) {
                        if (oldVlans.get(k) == oldVlanId) {
                            oldVlans.remove(k);
                            break;
                        }
                    }
                    // Now, insert the new hash value/newVlanId.
                    newVlans.add(newVlanId.toShort());
                    for (Short vlan : oldVlans) {
                        if (vlan != null) {
                            newVlans.add(vlan);
                        }
                    }
                    deviceIdHashList.replace(randomSwitchList.get(j), newVlans);
                    timeStampDeviceIdHashList.replace(timeStamp, deviceIdHashList);
                    // Now, insert into the global data structure
                    log.info("Now insert into the global data structure");
                    synchronized (timeStampedHashesDevicePairHashMap) {
                        timeStampedHashesDevicePairHashMap.put(randomSwitchList.get(i), timeStampDeviceIdHashList);
                    }
                }
            }
        }
        /*
         * Debug code for printing the values.
            for (DeviceId d : timeStampedHashesDevicePairHashMap.keySet()) {
                if (d.toString().compareTo(randomSwitch1.toString()) == 0 ||
                        d.toString().compareTo(randomSwitch2.toString()) == 0 ||
                        d.toString().compareTo(randomSwitch1.toString()) != 0) {
                    log.info("DeviceId: {}", d.toString());
                    for (Long l : timeStampedHashesDevicePairHashMap.get(d).keySet()) {
                        log.info("TimeStamp: {}", l);
                        for (DeviceId dId : timeStampedHashesDevicePairHashMap.get(d).get(l).keySet()) {
                            log.info("DeviceId: {}", dId.toString());
                            log.info("Hash values:{}", timeStampedHashesDevicePairHashMap.get(d).get(l).get(dId));
                        }
                    }
                }
                log.info("Next deviceKey");
            }
        */
        //Now remove only the old sampling rules based on the randomly selected oldVlanId.
        for (FlowEntry oldFlow : oldFlows) {
            for (Criterion crSwitch1 : oldFlow.selector().criteria()) {
                if (crSwitch1.type() == Criterion.Type.VLAN_VID) {
                    if (((VlanIdCriterion) crSwitch1).vlanId().toShort() == oldVlanId) {
                        flowRuleService.removeFlowRules((FlowRule) oldFlow);                        
                    }
                }
            }
        }
    }
}
