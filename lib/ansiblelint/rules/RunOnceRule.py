
# Copyright (c) 2020 Sorin Sbarnea <sorin.sbarnea@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys

from ansiblelint.rules import AnsibleLintRule


class RunOnceRule(AnsibleLintRule):
    """RunOnceRule Class."""

    id = "107"
    shortdesc = "Unpredictable run_once"
    description = (
        "Use of run_once does not work with free execution strategy. "
        "Avoid it, or use noqa comments to ignore it.")
    severity = 'MEDIUM'
    tags = ['deprecated']
    version_added = 'v4.4.0'

    def matchtask(self, file, task):
        return 'run_once' in task


EXAMPLE_PLAYBOOK = """
- hosts: localhost
  strategy: free
  tasks:

    - name: task that mathes
      command: touch /tmp/foo
      run_once: true

    - name: task that does not match
      command: touch /tmp/foo
      run_once: true  # noqa 107
"""


if "pytest" in sys.modules:

    import pytest

    @pytest.mark.parametrize('rule_runner', (RunOnceRule, ), indirect=['rule_runner'])
    def test_107(rule_runner):
        """Test rule matches."""
        results = rule_runner.run_playbook(EXAMPLE_PLAYBOOK)
        assert len(results) == 1
        assert isinstance(results[0].rule, RunOnceRule)
        assert results[0].linenumber == 6
