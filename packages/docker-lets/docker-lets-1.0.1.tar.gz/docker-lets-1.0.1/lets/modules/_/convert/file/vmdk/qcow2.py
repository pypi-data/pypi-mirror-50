from lets.module import Module
from lets.extensions.docker import DockerExtension
from lets.utility import TEMP_DIRECTORY

class Qcow2(DockerExtension, Module):
    """
    Convert a vmdk file to a qcow2 file. Useful for converting an image used
    in VirtualBox to one used in qemu.
    """

    def usage(self) -> object:
        """
        Configure an ArgumentParser object with options relevant to the module.

        :return: ArgumentParser object
        """
        parser = super().usage()

        return parser

    @DockerExtension.ImageDecorator(["bannsec/pyrebox:latest"])
    def do(self, data:bytes=None, options:dict=None) -> bytes:
        """
        Main functionality.

        Module.do updates self.options with options.

        :param data: Data to be used by module, in bytes
        :param options: Dict of options to be used by module
        :return: Generator containing results of module execution, in bytes
        """
        super().do(data, options)

        # Validate input
        try:
            assert data, "Expecting file contents"
        except AssertionError as e:
            self.throw(e)

        cmd = "-c './qemu/qemu-img convert -f vmdk -O qcow2 /data/in.vmdk /data/out.qcow2'"

        # Prepare input and output files
        with self.IO(data, infile="/data/in.vmdk", outfile="/data/out.qcow2") as io:

            # Prepare container with input file and output file
            # mounted as volumes
            with self.Container(
                image="bannsec/pyrebox:latest",
                network_disabled=True,
                volumes=io.volumes,
                command=cmd) as container:

                # Handle container stdout and stderr
                for line in container.logs(stdout=True, stderr=True):
                    self.info(line.strip().decode(), decorate=False)

                # Handle data written to output file
                container.wait()
                yield io.outfile.read()

    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
