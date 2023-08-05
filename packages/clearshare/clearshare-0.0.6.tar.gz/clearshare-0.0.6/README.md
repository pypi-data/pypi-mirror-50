[![pipeline status](https://gitlab.com/clearos/clearfoundation/clearshare/badges/master/pipeline.svg)](https://gitlab.com/clearos/clearfoundation/clearshare/commits/master) [![coverage report](https://gitlab.com/clearos/clearfoundation/clearshare/badges/master/coverage.svg)](https://gitlab.com/clearos/clearfoundation/clearshare/commits/master)

# clearshare Decentralized Private Storage

`clearshare` provides privatized data storage backed by distributed and
decentralized systems. It does this by leveraging distributed ledegers to maintain
decentralized identifiers (DIDs) and documents that described those DIDs
(called DDOs). The DIDs are configured to described files stored in IPFS. To allow
sharing, the distributed ledgers are used to enable DID-based authentication
in the HTTP headers.

## Installation

Install from PyPI:

```bash
pip install clearshare
```

## Quickstart

The package provides a REST API server to process all interactions with the
ledgers and IPFS.

```python
from clearshare import start, stop
# Start the API server; it can be stopped later with stop().
start()
```

## Docker Dependencies

The package has several dependencies to manage the distributed ledger and DIDs,
and the private IPFS cluster. These can be started with `docker-compose`. The
`docker-compose.yml` in the repository root is used for *unit testing* only. To
start all dependencies, use:

```bash
cd docker
docker-compose up
```
