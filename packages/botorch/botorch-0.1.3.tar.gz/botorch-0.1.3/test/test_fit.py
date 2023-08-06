#! /usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved

import math
import unittest
import warnings

import torch
from botorch import fit_gpytorch_model
from botorch.exceptions.warnings import OptimizationWarning
from botorch.models import FixedNoiseGP, HeteroskedasticSingleTaskGP, SingleTaskGP
from botorch.optim.fit import (
    OptimizationIteration,
    fit_gpytorch_scipy,
    fit_gpytorch_torch,
)
from gpytorch.constraints import GreaterThan
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.mlls.exact_marginal_log_likelihood import ExactMarginalLogLikelihood


NOISE = [0.127, -0.113, -0.345, -0.034, -0.069, -0.272, 0.013, 0.056, 0.087, -0.081]

MAX_ITER_MSG = "TOTAL NO. of ITERATIONS REACHED LIMIT"
MAX_RETRY_MSG = "Fitting failed on all retries."


class TestFitGPyTorchModel(unittest.TestCase):
    def _getModel(self, double=False, cuda=False):
        device = torch.device("cuda") if cuda else torch.device("cpu")
        dtype = torch.double if double else torch.float
        train_x = torch.linspace(0, 1, 10, device=device, dtype=dtype).unsqueeze(-1)
        noise = torch.tensor(NOISE, device=device, dtype=dtype)
        train_y = torch.sin(train_x.view(-1) * (2 * math.pi)) + noise
        model = SingleTaskGP(train_x, train_y)
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        return mll.to(device=device, dtype=dtype)

    def _getBatchedModel(self, kind="SingleTaskGP", double=False, cuda=False):
        device = torch.device("cuda") if cuda else torch.device("cpu")
        dtype = torch.double if double else torch.float
        train_x = torch.linspace(0, 1, 10, device=device, dtype=dtype).unsqueeze(-1)
        noise = torch.tensor(NOISE, device=device, dtype=dtype)
        train_y1 = torch.sin(train_x.view(-1) * (2 * math.pi)) + noise
        train_y2 = torch.sin(train_x.view(-1) * (2 * math.pi)) + noise
        train_y = torch.stack([train_y1, train_y2], dim=-1)
        if kind == "SingleTaskGP":
            model = SingleTaskGP(train_x, train_y)
        elif kind == "FixedNoiseGP":
            model = FixedNoiseGP(train_x, train_y, 0.1 * torch.ones_like(train_y))
        elif kind == "HeteroskedasticSingleTaskGP":
            model = HeteroskedasticSingleTaskGP(
                train_x, train_y, 0.1 * torch.ones_like(train_y)
            )
        else:
            raise NotImplementedError
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        return mll.to(device=device, dtype=dtype)

    def test_fit_gpytorch_model(self, cuda=False, optimizer=fit_gpytorch_scipy):
        options = {"disp": False, "maxiter": 5}
        for double in (False, True):
            mll = self._getModel(double=double, cuda=cuda)
            with warnings.catch_warnings(record=True) as ws:
                mll = fit_gpytorch_model(
                    mll, optimizer=optimizer, options=options, max_retries=1
                )
                if optimizer == fit_gpytorch_scipy:
                    self.assertEqual(len(ws), 1)
                    self.assertTrue(MAX_RETRY_MSG in str(ws[0].message))
            model = mll.model
            # Make sure all of the parameters changed
            self.assertGreater(model.likelihood.raw_noise.abs().item(), 1e-3)
            self.assertLess(model.mean_module.constant.abs().item(), 0.1)
            self.assertGreater(
                model.covar_module.base_kernel.raw_lengthscale.abs().item(), 0.1
            )
            self.assertGreater(model.covar_module.raw_outputscale.abs().item(), 1e-3)

            # test overriding the default bounds with user supplied bounds
            mll = self._getModel(double=double, cuda=cuda)
            with warnings.catch_warnings(record=True) as ws:
                mll = fit_gpytorch_model(
                    mll,
                    optimizer=optimizer,
                    options=options,
                    max_retries=1,
                    bounds={"likelihood.noise_covar.raw_noise": (1e-1, None)},
                )
                if optimizer == fit_gpytorch_scipy:
                    self.assertEqual(len(ws), 1)
                    self.assertTrue(MAX_RETRY_MSG in str(ws[0].message))

            model = mll.model
            self.assertGreaterEqual(model.likelihood.raw_noise.abs().item(), 1e-1)
            self.assertLess(model.mean_module.constant.abs().item(), 0.1)
            self.assertGreater(
                model.covar_module.base_kernel.raw_lengthscale.abs().item(), 0.1
            )
            self.assertGreater(model.covar_module.raw_outputscale.abs().item(), 1e-3)

            # test tracking iterations
            mll = self._getModel(double=double, cuda=cuda)
            if optimizer is fit_gpytorch_torch:
                options["disp"] = True
            with warnings.catch_warnings(record=True) as ws:
                mll, iterations = optimizer(mll, options=options, track_iterations=True)
                if optimizer == fit_gpytorch_scipy:
                    self.assertEqual(len(ws), 1)
                    self.assertTrue(MAX_ITER_MSG in str(ws[0].message))
            self.assertEqual(len(iterations), options["maxiter"])
            self.assertIsInstance(iterations[0], OptimizationIteration)

            # test extra param that does not affect loss
            options["disp"] = False
            mll = self._getModel(double=double, cuda=cuda)
            mll.register_parameter(
                "dummy_param",
                torch.nn.Parameter(
                    torch.tensor(
                        [5.0],
                        dtype=torch.double if double else torch.float,
                        device=torch.device("cuda" if cuda else "cpu"),
                    )
                ),
            )
            with warnings.catch_warnings(record=True) as ws:
                mll = fit_gpytorch_model(
                    mll, optimizer=optimizer, options=options, max_retries=1
                )
                if optimizer == fit_gpytorch_scipy:
                    self.assertEqual(len(ws), 1)
                    self.assertTrue(MAX_RETRY_MSG in str(ws[0].message))
            self.assertTrue(mll.dummy_param.grad is None)

    def test_fit_gpytorch_model_cuda(self):
        if torch.cuda.is_available():
            self.test_fit_gpytorch_model(cuda=True)

    def test_fit_gpytorch_model_singular(self, cuda=False):
        options = {"disp": False, "maxiter": 5}
        device = torch.device("cuda") if cuda else torch.device("cpu")
        for dtype in (torch.float, torch.double):
            X_train = torch.rand(2, 2, device=device, dtype=dtype)
            Y_train = torch.zeros(2, device=device, dtype=dtype)
            test_likelihood = GaussianLikelihood(
                noise_constraint=GreaterThan(-1.0, transform=None, initial_value=0.0)
            )
            gp = SingleTaskGP(X_train, Y_train, likelihood=test_likelihood)
            mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
            mll.to(device=device, dtype=dtype)
            # this will do multiple retries (and emit warnings, which is desired)
            fit_gpytorch_model(mll, options=options, max_retries=2)

    def test_fit_gpytorch_model_singular_cuda(self):
        if torch.cuda.is_available():
            self.test_fit_gpytorch_model_singular(cuda=True)

    def test_fit_gpytorch_model_torch(self, cuda=False):
        self.test_fit_gpytorch_model(cuda=cuda, optimizer=fit_gpytorch_torch)

    def test_fit_gpytorch_model_torch_cuda(self):
        if torch.cuda.is_available():
            self.test_fit_gpytorch_model_torch(cuda=True)

    def test_fit_gpytorch_model_sequential(self, cuda=False):
        options = {"disp": False, "maxiter": 1}
        for double in (False, True):
            for kind in ("SingleTaskGP", "FixedNoiseGP", "HeteroskedasticSingleTaskGP"):
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=OptimizationWarning)
                    mll = self._getBatchedModel(kind=kind, double=double, cuda=cuda)
                    mll = fit_gpytorch_model(mll, options=options, max_retries=1)
                    mll = self._getBatchedModel(kind=kind, double=double, cuda=cuda)
                    mll = fit_gpytorch_model(
                        mll, options=options, sequential=True, max_retries=1
                    )
                    mll = self._getBatchedModel(kind=kind, double=double, cuda=cuda)
                    mll = fit_gpytorch_model(
                        mll, options=options, sequential=False, max_retries=1
                    )

    def test_fit_gpytorch_model_sequential_cuda(self):
        if torch.cuda.is_available():
            self.test_fit_gpytorch_model_sequential(cuda=True)
