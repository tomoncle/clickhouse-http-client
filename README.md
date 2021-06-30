# clickhouse-http-client
clickhouse http client.

## Install

* source:
```shell
$ git clone https://github.com/tomoncle/clickhouse-http-client.git
$ cd clickhouse-http-client && sudo python setup.py install
```
* pip: `$ pip install clickhouse-http-client`

## Usage

```python
from clickhouse_http_client import ClickHouse
ck = ClickHouse()
ck.text("select * from table_name")
```

[travis]: https://travis-ci.org/tomoncle/clickhouse-http-client