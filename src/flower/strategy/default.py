# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Configurable strategy implementation."""


from typing import Callable, List, Optional, Tuple

from flower.typing import Weights

from .aggregate import aggregate, weighted_loss_avg
from .strategy import Strategy


class DefaultStrategy(Strategy):
    """Configurable default strategy."""

    # pylint: disable-msg=too-many-arguments
    def __init__(
        self,
        fraction_fit: float = 0.1,
        fraction_eval: float = 0.1,
        min_fit_clients: int = 1,
        min_eval_clients: int = 1,
        min_available_clients: int = 1,
        eval_fn: Optional[Callable[[Weights], Optional[Tuple[float, float]]]] = None,
    ) -> None:
        """Constructor."""
        super().__init__()
        self.min_fit_clients = min_fit_clients
        self.min_eval_clients = min_eval_clients
        self.fraction_fit = fraction_fit
        self.fraction_eval = fraction_eval
        self.min_available_clients = min_available_clients
        self.eval_fn = eval_fn

    def should_evaluate(self) -> bool:
        """Evaluate every round."""
        return self.eval_fn is None

    def num_fit_clients(self, num_available_clients: int) -> Tuple[int, int]:
        """Use a fraction of available clients for training."""
        num_clients = int(num_available_clients * self.fraction_fit)
        return max(num_clients, self.min_fit_clients), self.min_available_clients

    def num_evaluation_clients(self, num_available_clients: int) -> Tuple[int, int]:
        """Use a fraction of available clients for evaluation."""
        num_clients = int(num_available_clients * self.fraction_eval)
        return max(num_clients, self.min_eval_clients), self.min_available_clients

    def evaluate(self, weights: Weights) -> Optional[Tuple[float, float]]:
        """Evaluate model weights using an evaluation function (if provided)."""
        if self.eval_fn is None:
            # No evaluation function provided
            return None
        return self.eval_fn(weights)

    def on_aggregate_fit(
        self, results: List[Tuple[Weights, int]], failures: List[BaseException]
    ) -> Optional[Weights]:
        """Aggregate fit results using weighted average (as in FedAvg)."""
        return aggregate(results)

    def on_aggregate_evaluate(
        self, results: List[Tuple[int, float]], failures: List[BaseException]
    ) -> Optional[float]:
        """Aggregate evaluation losses using weighted average."""
        return weighted_loss_avg(results)
