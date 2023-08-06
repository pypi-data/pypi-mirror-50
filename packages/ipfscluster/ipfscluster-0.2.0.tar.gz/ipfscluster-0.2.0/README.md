[![pipeline status](https://gitlab.com/clearos/clearfoundation/py-ipfs-cluster-api/badges/master/pipeline.svg)](https://gitlab.com/clearos/clearfoundation/py-ipfs-cluster-api/commits/master) [![coverage report](https://gitlab.com/clearos/clearfoundation/py-ipfs-cluster-api/badges/master/coverage.svg)](https://gitlab.com/clearos/clearfoundation/py-ipfs-cluster-api/commits/master)

# IPFS Cluster HTTP API

This is a python package to interact with the HTTP REST API of the IPFS cluster.
[Full API documentation](https://clearos.gitlab.io/clearfoundation/py-ipfs-cluster-api)
is available on gitlab pages.

## Installation

`ipfscluster` is available from the PyPI repository:

```bash
pip install ipfscluster
```

## Getting an IPFS Cluster Running

To try the API out, you need to have a running IPFS cluster. The easiest way to
get one of those is to use `docker`. In the `docker-compose.yml` file shown
below, you will need to adjust the `volumes` tags to reference actual folders
on your host machine. The change in `environment` variables for `ipfs_cluster`
service makes use the docker network DNS resolution by service name. Since our
docker agent is called `ipfs`, we can get its IP address in the internal,
`backend` network by using `ipfs` as its DNS name.

Copy this YML into a `docker-compose.yml` file in some folder and then run
`docker-compose up`.

```yaml
version: "3.7"
services:

  ipfs:
    image: ipfs/go-ipfs:latest
    ports:
      - "4001:4001"
      - "5001:5001"
    networks:
      - backend
    volumes:
      - ~/ipfs/ipfs:/data/ipfs

  ipfs_cluster:
    image: ipfs/ipfs-cluster:latest
    ports:
      - "9094:9094"
      - "9095:9094"
      - "9096:9096"
    volumes:
      - ~/ipfs/ipfs-cluster:/data/ipfs-cluster
    networks:
      - backend
    depends_on:
      - ipfs
    environment:
      - CLUSTER_IPFSHTTP_NODEMULTIADDRESS=/dns4/ipfs/tcp/5001
      - CLUSTER_IPFSPROXY_NODEMULTIADDRESS=/dns4/ipfs/tcp/5001

  networks:
    backend:
```

## Try out the API

Now that you have a cluster running, you can try the API out. Open a python
CLI and try:

```python
client = connect()
m = {'name': 'bytes',
       'cid': {'/': 'QmZfF6C9j4VtoCsTp4KSrhYH47QMd3DNXVZBKaxJdhaPab'},
       'size': 30}
with client:
    r = client.add_bytes(b"Mary had a little lamb")
assert r == m
```

## Running Unit Tests

Running unit tests can prove to be a massive pain because the gitlab CI runner
runs on docker. For a project like this that uses `docker-compose`, we have
to use `docker-in-docker` according to their instructions. However, the
documentation is sparse and there are lots of dead-ends... Here are the steps to
get the `docker-compose.yml` file to work:

1. Install a local `gitlab-runner` using `brew install gitlab-runner`.
2. `gitlab-runner exec docker --docker-privileged test`. Notice that there is a
   `--docker-privileged` argument. Without that, the `docker-in-docker` won't
   work.
3. Make sure all the `multiaddr` reference the `docker` service (which hosts
   all the other containers using `dind`).
4. `tox` should work, but for some reason: running the tests using `tox` produces
   connection refused errors, whereas running straight with `pytest` does not.
   Something about the tox environment screws things up.
