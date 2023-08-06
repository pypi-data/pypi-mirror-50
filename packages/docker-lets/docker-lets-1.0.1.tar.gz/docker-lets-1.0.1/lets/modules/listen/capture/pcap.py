from lets.module import Module
from lets.extensions.docker import DockerExtension

# Imports required to execute this module
import unittest


class PCAP(DockerExtension, Module):
    """
    Sniff and capture traffic on the local network.
    """

    def usage(self) -> object:
        """
        Configure an ArgumentParser object with options relevant
        to the module.

        :return: ArgumentParser object
        """
        parser = super().usage()

        # Enable convert before encode
        # parser.add_argument("-u", "--upper",
        #     help="convert to uppercase before encoding",
        #     action="store_true",
        #     default=False)

        return parser

    @DockerExtension.ImageDecorator(["local/linux/tcpdump:latest"])
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

        # Validate input
        # try:
        #     assert data, "Expecting data"
        # except AssertionError as e:
        #     self.throw(e)

        # Convert, if necessary
        # if self.options.get("upper"):
        #     try:
        #         self.info("Converting to uppercase")
        #         data = data.decode().upper().encode()
        #     except UnicodeDecodeError as e:
        #         self.throw(e)

        # Build command
        # cmd = "tcpdump -nnvvXSs 1514 -w /data/out"
        cmd = "tcpdump -nnvvXSs 1514 -w /tmp/pcap"
        # cmd = "chown root:root /data/out"

        # Prepare input and output files
        with self.IO(outfile="/data/out") as io:

            # Start container
            with self.Container(
                image="local/linux/tcpdump:latest",
                # privileged=True,
                network="host",
                cap_add=[
                    "net_raw",
                    "net_admin"
                ],
                user="root",
                # stdin_open=True,
                # tty=True,
                volumes=io.volumes,
                command=cmd
                ) as container:

                # Handle container stdout and stderr
                for line in container.logs(
                    stdout=True, stderr=True):
                    self.info(line.strip().decode(), decorate=False)
                # container.interact()

                # Handle data written to output file
                container.wait()
                yield io.outfile.read()

    # @unittest.expectedFailure("Broken module")
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
        self.assertTrue(False, "Cannot write to /data/out while privileged...")
        # raise(AssertionError("Cannot write to /data/out while privileged..."))
        # # Test generic
        # self.assertEqual(
        #     b"".join(self.do(b"abcd", {"upper" : False})),
        #     b"YWJjZA==",
        #     "Defaults produced inaccurate results")

        # # Test with uppercase conversion
        # self.assertEqual(
        #     b"".join(self.do(b"abcd", {"upper" : True})),
        #     b"QUJDRA==",
        #     "Uppercase produced inaccurate results")
