from lets.module import Module
from lets.extensions.docker import DockerExtension


class Pupy(DockerExtension, Module):
    """
    Launch a `Pupy`_ console.

    .. _Pupy:
        https://github.com/n1nj4sec/pupy
    """
    interactive = True
    platforms = ["linux"] # Host networking does not work in VM based docker

    def usage(self) -> object:
        """
        Configure an ArgumentParser object with options relevant to the module.

        :return: ArgumentParser object
        """
        parser = super().usage()

        # Share directory with container, if desired
        parser.add_argument("-d", "--directory",
            help="directory to use as '/project'",
            type=str,
            default=None)

        return parser

    @DockerExtension.ImageDecorator(["local/tools/pupy:latest"])
    def do(self, data:bytes=None, options:dict=None) -> bytes:
        """
        Main functionality.

        Module.do updates self.options with options.

        :param data: Data to be used by module, in bytes
        :param options: Dict of options to be used by module
        :return: Generator containing results of module execution, in bytes
        """
        super().do(data, options)

        volumes = {}

        # Mount directory in container, if specified
        volume = self.options.get("directory")
        if volume:
            volumes[volume] = {
                "bind" : "/project/",
                "mode" : "rw"
            }

        # Prepare container with input file and output file
        # mounted as volumes
        with self.Container(
            image="local/tools/pupy:latest",
            network_mode="host",
            stdin_open=True,
            tty=True,
            volumes=volumes) as container:

            # Enter container
            container.interact()

    @DockerExtension.ImageDecorator(["local/tools/pupy:latest"])
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
