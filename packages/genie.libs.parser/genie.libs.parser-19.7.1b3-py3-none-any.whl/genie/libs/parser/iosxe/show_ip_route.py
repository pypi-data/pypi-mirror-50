""" show_ip_route.py

IOSXE parsers for the following show commands:
    * 'show ip route bgp'
    * 'show ip route vrf <WORD> bgp'
    * 'show ipv6 route bgp'
    * 'show ipv6 route vrf <WORD> bgp'
"""
import re   
from genie.metaparser import MetaParser   
from genie.metaparser.util.schemaengine import Any, Optional 


class ShowIpRouteSchema(MetaParser):
    """Schema for:
         show ip route bgp
         show ip route vrf <WORD> bgp
         show ipv6 route bgp
         show ipv6 route vrf <WORD> bgp"""

    schema = {
        'vrf':
            {Any():
                {Optional('address_family'):
                    {Any():
                        {'ip':
                            {Any():
                                {Optional('nexthop'):
                                    {Optional(Any()):
                                        {Optional('protocol'):
                                            {Optional(Any()):
                                                {Optional('route_table'): str,
                                                Optional('candidate_default'): bool,
                                                Optional('uptime'): str,
                                                Optional('preference'): str,
                                                Optional('metric'): str,
                                                Optional('attribute'): str,
                                                }
                                            },
                                        }
                                    },
                                }
                            },
                        }
                    },
                }
            },
        }


class ShowIpRoute(ShowIpRouteSchema):
    """Parser for:
        show ip route bgp
        show ip route vrf <vrf> bgp
        show ipv6 route bgp
        show ipv6 route vrf <vrf> bgp"""
    cli_command = ['show {ip} route vrf {vrf} {protocol}','show {ip} route {protocol}','show ip route vrf {vrf} {protocol}',\
                   'show route {protocol}']
    def cli(self, protocol, vrf='', ip='ip',output=None):
        if output is None:
            # Calling the corresponding show command
            if ip:
                if vrf:
                    cmd = self.cli_command[0].format(ip=ip,vrf=vrf, protocol= protocol)
                else:
                    vrf = 'default'
                    cmd = self.cli_command[1].format(ip=ip,protocol= protocol)
            else:
                if vrf:
                    cmd = self.cli_command[2].format(vrf=vrf,protocol= protocol)
                else:
                    vrf = 'default'
                    cmd = self.cli_command[3].format(protocol= protocol)

            out = self.device.execute(cmd)
        else:
            out = output

        # Init dict
        bgp_dict = {}
        sub_dict = {}
        address_family = None
        preference = None
        metric = None
        mask = ''
        candidate_dafault = False

        source_protocol_dict = {}
        source_protocol_dict['ospf'] = ['O', 'IA', 'N1', 'N2', 'E1', 'E2']
        source_protocol_dict['odr'] = ['o']
        source_protocol_dict['isis'] = ['i', 'su', 'L1', 'L2', 'ia']
        source_protocol_dict['eigrp'] = ['D', 'EX']
        source_protocol_dict['static'] = ['S']
        source_protocol_dict['mobile'] = ['M']
        source_protocol_dict['rip'] = ['R']
        source_protocol_dict['lisp'] = ['I']
        source_protocol_dict['nhrp'] = ['H']
        source_protocol_dict['local'] = ['L']
        source_protocol_dict['connected'] = ['C']
        source_protocol_dict['bgp'] = ['B']

        # Setting the address_family
        if vrf == 'default' and ip =='ip':
            address_family = 'ipv4 unicast'
        elif vrf != 'default' and ip =='ip':
            address_family = 'vpnv4 unicast'
        elif vrf == 'default' and ip =='ipv6':
            address_family = 'ipv6 unicast'
        elif vrf != 'default' and ip =='ipv6':
            address_family = 'vpnv6 unicast'

        for line in out.splitlines():
            line = line.strip()

            # 10.225.0.0/24 is subnetted, 5 subnets
            p1 = re.compile(r'^\s*(?P<address>[0-9\.]+)(?P<mask>[0-9\/]+)'
                             ' +is +subnetted,'
                             ' +(?P<subnets>[0-9]+) +subnets$')
            m = p1.match(line)
            if m:
                address = str(m.groupdict()['address'])
                mask = str(m.groupdict()['mask'])
                subnets = int(m.groupdict()['subnets'])

                continue

            # B   646:11:11:1::/64 [20/2219]
            # B   646:22:22::/64 [20/2219]
            # B   615:11:11::/64 [200/2219]
            # B   2001:2:2:2::2/128 [200/0]
            # B        10.1.1.0 [200/2219] via 10.4.1.1, 01:40:40
            # B        10.9.2.0 [20/2219] via 10.66.6.6 (VRF2), 01:36:26
            # S*    0.0.0.0/0 [20/0] via 10.1.1.1, 4d22h
            p2 = re.compile(r'^\s*(?P<protocol>[a-zA-Z0-9\+\%]+)(?P<candidate_dafault>\*)?'
                             ' +(?P<ip_add>[0-9\.\:\/]+)'
                             ' +(\[(?P<preference>[0-9]+)/(?P<metric>[0-9]+)\])'
                             '( +via +(?P<next_hop>[0-9\.]+)(\s)?(\()?'
                             '(?P<table>[a-zA-Z0-9]+)?(\)?),'
                             ' +(?P<up_time>[\w\:]+))?$')
            m = p2.match(line)
            if m:
                protocol_abr = str(m.groupdict()['protocol'])
                for key, val in source_protocol_dict.items():
                    if protocol_abr in val:
                        protocol = key

                ip_add = str(m.groupdict()['ip_add'])
                if mask:
                    ip_add = ip_add+mask
                preference = m.groupdict()['preference']
                metric = m.groupdict()['metric']
                if m.groupdict()['candidate_dafault']:
                    candidate_dafault = True

                # Init vrf dict
                if 'vrf' not in bgp_dict:
                    bgp_dict['vrf'] = {}
                if vrf and vrf not in bgp_dict['vrf']:
                    bgp_dict['vrf'][vrf] = {}

                # Init address_family dict
                if 'address_family' not in bgp_dict['vrf'][vrf]:
                    bgp_dict['vrf'][vrf]['address_family'] = {}
                if address_family is not None and \
                   address_family not in bgp_dict['vrf'][vrf]['address_family']:
                   bgp_dict['vrf'][vrf]['address_family'][address_family] = {}

                # Create sub_dict
                sub_dict = bgp_dict['vrf'][vrf]['address_family'][address_family]

                # Init address_family dict
                if 'ip' not in sub_dict:
                    sub_dict['ip'] = {}
                if ip_add not in sub_dict['ip']:
                    sub_dict['ip'][ip_add] = {}
                if m.groupdict()['next_hop']:
                    next_hop = str(m.groupdict()['next_hop'])
                    if 'nexthop' not in sub_dict['ip'][ip_add]:
                        sub_dict['ip'][ip_add]['nexthop'] = {}
                    if next_hop not in sub_dict['ip'][ip_add]['nexthop']:
                        sub_dict['ip'][ip_add]['nexthop'][next_hop] = {}
                    if 'protocol' not in sub_dict['ip'][ip_add]['nexthop'][next_hop]:
                        sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol'] = {}
                    if protocol not in sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol']:
                        sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol'][protocol] = {}

                    # Create sub_dict
                    prot_dict = sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol']
                    if m.groupdict()['table']:
                        table = m.groupdict()['table']
                        prot_dict[protocol]['route_table'] = table

                    prot_dict[protocol]['preference'] = preference
                    if candidate_dafault == True:
                        prot_dict[protocol]['candidate_dafault'] = True
                    metric = m.groupdict()['metric']
                    prot_dict[protocol]['metric'] = metric

                    if m.groupdict()['up_time']:
                        up_time = m.groupdict()['up_time']
                        prot_dict[protocol]['uptime'] = up_time

                continue

            #      via 2001:DB8:1:1::2
            #      via 10.4.1.1%default, indirectly connected
            #      via 2001:DB8:4:6::6
            #      via 2001:DB8:20:4:6::6%VRF2
            p3 = re.compile(r'^\s*via +(?P<next_hop>[a-zA-Z0-9\.\/\:]+)'
                             '(\%(?P<table>[a-zA-Z0-9]+))?'
                             '(,)?(\s+)?(?P<attribute>[a-zA-Z\s]+)?$')
            m = p3.match(line)
            if m:
                next_hop = str(m.groupdict()['next_hop'])
                if 'nexthop' not in sub_dict['ip'][ip_add]:
                    sub_dict['ip'][ip_add]['nexthop'] = {}
                if next_hop not in sub_dict['ip'][ip_add]['nexthop']:
                    sub_dict['ip'][ip_add]['nexthop'][next_hop] = {}
                if 'protocol' not in sub_dict['ip'][ip_add]['nexthop'][next_hop]:
                    sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol'] = {}
                if protocol not in sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol']:
                    sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol'][protocol] = {}

                # Create sub_dict
                prot_dict = sub_dict['ip'][ip_add]['nexthop'][next_hop]['protocol']

                if m.groupdict()['table']:
                    table = m.groupdict()['table']
                    prot_dict[protocol]['route_table'] = table

                if m.groupdict()['attribute']:
                    attribute = m.groupdict()['attribute']
                    prot_dict[protocol]['attribute'] = attribute

                if preference:
                    prot_dict[protocol]['preference'] = preference

                if metric:
                    prot_dict[protocol]['metric'] = metric

        return bgp_dict


class ShowIpv6Route(ShowIpRoute):
    """Parser for:
        show ipv6 route bgp
        show ipv6 route vrf <vrf> bgp"""

    def cli(self, protocol, ip='ipv6', vrf = '',output=None):
        return(super().cli(protocol=protocol, ip='ipv6', vrf=vrf,output=output))
