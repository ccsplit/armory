from armory.database.repositories import (
    IPRepository,
    DomainRepository,
    PortRepository,
    UrlRepository,
)
from armory.included.ModuleTemplate import ToolTemplate
from armory.included.utilities import get_urls
from armory.included.utilities.color_display import display_warning, display
import os
import tempfile
import time


class Module(ToolTemplate):
    """
    This module uses Tomnomnom's Meg to check URLs on the included hosts. The tool can be
    installed from: https://github.com/tomnomnom/meg with `go get -u -v github.com/tomnomnom/meg`

    """

    name = "Meg"
    binary_name = "meg"

    def __init__(self, db):
        self.db = db
        self.IPAddress = IPRepository(db, self.name)
        self.Domain = DomainRepository(db, self.name)
        self.Port = PortRepository(db, self.name)
        self.Url = UrlRepository(db, self.name)

    def set_options(self):
        super(Module, self).set_options()

        self.options.add_argument(
            "-p", "--path", help="Path/File to use for the meg path option."
        )

        self.options.add_argument("-H", "--host", help="Host to check")
        self.options.add_argument("--host_file", help="Import Hosts from file")

        self.options.add_argument(
            "-i",
            "--import_database",
            help="Import URLs from database",
            action="store_true",
        )
        self.options.add_argument(
            "--rescan",
            help="Rescan domains that have already been brute forced",
            action="store_true",
        )
        self.options.set_defaults(timeout=0)  # Disable the default timeout.

    def add_host(self, meg_file, host):
        if "http" in host:
            meg_file.write("{}\n".format(host))
        else:
            meg_file.write("http://{}\n".format(host))
            meg_file.write("https://{}\n".format(host))

    def get_targets(self, args):
        targets = []
        _, fname = tempfile.mkstemp()
        with open(fname, "w") as meg_file:
            if args.host:
                self.add_host(meg_file, args.host)

            if args.host_file:
                if not os.path.exists(args.host_file):
                    print("File: '{}' does not exist".format(args.host_file))
                    exit(1)
                with open(args.host_file) as host_file:
                    for line in host_file:
                        line = line.strip()
                        if line:
                            self.add_host(meg_file, line)

            if args.import_database:
                if args.rescan:
                    for url in get_urls.run(self.db, scope_type="active"):
                        meg_file.write("{}\n".format(url))
                else:
                    for url in get_urls.run(
                        self.db, tool=self.name, scope_type="active"
                    ):
                        meg_file.write("{}\n".format(url))

            if args.output_path[0] == "/":
                output_path = os.path.join(
                    self.base_config["PROJECT"]["base_path"],
                    args.output_path[1:],
                    str(int(time.time())),
                )
            else:
                output_path = os.path.join(
                    self.base_config["PROJECT"]["base_path"],
                    args.output_path,
                    str(int(time.time())),
                )

            if not os.path.exists(output_path):
                os.makedirs(output_path)
        return [{"target": fname, "output": os.path.join(output_path),}]

    def build_cmd(self, args):

        cmd = self.binary
        cmd += " --verbose -s 200 -s 302 -s 301 -s 401"
        cmd += " {}".format(args.path)
        cmd += " {target} {output}"

        if args.tool_args:
            cmd += args.tool_args

        return cmd

    def process_output(self, cmds):
        print("No post processing for Meg.")
        if cmds[0]["target"]:
            os.unlink(cmds[0]["target"])
