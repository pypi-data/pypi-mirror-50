from __future__ import print_function

from delfick_logging import setup_logging, setup_logging_theme
from delfick_error import DelfickError, UserQuit
import logging.handlers
import subprocess
import argparse
import logging
import signal
import shlex
import time
import six
import sys
import os

log = logging.getLogger("delfick_app")

class Ignore(object):
    pass

class BadOption(DelfickError):
    desc = "Bad option"

class CouldntKill(DelfickError):
    desc = "Bad process"

class ArgumentError(DelfickError):
    desc = "Bad cli argument"

########################
###   APP
########################

class App(object):
    """
    .. automethod:: main

    ``Attributes``

        .. autoattribute:: VERSION

            The version of your application, best way is to define this somewhere
            and import it into your mainline and setup.py from that location

        .. autoattribute:: CliParserKls

            The class to use for our CliParser

        .. autoattribute:: logging_handler_file

            The file to log output to (default is stderr)

        .. autoattribute:: boto_useragent_name

            The name to append to your boto useragent if that's a thing you want
            to happen

        .. autoattribute:: cli_categories

            self.execute is passed a dictionary args_dict which is from looking
            at the args_obj object returned by argparse

            This option will break up arguments into hierarchies based on the
            name of the argument.

            For example:

            ``cli_categories = ['app']``

            and we have arguments for
            ``[silent, verbose, debug, app_config, app_option1, app_option2]``

            Then args_dict will be:

            .. code-block:: json

                { "app": {"config": value, "option1": value, "option2": value}
                , "silent": value, "verbose": value, "debug": value
                }

        .. autoattribute:: cli_description

            The description to give at the top of --help output

        .. autoattribute:: cli_environment_defaults

            A map of environment variables to --argument that you want to map

            For example:

            ``cli_environment_defaults = {"APP_CONFIG": "--config"}``

            Items may also be a tuple of ``(replacement, default)``

            For example, ``{"APP_CONFIG": ("--config", "./config.yml")}``

            Which means ``defaults["--config"] == {'default': "./config.yml"}``
            if APP_CONFIG isn't in the environment.

        .. autoattribute:: cli_positional_replacements

            A list mapping positional arguments to --arguments

            For example:

            ``cli_positional_replacements = ['--environment', '--stack']``
                Will mean the first positional argument becomes the value for
                --environment and the second positional becomes the value for
                '--stack'

                Note for this to work, you must do something like:

                .. code-block:: python

                    def setup_other_args(self, parser, defaults):
                        parser.add_argument('--environment'
                            , help = "the environment!"
                            , **defaults['--environment']
                            )

            Items in positional_replacements may also be a tuple of
            ``(replacement, default)``

            For example:

            ``cli_positional_replacements = [('--task', 'list_tasks')]``
                will mean the first positional argument becomes the value for
                --task

                But if it's not specified, then
                ``defaults['--task'] == {"default": "list_tasks"}``

        .. autoattribute:: issue_tracker_link

            A link to where users can go to post issues

            It is used when we get an unexpected exception.

    ``Hooks``

        .. automethod:: execute

        .. automethod:: setup_other_logging

        .. automethod:: specify_other_args

        .. automethod:: exception_handler
    """

    ########################
    ###   SETTABLE PROPERTIES
    ########################

    VERSION = Ignore
    issue_tracker_link = None
    boto_useragent_name = Ignore

    CliParserKls = property(lambda s: CliParser)
    logging_handler_file = property(lambda s: sys.stderr)

    cli_categories = None
    cli_description = "My amazing app"
    cli_environment_defaults = None
    cli_positional_replacements = None

    ########################
    ###   USAGE
    ########################

    @classmethod
    def main(kls, argv=None, **execute_args):
        """
        Instantiates this class and calls the mainline

        Usage is intended to be:

        .. code-block:: python

            from delfick_app import App

            class MyApp(App):
                [..]

            main = MyApp.main
        """
        app = kls()
        app.mainline(argv, **execute_args)

    def execute(self, args_obj, args_dict, extra_args, logging_handler):
        """Hook for executing the application itself"""
        raise NotImplementedError()

    def setup_other_logging(self, args_obj, verbose=False, silent=False, debug=False):
        """
        Hook for setting up any other logging configuration

        For example:

        .. code-block:: python

            def setup_other_logging(self, args_obj, verbose, silent, debug):
                logging.getLogger("boto").setLevel([logging.CRITICAL, logging.ERROR][verbose or debug])
                logging.getLogger("requests").setLevel([logging.CRITICAL, logging.ERROR][verbose or debug])
                logging.getLogger("paramiko.transport").setLevel([logging.CRITICAL, logging.ERROR][verbose or debug])
        """

    def specify_other_args(self, parser, defaults):
        """
        Hook for adding more arguments to the argparse Parser

        For example:

        .. code-block:: python

            def specify_other_args(self, parser, defaults):
                parser.add_argument("--special"
                    , help = "taste the rainbow"
                    , action = "store_true"
                    )
        """

    ########################
    ###   INTERNALS
    ########################

    def set_boto_useragent(self):
        """Make boto report this application as the user agent"""
        if self.boto_useragent_name is not Ignore and self.VERSION is not Ignore:
            __import__("boto")
            useragent = sys.modules["boto.connection"].UserAgent
            if self.boto_useragent_name not in useragent:
                sys.modules["boto.connection"].UserAgent = "{0} {1}/{2}".format(useragent, self.boto_useragent_name, self.VERSION)

    def mainline(self, argv=None, print_errors_to=sys.stdout, **execute_args):
        """
        The mainline for the application

        * Initialize parser and parse argv
        * Initialize the logging
        * run self.execute()
        * Catch and display DelfickError
        * Display traceback if we catch an error and args_obj.debug
        """
        cli_parser = None
        args_obj, args_dict, extra_args = None, None, None
        try:
            cli_parser = self.make_cli_parser()
            try:
                args_obj, args_dict, extra_args = cli_parser.interpret_args(argv, self.cli_categories)
                if args_obj.version:
                    print(self.VERSION)
                    return

                handler = self.setup_logging(args_obj)
                self.set_boto_useragent()
                self.execute(args_obj, args_dict, extra_args, handler, **execute_args)
            except KeyboardInterrupt:
                if cli_parser and cli_parser.parse_args(argv)[0].debug:
                    raise
                raise UserQuit()
            except:
                self.exception_handler(sys.exc_info(), args_obj, args_dict, extra_args)
                raise
        except DelfickError as error:
            print("", file=print_errors_to)
            print("!" * 80, file=print_errors_to)
            print("Something went wrong! -- {0}".format(error.__class__.__name__), file=print_errors_to)
            print("\t{0}".format(error), file=print_errors_to)
            if cli_parser and cli_parser.parse_args(argv)[0].debug:
                raise
            sys.exit(1)
        except Exception:
            msg = "Something unexpected happened!! Please file a ticket in the issue tracker! {0}".format(self.issue_tracker_link)
            print("\n\n{0}\n{1}\n".format(msg, '=' * len(msg)))
            raise

    def exception_handler(self, exc_info, args_obj, args_dict, extra_args):
        """Handler for doing things like bugsnag"""

    def setup_logging(self, args_obj, log=None, only_message=False):
        """Setup the handler for the logs and call setup_other_logging"""
        level = [logging.INFO, logging.DEBUG][args_obj.verbose or args_obj.debug]
        if args_obj.silent:
            level = logging.ERROR

        handler = setup_logging(
              log = log
            , level = level
            , program = args_obj.logging_program
            , syslog_address = args_obj.syslog_address
            , udp_address = args_obj.udp_logging_address
            , tcp_address = args_obj.tcp_logging_address
            , only_message = only_message
            , logging_handler_file = self.logging_handler_file
            , json_to_console = args_obj.json_console_logs
            )

        self.setup_other_logging(args_obj, args_obj.verbose, args_obj.silent, args_obj.debug)
        return handler

    def setup_logging_theme(self, handler, colors="light"):
        """Setup a logging theme"""
        return setup_logging_theme(handler, colors=colors)

    def make_cli_parser(self):
        """Return a CliParser instance"""
        properties = {"specify_other_args": self.specify_other_args}
        kls = type("CliParser", (self.CliParserKls, ), properties)
        return kls(self.cli_description, self.cli_positional_replacements, self.cli_environment_defaults)

########################
###   CliParser
########################

class CliParser(object):
    """Knows what argv looks like"""
    def __init__(self, description, positional_replacements=None, environment_defaults=None):
        self.description = description
        self.positional_replacements = positional_replacements
        if self.positional_replacements is None:
            self.positional_replacements = []

        self.environment_defaults = environment_defaults
        if self.environment_defaults is None:
            self.environment_defaults = {}

    def specify_other_args(self, parser, defaults):
        """Hook to specify more arguments"""

    def interpret_args(self, argv, categories=None):
        """
        Parse argv and return (args_obj, args_dict, extra)

        Where args_obj is the object return by argparse
        extra is all the arguments after a --
        and args_dict is a dictionary representation of the args_obj object
        """
        if categories is None:
            categories = []
        args_obj, extra = self.parse_args(argv)

        args_dict = {}
        for category in categories:
            args_dict[category] = {}
        for key, val in sorted(vars(args_obj).items()):
            found = False
            for category in categories:
                if key.startswith("{0}_".format(category)):
                    args_dict[category][key[(len(category) + 1):]] = val
                    found = True
                    break

            if not found:
                args_dict[key] = val

        return args_obj, args_dict, extra

    def parse_args(self, argv=None):
        """
        Build up an ArgumentParser and parse our argv!

        Also complain if any --argument is both specified explicitly and as a positional
        """
        if argv is None:
            argv = sys.argv[1:]
        args, other_args, defaults = self.split_args(argv)
        parser = self.make_parser(defaults)
        parsed = parser.parse_args(args)
        self.check_args(argv, defaults, self.positional_replacements)
        return parsed, other_args

    def check_args(self, argv, defaults, positional_replacements):
        """Check that we haven't specified an arg as positional and a --flag"""
        num_positionals = 0
        args = []
        for thing in argv:
            if thing == "--":
                break
            if thing.startswith("-"):
                args.append(thing)
            elif not args:
                num_positionals += 1

        for index, replacement in enumerate(positional_replacements):
            if type(replacement) is tuple:
                replacement, _ = replacement
            if index < num_positionals and "default" in defaults.get(replacement, {}) and replacement in args:
                raise BadOption("Please don't specify an option as a positional argument and as a --flag", argument=replacement, position=index + 1)

    def split_args(self, argv):
        """
        Split up argv into args, other_args and defaults

        Other args is anything after a "--" and args is everything before a "--"
        """
        if argv is None:
            argv = sys.argv[1:]

        args = []
        argv = list(argv)
        extras = None

        while argv:
            nxt = argv.pop(0)
            if extras is not None:
                extras.append(nxt)
            elif nxt == "--":
                extras = []
            else:
                args.append(nxt)

        other_args = ""
        if extras:
            other_args = " ".join(extras)

        defaults = self.make_defaults(args, self.positional_replacements, self.environment_defaults)
        return args, other_args, defaults

    def make_defaults(self, argv, positional_replacements, environment_defaults):
        """
        Make and return a dictionary of {--flag: {"default": value}}

        This method will also remove the positional arguments from argv
        that map to positional_replacements.

        Defaults are populated from mapping environment_defaults to --arguments
        and mapping positional_replacements to --arguments

        So if positional_replacements is [--stack] and argv is ["blah", "--stuff", 1]
        defaults will equal {"--stack": {"default": "blah"}}

        If environment_defaults is {"CONFIG_LOCATION": "--config"}
        and os.environ["CONFIG_LOCATION"] = "/a/path/to/somewhere.yml"
        then defaults will equal {"--config": {"default": "/a/path/to/somewhere.yml"}}

        Positional arguments will override environment defaults.
        """
        defaults = {}

        class Ignore(object): pass

        for env_name, replacement in environment_defaults.items():
            default = Ignore
            if type(replacement) is tuple:
                replacement, default = replacement

            if env_name in os.environ:
                defaults[replacement] = {"default": os.environ[env_name]}
            else:
                if default is Ignore:
                    defaults[replacement] = {}
                else:
                    defaults[replacement] = {"default": default}

        for replacement in positional_replacements:
            if type(replacement) is tuple:
                replacement, _ = replacement
            if argv and not argv[0].startswith("-"):
                defaults[replacement] = {"default": argv[0]}
                argv.pop(0)
            else:
                break

        for replacement in positional_replacements:
            default = Ignore
            if type(replacement) is tuple:
                replacement, default = replacement
            if replacement not in defaults:
                if default is Ignore:
                    defaults[replacement] = {}
                else:
                    defaults[replacement] = {"default": default}

        return defaults

    def make_parser(self, defaults):
        """Create an argparse ArgumentParser, setup --verbose, --silent, --debug and call specify_other_args"""
        parser = argparse.ArgumentParser(description=self.description)

        logging = parser.add_mutually_exclusive_group()
        logging.add_argument("--verbose"
            , help = "Enable debug logging"
            , action = "store_true"
            )

        if "default" in defaults.get("--silent", {}):
            kwargs = defaults["--silent"]
        else:
            kwargs = {"action": "store_true"}
        logging.add_argument("--silent"
            , help = "Only log errors"
            , **kwargs
            )

        logging.add_argument("--debug"
            , help = "Debug logs"
            , action = "store_true"
            )

        logging.add_argument("--logging-program"
            , help = "The program name to use when not logging to the console"
            )

        parser.add_argument("--tcp-logging-address"
            , help = "The address to use for giving log messages to tcp (i.e. localhost:9001)"
            , default = ""
            )

        parser.add_argument("--udp-logging-address"
            , help = "The address to use for giving log messages to udp (i.e. localhost:9001)"
            , default = ""
            )

        parser.add_argument("--syslog-address"
            , help = "The address to use for syslog (i.e. /dev/log)"
            , default = ""
            )

        parser.add_argument("--json-console-logs"
            , help = "If we haven't set other logging arguments, this will mean we log json lines to the console"
            , action = "store_true"
            )

        parser.add_argument("--version"
            , help = "Print out the version!"
            , action = "store_true"
            )

        self.specify_other_args(parser, defaults)
        return parser

########################
###   ARGPARSE
########################

class DelayedFileType(object):
    """
    Argparse in python2.6 is silly and tries to open the default

    So, to get around this, we create an argparse type that returns a function.

    Thus delaying opening the file until we have the value that is specified by the commandline::

        parser = argparse.ArgumentParser(description="My amazing application")
        parser.add_argument("--config"
            , help = "Config file for my amazing application"
            , default = "./fileThatDoesntNecesarilyExist.yml"
            , type = delfick_app.DelayedFileType('r')
            )

        args_obj = parser.parse_args(["--config", "./fileThatExists.yml"])
        config = args_obj.config()
    """
    def __init__(self, mode):
        self.mode = mode

    def __call__(self, location):
        if hasattr(location, "read") and hasattr(location, "close"):
            return lambda: location
        else:
            def opener(optional=False):
                if optional and not os.path.exists(location):
                    return None

                try:
                    return argparse.FileType(self.mode)(location)
                except IOError as error:
                    error_str = str(error)
                    suffix = ": '{0}'".format(location)
                    if error_str.endswith(suffix):
                        error_str = error_str[:-len(suffix)]
                    raise ArgumentError("Failed to open the file", error=error_str, location=location)
                except argparse.ArgumentTypeError as error:
                    error_str = str(error)
                    prefix = "can't open '{0}': ".format(location)
                    suffix = ": '{0}'".format(location)
                    if error_str.startswith(prefix):
                        error_str = error_str[len(prefix):]
                    if error_str.endswith(suffix):
                        error_str = error_str[:-len(suffix)]
                    raise ArgumentError("Failed to open the file", error=error_str, location=location)
            return opener

########################
###   PROCESSES
########################

def read_non_blocking(stream):
    """Read from a non-blocking stream"""
    if stream:
        while True:
            nxt = b''
            empty = 0
            while not nxt.decode('utf-8').endswith("\n"):
                try:
                    read = stream.readline()
                    if len(read) == 0:
                        if empty < 3:
                            time.sleep(0.01)
                        else:
                            break
                        empty += 1
                    nxt += read
                except IOError as error:
                    if error.errno in (11, 35):
                        # Resource temporarily unavailable
                        if empty < 3:
                            time.sleep(0.01)
                        else:
                            break
                        empty += 1
                    else:
                        raise

            if nxt:
                yield nxt
            else:
                break

def set_non_blocking_io(fh):
    if sys.platform in ['win32']:
        # TODO: windows magic
        raise NotImplementedError("Non-blocking process I/O not implemented on {}".format(sys.platform))
    else:
        import fcntl
        fl = fcntl.fcntl(fh, fcntl.F_GETFL)
        fcntl.fcntl(fh, fcntl.F_SETFL, fl | os.O_NONBLOCK)

def command_output(command, *command_extras, **kwargs):
    """
    Get the output from a command

    Does so in a non blocking fashion and will ensure that the process ends.

    Keyword arguments are:

    timeout
        Defaults to 10, if the process isn't over by this timeout, it will be sent a SIGTERM

        If that doesn't kill it, a SIGKILL is sent to it

    verbose
        Defaults to False and makes the command a bit more verbose

    stdin
        Defaults to None. If specified, it is sent to the process as stdin

    Command is split with shlex.split and is prepended to command_extras to create the command for the process

    The return of this command is (output, status) where output is the stderr and stdout of the process
    and status is the exit code of the process.
    """
    output = []
    cwd = kwargs.get("cwd", None)
    if isinstance(command, six.string_types):
        args = shlex.split(' '.join([command] + list(command_extras)))
    else:
        args = command + shlex.split(' '.join(list(command_extras)))
    stdin = kwargs.get("stdin", None)
    timeout = kwargs.get("timeout", 10)
    verbose = kwargs.get("verbose", False)

    log_level = log.info if verbose else log.debug
    log_level("Running command\targs=%s", args)

    process_kwargs = {"stderr": subprocess.STDOUT, "stdout": subprocess.PIPE, "cwd": cwd}
    if stdin is not None:
        process_kwargs["stdin"] = stdin
    process = subprocess.Popen(args, **process_kwargs)

    set_non_blocking_io(process.stdout)

    start = time.time()
    while True:
        if time.time() - start > timeout:
            break
        if process.poll() is not None:
            break
        for nxt in read_non_blocking(process.stdout):
            output.append(nxt.decode("utf8").strip())
            if verbose:
                print(output[-1])
        time.sleep(0.01)

    attempted_sigkill = False
    if process.poll() is None:
        start = time.time()
        log.error("Command taking longer than timeout (%s). Terminating now\tcommand=%s", timeout, args)
        process.terminate()

        while True:
            if time.time() - start > timeout:
                break
            if process.poll() is not None:
                break
            for nxt in read_non_blocking(process.stdout):
                output.append(nxt.decode("utf8").strip())
                if verbose:
                    print(output[-1])
            time.sleep(0.01)

        if process.poll() is None:
            log.error("Command took another %s seconds after terminate, so sigkilling it now", timeout)
            os.kill(process.pid, signal.SIGKILL)
            attempted_sigkill = True

    for nxt in read_non_blocking(process.stdout):
        output.append(nxt.decode("utf8").strip())
        if verbose:
            print(output[-1])

    if attempted_sigkill:
        time.sleep(0.01)
        if process.poll() is None:
            raise CouldntKill("Failed to sigkill hanging process", pid=process.pid, command=args, output="\n".join(output))

    if process.poll() != 0:
        log.error("Failed to run command\tcommand=%s", args)

    for nxt in read_non_blocking(process.stdout):
        nxt_out = nxt.decode("utf8").strip()
        output.append(nxt_out)
        if verbose:
            print(nxt_out)

    return output, process.poll()
