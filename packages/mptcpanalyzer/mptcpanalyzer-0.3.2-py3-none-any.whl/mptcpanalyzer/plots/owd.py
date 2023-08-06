import mptcpanalyzer as mp
from mptcpanalyzer import _receiver, _sender, PreprocessingActions, Protocol
import mptcpanalyzer.plot as plot
import mptcpanalyzer.data as woo
from mptcpanalyzer.connection import MpTcpConnection, TcpConnection
import pandas as pd
import logging
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import inspect
import collections
from mptcpanalyzer.cache import CacheId
from mptcpanalyzer.parser import gen_bicap_parser, gen_pcap_parser, MpTcpAnalyzerParser
from cmd2 import argparse_completer
from typing import Iterable, List  # Any, Tuple, Dict, Callable
from itertools import cycle
from mptcpanalyzer.debug import debug_dataframe

# global log and specific log
log = logging.getLogger(__name__)


TCP_DEBUG_FIELDS = ['hash', 'ipsrc', 'ipdst', 'tcpstream', 'packetid', "reltime", "abstime", "tcpdest", "mptcpdest"]


class TcpOneWayDelay(plot.Matplotlib):
    """
    The purpose of this plot is to display the "one-way delay" (OWD) (also called
    one-way latency (OWL)) between the client
    and the server.
    To do this, you need to capture a communication at both ends, client and server.

    .. note:: both hosts should have their clock synchronized. If this can be hard
    with real hosts, perfect synchronization is available in network simulators
    such as ns3.

    """

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )
        self.x_label = "Time (s)"
        self.y_label = "One Way Delay (s)"

        # self.tshark_config.filter = "tcp";

    # TODO simplify
    def default_parser(self, *args, **kwargs):
        parser = MpTcpAnalyzerParser(
            description=inspect.cleandoc("""
                Plot One Way Delays"
            """)
        )

        subparsers = parser.add_subparsers(dest="protocol",
            title="Subparsers", help='sub-command help',)
        subparsers.required = True  # type: ignore

        orig_actions = {
            "tcp": PreprocessingActions.MergeTcp | PreprocessingActions.FilterDestination,
            "mptcp": PreprocessingActions.MergeMpTcp | PreprocessingActions.FilterDestination,
        }

        for protocol, actions in orig_actions.items():

            expected_pcaps = {
                "pcap": actions
            }

            temp = gen_pcap_parser(input_pcaps=expected_pcaps, parents=[super().default_parser()])
            subparser = subparsers.add_parser(protocol, parents=[temp, ],
                    add_help=False)

        parser.description = inspect.cleandoc('''
            Helps plotting One Way Delays between tcp connections
        ''')

        parser.epilog = inspect.cleandoc('''
            Example for TCP:
            > plot owd tcp examples/client_2_filtered.pcapng 0 examples/server_2_filtered.pcapng 0 --display

            And for MPTCP:
            > plot owd mptcp examples/client_2_filtered.pcapng 0 examples/client_2_filtered.pcapng 0 --display
        ''')
        return parser

        # here we recompute the OWDs

    def plot(self, pcap, protocol, **kwargs):
        """
        Ideally it should be mapped automatically
        For now plots only one direction but there could be a wrapper to plot forward owd, then backward OWDs
        Disclaimer: Keep in mind this assumes a perfect synchronization between nodes, i.e.,
        it relies on the pcap absolute time field.
        While this is true in discrete time simulators such as ns3

        """
        fig = plt.figure()
        axes = fig.gca()
        res = pcap
        destinations = kwargs.get("pcap_destinations")
        res[_sender("abstime")] = pd.to_datetime(res[_sender("abstime")], unit="s")


        # TODO here we should rewrite
        debug_fields = _sender(TCP_DEBUG_FIELDS) + _receiver(TCP_DEBUG_FIELDS) + ["owd"]

        # print("columns", pcap)
        debug_dataframe(res, "owd dataframe")
        # print(res.loc[res.merge_status == "both", debug_fields])

        df = res

        # print("DESTINATION=%r" % destinations)
        # df= df[df.owd > 0.010]

        fields = ["tcpdest", "tcpstream", ]
        # if True:
        # TODO: use Protocol.MPTCP:
        if protocol == "mptcp":
            self.plot_mptcp(df, fig, fields, **kwargs)
        elif protocol == "tcp":
            self.plot_tcp(df, fig, fields, **kwargs)
        else:
            raise Exception("Unsupported protocol %r" % protocol)


        self.title_fmt = "One Way Delays for {protocol}"
        if len(destinations) == 1:
            self.title_fmt = self.title_fmt + " towards {dest}"

        self.title_fmt = self.title_fmt.format(
            protocol=protocol,
            # kwargs.get("pcap1stream"),
            # kwargs.get("pcap2stream"),
            dest=destinations[0].to_string()
        )

        return fig


    def plot_tcp(self, df, fig, fields, **kwargs):
        axes = fig.gca()
        # fields = ["tcpdest", "tcpstream"]


        label_fmt = "Stream {tcpstream} towards {tcpdest}"
        for idx, subdf in df.groupby(_sender(fields), sort=False):

            # print("t= %r" % (idx,))
            print("len= %r" % len(subdf))
            tcpdest, tcpstream = idx

            # print("tcpdest= %r" % tcpdest)
            # print("=== less than 0\n", subdf[subdf.owd < 0.050])
            # print("=== less than 0\n", subdf.tail())

            # if tcpdest
            debug_dataframe(subdf, "subdf stream %d destination %r" % (tcpstream, tcpdest))

            pplot = subdf.plot.line(
                # gca = get current axes (Axes), create one if necessary
                ax=axes,
                legend=True,
                # TODO should depend from
                x=_sender("abstime"),
                y="owd",
                label=label_fmt.format(tcpstream=tcpstream, tcpdest=tcpdest),
            )

    def plot_mptcp(self, df, fig, fields, pcap_destinations, **kwargs):
        axes = fig.gca()
        fields = ["tcpdest", "tcpstream", "mptcpdest"]
        destinations = pcap_destinations


        label_fmt = "Stream {tcpstream}"

        if len(destinations) > 1:
            label_fmt = label_fmt + " towards {dest}"

        print("pcap", pcap_destinations)

        for idx, subdf in df.groupby(_sender(fields), sort=False):

            tcpdest, tcpstream, mptcpdest = idx
            if mptcpdest not in destinations:
                log.debug("Ignoring destination %s", mptcpdest)
                continue

            # print("OWD")
            # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            #     # more options can be specified also
            #     # print(df)
            #     print(df.owd)

# "Subflow %d towards tcp %s" % (tcpstream, tcpdest),  # seems to be a bug
            pplot = subdf.plot(
                # gca = get current axes (Axes), create one if necessary
                ax=axes,
                legend=True,
                # TODO should depend from
                x=_sender("abstime"),
                y="owd",
                label=label_fmt.format(tcpstream=tcpstream, dest=mp.ConnectionRoles(mptcpdest).to_string())
            )
