# Copyright (c) 2018 Red Hat, Inc. and others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html

import json
import logging

from odltools.mdsal.models.neutron import Neutron
from odltools.mdsal.models.opendaylight_inventory import Nodes
from odltools.netvirt import cluster
from odltools.netvirt import config
from odltools.netvirt import flows
from odltools.netvirt import tables
from odltools.netvirt import utils

logger = logging.getLogger("netvirt.show")


def show_elan_instances(args):
    config.get_models(args, {"elan_elan_instances"})
    instances = config.gmodels.elan_elan_instances.get_clist_by_key()
    for k, v in instances.items():
        print("ElanInstance: {}, {}".format(k, utils.format_json(args, v)))


def get_duplicate_ids(args):
    config.get_models(args, {"id_manager_id_pools"})
    duplicate_ids = {}
    pools = config.gmodels.id_manager_id_pools.get_clist_by_key()
    for k, pool in pools.items():
        id_values = {}
        for id_entry in pool.get('id-entries', []):
            id_info = {}
            id_value = id_entry.get('id-value')[0]
            id_key = id_entry.get('id-key')
            if id_values and id_values.get(id_value, None):
                key_list = id_values.get(id_value)
                key_list.append(id_key)
                id_info['id-value'] = id_value
                id_info['id-keys'] = key_list
                id_info['pool-name'] = pool.get('pool-name')
                id_info['parent-pool-name'] = pool.get('parent-pool-name')
                duplicate_ids[id_value] = id_info
            else:
                id_values[id_value] = [id_key]
    return duplicate_ids


def show_all_idpools(args):
    config.get_models(args, {"id_manager_id_pools"})
    pools = config.gmodels.id_manager_id_pools.get_clist_by_key()
    print("\nid-pools\n")
    if not args.short:
        print(utils.format_json(args, pools))
    else:
        print("pool-name                          ")
        print("-----------------------------------")
        for k, v in sorted(pools.items()):
            print("{:30}".format(v.get("pool-name")))


def show_dup_idpools(args):
    config.get_models(args, {"neutron_neutron"})
    ports = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.PORTS)
    iface_ids = []
    for k, v in get_duplicate_ids(args).iteritems():
        result = "Id:{},Keys:{}".format(k, json.dumps(v.get('id-keys')))
        if v.get('pool-name'):
            result = "{},Pool:{}".format(result, v.get('pool-name'))
            if v.get('pool-name') == 'interfaces':
                iface_ids.extend(v.get('id-keys'))
        if v.get('parent-pool-name'):
            result = "{},ParentPool:{}".format(result, v.get('parent-pool-name'))
        print(result)
    print("\nNeutron Ports")
    print("=============")
    for id in iface_ids:
        port = ports.get(id, {})
        print("Iface={}, NeutronPort={}".format(id, utils.format_json(args, port)))


def show_idpools(args):
    print("args: {}".format(args))
    if args.type == "all":
        show_all_idpools(args)
    elif args.type == "duplicate":
        show_dup_idpools(args)


def show_groups(args):
    config.get_models(args, {"odl_inventory_nodes"})
    of_nodes = config.gmodels.odl_inventory_nodes.get_clist_by_key()
    groups = config.gmodels.odl_inventory_nodes.get_groups(of_nodes)
    for dpn in groups:
        for group_key in groups[dpn]:
            print("Dpn: {}, ID: {}, Group: {}".format(dpn, group_key, utils.format_json(args, groups[dpn][group_key])))


def get_data_path(res_type, data):
    if res_type == 'bindings':
        return 'interface-service-bindings:service-bindings/services-info/{}/{}'.format(
            data['interface-name'], data['service-mode'])
    elif res_type == 'flows':
        return 'opendaylight-inventory:nodes/node/openflow:{}/flow-node-inventory:table/{}/flow/{}'.format(
            data.pdata['dpnid'], data.rdata['table_id'], data.rdata['id'])


def show_stale_bindings(args):
    config.get_models(args, {"ietf_interfaces_interfaces", "interface_service_bindings_service_bindings"})
    stale_ids, bindings = flows.get_stale_bindings(args)
    for iface_id in sorted(stale_ids):
        for binding in bindings[iface_id].values():
            # if binding.get('bound-services'):
            path = get_data_path('bindings', binding)
            print(utils.format_json(args, bindings[iface_id]))
            print('http://{}:{}/restconf/config/{}'.format(args.ip, args.port, path))


def show_tables(args):
    config.get_models(args, {"odl_inventory_nodes"})
    of_nodes = config.gmodels.odl_inventory_nodes.get_clist_by_key()

    tableset = set()
    for node in of_nodes.values():
        for table in node[Nodes.NODE_TABLE]:
            if table.get('flow'):
                tableset.add(table['id'])

    for table in (sorted(tableset)):
        result = '{:3}:{} '.format(table, tables.get_table_name(table))
        print(result)


def show_flows(args):
    if args.flowtype == "all":
        flows.show_all_flows(args)
    if args.flowtype == "duplicate":
        flows.show_dup_flows(args)
    if args.flowtype == "learned":
        flows.show_learned_mac_flows(args)
    if args.flowtype == "stale":
        flows.show_stale_flows(args)
    if args.flowtype == "elan":
        flows.show_elan_flows(args)


def print_neutron_networks(args, obj, data):
    print("uuid                                 type  name")
    print("------------------------------------ ----- --------------------")
    for k, v in data.items():
        ntype = v.get("neutron-provider-ext:network-type").rpartition("-")[2]
        print("{} {:5} {}".format(k, ntype, v.get("name")))


def print_neutron_ports(args, obj, data):
    print("uuid                                 network-id                           mac               "
          "ip              name")
    print("------------------------------------ ------------------------------------ ----------------- "
          "--------------- --------------------")
    for k, v in data.items():
        network_id = v.get("network-id")
        mac = v.get("mac-address")
        fixed_ip = v.get("fixed-ips")
        ip = None
        if fixed_ip is not None:
            ip = fixed_ip[0].get("ip-address")
        name = v.get("name")
        print("{} {} {} {:15} {}".format(k, network_id, mac, ip, name))


def print_neutron(args, obj, data):
    if args.short:
        if obj == Neutron.NETWORKS:
            print_neutron_networks(args, obj, data)
        elif obj == Neutron.PORTS:
            print_neutron_ports(args, obj, data)
        else:
            print(utils.format_json(args, data))
    else:
        print(utils.format_json(args, data))


def print_neutron_resource_count(args, objs):
    print("\n=====================")
    print("Total Resource Count")
    print("=====================\n")

    resources = {
        Neutron.SECURITY_GROUPS: "Security Groups: {}",
        Neutron.SECURITY_RULES: "Security Rules: {}",
        Neutron.NETWORKS: "Networks: {}",
        Neutron.SUBNETS: "Subnets: {}",
        Neutron.PORTS: "Ports: {}",
        Neutron.ROUTERS: "Routers: {}",
        Neutron.FLOATINGIPS: "Floatingips: {}",
        Neutron.TRUNKS: "Trunks: {}",
        Neutron.BGPVPNS: "Bgpvpns: {}"
    }

    for obj in objs:
        data = config.gmodels.neutron_neutron.get_objects_by_key(obj=obj)
        print(resources.get(obj, "Count: 0").format(len(data)))


def print_unused_neutron_resource(args):
    try:
        check_unused_resources_type = [Neutron.SECURITY_GROUPS]

        all_security_groups = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.SECURITY_GROUPS)
        all_ports = config.gmodels.neutron_neutron.get_objects_by_key(obj=Neutron.PORTS)

        for re_type in check_unused_resources_type:
            if (re_type == Neutron.SECURITY_GROUPS):
                sec_group_ids_in_ports = []
                if all_ports:
                    for port_key, port_value in all_ports.items():
                        if 'security-groups' in port_value:
                            security_groups_in_port = port_value['security-groups']
                            if security_groups_in_port:
                                for group in security_groups_in_port:
                                    sec_group_ids_in_ports.append(group)

                unused_sec_group_ids = (list(set(all_security_groups.keys()) -
                                             set(sec_group_ids_in_ports)))
                if unused_sec_group_ids:
                    print("\n========================")
                    print("Unused Security Groups")
                    print("========================\n")
                    print("{:40} {:40} {:40}".format('ID', 'NAME', 'TENANT'))
                for unused_sec_group_id in unused_sec_group_ids:
                    print("{:40} {:40} {:40}".format(unused_sec_group_id,
                                                     all_security_groups[unused_sec_group_id].get('name'),
                                                     all_security_groups[unused_sec_group_id].get('tenant-id')))
    except Exception as ex:
        print('Failed in detecting Unused resources.')


def show_neutron(args):
    objs = []
    config.get_models(args, {"neutron_neutron"})
    if args.object == "all":
        objs = Neutron.ALL_OBJECTS
    elif args.object == "unused-security-groups":
        print_unused_neutron_resource(args)
    else:
        objs.append(args.object)

    for obj in objs:
        print("\nneutron {}:\n".format(obj))
        data = config.gmodels.neutron_neutron.get_objects_by_key(obj=obj)
        print_neutron(args, obj, data)
    if objs:
        print_neutron_resource_count(args, objs)


def show_eos(args):
    cluster.show_eos(args)


def show_cluster_information(args):
    cluster.show_cluster_information(args)
