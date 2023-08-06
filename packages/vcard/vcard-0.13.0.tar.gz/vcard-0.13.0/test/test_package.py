#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import doctest
import os
import unittest
import warnings

from vcard import vcard, vcard_definitions, vcard_errors, vcard_utils, vcard_validator, vcard_validators

TEST_DIRECTORY = os.path.dirname(__file__)


def _get_vcard_file(path):
    """
    Get the vCard contents locally or remotely.

    @param path: File relative to current directory or a URL
    @return: Text in the given file
    """
    if path in ("", None):
        return ""

    filename = os.path.join(TEST_DIRECTORY, path)

    with codecs.open(filename, "r", "utf-8") as file_pointer:
        contents = file_pointer.read()

    return contents


# vCards with errors
VCARDS_CONTINUATION_AT_START = {
    "message": vcard_errors.NOTE_CONTINUATION_AT_START,
    "vcards": ("continuation_at_start.vcf",),
}
VCARDS_DOT_AT_LINE_START = {"message": vcard_errors.NOTE_DOT_AT_LINE_START, "vcards": ("dot_at_line_start.vcf",)}
VCARDS_EMPTY_VCARD = {"message": vcard_errors.NOTE_EMPTY_VCARD, "vcards": ("", None)}
VCARDS_INVALID_DATE = {"message": vcard_errors.NOTE_INVALID_DATE, "vcards": tuple()}
VCARDS_INVALID_LANGUAGE_VALUE = {
    "message": vcard_errors.NOTE_INVALID_LANGUAGE_VALUE,
    "vcards": ("invalid_language_value.vcf",),
}
VCARDS_INVALID_LINE_SEPARATOR = {
    "message": vcard_errors.NOTE_INVALID_LINE_SEPARATOR,
    "vcards": ("line_ending_mac.vcf", "line_ending_unix.vcf", "line_ending_mixed.vcf"),
}
VCARDS_INVALID_PARAM_NAME = {"message": vcard_errors.NOTE_INVALID_PARAMETER_NAME, "vcards": ("invalid_param_name.vcf",)}
VCARDS_INVALID_PARAM_VALUE = {
    "message": vcard_errors.NOTE_INVALID_PARAMETER_VALUE,
    "vcards": ("invalid_param_value.vcf",),
}
VCARDS_INVALID_PROPERTY_NAME = {
    "message": vcard_errors.NOTE_INVALID_PROPERTY_NAME,
    "vcards": ("invalid_property_foo.vcf",),
}
VCARDS_INVALID_SUB_VALUE = {"message": vcard_errors.NOTE_INVALID_SUB_VALUE, "vcards": tuple()}
VCARDS_INVALID_SUB_VALUE_COUNT = {"message": vcard_errors.NOTE_INVALID_SUB_VALUE_COUNT, "vcards": tuple()}
VCARDS_INVALID_TEXT_VALUE = {"message": vcard_errors.NOTE_INVALID_TEXT_VALUE, "vcards": tuple()}
VCARDS_INVALID_TIME = {"message": vcard_errors.NOTE_INVALID_TIME, "vcards": tuple()}
VCARDS_INVALID_TIME_ZONE = {"message": vcard_errors.NOTE_INVALID_TIME_ZONE, "vcards": tuple()}
VCARDS_INVALID_URI = {"message": vcard_errors.NOTE_INVALID_URI, "vcards": tuple()}
VCARDS_INVALID_VALUE = {"message": vcard_errors.NOTE_INVALID_VALUE, "vcards": ("invalid_begin.vcf",)}
VCARDS_INVALID_VALUE_COUNT = {
    "message": vcard_errors.NOTE_INVALID_VALUE_COUNT,
    "vcards": ("invalid_value_count_wp.vcf",),
}
VCARDS_INVALID_X_NAME = {"message": vcard_errors.NOTE_INVALID_X_NAME, "vcards": tuple()}
VCARDS_MISMATCH_GROUP = {"message": vcard_errors.NOTE_MISMATCH_GROUP, "vcards": ("mismatch_group.vcf",)}
VCARDS_MISMATCH_PARAMETER = {"message": vcard_errors.NOTE_MISMATCH_PARAMETER, "vcards": tuple()}
VCARDS_MISSING_GROUP = {"message": vcard_errors.NOTE_MISSING_GROUP, "vcards": ("missing_group.vcf",)}
VCARDS_MISSING_PARAMETER = {"message": vcard_errors.NOTE_MISSING_PARAMETER, "vcards": ("missing_photo_param.vcf",)}
VCARDS_MISSING_PARAM_VALUE = {"message": vcard_errors.NOTE_MISSING_PARAM_VALUE, "vcards": ("missing_param_value.vcf",)}
VCARDS_MISSING_PROPERTY = {
    "message": vcard_errors.NOTE_MISSING_PROPERTY,
    "vcards": (
        "missing_properties.vcf",
        "missing_start.vcf",
        "missing_end.vcf",
        "missing_version.vcf",
        "missing_n.vcf",
        "missing_fn.vcf",
    ),
}
VCARDS_MISSING_VALUE_STRING = {"message": vcard_errors.NOTE_MISSING_VALUE_STRING, "vcards": ("missing_n_value.vcf",)}

VCARDS_WITH_ERROR = (
    VCARDS_CONTINUATION_AT_START,
    VCARDS_DOT_AT_LINE_START,
    VCARDS_EMPTY_VCARD,
    VCARDS_INVALID_DATE,
    VCARDS_INVALID_LANGUAGE_VALUE,
    VCARDS_INVALID_LINE_SEPARATOR,
    VCARDS_INVALID_PARAM_NAME,
    VCARDS_INVALID_PARAM_VALUE,
    VCARDS_INVALID_PROPERTY_NAME,
    VCARDS_INVALID_SUB_VALUE,
    VCARDS_INVALID_SUB_VALUE_COUNT,
    VCARDS_INVALID_TIME,
    VCARDS_INVALID_TIME_ZONE,
    VCARDS_INVALID_URI,
    VCARDS_INVALID_VALUE,
    VCARDS_INVALID_VALUE_COUNT,
    VCARDS_INVALID_X_NAME,
    VCARDS_MISMATCH_GROUP,
    VCARDS_MISMATCH_PARAMETER,
    VCARDS_MISSING_GROUP,
    VCARDS_MISSING_PARAMETER,
    VCARDS_MISSING_PARAM_VALUE,
    VCARDS_MISSING_PROPERTY,
    VCARDS_MISSING_VALUE_STRING,
)

# Reference cards with errors
VCARDS_REFERENCE_ERRORS = (
    # https://tools.ietf.org/html/rfc2426
    "rfc_2426_a.vcf",
    "rfc_2426_b.vcf",
)

# Valid vCards
VCARDS_VALID = ("minimal.vcf", "maximal.vcf", "scrambled_case.vcf")


class TestVCards(unittest.TestCase):
    """Test example vCards"""

    def test_failing(self):
        """vCards with errors"""
        for test_group in VCARDS_WITH_ERROR:
            for vcard_file in test_group["vcards"]:
                vcard_text = _get_vcard_file(vcard_file)
                if vcard_text is None:
                    continue

                try:
                    with warnings.catch_warnings(record=True):
                        vcard_validator.VCard(vcard_text, filename=vcard_file)
                        self.fail("Invalid vCard created:\n{0}".format(vcard_text))
                except vcard_errors.VCardError as error:
                    error_message = "\n\n".join(
                        (
                            "Wrong message for vCard {vcard_file!r}:".format(vcard_file=vcard_file),
                            "Expected: {expected}".format(expected=test_group["message"]),
                            "Got: {got}".format(got=str(error)),
                        )
                    )
                    self.assertTrue(test_group["message"] in str(error), msg=error_message)

    def test_valid(self):
        """Valid (but not necessarily sane) vCards"""
        for vcard_file in VCARDS_VALID:
            vcard_text = _get_vcard_file(vcard_file)
            if vcard_text is None:
                continue

            try:
                with warnings.catch_warnings(record=True):
                    vc_obj = vcard_validator.VCard(vcard_text, filename=vcard_file)
                self.assertNotEqual(vc_obj, None)
            except vcard_errors.VCardError as error:
                error_message = "\n\n".join(
                    (
                        "Expected valid vCard for {vcard_file!r}, but it failed to validate".format(
                            vcard_file=vcard_file
                        ),
                        str(error),
                    )
                )
                self.fail(error_message)

    def test_online(self):
        """vCards in references which are invalid"""
        for vcard_file in VCARDS_REFERENCE_ERRORS:
            vcard_text = _get_vcard_file(vcard_file)
            if vcard_text is None:
                continue

            with warnings.catch_warnings(record=True):
                self.assertRaises(vcard_errors.VCardError, vcard_validator.VCard, vcard_text)

    def test_doc(self):
        """Run DocTests"""
        self.assertEqual(doctest.testmod(vcard)[0], 0)
        self.assertEqual(doctest.testmod(vcard_definitions)[0], 0)
        self.assertEqual(doctest.testmod(vcard_errors)[0], 0)
        self.assertEqual(doctest.testmod(vcard_utils)[0], 0)
        self.assertEqual(doctest.testmod(vcard_validators)[0], 0)
