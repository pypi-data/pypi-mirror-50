from __future__ import absolute_import

import os, inspect
import warnings
from collections import namedtuple
import multiaddr
from typing import List, Mapping
import re
rxname = re.compile(r'.*?filename="([^/ \\:?*"><|]+)"')
"""re.Pattern: for detecting the file name from a multipart form upload.
"""

DEFAULT_ADDR = multiaddr.Multiaddr(os.environ.get("PY_IPFS_CLUSTER_DEFAULT_ADDR", '/dns/localhost/tcp/9094/http'))
"""str: default multiaddr for connecting to the cluster HTTP endpoint.
"""
DEFAULT_BASE = str(os.environ.get("PY_IPFS_CLUSTER_DEFAULT_BASE", ''))
"""str: base version for the API; basically sets the root of the URL path for
submitting queries. Default value is `/api/v0`.
"""

from ipfshttpclient.client import assert_version, base, files, miscellaneous
from ipfshttpclient import encoding, exceptions, multipart, utils

from . import health
from . import allocations
from . import pins
from . import peers
from . import http

def connect(addr=DEFAULT_ADDR, base=DEFAULT_BASE,
            chunk_size=multipart.default_chunk_size,
            session=False, **defaults):
    """Create a new :class:`~ipfscluster.Client` instance and connect to the
    daemon to validate that its version is supported. All parameters are
    identical to those passed to the constructor of the
    :class:`~ipfscluster.Client` class.

    Returns:
        :class:`~ipfscluster.Client`
    """
    # Create client instance
    client = Client(addr, base, chunk_size, session, **defaults)

    #Query version number from daemon and validate it; the IPFS cluster uses
    #git version hashes, so this doesn't work the same way. Maybe figure out
    #later how to do this. For now, just check that the version returns.
    assert client.version()['version'] != ''

    return client

class PinOptions:
    """Options for pinning files in IPFS cluster.

    Args:
        replication_factor_min (int):
        replication_factor_max (int):
        name (str):
        shard_size (int):
    """
    varmap = {
        "replication_factor_min": "replication-min",
        "replication_factor_max": "replication-max",
        "name": "name",
        "shard_size": "shard-size",
    }
    def __init__(self, replication_factor_min: int = None,
                 replication_factor_max: int = None, name: str = None,
                 shard_size: int = None):
        self.params = {}
        locvars = locals()
        for v, m in self.varmap.items():
            if locvars[v] is not None:
                self.params[m] = locvars[v]

class AddOptions:
    """Options for adding files/bytes/etc. to the cluster.

    Args:
        pinopts (PinOptions): options related to how the new file will be pinned
            in the cluster.
        recursive (bool): when True, if the path being added is a directory, the
            files will be recursively added too.
        layout (str):
        chunker (str):
        raw_leaves (bool):
        hidden (bool):
        wrap (bool):
        shard (bool):
        progress (bool):
        cid_version (int):
        hashfun (str):
        stream_channels (bool):
        nocopy (bool):
    """
    varmap = {
        "pinopts": "PinOptions",
        "recursive": "recursive",
        "layout": "layout",
        "chunker": "chunker",
        "raw_leaves": "raw-leaves",
        "hidden": "hidden",
        "wrap": "wrap-with-directory",
        "shard": "shard",
        "progress": "progress",
        "cid_version": "cid-version",
        "hashfun": "hash",
        "stream_channels": "stream-channels",
        "nocopy": "nocopy"
    }
    def __init__(self, pinopts: PinOptions = None, recursive: bool = None,
                 layout: str = None, chunker: str = None,
                 raw_leaves: bool = None, hidden: bool = None,
                 wrap: bool = None, shard: bool = None, progress: bool = None,
                 cid_version: int = None, hashfun: str = None,
                 stream_channels: bool = None, nocopy: bool = None):
        self.params = {}
        locvars = locals()
        for v, m in self.varmap.items():
            if locvars[v] is not None:
                if v == "pinopts":
                    self.params.update(locvars[v].params.items())
                    continue

                if isinstance(locvars[v], bool):
                    self.params[m] = "true" if locvars[v] else "false"
                else:
                    self.params[m] = locvars[v]

def get_adjusted_params(addopts, headers):
    """Returns a set of parameters adjusted for possible filenames specified
    only in the form headers of a request.

    Args:
        addopts (AddOptions): for modifying how IPFS adds the file.
        headers (dict): headers being sent with the add request.
    """
    params = {}
    if addopts is not None:
        params.update(addopts.params)

    if "name" not in params:
        hcontent = headers["Content-Disposition"]
        mname = rxname.match(hcontent)
        if mname:
            params["name"] = mname.groups(0)[0]

    return params

class Client(files.Base, miscellaneous.Base):
    """The main IPFS Cluster HTTP client class

    Allows access to an IPFS cluster instance using its HTTP API by exposing an
    interface compatible set of methods.

    It is possible to instantiate this class directly, using the same parameters
    as :func:`connect`, to prevent the client from checking for an active and
    compatible version of the daemon. In general however, calling
    :func:`connect` should be preferred.

    In order to reduce latency between individual API calls, this class may keep
    a pool of TCP connections between this client and the API daemon open
    between requests. The only caveat of this is that the client object should
    be closed when it is not used anymore to prevent resource leaks.

    The easiest way of using this “session management” facility is using a
    context manager:

    .. code-block:: python

        with ipfscluster.connect() as client:
            print(client.version())  # These calls…
            print(client.version())  # …will reuse their TCP connection

    A client object may be re-opened several times:

    .. code-block:: python

        client = ipfscluster.connect()
        print(client.version())  # Perform API call on separate TCP connection
        with client:
            print(client.version())  # These calls…
            print(client.version())  # …will share a TCP connection
        with client:
            print(client.version())  # These calls…
            print(client.version())  # …will share a different TCP connection

    When storing a long-running :class:`Client` object use it like this:

    .. code-block::

        class Consumer:
            def __init__(self):
                self._client = ipfscluster.connect(session=True)

            # … other code …

            def close(self):  # Call this when you're done
                self._client.close()
    """
    health      = base.SectionProperty(health.Section)
    allocations = base.SectionProperty(allocations.Section)
    pins        = base.SectionProperty(pins.Section)
    peers       = base.SectionProperty(peers.Section)

    def __init__(self, addr=DEFAULT_ADDR, base=DEFAULT_BASE,
	             chunk_size=multipart.default_chunk_size,
	             session=False, **defaults):
        self.chunk_size = chunk_size
        self._client = http.HTTPClusterClient(addr, base, **defaults)
        if session: # pragma: no cover
            self._client.open_session()

    ######################
    # SESSION MANAGEMENT #
    ######################

    def __enter__(self):
        self._client.open_session()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close any currently open client session and free any associated
        resources.

        If there was no session currently open this method does nothing. An open
        session is not a requirement for using a :class:`~ipfscluster.Client`
        object and as such all method defined on it will continue to work, but
        a new TCP connection will be established for each and every API call
        invoked. Such a usage should therefor be avoided and may cause a warning
        in the future. See the class's description for details.
        """
        self._client.close_session()

    ###########
    # HELPERS #
    ###########

    @base.returns_single_item
    def add_bytes(self, data, name: str = "bytes", addopts: AddOptions = None, **kwargs):
        """Adds a set of bytes as a file to IPFS.

        Args:
            name (str): name to attach to this pin in the cluster.

        Examples:
            >>> client.add_bytes(b"Mary had a little lamb")
            {
                'name': 'bytes',
                'cid': {'/': 'QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab'},
                'size': 30
            }

            Also accepts and will stream generator objects.

        Args:
            data(bytes): Content to be added as a file.

        Returns:
            str: Hash of the added IPFS object.
        """
        stream = multipart.BytesFileStream(data, chunk_size=self.chunk_size, name=name)
        body, headers = stream.body(), stream.headers()
        params = get_adjusted_params(addopts, headers)
        return self._client.request('/add', decoder='json', opts=params,
                                    data=body, headers=headers, **kwargs)

    @base.returns_single_item
    def add_files(self, data, addopts: AddOptions = None, **kwargs):
        """Adds file(s) to IPFS cluster.

        Examples:
            >>> client.add_files("/path/to/file")
            {
                'name': 'bytes',
                'cid': {'/': 'QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab'},
                'size': 30
            }

            Also accepts and will stream generator objects.

        Args:
            data(file-like): Content to be added as a file.

        Returns:
            str: Hash of the added IPFS object.
        """
        body, headers = multipart.stream_files(data, self.chunk_size)
        params = get_adjusted_params(addopts, headers)
        return self._client.request('/add', decoder='json', opts=params,
                                    data=body, headers=headers, **kwargs)

    def add_str(self, string, name: str = "bytes", addopts: AddOptions = None, **kwargs):
        """Adds a Python string as a file to IPFS.

        Examples:
            >>> client.add_str(u"Mary had a little lamb")
            {
                'name': 'bytes',
                'cid': {'/': 'QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab'},
                'size': 30
            }

            Also accepts and will stream generator objects.

        Args:
            string (str): Content to be added as a file.

        Returns:
            str: Hash of the added IPFS object.
        """
        if inspect.isgenerator(string):
            def binary_stream():
                for item in string:
                    yield item.encode("utf-8")

            data = binary_stream()
        else:
            data = string.encode("utf-8")
        return self.add_bytes(data, name=name, addopts=addopts, **kwargs)

    def add_json(self, json_obj, name="bytes", addopts: AddOptions = None, **kwargs):
        """Adds a json-serializable Python dict as a json file to IPFS.

        Examples:
            >>> client.add_json({'one': 1, 'two': 2, 'three': 3})
            {
                'name': 'bytes',
                'cid': {'/': 'QmSsf2JAfrKaVPgPpFY1qEjLTiiqaWt8aHFRRKrx3dRXBz'},
                'size': 35
            }

        Args:
            json_obj(dict): A json-serializable Python dictionary.

        Returns:
            str: Hash of the added IPFS object.
        """
        return self.add_bytes(encoding.Json().encode(json_obj),
                              name=name, addopts=addopts, **kwargs)

    @base.returns_single_item
    def id(self, **kwargs):
        """Queries the cluster for identifyg data via `/id` endpoint.

        Examples:

            >>> client.id()
            {
                "id": "12D3...",
                "addresses":
                    ["/ip4/127.0.0.1/tcp/9096/ipfs/12D3...",
                     "/ip4/172.28.0.4/tcp/9096/ipfs/12D3..."],
                "cluster_peers":
                    ["12D3..."],
                "cluster_peers_addresses": [],
                "version": "0.10.1+git7ffbbef...",
                "commit": "",
                "rpc_protocol_version": "/ipfscluster/0.10/rpc",
                "error": "",
                "ipfs": {
                    "id":"QmSU...",
                    "addresses":
                        ["/ip4/127.0.0.1/tcp/4001/ipfs/QmSU...",
                         "/ip4/172.28.0.2/tcp/4001/ipfs/QmSU..."],
                    "error": ""
                },
                "peername": "fab67a4286dd"
            }
        """
        return self._client.request('/id', decoder='json', **kwargs)

    @base.returns_single_item
    def version(self, **kwargs):
        """Queries the cluster for the daemon version.

        Examples:

            >>> client.version()
            {"version":"0.10.1+git7ffbbef..."}
        """
        return self._client.request('/version', decoder='json', **kwargs)
