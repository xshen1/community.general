# -*- coding: utf-8 -*-
# Copyright (c) Alexei Znamensky (russoz@gmail.com)
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import json
from ansible_collections.community.general.plugins.modules import opkg as module

import pytest

from .cmd_runner_test_utils import CmdRunnerTestHelper


TESTED_MODULE = module.__name__
with open("tests/unit/plugins/modules/test_opkg.yaml", "r") as TEST_CASES:
    helper = CmdRunnerTestHelper(command="opkg", test_cases=TEST_CASES)
    patch_bin = helper.cmd_fixture


@pytest.mark.parametrize('patch_ansible_module, testcase',
                         helper.testcases_params, ids=helper.testcases_ids,
                         indirect=['patch_ansible_module'])
@pytest.mark.usefixtures('patch_ansible_module')
def test_module(mocker, capfd, patch_bin, testcase):
    """
    Run unit tests for test cases listed in TEST_CASES
    """

    with helper(testcase, mocker) as ctx:
        # Try to run test case
        with pytest.raises(SystemExit):
            module.main()

        out, err = capfd.readouterr()
        results = json.loads(out)

        ctx.check_results(results)
