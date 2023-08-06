from lets.module import Module
from lets.extensions.docker import DockerExtension

# Imports required to execute this module
from datetime import datetime, timedelta
import tempfile


class Server(DockerExtension, Module):
    """
    Launch a `PoshC2`_ Server, to be used in conjunction with a PoshC2 Implant
    Handler.

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

        parser.add_argument("host",
            help="host to point payloads to (domain or ip)",
            type=str,
            default=None)

        parser.add_argument("-p", "--port",
            help="port to bind listener to",
            type=int,
            default=443)

        parser.add_argument("-k", "--killdate",
            help="date implants should expire - DD/MM/YYYY",
            type=str,
            default=(datetime.now() + timedelta(days=14)).strftime("%d/%m/%Y"))

        parser.add_argument("-s", "--sleep",
            help="sleep between beacons, in seconds",
            type=int,
            default=60)

        parser.add_argument("-j", "--jitter",
            help="jitter percent of sleep",
            type=float,
            default=0.20)

        parser.add_argument("-a", "--useragent",
            help="useragent to use in HTTP headers",
            type=str,
            default="Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko")

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

        config = tempfile.NamedTemporaryFile(dir="/tmp")
        config.write(("""
#!/usr/bin/env python
import os
from UrlConfig import UrlConfig

HOST_NAME = '0.0.0.0'
PORT_NUMBER = %(port)d # This is the bind port

POSHDIR = "/opt/PoshC2_Python/"
ROOTDIR = "/opt/PoshC2_Project/"
HostnameIP = "https://%(host)s"
DomainFrontHeader = "" # example df.azureedge.net
DefaultSleep = "%(sleep)ds"
Jitter = %(jitter)f
KillDate = "%(killdate)s"
UserAgent = "%(useragent)s"
urlConfig = UrlConfig("%%soldurls.txt" %% POSHDIR) # Instantiate UrlConfig object - old urls using a list from a text file
#urlConfig = UrlConfig(wordList="%%swordlist.txt" %% POSHDIR) # Instantiate UrlConfig object - wordlist random url generator
QuickCommand = urlConfig.fetchQCUrl()
DownloadURI = urlConfig.fetchConnUrl()
Sounds = "No"
ServerPort = "%(port)d" # This the port the payload communicates with 
NotificationsProjectName = "PoshC2"
EnableNotifications = "No"
DefaultMigrationProcess = "C:\\\\Windows\\\\system32\\\\netsh.exe" # Used in the PoshXX_migrate.exe payloads

# ClockworkSMS - https://www.clockworksms.com
APIKEY = ""
MobileNumber = '"07777777777","07777777777"'

# Pushover - https://pushover.net/
APIToken = ""
APIUser = ""
URLS = urlConfig.fetchUrls()
SocksURLS = urlConfig.fetchSocks()
Referrer = "" # optional
HTTPResponse = \"\"\"<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache (Debian) Server</address>
</body></html>
\"\"\"
HTTPResponses = [
"STATUS 200",
"OK",
"<html><head></head><body>#RANDOMDATA#</body></html>",
"<html><body>#RANDOMDATA#</body></html>",
\"\"\"<?xml version="1.0" encoding="UTF-8"?>
<heading>#RANDOMDATA#</heading>
<body>#RANDOMDATA#</body>\"\"\",
"<html><head>#RANDOMDATA#</head><body><div>#RANDOMDATA#</div></body></html>"
]
ServerHeader = "Apache"
Insecure = "[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}"

# DO NOT CHANGE #
FilesDirectory = "%%sFiles%%s" %% (POSHDIR, os.sep)
PayloadsDirectory = "%%spayloads%%s" %% (ROOTDIR, os.sep)
ModulesDirectory = "%%sModules%%s" %% (POSHDIR, os.sep)
DownloadsDirectory = "%%sdownloads%%s" %% (ROOTDIR, os.sep)
ReportsDirectory = "%%sreports%%s" %% (ROOTDIR, os.sep)
Database = "%%s%%sPowershellC2.SQLite" %% (ROOTDIR, os.sep)
""" % options).encode())

        config.seek(0)

        # Prepare container with project volume shared with handler
        with self.Container(
            image="local/tools/poshc2:latest",
            network_mode="host",
            stdin_open=True,
            tty=True,
            ports={
                "%(port)d/tcp" % self.options : ("0.0.0.0", self.options.get("port")),
            },
            volumes={
                self.options.get("directory") : {
                    "bind" : "/opt/PoshC2_Project",
                    "mode" : "rw"
                },
                config.name : {
                    "bind" : "/opt/PoshC2_Python/Config.py",
                    "mode" : "ro"
                }
            },
            command="python /opt/PoshC2_Python/C2Server.py") as container:

            # Enter container
            container.interact()

    @DockerExtension.ImageDecorator(["local/tools/poshc2:latest"])
    def test(self):
        """
        Perform unit tests to verify this module's functionality.
        """
