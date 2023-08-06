from lets.module import Module
from lets.extensions.docker import DockerExtension

# Imports required to execute this module
import unittest


class HTTP(DockerExtension, Module):
    """
    Sniff HTTP traffic on the local network.
    """

    def usage(self) -> object:
        """
        Configure an ArgumentParser object with options relevant
        to the module.

        :return: ArgumentParser object
        """
        parser = super().usage()

        # Allow interface customization
        parser.add_argument("-i", "--interface",
            help="interface to listen on",
            type=str,
            default=None)
        parser.add_argument("-p", "--port",
            help="port to listen on",
            type=int,
            default=80)

        return parser

    @DockerExtension.ImageDecorator(["local/linux/tshark:latest"])
    def do(self, data:bytes=None, options:dict=None) -> bytes:
        """
        Main functionality.

        Module.do updates self.options with options.

        :param data: Data to be used by module, in bytes
        :param options: Dict of options to be used by module
        :return: Generator containing results of module execution,
            in bytes
        """
        super().do(data, options)

        # Build command
        cmd = "tshark -Y http -f 'port %(port)d'" % self.options

        # Customize command
        if self.options.get("interface"):
            cmd += " -i %(interface)s" % self.options

        # Start container
        with self.Container(
            image="local/linux/tshark:latest",
            network="host",
            cap_add=[
                "net_raw",
                "net_admin"
            ],
            tty=True,
            command=cmd) as container:

            # Enter container
            container.interact()

    @unittest.skip("Interactive")
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
