from lets.module import Module
from lets.extensions.docker import DockerExtension

# Imports required to execute this module
import random, string


class Empire(DockerExtension, Module):
    """
    Launch a `PowerShell Empire`_ console.

    .. _Powershell Empire:
        https://github.com/EmpireProject/Empire
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
            help="directory to share with container",
            type=str,
            default=None)

        # Specify staging key, for consistency across servers
        parser.add_argument("-k", "--key",
            help="staging key",
            type=str,
            default=None)

        return parser

    @DockerExtension.ImageDecorator(["empireproject/empire:latest"])
    def do(self, data:bytes=None, options:dict=None) -> bytes:
        """
        Main functionality.

        Module.do updates self.options with options.

        :param data: Data to be used by module, in bytes
        :param options: Dict of options to be used by module
        :return: Generator containing results of module execution, in bytes
        """
        super().do(data, options)

        key = self.options.get("key")

        # Create staging key, if not specified
        if not key:
            punctuation = '!#%&()*+,-./:;<=>?@[]^_{|}~'
            key = ''.join(random.sample(string.ascii_letters + string.digits + punctuation, 32))

        self.info("Using staging key: %s" % str(key))
        key = key.encode()

        volumes = {}

        # Mount directory in container, if specified
        volume = self.options.get("directory")
        if volume:
            volumes[volume] = {
                "bind" : volume,
                "mode" : "rw"
            }

        # Prepare container with input file and output file
        # mounted as volumes
        with self.Container(
            image="empireproject/empire:latest",
            network_mode="host",
            stdin_open=True,
            tty=True,
            volumes=volumes,
            environment={
                "STAGING_KEY" : key
            }) as container:

            # Enter container
            container.interact()

    @DockerExtension.ImageDecorator(["empireproject/empire:latest"])
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
