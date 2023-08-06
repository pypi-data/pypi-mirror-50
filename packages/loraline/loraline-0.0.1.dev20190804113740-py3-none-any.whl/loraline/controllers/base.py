""" Loraline LoRaWAN command-line toolkit for interfacing with RN2483 and RN2903 transceivers """
import sys
import distro
from cement import Controller, ex
from cement.utils.shell import Prompt
from ..core.version import get_version

VERSION_BANNER = """
Loraline Command-Line Toolkit

Version: {version}
Platform: {platform}
Distribution: {distribution}
Framework: {framework}
""".format(
    version=get_version(),
    platform=sys.platform,
    distribution=' '.join(distro.linux_distribution()),
    framework="Cement 3.0.4")

INTRO = """
    #----[ Welcome to Loraline Command-Line Toolkit ]----#

    This toolkit can be used to configure the LoRaWAN
    trasceivers, RN2483 and RN2903, by installing custom
    or built-in profiles by using the "config" command.
    The "connect" command can be used to connect a host
    device (either local machine or microcontroller) to
    the trasceivers.

Author: Alexandros Antoniades
Version: {version}
Github: https://github.com/alexantoniades/
Repository: https://github.com/alexantoniades/loraline/
License: Apache 2.0

{help}

""".format(version="0.1", help="For help type: loraline --help")

class Base(Controller):
    """ Base class for controller default functionality """
    class Meta:
        """ Meta class for base controller """
        label = 'base'

        # text displayed at the top of --help output
        description = INTRO.format(help=None)

        # text displayed at the bottom of --help output
        epilog = 'Usage: loraline [module] --argument (optional)'

        # controller level arguments. ex: 'loraline --version'
        arguments = [
            (['-v', '--version'], {
                'action'  : 'version',
                'version' : VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""
        print(INTRO)
        #self.app.args.print_help()

    @ex(
        help='Configure transceiver mode',
        arguments=[
            (['--mode'], {
                'help': 'Select mode to configure',
                'action': 'store',
                'dest': 'mode'})
        ]
    )
    def config(self):
        """Configure transceiver mode"""

        if self.app.pargs.mode is not None:
            mode = self.app.pargs.mode
        else:
            mode = Prompt(
                "Select a mode:",
                options=['lorawan', 'lora', 'p2p'],
                numbered=True).input

        print(mode)

    @ex(
        help='Connect trasceiver to host',
        arguments=[
            (['--host'], {
                'help': 'Select host to bind',
                'action': 'store',
                'dest': 'host'})
        ]
    )
    def connect(self):
        """Connect trasceiver to host"""
        if self.app.pargs.host is not None:
            host = self.app.pargs.host
        else:
            host = Prompt(
                "Select a host:",
                options=['raspberrypi', 'esp32', 'esp8266', 'pyboard'],
                numbered=True).input

        print(host)
