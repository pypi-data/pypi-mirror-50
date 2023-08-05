from typing import List, Optional, Tuple, Union

from dvcr.containers.base import BaseContainer
from dvcr.network import Network


class Postgres(BaseContainer):
    def __init__(
        self,
        repo: str = "postgres",
        tag: str = "11",
        port: int = 5432,
        environment: Optional[dict] = None,
        name: str = "postgres",
        network: Optional[Network] = None,
    ):
        super(Postgres, self).__init__(
            port=port, repo=repo, tag=tag, name=name, network=network
        )

        if not environment:
            environment = {"POSTGRES_USER": "postgres", "POSTGRES_PASSWORD": ""}

        environment["PGPORT"] = port

        self.user = environment.get("POSTGRES_USER", "postgres")
        self.password = environment.get("POSTGRES_PASSWORD", "")
        self.db = environment.get("POSTGRES_DB", "postgres")

        self._container = self._client.containers.run(
            image=repo + ":" + tag,
            detach=True,
            name=name,
            network=self._network.name,
            healthcheck={
                "test": [
                    "CMD",
                    "pg_isready",
                    "--port",
                    str(self.port),
                    "--username",
                    self.user,
                ],
                "interval": 1000000000,
            },
            ports={port: port},
            environment=environment,
        )

    def sql_alchemy_conn(self, dialect="postgresql", driver=None):

        dialect_driver = dialect

        if driver:
            dialect_driver = dialect_driver + "+" + driver

        return "{dialect_driver}://{user}:{pwd}@{host}:{port}/{db}".format(
            dialect_driver=dialect_driver,
            user=self.user,
            pwd=self.password,
            host=self._container.name,
            port=self.port,
            db=self.db,
        )

    def execute_query(self, query: str, path_or_str: Union[str, bytes, None] = None):

        self.exec(
            cmd=["psql", "-U", self.user, "-e", "--command", query],
            path_or_str=path_or_str,
        )

        return self

    def create_schema(self, name: str):

        self.execute_query(query="CREATE SCHEMA IF NOT EXISTS {};".format(name))

        return self

    def create_table(self, schema: str, table: str, columns: List[Tuple[str, str]]):
        self.create_schema(name=schema)

        cols = ", ".join([col + " " + dtype for col, dtype in columns])

        self.execute_query(
            query="CREATE TABLE {schema}.{table} ({columns});".format(
                schema=schema, table=table, columns=cols
            )
        )

        return self

    def copy(self, schema: str, table: str, path_or_str: Union[str, bytes]):

        self.execute_query(
            query="COPY {schema}.{table} FROM STDIN DELIMITER ',';".format(
                schema=schema, table=table
            ),
            path_or_str=path_or_str,
        )

        return self
