
"""JUnit XML output handler for Rotest."""
# pylint: disable=protected-access
from __future__ import absolute_import

import os

from xmltodict import unparse
from future.builtins import str

from rotest.core import skip_if_not_main, TestFlow
from rotest.core.result.handlers.abstract_handler import AbstractResultHandler


class XmlHandler(AbstractResultHandler):
    """JUnit XML handler.

    Overrides result handler's method to generate JUnit compatible XML reports
    per test.
    """
    NAME = "xml"

    XML_REPORT_PATH = "result.xml"

    def _create_xml_report(self, test, xml_dict):
        """Save an XML object to the report file in the test's work dir.

        Args:
            test (object): test item instance.
            xml_obj (dict): the xml content's as a dict.
        """
        xml_report_path = os.path.join(test.work_dir,
                                       self.XML_REPORT_PATH)
        with open(xml_report_path, 'wb') as xml_report:
            xml_report.write(unparse(xml_dict, pretty=True))

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
        if isinstance(test, TestFlow):
            test_name = test.data.name
            method_name = TestFlow.TEST_METHOD_NAME

        else:
            test_name, method_name = test.data.name.split(".")

        test_case = {"@classname": test_name,
                     "@name": method_name}
        test_case.update(result_description)

        test_suite = {"testsuite": {"testcase": test_case,
                                    "@errors": str(int(error)),
                                    "@failures": str(int(failure)),
                                    "@name": test_name,
                                    "@tests": "1"}}

        self._create_xml_report(test, test_suite)

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
