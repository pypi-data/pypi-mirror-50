# command line interface

import os
import sys
import trio_click as click
import time
import anyio
from pprint import pprint
import yaml

from distkv.util import (
    attrdict,
    PathLongener,
    MsgReader,
    PathShortener,
    split_one,
    NotGiven,
)
from distkv.client import open_client, StreamedRequest
from distkv.command import Loader
from distkv.default import CFG
from distkv.server import Server
from distkv.auth import loader, gen_auth
from distkv.exceptions import ClientError, ServerError
from distkv.errors import ErrorRoot
from distkv.util import yprint

import logging

logger = logging.getLogger(__name__)


@main.group()
@click.pass_obj
async def cli(obj):
    """Manage error records in DistKV."""
    obj.err = await ErrorRoot.as_handler(obj.client)


@cli.command()
@click.option("-n", "--node", help="add details from this node")
@click.option("-a", "--all-nodes", is_flag=True, help="add details from all nodes")
@click.option(
    "-d",
    "--as-dict",
    default=None,
    help="YAML: structure as dictionary. The argument is the key to use "
    "for values. Default: return as list",
)
@click.argument("path", nargs=-1)
@click.pass_obj
async def list(obj, as_dict, path, node, all_nodes):
    """List error entries.
    """
    path_ = obj.cfg["errors"].prefix
    if node:
        res = obj.client.get_tree(
            *path_, node, min_depth=1, max_depth=1, nchain=3 if obj.meta else 0
        )
    else:
        res = obj.client.get_tree(
            *path_, min_depth=2, max_depth=2, nchain=3 if obj.meta else 0
        )
    # TODO increase max_depth and attach the data to

    y = {}
    async for r in res:
        rp = r.value.path
        if rp[: len(path)] != path:
            continue
        rp = rp[len(path) :]
        rpe = r.pop("path")
        r.value.path = rpe[-2:]

        if all_nodes:
            rn = {}
            rs = await obj.client._request(
                action="get_tree",
                min_depth=1,
                max_depth=1,
                path=rpe,
                iter=True,
                nchain=3 if obj.meta else 0,
            )
            async for rr in rs:
                rn[rr.path[-1]] = rr if obj.meta else rr.value
        elif node is not None:
            rn = {}
            rr = await obj.client._request(
                action="get_value",
                path=rpe + (node,),
                iter=False,
                nchain=3 if obj.meta else 0,
            )
            if "value" not in rr:
                continue
            if rr is not None and "value" in rr:
                rn[node] = rr if obj.meta else rr.value
        else:
            rn = None

        if as_dict is not None:
            yy = y
            for p in rp:
                yy = yy.setdefault(p, {})
            yy[as_dict] = r if obj.meta else r.pop("value")
        else:
            yy = {}
            yy[rp] = r if obj.meta else r.value

        if rn:
            yy["nodes"] = rn

        if as_dict is None:
            yprint([yy], stream=obj.stdout)

    if as_dict is not None:
        yprint(y, stream=obj.stdout)


@cli.command()
@click.option(
    "-c", "--code", help="Path to the code that should run. Space separated path."
)
@click.option("-t", "--time", "tm", type=float, help="time the code should next run at")
@click.option("-r", "--repeat", type=int, help="Seconds the code should re-run after")
@click.option("-b", "--backoff", type=float, help="Back-off factor. Default: 1.4")
@click.option(
    "-d", "--delay", type=int, help="Seconds the code should retry after (w/ backoff)"
)
@click.option("-i", "--info", help="Short human-readable information")
@click.option(
    "-e", "--eval", "eval_", help="'code' is a Python expression (must eval to a list)"
)
@click.argument("path", nargs=-1)
@click.pass_obj
async def set(obj, path, code, eval_, tm, info, repeat, delay, backoff):
    """Save / modify a run entry."""
    if not path:
        raise click.UsageError("You need a non-empty path.")
    if eval_:
        code = eval(code)
        if not isinstance(code, (list, tuple)):
            raise click.UsageError("'code' must be a list")
    elif code is not None:
        code = code.split(" ")

    if obj.node is None:
        path = obj.cfg["anyrunner"].prefix + path
    else:
        path = obj.cfg["singlerunner"].prefix + (obj.node,) + path

    try:
        res = await obj.client._request(
            action="get_value", path=path, iter=False, nchain=3
        )
        if "value" not in res:
            raise ServerError
    except ServerError:
        if code is None:
            raise click.UsageError("New entry, need code")
        res = {}
        chain = None
    else:
        chain = res["chain"]
        res = res["value"]

    if code is not None:
        res["code"] = code
    if info is not None:
        res["info"] = info
    if backoff is not None:
        res["backoff"] = backoff
    if delay is not None:
        res["delay"] = delay
    if repeat is not None:
        res["repeat"] = repeat
    if tm is not None:
        res["target"] = time.time() + tm

    res = await obj.client._request(
        action="set_value", value=res, path=path, iter=False, nchain=3, chain=chain
    )
    yprint(res, stream=obj.stdout)
