from lets.module import Module
from lets.extensions.docker import DockerExtension


class Handler(DockerExtension, Module):
    """
    Launch a `PoshC2`_ Implant Handler, to be used in conjunction with a PoshC2
    Server.

    .. _PoshC2:
        https://poshc2.readthedocs.io/en/latest/
    """
    interactive = True
    platforms = ["linux"] # Host networking does not work in VM based docker

    def usage(self) -> object:
        """
        Configure an ArgumentParser object with options relevant to the module.

        :return: ArgumentParser object
        """
        parser = super().usage()

        # Specify directory to store project data, otherwise will use named volume
        # to synchronize between server and handler
        parser.add_argument("-d", "--directory",
            help="specify directory to store project data",
            type=str,
            default="/tmp/poshc2")

        return parser

    @DockerExtension.ImageDecorator(["local/tools/poshc2:latest"])
    def do(self, data:bytes=None, options:dict=None) -> bytes:
        """
        Main functionality.

        Module.do updates self.options with options.

        :param data: Data to be used by module, in bytes
        :param options: Dict of options to be used by module
        :return: Generator containing results of module execution, in bytes
        """
        super().do(data, options)

        # Prepare container with project volume shared with server
        with self.Container(
            image="local/tools/poshc2:latest",
            network_disabled=True,
            stdin_open=True,
            tty=True,
            volumes={
                self.options.get("directory") : {
                    "bind" : "/opt/PoshC2_Project",
                    "mode" : "rw"
                }
            },
            command="python /opt/PoshC2_Python/ImplantHandler.py") as container:

            # Enter container
            container.interact()

    @DockerExtension.ImageDecorator(["local/tools/poshc2:latest"])
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
