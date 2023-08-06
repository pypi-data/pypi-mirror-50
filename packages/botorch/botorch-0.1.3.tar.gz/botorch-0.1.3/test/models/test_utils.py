#! /usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import unittest
import warnings

import torch
from botorch.exceptions import InputDataError, InputDataWarning
from botorch.models.utils import (
    add_output_dim,
    check_min_max_scaling,
    check_no_nans,
    check_standardization,
    multioutput_to_batch_mode_transform,
)


class TestMultiOutputToBatchModeTransform(unittest.TestCase):
    def test_multioutput_to_batch_mode_transform(self, cuda=False):
        for double in (False, True):
            tkwargs = {
                "device": torch.device("cuda") if cuda else torch.device("cpu"),
                "dtype": torch.double if double else torch.float,
            }
            n = 3
            num_outputs = 1
            train_X = torch.rand(n, 1, **tkwargs)
            train_Y = torch.rand(n, **tkwargs)
            train_Yvar = torch.rand(n, **tkwargs)
            # num_outputs = 1 and train_Y has shape `n`
            X_out, Y_out, Yvar_out = multioutput_to_batch_mode_transform(
                train_X=train_X,
                train_Y=train_Y,
                num_outputs=num_outputs,
                train_Yvar=train_Yvar,
            )
            self.assertTrue(torch.equal(X_out, train_X))
            self.assertTrue(torch.equal(Y_out, train_Y))
            self.assertTrue(torch.equal(Yvar_out, train_Yvar))
            # num_outputs > 1
            num_outputs = 2
            train_Y = torch.rand(n, num_outputs, **tkwargs)
            train_Yvar = torch.rand(n, num_outputs, **tkwargs)
            X_out, Y_out, Yvar_out = multioutput_to_batch_mode_transform(
                train_X=train_X,
                train_Y=train_Y,
                num_outputs=num_outputs,
                train_Yvar=train_Yvar,
            )
            expected_X_out = train_X.unsqueeze(0).expand(num_outputs, -1, 1)
            self.assertTrue(torch.equal(X_out, expected_X_out))
            self.assertTrue(torch.equal(Y_out, train_Y.transpose(0, 1)))
            self.assertTrue(torch.equal(Yvar_out, train_Yvar.transpose(0, 1)))

    def test_multioutput_to_batch_mode_transform_cuda(self):
        if torch.cuda.is_available():
            self.test_multioutput_to_batch_mode_transform(cuda=True)


class TestAddOutputDim(unittest.TestCase):
    def test_add_output_dim(self, cuda=False):
        for double in (False, True):
            tkwargs = {
                "device": torch.device("cuda") if cuda else torch.device("cpu"),
                "dtype": torch.double if double else torch.float,
            }
            original_batch_shape = torch.Size([2])
            # check exception is raised when trailing batch dims do not line up
            X = torch.rand(2, 3, 2, 1, **tkwargs)
            with self.assertRaises(RuntimeError):
                add_output_dim(X=X, original_batch_shape=original_batch_shape)
            # test no new batch dims
            X = torch.rand(2, 2, 1, **tkwargs)
            X_out, output_dim_idx = add_output_dim(
                X=X, original_batch_shape=original_batch_shape
            )
            self.assertTrue(torch.equal(X_out, X.unsqueeze(1)))
            self.assertEqual(output_dim_idx, 1)
            # test new batch dims
            X = torch.rand(3, 2, 2, 1, **tkwargs)
            X_out, output_dim_idx = add_output_dim(
                X=X, original_batch_shape=original_batch_shape
            )
            self.assertTrue(torch.equal(X_out, X.unsqueeze(2)))
            self.assertEqual(output_dim_idx, 2)

    def test_add_output_dim_cuda(self, cuda=False):
        if torch.cuda.is_available():
            self.test_add_output_dim(cuda=True)


class TestInputDataChecks(unittest.TestCase):
    def test_check_no_nans(self):
        check_no_nans(torch.tensor([1.0, 2.0]))
        with self.assertRaises(InputDataError):
            check_no_nans(torch.tensor([1.0, float("nan")]))

    def test_check_min_max_scaling(self):
        # check unscaled input in unit cube
        X = 0.1 + 0.8 * torch.rand(4, 2, 3)
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=X)
            self.assertFalse(any(issubclass(w.category, InputDataWarning) for w in ws))
        check_min_max_scaling(X=X, raise_on_fail=True)
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=X, strict=True)
            self.assertTrue(any(issubclass(w.category, InputDataWarning) for w in ws))
            self.assertTrue(any("not scaled" in str(w.message) for w in ws))
        with self.assertRaises(InputDataError):
            check_min_max_scaling(X=X, strict=True, raise_on_fail=True)
        # check proper input
        Xmin, Xmax = X.min(dim=-1, keepdim=True)[0], X.max(dim=-1, keepdim=True)[0]
        Xstd = (X - Xmin) / (Xmax - Xmin)
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=Xstd)
            self.assertFalse(any(issubclass(w.category, InputDataWarning) for w in ws))
        check_min_max_scaling(X=Xstd, raise_on_fail=True)
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=Xstd, strict=True)
            self.assertFalse(any(issubclass(w.category, InputDataWarning) for w in ws))
        check_min_max_scaling(X=Xstd, strict=True, raise_on_fail=True)
        # check violation
        X[0, 0, 0] = 2
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=X)
            self.assertTrue(any(issubclass(w.category, InputDataWarning) for w in ws))
            self.assertTrue(any("not contained" in str(w.message) for w in ws))
        with self.assertRaises(InputDataError):
            check_min_max_scaling(X=X, raise_on_fail=True)
        with warnings.catch_warnings(record=True) as ws:
            check_min_max_scaling(X=X, strict=True)
            self.assertTrue(any(issubclass(w.category, InputDataWarning) for w in ws))
            self.assertTrue(any("not contained" in str(w.message) for w in ws))
        with self.assertRaises(InputDataError):
            check_min_max_scaling(X=X, strict=True, raise_on_fail=True)

    def test_check_standardization(self):
        Y = torch.randn(3, 4, 2)
        # check standardized input
        Yst = (Y - Y.mean(dim=-2, keepdim=True)) / Y.std(dim=-2, keepdim=True)
        with warnings.catch_warnings(record=True) as ws:
            check_standardization(Y=Yst)
            self.assertFalse(any(issubclass(w.category, InputDataWarning) for w in ws))
        check_standardization(Y=Yst, raise_on_fail=True)
        # check nonzero mean
        with warnings.catch_warnings(record=True) as ws:
            check_standardization(Y=Yst + 1)
            self.assertTrue(any(issubclass(w.category, InputDataWarning) for w in ws))
            self.assertTrue(any("not standardized" in str(w.message) for w in ws))
        with self.assertRaises(InputDataError):
            check_standardization(Y=Yst + 1, raise_on_fail=True)
        # check non-unit variance
        with warnings.catch_warnings(record=True) as ws:
            check_standardization(Y=Yst * 2)
            self.assertTrue(any(issubclass(w.category, InputDataWarning) for w in ws))
            self.assertTrue(any("not standardized" in str(w.message) for w in ws))
        with self.assertRaises(InputDataError):
            check_standardization(Y=Yst * 2, raise_on_fail=True)
