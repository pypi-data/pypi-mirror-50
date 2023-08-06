#!/usr/bin/env python3

import unittest
import subprocess
import os
import shutil
import sys
import pkgutil


def call(arguments, env=os.environ.copy()):
    """
    return a triple with (returncode, stdout, stderr) from the call to subprocess
    """
    result = ()
    if sys.version_info > (3, 5):
        out = subprocess.run(
            arguments,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        result = (
            out.returncode,
            out.stdout.decode("utf-8"),
            out.stderr.decode("utf-8"))
    else:
        p = subprocess.Popen(
            arguments,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        p.wait()
        result = (p.returncode, stdout.decode("utf-8"), stderr.decode("utf-8"))
    return result


class TestScorepBindingsPython(unittest.TestCase):
    maxDiff = None
    python = sys.executable

    def assertRegex(self, in1, in2):
        if sys.version_info > (3, 5):
            super().assertRegex(in1, in2)
        else:
            super(TestScorepBindingsPython, self).assertRegexpMatches(in1, in2)

    def setUp(self):
        self.env = os.environ.copy()
        self.expected_std_err = ""

    def test_user_regions(self):
        env = self.env

        out = call([self.python,
                    "test_user_regions.py"],
                   env=env)
        std_out = out[1]
        std_err = out[2]

        self.assertEqual(std_err, self.expected_std_err)
        self.assertEqual(std_out, "hello world\n")

    def test_context(self):
        env = self.env

        out = call([self.python,
                    "test_context.py"],
                   env=env)
        std_out = out[1]
        std_err = out[2]

        self.assertEqual(std_err, self.expected_std_err)
        self.assertEqual(std_out, "hello world\nhello world\nhello world\n")

    def test_user_regions_scorep(self):
        env = self.env

        out = call([self.python,
                    "-m",
                    "scorep",
                    "test_user_regions.py"],
                   env=env)
        std_out = out[1]
        std_err = out[2]

        self.assertIn("This module is not for tracing", std_err)
        self.assertEqual(std_out, "")


if __name__ == '__main__':
    unittest.main()
