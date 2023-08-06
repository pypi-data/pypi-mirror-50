#! /usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import unittest

from botorch.exceptions.errors import (
    BotorchError,
    CandidateGenerationError,
    InputDataError,
    UnsupportedError,
)


class TestBotorchExceptions(unittest.TestCase):
    def test_botorch_exception_hierarchy(self):
        self.assertIsInstance(BotorchError(), Exception)
        self.assertIsInstance(CandidateGenerationError(), BotorchError)
        self.assertIsInstance(InputDataError(), BotorchError)
        self.assertIsInstance(UnsupportedError(), BotorchError)

    def test_raise_botorch_exceptions(self):
        for ErrorClass in (
            BotorchError,
            CandidateGenerationError,
            InputDataError,
            UnsupportedError,
        ):
            with self.assertRaises(ErrorClass):
                raise ErrorClass("message")
