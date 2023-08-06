from abc import abstractmethod

import torch

from flambe.metric.metric import Metric


class BinaryMetric(Metric):

    def __init__(self, threshold: float = 0.5) -> None:
        """Initialize the Binary metric.

        Parameters
        ---------
        threshold: float
            Given a probability p of belonging to Positive class,
            p < threshold will be considered tagged as Negative by
            the classifier when computing the metric.

        """
        self.threshold = threshold

    def compute(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        """Compute the metric given predictions and targets

        Parameters
        ----------
        pred : Tensor
            The model predictions
        target : Tensor
            The binary targets

        Returns
        -------
        float
            The computed binary metric

        """
        # Cast because pytorch's byte method returns a Tensor type
        pred = (pred > self.threshold).byte()
        target = target.byte()
        return self.compute_binary(pred, target)

    @abstractmethod
    def compute_binary(self,
                       pred: torch.Tensor,
                       target: torch.Tensor) -> torch.Tensor:
        """Compute a binary-input metric.

        Parameters
        ---------
        pred: torch.Tensor
            Predictions made by the model. It should be a probability
            0 <= p <= 1 for each sample, 1 being the positive class.
        target: torch.Tensor
            Ground truth. Each label should be either 0 or 1.

        Returns
        ------
        torch.float
            The computed binary metric

        """
        pass


class BinaryPrecision(BinaryMetric):
    """Compute Binary Precision.

    An example is considered negative when its score is below the
    specified threshold. Binary precition is computed as follows:

    ```
    |True positives| / |True Positives| + |False Positives|
    ```

    """

    def compute_binary(self,
                       pred: torch.Tensor,
                       target: torch.Tensor) -> torch.Tensor:
        """Compute binary precision.

        Parameters
        ---------
        pred: torch.Tensor
            Predictions made by the model. It should be a probability
            0 <= p <= 1 for each sample, 1 being the positive class.
        target: torch.Tensor
            Ground truth. Each label should be either 0 or 1.

        Returns
        ------
        torch.float
            The computed binary metric

        """
        acc = pred == target
        true_p = acc & target

        if pred.sum() == 0:
            metric = torch.tensor(0)
        else:
            # Again, weird typing from pytorch
            # check periodically for a fix
            metric = (true_p.sum().float() / pred.sum().float())

        return metric


class BinaryRecall(BinaryMetric):
    """Compute binary recall.

    An example is considered negative when its score is below the
    specified threshold. Binary precition is computed as follows:

    ```
    |True positives| / |True Positives| + |False Negatives|
    ```

    """

    def compute_binary(self,
                       pred: torch.Tensor,
                       target: torch.Tensor) -> torch.Tensor:
        """Compute binary recall.

        Parameters
        ---------
        pred: torch.Tensor
            Predictions made by the model. It should be a probability
            0 <= p <= 1 for each sample, 1 being the positive class.
        target: torch.Tensor
            Ground truth. Each label should be either 0 or 1.

        Returns
        ------
        torch.float
            The computed binary metric

        """
        acc = pred == target
        true_p = acc & target

        if target.sum() == 0:
            metric = torch.tensor(0)
        else:
            metric = true_p.sum().float() / target.sum().float()

        return metric
