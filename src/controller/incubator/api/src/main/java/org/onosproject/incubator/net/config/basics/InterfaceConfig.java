/*
 * Copyright 2015 Open Networking Laboratory
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
 */

package org.onosproject.incubator.net.config.basics;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.google.common.annotations.Beta;
import com.google.common.collect.Sets;
import org.onlab.packet.MacAddress;
import org.onlab.packet.VlanId;
import org.onosproject.incubator.net.intf.Interface;
import org.onosproject.net.ConnectPoint;
import org.onosproject.net.config.Config;
import org.onosproject.net.host.InterfaceIpAddress;

import java.util.Iterator;
import java.util.Set;

/**
 * Configuration for interfaces.
 */
@Beta
public class InterfaceConfig extends Config<ConnectPoint> {
    public static final String NAME = "name";
    public static final String IPS = "ips";
    public static final String MAC = "mac";
    public static final String VLAN = "vlan";

    public static final String CONFIG_VALUE_ERROR = "Error parsing config value";

    /**
     * Retrieves all interfaces configured on this port.
     *
     * @return set of interfaces
     * @throws ConfigException if there is any error in the JSON config
     */
    public Set<Interface> getInterfaces() throws ConfigException {
        Set<Interface> interfaces = Sets.newHashSet();

        try {
            for (JsonNode intfNode : array) {
                String name = intfNode.path(NAME).asText(null);

                Set<InterfaceIpAddress> ips = getIps(intfNode);

                String mac = intfNode.path(MAC).asText();
                MacAddress macAddr = mac.isEmpty() ? null : MacAddress.valueOf(mac);

                VlanId vlan = getVlan(intfNode);

                interfaces.add(new Interface(name, subject, ips, macAddr, vlan));
            }
        } catch (IllegalArgumentException e) {
            throw new ConfigException(CONFIG_VALUE_ERROR, e);
        }

        return interfaces;
    }

    /**
     * Adds an interface to the config.
     *
     * @param intf interface to add
     */
    public void addInterface(Interface intf) {
        ObjectNode intfNode = array.addObject();

        intfNode.put(NAME, intf.name());

        if (intf.mac() != null) {
            intfNode.put(MAC, intf.mac().toString());
        }

        if (!intf.ipAddresses().isEmpty()) {
            intfNode.set(IPS, putIps(intf.ipAddresses()));
        }

        if (!intf.vlan().equals(VlanId.NONE)) {
            intfNode.put(VLAN, intf.vlan().toString());
        }
    }

    /**
     * Removes an interface from the config.
     *
     * @param name name of the interface to remove
     */
    public void removeInterface(String name) {
        Iterator<JsonNode> it = array.iterator();
        while (it.hasNext()) {
            JsonNode node = it.next();
            if (node.path(NAME).asText().equals(name)) {
                it.remove();
                break;
            }
        }
    }

    private VlanId getVlan(JsonNode node) {
        VlanId vlan = VlanId.NONE;
        if (!node.path(VLAN).isMissingNode()) {
            vlan = VlanId.vlanId(Short.valueOf(node.path(VLAN).asText()));
        }
        return vlan;
    }

    private Set<InterfaceIpAddress> getIps(JsonNode node) {
        Set<InterfaceIpAddress> ips = Sets.newHashSet();

        JsonNode ipsNode = node.get(IPS);
        if (ipsNode != null) {
            ipsNode.forEach(jsonNode ->
                    ips.add(InterfaceIpAddress.valueOf(jsonNode.asText())));
        }

        return ips;
    }

    private ArrayNode putIps(Set<InterfaceIpAddress> intfIpAddresses) {
        ArrayNode ipArray = mapper.createArrayNode();

        intfIpAddresses.forEach(i -> ipArray.add(i.toString()));

        return ipArray;
    }

}
