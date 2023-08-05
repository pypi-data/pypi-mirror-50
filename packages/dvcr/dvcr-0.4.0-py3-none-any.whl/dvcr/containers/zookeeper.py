from typing import Optional

from dvcr.containers.base import BaseContainer
from dvcr.network import Network


class Zookeeper(BaseContainer):
    def __init__(
        self,
        repo: str = "confluentinc/cp-zookeeper",
        tag: str = "latest",
        port: int = 2181,
        name: str = "zookeeper",
        network: Optional[Network] = None,
    ):
        """

        :param repo:
        :param tag:
        :param port:
        :param name:
        :param network:
        """
        super(Zookeeper, self).__init__(
            port=port, repo=repo, tag=tag, name=name, network=network
        )

        self.port = port

        self._container = self._client.containers.run(
            image=repo + ":" + tag,
            environment={
                "ZOOKEEPER_CLIENT_PORT": port,
                "ZOOKEEPER_TICK_TIME": 2000,
            },
            detach=True,
            hostname=name,
            healthcheck={
                "test": ["CMD", "echo", "ruok", "|", "nc", name, "2181"],
                "interval": 1000000000,
            },
            name=name,
            network=self._network.name,
        )
