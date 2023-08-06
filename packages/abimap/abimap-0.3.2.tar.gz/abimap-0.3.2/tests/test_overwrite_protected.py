# -*- coding: utf-8 -*-

import os
from stat import S_IRGRP
from stat import S_IROTH
from stat import S_IRUSR

import pytest
from conftest import run_tc


# Special case that need setup first
@pytest.mark.skipif(pytest.__version__ < '3.4', reason="caplog not supported")
def test_overwrite_protected(testcases, datadir, capsys, caplog):

    protected = os.path.join(str(datadir), "overwrite_protected.in.old")

    # Change permission to be read only
    os.chmod(protected, S_IRUSR | S_IRGRP | S_IROTH)

    for tc in testcases:
        run_tc(tc, datadir, capsys, caplog)
