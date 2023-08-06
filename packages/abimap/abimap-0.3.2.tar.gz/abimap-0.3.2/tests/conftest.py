import filecmp
import os
import re
from distutils import dir_util

import pytest
import yaml

from abimap import symver


@pytest.fixture
def datadir(tmpdir, request):
    """
    Fixture responsible for searching a folder with the same name of test
    module in the \'data\' directory and, if available, moving all contents
    to a temporary directory so tests can use them freely.

    :param tmpdir: fixture which creates a temporary directory
    :param request: the test request context
    """

    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    # Get the parent directory and the test module name
    parent_dir = os.path.dirname(test_dir)
    test_name = os.path.basename(test_dir)

    # Insert the "data" to search in the data directory
    data_dir = os.path.join(parent_dir, "data", test_name)

    # If there are data for such test, copy to a temporary directory
    if os.path.isdir(data_dir):
        dir_util.copy_tree(data_dir, str(tmpdir))

    return tmpdir


@pytest.fixture
def testcases(datadir, capsys):
    """
    Returns the test cases for a given test

    :param datadir: fixture which gives a temporary dir with the test files
    :param capsys: fixture which captures the outputs to stderr and stdout
    """

    input_list = datadir.listdir()

    all_tests = []

    # Read the testcases from the YAML files
    for test_input in input_list:
        if os.path.isfile(str(test_input)):
            _, file_type = os.path.splitext(str(test_input))
            if file_type.lower() == ".yml" or file_type.lower() == ".yaml":
                with open(str(test_input), 'r') as stream:
                    try:
                        all_tests.extend(yaml.load(stream,
                                                   Loader=yaml.FullLoader))
                    except yaml.YAMLError as e:
                        with capsys.disabled():
                            print(e)
                        raise e

    return all_tests


class cd:
    """
    Class used to manage the working directory

    Use as context manager::

        with cd(datadir):
            # Here you are in the temporary working directory

    """

    def __init__(self, new_path):
        self.new_path = str(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


def is_warning_in_log(expected, log):
    """
    Search for a warning containing the expected message in the log. Returns
    True if found; False otherwise.

    :param expected: The regular expression
    "param log: The input string
    """

    # Escape possibly existing special characters
    escaped = re.escape(expected)

    regex = "WARNING.*" + escaped

    to_match = re.compile(regex)
    found = to_match.search(log)
    if found:
        return True

    return False


def is_error_in_log(expected, log):
    """
    Search for an error containing the expected message in the log. Returns
    True if found; False otherwise.

    :param expected: The regular expression
    "param log: The input string
    """

    # Escape possibly existing special characters
    escaped = re.escape(expected)

    regex = "ERROR.*" + escaped

    to_match = re.compile(regex)
    found = to_match.search(log)
    if found:
        return True

    return False


def run_tc(tc, datadir, capsys, caplog):
    """
    Run a command test case (for update and new commands)

    :param tc: The tescase
    :param datadir: The path to the directory where the test input are
    :param capsys: The output capture fixture
    :param caplog: The log capture fixture
    """

    class C(object):
        """
        Empty class used as a namespace
        """
        pass

    # Change directory to the temporary directory
    with cd(datadir):
        # Get a parser
        parser = symver.get_arg_parser()

        tc_in = tc["input"]
        tc_out = tc["output"]

        # Add the simulated program name
        ns = C()
        ns.program = 'abimap'

        # Parse the testcase arguments
        args = parser.parse_args(tc_in["args"], namespace=ns)

        # TODO Using args.input to give the input from stdin
        if not args.input:
            if tc_in["stdin"]:
                args.input = tc_in["stdin"]

        # Call the function
        if tc_out["exceptions"]:
            with pytest.raises(Exception) as e:
                args.func(args)
            for expected in tc_out["exceptions"]:
                assert expected in str(e.value)
        else:
            args.func(args)

        # Capture stdout and stderr
        out, err = capsys.readouterr()

        # If there is an expected output file
        if tc_out["file"]:
            if args.out:
                assert filecmp.cmp(args.out, tc_out["file"], shallow=False)
            else:
                with capsys.disabled():
                    print(tc)
                # Fail
                assert 0
        else:
            if args.out:
                if os.path.isfile(args.out):
                    with capsys.disabled():
                        print(tc)
                        print("Unexpected output file created:\n" + args.out)
                    # Fail
                    assert 0

        # If there is an expected output to stdout
        if tc_out["stdout"]:
            with open(tc_out["stdout"], "r") as tcout:
                expected = tcout.read()
                assert out == expected
        else:
            if out:
                with capsys.disabled():
                    print(tc)
                    print("Unexpected output in stdout:\n" + out)
                # Fail
                assert 0

        # Check if the expected warning messages are in the log
        if tc_out["warnings"]:
            for expected in tc_out["warnings"]:
                assert is_warning_in_log(expected, caplog.text)

        # Check if the expected error messages are in the log
        if tc_out["errors"]:
            for expected in tc_out["errors"]:
                assert is_error_in_log(expected, caplog.text)

        # If a log file was supposed to exist, check the content
        if args.logfile:
            if os.path.isfile(args.logfile):
                with open(args.logfile, "r") as log:
                    logged = log.read()
                    if tc_out["warnings"]:
                        for expected in tc_out["warnings"]:
                            assert is_warning_in_log(expected, caplog.text)
                    if tc_out["errors"]:
                        for expected in tc_out["errors"]:
                            assert is_error_in_log(expected, caplog.text)
                    if tc_out["exceptions"]:
                        for expected in tc_out["exceptions"]:
                            assert expected in logged
            else:
                if tc_out["warnings"] or tc_out["exceptions"]:
                    with capsys.disabled():
                        print(tc)
                        print("Expected to have a logfile:\n" + args.logfile)
                    # Fail
                    assert 0

        # Clear the captured log and output so far
        caplog.clear()
