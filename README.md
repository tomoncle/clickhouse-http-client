# clickhouse-http-client
clickhouse http client.

## Install

* Use source:

```bash
$ git clone https://github.com/tomoncle/clickhouse-http-client.git
$ cd clickhouse-http-client
$ sudo python setup.py install
```


* Use pip:

```bash
$ pip install clickhouse-http-client
```


## Usage

* query

```python
from clickhouse_http_client import ClickHouse

ck = ClickHouse(password="123456")

ck.text("select * from table_name")
ck.json("select * from table_name")
```

* delete

```python
from clickhouse_http_client import ClickHouse

ck = ClickHouse(password="123456")
ck.delete("table_name", "id IS NOT NULL")
```

* save

```python
from clickhouse_http_client import ClickHouse

ck = ClickHouse(password="123456")
ck.insert("table_name", {"name":"tomoncle", "age":"27"})
```

* update

```python
from clickhouse_http_client import ClickHouse

ck = ClickHouse(password="123456", show_sql=True)
```