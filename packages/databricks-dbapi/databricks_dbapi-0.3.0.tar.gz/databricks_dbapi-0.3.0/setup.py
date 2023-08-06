# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['databricks_dbapi']

package_data = \
{'': ['*']}

install_requires = \
['pyhive[hive]>=0.6.1,<0.7.0']

extras_require = \
{'sqlalchemy': ['sqlalchemy>=1.3,<2.0']}

entry_points = \
{'sqlalchemy.dialects': ['databricks.pyhive = '
                         'databricks_dbapi.sqlalchemy_databricks:DatabricksDialect']}

setup_kwargs = {
    'name': 'databricks-dbapi',
    'version': '0.3.0',
    'description': 'A DBAPI 2.0 interface and SQLAlchemy dialect for Databricks interactive clusters.',
    'long_description': 'databricks-dbapi\n================\n\n|pypi| |pyversions|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/databricks-dbapi.svg\n    :target: https://pypi.python.org/pypi/databricks-dbapi\n\n.. |pyversions| image:: https://img.shields.io/pypi/pyversions/databricks-dbapi.svg\n    :target: https://pypi.python.org/pypi/databricks-dbapi\n\nA thin wrapper around `pyhive <https://github.com/dropbox/PyHive>`_ for creating a `DBAPI <https://www.python.org/dev/peps/pep-0249/>`_ connection to an interactive Databricks cluster.\n\nAlso provides a SQLAlchemy Dialect for Databricks interactive clusters.\n\nInstallation\n------------\n\nInstall using pip:\n\n.. code-block:: bash\n\n    pip install databricks-dbapi\n\n\nFor SQLAlchemy support install with:\n\n.. code-block:: bash\n\n    pip install databricks-dbapi[sqlalchemy]\n\nUsage\n-----\n\nThe ``connect()`` function returns a ``pyhive`` Hive connection object, which internally wraps a ``thrift`` connection.\n\nUsing a Databricks API token (recommended):\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import databricks\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    cluster = os.environ["DATABRICKS_CLUSTER"]\n\n\n    connection = databricks.connect(\n        host=host,\n        cluster=cluster,\n        token=token,\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100")\n\n    print(cursor.fetchone())\n    print(cursor.fetchall())\n\n\nUsing your username and password (not recommended):\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import databricks\n\n\n    user = os.environ["DATABRICKS_USER"]\n    password = os.environ["DATABRICKS_PASSWORD"]\n    host = os.environ["DATABRICKS_HOST"]\n    cluster = os.environ["DATABRICKS_CLUSTER"]\n\n\n    connection = databricks.connect(\n        host=host,\n        cluster=cluster,\n        user=user,\n        password=password\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100")\n\n    print(cursor.fetchone())\n    print(cursor.fetchall())\n\n\nConnecting on Azure platform, or with ``http_path``:\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import databricks\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    http_path = os.environ["DATABRICKS_HTTP_PATH"]\n\n\n    connection = databricks.connect(\n        host=host,\n        http_path=http_path,\n        token=token,\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100")\n\n    print(cursor.fetchone())\n    print(cursor.fetchall())\n\n\nThe ``pyhive`` connection also provides async functionality:\n\n.. code-block:: python\n\n    import os\n\n    from databricks_dbapi import databricks\n    from TCLIService.ttypes import TOperationState\n\n\n    token = os.environ["DATABRICKS_TOKEN"]\n    host = os.environ["DATABRICKS_HOST"]\n    cluster = os.environ["DATABRICKS_CLUSTER"]\n\n\n    connection = databricks.connect(\n        host=host,\n        cluster=cluster,\n        token=token,\n    )\n    cursor = connection.cursor()\n\n    cursor.execute("SELECT * FROM some_table LIMIT 100", async_=True)\n\n    status = cursor.poll().operationState\n    while status in (TOperationState.INITIALIZED_STATE, TOperationState.RUNNING_STATE):\n        logs = cursor.fetch_logs()\n        for message in logs:\n            print(message)\n\n        # If needed, an asynchronous query can be cancelled at any time with:\n        # cursor.cancel()\n\n        status = cursor.poll().operationState\n\n    print(cursor.fetchall())\n\n\n\nSQLAlchemy\n----------\n\nOnce the ``databricks-dbapi`` package is installed, the ``databricks+pyhive`` dialect/driver will be registered to SQLAlchemy. Fill in the required information when passing the engine URL.\n\n.. code-block:: python\n\n    from sqlalchemy import *\n    from sqlalchemy.engine import create_engine\n    from sqlalchemy.schema import *\n\n\n    # Standard Databricks with user + password\n    # provide user, password, company name for url, database name, cluster name\n    engine = create_engine(\n        "databricks+pyhive://<user>:<password>@<companyname>.cloud.databricks.com:443/<database>",\n        connect_args={"cluster": "<cluster>"}\n    )\n\n    # Standard Databricks with token\n    # provide token, company name for url, database name, cluster name\n    engine = create_engine(\n        "databricks+pyhive://token:<databricks_token>@<companyname>.cloud.databricks.com:443/<database>",\n        connect_args={"cluster": "<cluster>"}\n    )\n\n    # Azure Databricks with user + password\n    # provide user, password, region for url, database name, http_path (with cluster name)\n    engine = create_engine(\n        "databricks+pyhive://<user>:<password>@<region>.azuredatabricks.net:443/<database>",\n        connect_args={"http_path": "<azure_databricks_http_path>"}\n    )\n\n    # Azure Databricks with token\n    # provide token, region for url, database name, http_path (with cluster name)\n    engine = create_engine(\n        "databricks+pyhive://token:<databrickstoken>@<region>.azuredatabricks.net:443/<database>",\n        connect_args={"http_path": "<azure_databricks_http_path>"}\n    )\n\n\n    logs = Table("my_table", MetaData(bind=engine), autoload=True)\n    print(select([func.count("*")], from_obj=logs).scalar())\n\n\nRefer to the following documentation for more details on hostname, cluster name, and http path:\n\n* `Databricks <https://docs.databricks.com/user-guide/bi/jdbc-odbc-bi.html>`_\n* `Azure Databricks <https://docs.azuredatabricks.net/user-guide/bi/jdbc-odbc-bi.html>`_\n\n\nRelated\n-------\n\n* `pyhive <https://github.com/dropbox/PyHive>`_\n* `thrift <https://github.com/apache/thrift/tree/master/lib/py>`_\n',
    'author': 'Christopher Flynn',
    'author_email': 'crf204@gmail.com',
    'url': 'https://github.com/crflynn/databricks-dbapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
