import logging
import argparse
import cmd2
import os.path
import functools
from cmd2.argparse_custom import ChoicesCallable, ATTR_CHOICES_CALLABLE
from typing import Iterable, List, Dict, Callable, Optional, Any, Union
from mptcpanalyzer.tshark import TsharkConfig
from mptcpanalyzer.data import (load_into_pandas, load_merged_streams_into_pandas)
from mptcpanalyzer import (PreprocessingActions, ConnectionRoles, DestinationChoice,
            CustomConnectionRolesChoices, TcpStreamId, MpTcpStreamId, Protocol)
import mptcpanalyzer as mp
from functools import partial
from mptcpanalyzer.connection import MpTcpConnection, TcpConnection
from mptcpanalyzer.debug import debug_dataframe

log = logging.getLogger(__name__)


"""

TODO
- action to generate connection


"""

# TODO add it to a custom MptcpAnalyzerAction
# TODO insert it instead into dict
def _add_dataframe(namespace, dest, df):

    # if not hasattr(namespace, "_dataframes"):
    #     setattr(namespace, "_dataframes", {})
    # namespace._dataframes.update({
    #     dest: df
    # })

    if not hasattr(namespace, "_dataframes"):
        setattr(namespace, "_dataframes", {})

    namespace._dataframes.update({dest: df})


class DataframeAction(argparse.Action):
    '''
    If you need the action to act on a specific dataframe
    '''

    def __init__(self, df_name: str, **kwargs) -> None:
        argparse.Action.__init__(self, **kwargs)

        self.df_name = df_name
        # self.dest = df_name + self.dest

    def add_dataframe(self, namespace, df):
        _add_dataframe(namespace, self.df_name, df)



class LoadSinglePcap(DataframeAction):
    '''
    Test action !!
    '''
    def __init__(self, loader=TsharkConfig(), **kwargs) -> None:
        super().__init__(df_name=kwargs.get("dest"), **kwargs)
        self.loader = loader

        # 'completer_method': cmd2.Cmd.path_complete
        # setattr(self, cmd2.argparse_completer.ACTION_ARG_CHOICES, ('path_complete', os.path.isfile))
        completer_method = functools.partial(cmd2.Cmd.path_complete, path_filter=lambda path: os.path.isfile(path))
        setattr(self, ATTR_CHOICES_CALLABLE,
                ChoicesCallable(is_method=True, is_completer=True, to_call=completer_method))
    def __call__(self, parser, namespace, values, option_string=None):
        if type(values) == list:
            parser.error("lists unsupported")
        else:
            df = load_into_pandas(values, self.loader)

            setattr(namespace, self.dest, values)

        self.add_dataframe(namespace, df)

#     return arg_decorator
# def with_argparser(argparser: argparse.ArgumentParser,
#                    preserve_quotes: bool=False) -> Callable[[argparse.Namespace], Optional[bool]]:
#     """A decorator to alter a cmd2 method to populate its ``args`` argument by parsing arguments
#     with the given instance of argparse.ArgumentParser.

#     :param argparser: unique instance of ArgumentParser
#     :param preserve_quotes: if True, then arguments passed to argparse maintain their quotes
#     :return: function that gets passed the argparse-parsed args
#     """
#     import functools

#     # noinspection PyProtectedMember
#     def arg_decorator(func: Callable[[Statement], Optional[bool]]):
#         @functools.wraps(func)
#         def cmd_wrapper(instance, cmdline):
#             lexed_arglist = parse_quoted_string(cmdline, preserve_quotes)
#             try:
#                 args = argparser.parse_args(lexed_arglist)
#             except SystemExit:
#                 return
#             else:
#                 return func(instance, args)

#         # argparser defaults the program name to sys.argv[0]
#         # we want it to be the name of our command
#         argparser.prog = func.__name__[len(COMMAND_FUNC_PREFIX):]

#         # If the description has not been set, then use the method docstring if one exists
#         if argparser.description is None and func.__doc__:
#             argparser.description = func.__doc__

#         # Set the command's help text as argparser.description (which can be None)
#         cmd_wrapper.__doc__ = argparser.description

#         # Mark this function as having an argparse ArgumentParser
#         setattr(cmd_wrapper, 'argparser', argparser)

#         return cmd_wrapper

#     return arg_decorator

# with_argparser_and_unknown_args
# def with_argparser_test(

# see cmd2/cmd2.py for the original with_argparser_and_unknown_args
# goal here is to be able to pass a custom namespace
# see https://github.com/python-cmd2/cmd2/issues/596
def with_argparser_test(
    argparser: argparse.ArgumentParser,
    preserve_quotes: bool = False,
    preload_pcap: bool = False,
) -> Callable[[argparse.Namespace, List], Optional[bool]]:
    """
    Arguments:
        preload_pcap: Use the preloaded pcap as a dataframe
    """
    import functools

    # noinspection PyProtectedMember
    def arg_decorator(func: Callable):
        @functools.wraps(func)
        def cmd_wrapper(cmd2_instance, statement: Union[cmd2.Statement, str]):
            statement, parsed_arglist = cmd2_instance.statement_parser.get_command_arg_list(command_name,
                                                                                            statement,
                                                                                            preserve_quotes)
            try:
                myNs = argparse.Namespace()
                if preload_pcap:
                    myNs._dataframes = {"pcap": cmd2_instance.data.copy()}

                args, unknown = argparser.parse_known_args(parsed_arglist, myNs)

                # print("namespace: %r" % args)
            except SystemExit:
                return
            else:
                # original cmd2 has the same warning
                return func(cmd2_instance, args, unknown)  # type:ignore

        # cmd2.COMMAND_FUNC_PREFIX
        command_name = func.__name__[len("do_"):]
        argparser.prog = command_name

        # If the description has not been set, then use the method docstring if one exists
        if argparser.description is None and func.__doc__:
            argparser.description = func.__doc__

        # Set the command's help text as argparser.description (which can be None)
        cmd_wrapper.__doc__ = argparser.description

        # Mark this function as having an argparse ArgumentParser
        setattr(cmd_wrapper, 'argparser', argparser)

        return cmd_wrapper

    return arg_decorator  # type: ignore


class AppendDestination(argparse.Action):
    """
    assume convention on naming
    TODO check if it's ok with FilterDest
    """
    def __init__(self, *args, **kwargs) -> None:
        self.already_called = False
        self.destinations = list(ConnectionRoles)
        # TODO pass the type as well
        # print(args)
        # print(kwargs)
        kwargs.update({
            "choices": CustomConnectionRolesChoices([e.name for e in ConnectionRoles]),
            "type": lambda x: ConnectionRoles.from_string(x),
            "default": list(ConnectionRoles),
        })
        super().__init__(*args, **kwargs)
        # print("destinations", self.dest)


    # TODO check if it's called several times
    def __call__(self, parser, namespace, values, option_string=None):

        # print("APPEND DEST")
        if self.already_called is True:
            # TODO change the default ?
            # setattr(namespace, self.dest, [])
            # print("Already set")
            # print("setting value %r" % values)
            # print("setting value %r" % self.destinations)
            # to make it unique
            self.destinations.append(values)
            self.destinations = list(set(self.destinations))
            # print("new result %r" % self.destinations)
        else:
            # print("Received first value %r" % values)
            self.destinations = [values]
        # else:
        #     self.destinations = list(ConnectionRoles)

        self.already_called = True
        # df_name + "destinations"
        # print("setting into %s" % self.dest)
        setattr(namespace, self.dest, self.destinations)
        # pcap1 = getattr(namespace, self.df_name + "1")
        # pcap2 = getattr(namespace, self.df_name + "2")
        # dest = values
        # if type(values) == list:
        #     print("destination", option_string)
        #     print("first time called ?", self.already_called)
        #     if values == []:
        #         values = list(mp.ConnectionRoles)
        #         print("empty values, setting these myself")

        #     # TODO do sthg like append
        #     setattr(namespace, self.dest, values)
        # else:
        # print("destination", values)


        # df = namespace._dataframes[self.df_name]
        # df = df[df.tcpdest == dest]



class MergePcaps(DataframeAction):
    """
    assume convention on naming
    """
    def __init__(
        self,
        name: str,
        protocol: Protocol,
        loader=TsharkConfig(),
        **kwargs
    ) -> None:
        """
        """
        self.loader = loader
        self.protocol = protocol
        DataframeAction.__init__(self, df_name=name, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        if type(values) == list:
            parser.error("list unsupported")


        log.debug("Merging pcaps")
        pcap1 = getattr(namespace, self.df_name + "1")
        pcap2 = getattr(namespace, self.df_name + "2")

        pcap1stream = getattr(namespace, self.df_name + "1stream")
        # pcap2stream = getattr(namespace, self.name2 + "stream")
        pcap2stream = values

        assert pcap1
        assert pcap2
        assert pcap1stream is not None
        # assert pcap2stream is not None

        df = load_merged_streams_into_pandas(
            pcap1,
            pcap2,
            pcap1stream,
            pcap2stream,
            self.protocol == Protocol.MPTCP,
            self.loader,
        )

        setattr(namespace, self.dest, values)
        setattr(namespace, self.df_name + "stream", pcap1stream)
        # TODO add to merged_dataframes ?
        # setattr(namespace, self.dest + "_merged_df", df)

        self.add_dataframe(namespace, df)


# class ClockOffset(argparse.Action):
#     def __init__(self, df, **kwargs) -> None:
#         argparse.Action.__init__(self, **kwargs)
#
#     def __call__(self, parser, namespace, values, option_string=None):
#         if type(values) == list:
#             # setattr(namespace, self.dest, map(self.validate_ip, values))
#         else:
#             # setattr(namespace, self.dest, self.validate_ip(values))
#             print()



# don't need the Mptcp flag anymore
def exclude_stream(df_name):
    query = "{field}!={streamid}"
    return partial(FilterStream, query, df_name)

# TODO va dependre du type en fait
def retain_stream(df_name):
    query = "{field}=={streamid}"
    return partial(FilterStream, query, df_name)


def filter_dest(df_name, mptcp: bool = False):
    # query = "tcpdest"
    # if mptcp:
    #     query = "mp" + query
    # query = query + "==%s"
    return partial(FilterDest, df_name)


class FilterDest(DataframeAction):
    '''
    For now accept a single value
    '''
    def __init__(self, df_name: str, **kwargs) -> None:
        # self.df_name = df_name

        # assert self.field == "tcpdest" or self.field == "mptcpdest"
        # self.mptcp = mptcp
        # self.seen
        # init with all destinations
        self.destinations = list(ConnectionRoles)
        self.already_called = False
        # TODO need to pass a type
        # TODO it could set choices automatically
        # type=lambda x: ConnectionRoles.from_string(x),
        super().__init__(df_name, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        # TODO move to function
        # if self.df_name not in namespace._dataframes:
        #     parser.error("Trying to filter stream in non-registered df %s" % self.df_name)
        #     # TODO set dest

        # make sure result
        # df = namespace._dataframes[self.df_name]

        log.debug("TODO Filtering dest %s", (values))
        # con = df.mptcp.connection(pcapstream)

        # TODO build a query
        # query = ""
        # make sure that it's called only after stream got selected ?
        # assert df[self.field].unique().size == 1
        # "tcpstream"
        # dest = values
        # assert dest in ConnectionRoles

        # TODO remove first the ones who already have the tcpdest set
        # (to prevent from doing it twice)
        # for streamid in df.groupby(field):

        #     if mptcp:
        #         # parser.error("mptcp filtering Unsupported")

        #         mptcpcon = MpTcpConnection.build_from_dataframe(dataframe, stream)
        #         # mptcpdest = main_connection.mptcp_dest_from_tcpdest(tcpdest)
        #         df = Xptcpdest_from_connections(df, mptcpcon)
        #         df = df[df.mptcpdest == dest]

        #     else:
        #         tcpcon = TcpConnection.build_from_dataframe(df, streamid)
        #         df = Xcpdest_from_connections(df, tcpcon)
        #         df = df[df.tcpdest == dest]

        # log.debug("Applying query %s" % self.query)

        # query = query_tpl %
        # df.query(query, inplace=True)

        # con = TcpConnection.build_from_dataframe(df, args.tcpstream)
        # if args.destination:
        #     self.poutput("Filtering destination")
        #     q = con.generate_direction_query(args.destination)
        #     df = df.query(q)


class FilterStream(DataframeAction):
    '''
    To keep a specific stream id
    '''
    def __init__(self, query: str, df_name: str, **kwargs) -> None:
        self.query_tpl = query
        super().__init__(df_name, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        # make sure result
        df = namespace._dataframes[self.df_name]

        log.debug("Filtering stream %s" % (values))

        field = "tcpstream"
        if isinstance(values, MpTcpStreamId):
            field = "mptcpstream"
            log.debug("Mptcp instance")
        elif isinstance(values, TcpStreamId):
            pass
        else:
            parser.error("Unsupported 'type' %s. Set it to TcpStreamId or MpTcpStreamId" % type(values))

        # super(argparse.Action).__call__(parser, namespace, values, option_string)
        log.debug("Assign filter to %s", (self.dest))
        setattr(namespace, self.dest, values)
        query = self.query_tpl.format(field=field, streamid=values)

        log.log(mp.TRACE, "Applying query [%s]" % query)
        debug_dataframe(df, "after query")  # usecolds ['tcpstream']

        import pandas as pd
        log.log(mp.TRACE, "use numexpr? %d", pd.get_option('compute.use_numexpr', False))
        df.query(query, inplace=True, engine="python")
        # TODO build dest automatically


def gen_bicap_parser(protocol: mp.Protocol, dest=False):
    """
    protocol in ["mptcp", "tcp"]
    """
    if protocol == mp.Protocol.MPTCP:
        actions = PreprocessingActions.FilterMpTcpStream | PreprocessingActions.MergeMpTcp
    else:
        actions = PreprocessingActions.FilterTcpStream | PreprocessingActions.MergeTcp
    # action = (PreprocessingActions.Preload | PreprocessingActions.FilterStream | PreprocessingActions.Merge)
    input_pcaps = {
        "pcap": actions,
    }

    return gen_pcap_parser(input_pcaps=input_pcaps, direction=dest)

# map pcaps to a group
# TODO pass a dict of @dataclass instead
# add subnamespace ?
class MpTcpAnalyzerParser(cmd2.argparse_custom.Cmd2ArgumentParser):
    '''
    Wrapper around cmd2 argparse completer
    Should allow to switch backends easily.
    Also allows to do some postprocessing once the arguments are parsed
    like loading dataframes etc

    '''

    def parse_known_args(self, args=None, namespace=None):
        """
        override it just to postprocess arguments
        """

        # returns a 2-item tuple
        known, unknown = super().parse_known_args(args, namespace)

        # TODO call filter_dataframe ?
        if getattr(known, "_dataframes", None):
            for name, _ in known._dataframes.items():
                # print
                # so now we can filter the destination ?
                log.debug("dataframe [%s] in namespace", name)

                # TODO here we should filter the destinations
        else:
            log.debug("No dataframe in namespace")

        # dataframes = dargs.pop("_dataframes", {})

        # # TODO move to parser
        # for pcap, df in dataframes.items():
        #     res = dargs.pop(pcap, None)
        #     if res:
        #         log.debug("Popping %s to prevent a duplicate with the one from _dataframes" % pcap)

        # postprocessing for filtering destination

        log.debug("MpTcpAnalyzerParser parser finished")
        # TODO pass along known, dataframes ?
        return (known, unknown)

    def add_pcap(self, name, **kwargs):
        # pass
        params = {
            'action': LoadSinglePcap,
            'help': 'Pcap file',
            'completer_method': cmd2.Cmd.path_complete
        }
        params.update(**kwargs)
        load_pcap = self.add_argument(name, type=str, **params)
        return load_pcap

    # with add_argument_group for instance ?
    # https://stackoverflow.com/questions/18668227/argparse-subcommands-with-nested-namespaces
    # def add_single_pcap(self, name, ):
    def filter_destination(self, *args, **kwargs):

        params = {
            'action': AppendDestination,
        }
        params.update(**kwargs)
        return self.add_argument(
            *args,
            '--dest',
            metavar="destination",
            # see preprocess functions to see how destinations is handled when empty
            # Both are already taken care of
            # TODO check how it works/FilterDest
            help='Filter flows according to their direction'
            '(towards the client or the server)',
            **params
        )

    def skip_subflow(self, df_name, **kwargs):
        return self.add_argument('--skip', type=TcpStreamId,
            action=exclude_stream(df_name,),
            # TODO careful this won't work as a default, need a special action
            default=[],
            help=("You can type here the tcp.stream of a subflow "
                "not to take into account (because"
                "it was filtered by iptables or else)")
        )


    def filter_stream(self, name, *args, protocol=None, **kwargs):
        assert protocol is not None, protocol

        proto_str = protocol.to_string()
        params = {
            'action': "store",
            'help': proto_str + '.stream wireshark id'
        }
        params.update(**kwargs)

        return self.add_argument(
            name,
            # name + 'stream',
            metavar=(name + "_{}stream").format(proto_str),
            type=MpTcpStreamId if protocol == mp.Protocol.MPTCP else TcpStreamId,
            **params
        )


def gen_pcap_parser(
    # rename input_pcaps to load_dataframes
    input_pcaps: Dict[str, PreprocessingActions],
    # protocol,
    direction: bool = False,
    parents=[],
    # TODO get rid of this/skip-stream
    skip_subflows: bool = True,
) -> MpTcpAnalyzerParser:
    """
    Generates a parser with common options.
    This parser can be completed or overridden by its children.

    Args:
        available_dataframe: True if a pcap was preloaded at start
        direction: Enable filtering the stream depending if the packets
        were sent towards the MPTCP client or the MPTCP server
        skip_subflows: Allow to hide some subflows from the plot

    Return:
        An argparse.ArgumentParser derivative

    """
    parser = MpTcpAnalyzerParser(
        parents=parents,
        add_help=not parents,
    )

    # TODO we should make this cleaner
    for df_name, bitfield in input_pcaps.items():


        # if bitfield & (PreprocessingActions.FilterStream | PreprocessingActions.Merge):
        #     # difficult to change the varname here => change it everywhere
        #     mptcp: bool = (bitfield & PreprocessingActions.FilterMpTcpStream) != 0
        #     protocol = "mptcp" if mptcp else "tcp"
        #     parser.filter_stream(name + 'stream',)
        #     parser.add_argument(
        #       name + 'stream',
        #       metavar=name + "_" + protocol + "stream",
        #       action=filterAction,
        #       type=MpTcpStreamId if protocol == "mptcp" else TcpStreamId,
        #       help=protocol + '.stream wireshark id')


        if bitfield & PreprocessingActions.Merge:
            # mptcp: bool = (bitfield & PreprocessingActions.FilterMpTcpStream) != 0
            # protocol = "mptcp" if mptcp else "tcp"
            protocol = mp.Protocol.MPTCP if bitfield & PreprocessingActions.MergeMpTcp else mp.Protocol.TCP
            parser.add_pcap(df_name+"1")
            parser.filter_stream(df_name+"1stream", protocol=protocol,)

            parser.add_pcap(df_name+"2")
            parser.filter_stream(df_name+"2stream", protocol=protocol,
                action=partial(MergePcaps, name=df_name, protocol=protocol),
            )

            # hidden
            # action is triggered only when meet the parameter
            # merge_pcap = parser.add_argument("--" + name + "_protocol",
            #     action=partial(MergePcaps, prefix=name, protocol=protocol),
            #     help=argparse.SUPPRESS)
            # merge_pcap.default = "TEST"
        else:
            # TODO check for Preload
            # TODO set action to str if there is no Preload flag ?!
            parser.add_pcap(df_name, )

            # TODO enforce a protocol !!
            protocol = mp.Protocol.MPTCP if bitfield & PreprocessingActions.FilterMpTcpStream else mp.Protocol.TCP
            parser.filter_stream(df_name + 'stream', protocol=protocol, action=retain_stream(df_name,))

        if bitfield & PreprocessingActions.FilterDestination or direction:
            parser.filter_destination(dest=df_name + "_destinations")


        # TODO add as an action
        if skip_subflows:
            parser.skip_subflow(dest=df_name + "skipped_subflows", df_name=df_name)

    return parser
