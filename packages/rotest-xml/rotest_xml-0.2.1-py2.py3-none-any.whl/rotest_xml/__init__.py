
"""JUnit XML output handler for Rotest."""
# pylint: disable=protected-access
from __future__ import absolute_import

import os

from xmltodict import unparse
from future.builtins import str

from rotest.core import skip_if_not_main
from rotest.core.result.handlers.abstract_handler import AbstractResultHandler


class XmlHandler(AbstractResultHandler):
    """JUnit XML handler.

    Overrides result handler's method to generate JUnit compatible XML reports
    per test.
    """
    NAME = "xml"

    XML_REPORT_PATH = "result.xml"

    def __init__(self, *args, **kwargs):
        super(XmlHandler, self).__init__(*args, **kwargs)

        self.all_results = []
        self.error_count = 0
        self.fail_count = 0

    def _create_xml_report(self):
        """Save an XML object to the report file in the work dir."""
        test_suite = {"testsuite": {"testcase": self.all_results,
                                    "@errors": str(self.error_count),
                                    "@failures": str(self.fail_count),
                                    "@name": self.main_test.data.name,
                                    "@tests": str(len(self.all_results))}}
        xml_report_path = os.path.join(self.main_test.work_dir,
                                       self.XML_REPORT_PATH)
        with open(xml_report_path, 'wt') as xml_report:
            xml_report.write(unparse(test_suite, pretty=True))

    def _add_test_report(self, test, result_description,
                         error=False, failure=False):
        """Generate an XML report for the given test in its work directory.

        Args:
            test (object): test item instance.
            result_description (lxml.builder.E / str): result description
                (e.g. E.result() / "result").
            error (bool): whether the test result is considered an Error.
            failure (bool): whether the test result is considered a Failure.
        """
        test_case = {"@classname": test.__class__.__name__,
                     "@name": test.data.name}

        test_case.update(result_description)
        self.all_results.append(test_case)
        if error:
            self.error_count += 1

        if failure:
            self.fail_count += 1

        self._create_xml_report()

    @skip_if_not_main
    def add_success(self, test):
        """Called when a test has completed successfully.

        Args:
            test (object): test item instance.
        """
        self._add_test_report(test, {})

    @skip_if_not_main
    def add_skip(self, test, reason):
        """Called when a test is skipped.

        Args:
            test (object): test item instance.
            reason (str): skip reason description.
        """
        skipped = {"skipped": reason}
        self._add_test_report(test, result_description=skipped)

    @skip_if_not_main
    def add_failure(self, test, exception_string):
        """Called when a failure has occurred.

        Args:
            test (object): test item instance.
            exception_string (str): exception traceback string.
        """
        failure = {"failure": exception_string}
        self._add_test_report(test, result_description=failure,
                              error=False, failure=True)

    @skip_if_not_main
    def add_expected_failure(self, test, exception_string):
        """Called when an expected failure has occurred.

        The expected failure is considered as success.

        Args:
            test (object): test item instance.
            exception_string (str): exception traceback string.
        """
        self._add_test_report(test, result_description=exception_string)

    @skip_if_not_main
    def add_error(self, test, exception_string):
        """Called when an error occurred.

        Args:
            test (object): test item instance.
            exception_string (str): exception traceback string.
        """
        error = {"error": exception_string}
        self._add_test_report(test, result_description=error,
                              error=True, failure=False)

    @skip_if_not_main
    def add_unexpected_success(self, test):
        """Called when a test was expected to fail, but succeed.

        The unexpected success is considered as failure.

        Args:
            test (object): test item instance.
        """
        failure = {"failure": "Unexpected Success"}
        self._add_test_report(test, result_description=failure,
                              error=False, failure=True)
