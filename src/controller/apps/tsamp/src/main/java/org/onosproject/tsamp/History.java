/**
 * The data structure to store events.
 * The History constitutes of a
 * Timestamp, Ethernet frame,
 * the Switch that sampled this frame,
 * the Port of the switch that sampled
 * this frame and
 * a Hash of the source-and-destination
 * MAC, IP and TCP/UDP Ports.
 * Currently, the names of the fields
 * and methods are not clear. Need to
 * change this.
 * Author: Kashyap Thimmaraju
 * Email: kashyap.thimmaraju@sect.tu-berlin.de
 */
package org.onosproject.tsamp;

import org.onlab.packet.Ethernet;
import org.onlab.packet.ICMP;
import org.onlab.packet.IPv4;
import org.onlab.packet.TCP;
import org.onlab.packet.UDP;
import org.onosproject.net.DeviceId;
import org.onosproject.net.PortNumber;

public class History {
    private long timeStamp;
    private Ethernet ethPacket;
    private DeviceId srcSwitch;
    private PortNumber srcSwitchInPort;
    private int ethPacketHash;
    private short bucketId;

    /*
     * The constructor
     * creates an empty/null
     * History event. This
     * could be optimized to give
     * it the necessary objects
     * on instantiation.
     */
    public History() {
        timeStamp = 0;
        ethPacket = null;
        srcSwitch = null;
        srcSwitchInPort = null;
        ethPacketHash = 0;
        bucketId = 0;
    }

    private void setTimeStamp(long timeStamp) {
        this.timeStamp = timeStamp;
    }

    private void setHistoryethPacket(Ethernet ethPacket) {
        this.ethPacket = ethPacket;
    }

    private void setSrcSwitch(DeviceId srcSwitch) {
        this.srcSwitch = srcSwitch;
    }

    private void setSrcSwitchInPort(PortNumber srcSwitchInPort) {
        this.srcSwitchInPort = srcSwitchInPort;
    }

    private void setEthPacketHash(Ethernet ethPacket) {
        this.ethPacketHash = hashEthPacket(ethPacket);
    }

    private void setBucketId(short bucketId) {
        this.bucketId = bucketId;
    }

    /*
     * A helper method that performs a hash on
     * fields ATS is only interested in.
     * result = 1 initially and changes as
     * the hashCode() for ethernet, ipv4 and
     * tcp provide their own hashCode() which
     * we make use of here.
     */
    public int hashEthPacket(Ethernet ethPacket) {
        final int prime = 7867;
        int result = 1;
        if (ethPacket.getEtherType() == Ethernet.TYPE_IPV4) {
            IPv4 ipv4Packet = (IPv4) ethPacket.getPayload();
            result = prime * result + ethPacket.hashCode();
            result = prime * result + ipv4Packet.hashCode();
            if (ipv4Packet.getProtocol() == IPv4.PROTOCOL_ICMP) {
                ICMP icmpPacket = (ICMP) ipv4Packet.getPayload();
                result = prime * result + icmpPacket.hashCode();
            } else if (ipv4Packet.getProtocol() == IPv4.PROTOCOL_TCP) {
                TCP tcpPacket = (TCP) ipv4Packet.getPayload();
                result = prime * result + tcpPacket.hashCode();
            } else if (ipv4Packet.getProtocol() == IPv4.PROTOCOL_UDP) {
                UDP udpPacket = (UDP) ipv4Packet.getPayload();
                result = prime * result + udpPacket.hashCode();
            }
        } else {
            //Set the hash to 0 for non-IPv4 packets
            result = 0;
        }
        return result;
    }

    /*
     * The addEvent method is invoked to fill up the
     * fields in the History event/object.
     */
    public void addEvent(long timeStamp, Ethernet ethPacket,
            DeviceId srcSwitch, PortNumber srcSwitchInPort) {
        setTimeStamp(timeStamp);
        setHistoryethPacket(ethPacket);
        setSrcSwitch(srcSwitch);
        setSrcSwitchInPort(srcSwitchInPort);
        setEthPacketHash(ethPacket);
        setBucketId(ethPacket.getVlanID());
    }

    public long getHistoryTimeStamp() {
        return this.timeStamp;
    }

    public Ethernet getHistoryEthPacket() {
        return this.ethPacket;
    }

    public DeviceId getHistorySrcSwitch() {
        return this.srcSwitch;
    }

    public PortNumber getHistorySrcSwitchInPort() {
        return this.srcSwitchInPort;
    }

    public int getHistoryEthPacketHash() {
        return this.ethPacketHash;
    }

    public short getHistoryBucketId() {
        return this.bucketId;
    }

    public String toString() {
        String out = "This History Object contains: ";
        out += "\nTimeStamp: " + getHistoryTimeStamp();
        out += "\nEthernet Frame: " + getHistoryEthPacket().toString();
        out += "\nSrcSwitch: " + getHistorySrcSwitch().toString();
        out += "\nSrcSwitchInPort: " + getHistorySrcSwitchInPort().toString();
        out += "\nEthPacketHash: " + getHistoryEthPacketHash();
        out += "\nBucketId: " + getHistoryBucketId();
        return out;
    }
}
