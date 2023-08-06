"""
Tests that require online ports.

Most tests use loopback port as this is the simplest configuration.
Some tests require two back-to-back ports, like stream statistics tests.

@author yoram@ignissoft.com
"""

from os import path
import json
import binascii
import time

from pypacker.layer12 import ethernet

from xenavalkyrie.xena_statistics_view import XenaPortsStats, XenaStreamsStats, XenaTpldsStats
from xenavalkyrie.tests.test_base import TestXenaBase
from xenavalkyrie.xena_port import XenaCaptureBufferType
from xenavalkyrie.xena_tshark import Tshark, TsharkAnalyzer


class TestXenaOnline(TestXenaBase):

    def test_online(self):
        self.ports = self.xm.session.reserve_ports([self.port1, self.port2], True)
        self.ports[self.port1].wait_for_up(16)
        self.ports[self.port2].wait_for_up(16)

    def test_traffic(self):
        port = self.xm.session.reserve_ports([self.port1])[self.port1]
        port.load_config(path.join(path.dirname(__file__), 'configs', 'test_config_loopback.xpc'))

        self.xm.session.clear_stats()
        port_stats = port.read_port_stats()
        print(json.dumps(port_stats, indent=1))
        self.xm.session.start_traffic()
        time.sleep(2)
        port_stats = port.read_port_stats()
        print(json.dumps(port_stats, indent=1))
        assert(abs(port_stats['pt_total']['packets'] - port_stats['pr_total']['packets']) < 1111)
        assert(abs(1000 - port.streams[0].read_stats()['pps']) < 111)
        assert(abs(1000 - port.tplds[0].read_stats()['pr_tpldtraffic']['pps']) < 111)
        self.xm.session.stop_traffic()
        self.xm.session.clear_stats()
        self.xm.session.start_traffic(blocking=True)

        ports_stats = XenaPortsStats(self.xm.session)
        ports_stats.read_stats()
        print(ports_stats.statistics.dumps())
        print(json.dumps(ports_stats.get_flat_stats(), indent=1))

        streams_stats = XenaStreamsStats(self.xm.session)
        streams_stats.read_stats()
        print(streams_stats.statistics.dumps())
        print(json.dumps(streams_stats.get_flat_stats(), indent=1))

        tplds_stats = XenaTpldsStats(self.xm.session)
        tplds_stats.read_stats()
        print(tplds_stats.statistics.dumps())
        print(json.dumps(tplds_stats.get_flat_stats(), indent=1))

    def test_stream_stats(self):
        """ For this test we need back-to-back ports. """
        ports = self.xm.session.reserve_ports([self.port1, self.port2])
        ports[self.port1].load_config(path.join(path.dirname(__file__), 'configs', 'test_config_1.xpc'))
        ports[self.port2].load_config(path.join(path.dirname(__file__), 'configs', 'test_config_2.xpc'))

        self.xm.session.start_traffic(blocking=True)

        tpld_stats = XenaTpldsStats(self.xm.session)
        print(tpld_stats.read_stats().dumps())

        streams_stats = XenaStreamsStats(self.xm.session)
        streams_stats.read_stats()
        print(streams_stats.tx_statistics.dumps())
        print(streams_stats.statistics.dumps())
        # Access TX counter using stream name or stream object, from tx_statistics or statistics.
        assert(streams_stats.tx_statistics['Stream 1-1']['packets'] == 8000)
        assert(streams_stats.tx_statistics[ports[self.port1].streams[0]]['packets'] == 8000)
        assert(streams_stats.statistics[ports[self.port1].streams[0]]['tx']['packets'] == 8000)
        assert(streams_stats.statistics['Stream 1-1']['tx']['packets'] == 8000)
        assert(streams_stats.statistics['/'.join(self.port1.split('/')[1:]) + '/0']['tx']['packets'] == 8000)
        # Access RX counter with port name on RX side or directly.
        assert(streams_stats.statistics['Stream 1-1']['rx']['pr_tpldtraffic']['pac'] == 8000)
        assert(streams_stats.statistics['Stream 1-1']['rx'][ports[self.port1]]['pr_tpldtraffic']['pac'] == 8000)
        assert(streams_stats.statistics['Stream 1-1']['rx'][self.port1]['pr_tpldtraffic']['pac'] == 8000)

    def test_capture(self):
        port = self.xm.session.reserve_ports([self.port1])[self.port1]
        port.load_config(path.join(path.dirname(__file__), 'configs', 'test_config_loopback.xpc'))

        port.streams[0].set_attributes(ps_ratepps=10, ps_packetlimit=80)
        port.remove_stream(1)

        port.start_capture()
        port.start_traffic(blocking=True)
        port.stop_capture()

        packets = port.capture.get_packets(0, 1, cap_type=XenaCaptureBufferType.raw)
        assert(len(packets) == 1)
        port.capture.packets[0].get_attributes()
        packet = ethernet.Ethernet(binascii.unhexlify(packets[0]))
        assert(packet.ip.dst_s == '1.1.0.0')

        packets = port.capture.get_packets(10, 20, cap_type=XenaCaptureBufferType.raw)
        print(packets[0])
        assert(len(packets) == 10)

        packets = port.capture.get_packets(file_name=path.join(self.temp_dir, 'xena_cap.txt'))
        print(packets[0])
        assert(len(packets) == 80)

        tshark = Tshark(self.config.get('General', 'wireshark_dir'))
        packets = port.capture.get_packets(cap_type=XenaCaptureBufferType.pcap,
                                           file_name=path.join(self.temp_dir, 'xena_cap.pcap'), tshark=tshark)
        analyser = TsharkAnalyzer()
        analyser.add_field('ip.src')
        analyser.add_field('ip.dst')
        fields = tshark.analyze(path.join(self.temp_dir, 'xena_cap.pcap'), analyser)
        print(fields)
        assert(len(fields) == 80)
