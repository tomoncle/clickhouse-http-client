clickhouse-http-client
======================
clickhouse http client.

Install
=======

Use source::

   $ git clone https://github.com/tomoncle/clickhouse-http-client.git
   $ cd clickhouse-http-client
   $ sudo python setup.py install

Use pip::

   $ pip install clickhouse-http-client



Usage
=====

init::

   from clickhouse_http_client import ClickHouse
   ck = ClickHouse(password="123456")

query::

   ck.text("select * from table_name")
   ck.json("select * from table_name")

delete::

   ck.delete("table_name", "id IS NOT NULL")

save::

   ck.insert("table_name", {"name":"tomoncle", "age":"27"})

update::

   ck.update("table_name", "status=1", {"name":"tomoncle", "age":"27"})

