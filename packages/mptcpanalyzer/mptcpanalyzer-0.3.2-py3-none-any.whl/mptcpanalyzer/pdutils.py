import logging
import pprint
import numpy as np
import pandas as pd
from mptcpanalyzer.connection import MpTcpConnection, TcpConnection
import mptcpanalyzer as mp
from mptcpanalyzer import TcpFlags
from mptcpanalyzer.data import classify_reinjections


log = logging.getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4)

# register_series_accessor
# pandas.api.extensions.register_index_accessor

@pd.api.extensions.register_dataframe_accessor("merged")
class MergedAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def sender(self):
        """ Return """
        # look at columns that start with the prefix and others
        # _sender()
        pass

    def already_classified(self) -> bool:
        """
        Check if dataframe entries have been classified
        """
        if "redundant" not in self._obj.columns:
            return False

        return not self._obj.columns["redundant"].hasnans

    def classify_reinjections(self):
        """
        not a copy
        """
        return classify_reinjections(self._obj)


# StreamAccessor ?
@pd.api.extensions.register_dataframe_accessor("tcp")
class TcpAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def connection(self, streamid) -> TcpConnection:
        # if tcpdest is None:
        #     tcpdest = list(mp.ConnectionRoles)
        return TcpConnection.build_from_dataframe(self._obj, streamid)

        # TODO copy the dataframe
        # TcpConnection.build_from_dataframe(self._obj, streamid)
        # TODO fill destination
        # TODO fill tcpdest
        # return self._obj.where(self._obj.tcpstream == streamid)

    # def match(self, , stream, df):
        # TODO
        # pass

    # def merge(self, df, stream):

    # need to filter the stream
    def syn_idx(self):
        # TODO
        syns = np.bitwise_and(self._obj['tcpflags'], TcpFlags.SYN)

        if len(syns.index) < 1:
            raise mp.MpTcpException("No packet with any SYN flag for tcpstream")

        idx = syns.index[0]
        return idx

    def fill_dest(self, streamid):
        '''
        '''
        con = self.connection(streamid)
        return con.fill_dest(self._obj)

    # TODO fill destination

@pd.api.extensions.register_dataframe_accessor("mptcp")
class MpTcpAccessor:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def connection(self, streamid) -> MpTcpConnection:
        return MpTcpConnection.build_from_dataframe(self._obj, streamid)

    # TODO rename to stream
    def filter(self, streamid) -> MpTcpConnection:
        return self._obj.where(self._obj.mptcpstream == streamid)

    def fill_dest(self, streamid):
        ''' '''
        con = self.connection(streamid)
        return con.fill_dest(self._obj)


def to_datetime(s, **opts):
    """
    pandas'to_datetime with some default arguments
    """
    # set origin to first entry of
    # defaults = {
    #     "origin":
    # }
    # defaults.update(opts)
    return pd.to_datetime()


# def filter_dataframe(
#     self,
#     rawdf,
#     # TODO choose prefix
#     merged_one,
#     tcpstream=None,
#     mptcpstream=None,
#     skipped_subflows=[],
#     destinations: list=None,
#     extra_query: str=None, **kwargs
# ):
#     """
#     Can filter a single dataframe beforehand
#     (hence call it several times for several dataframes).

#     Feel free to inherit/override this class.

#     Args:
#         rawdf: Raw dataframe
#         kwargs: expanded arguments returned by the parser
#         destination: Filters packets depending on their :enum:`.ConnectionRoles`
#         stream: keep only the packets related to mptcp.stream == mptcpstream
#         skipped_subflows: list of skipped subflows
#         extra_query: Add some more filters to the pandas query

#     This baseclass can filter on:

#     - mptcpstream
#     - destination (mptcpstream required)
#     - skipped_subflows

#     Returns:
#         Filtered dataframe
#     """
#     log.debug("Preprocessing dataframe with extra args %s" % kwargs)
#     queries = []
#     log.debug("tcp.stream %d mptcp: %d" % (tcpstream, mptcpstream))
#     stream = tcpstream if tcpstream is not None else mptcpstream
#     dataframe = rawdf

#     for skipped_subflow in skipped_subflows:
#         log.debug("Skipping subflow %d" % skipped_subflow)
#         queries.append(" tcpstream!=%d " % skipped_subflow)

#     if stream is not None:
#         protocol = "mptcp" if mptcpstream is not None else "tcp"
#         log.debug("Filtering %s stream #%d." % (protocol, stream))
#         queries.append(protocol + "stream==%d" % stream)


#         if protocol == "tcp":
#             # generates the "tcpdest" component of the dataframe
#             con2 = TcpConnection.build_from_dataframe(dataframe, stream)
#             dataframe = Xcpdest_from_connections(dataframe, con2)
#             # trust plots to do the filtering
#             # if destinations is not []:
#             #     queries.append(protocol + "dest==%d" % stream)
#         else:
#             # todo shall do the same for mptcp destinations
#             con = MpTcpConnection.build_from_dataframe(dataframe, stream)
#             # mptcpdest = main_connection.mptcp_dest_from_tcpdest(tcpdest)
#             df = Xptcpdest_from_connections(dataframe, con)
#             # TODO generate mptcpdest
#             # if protocol == "mptcp":
#             if destinations is not None:
#                 raise Exception("destination filtering is not ready yet for mptcp")

#                 log.debug("Filtering destination")

#                 # Generate a filter for the connection
#                 # con = MpTcpConnection.build_from_dataframe(dataframe, stream)
#                 # q = con.generate_direction_query(destination)
#                 # queries.append(q)
#     if extra_query:
#         log.debug("Appending extra_query=%s" % extra_query)
#         queries.append(extra_query)

#     query = " and ".join(queries)

#     # throws when querying with an empty query
#     if len(query) > 0:
#         log.info("Running query:\n%s\n" % query)
#         dataframe.query(query, inplace=True, engine="python")

#     return dataframe
