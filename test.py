from torch.autograd import Variable


class Test():
    """Tests the ``model`` on the specified test dataset using the
    data loader, and loss criterion.

    Keyword arguments:
    - model (``nn.Module``): the model instance to test.
    - data_loader (``Dataloader``): Provides single or multi-process
    iterators over the dataset.
    - criterion (``Optimizer``): The loss criterion.
    - metric (```Metric``): An instance specifying the metric to return.
    - use_cuda (``bool``): If ``True``, the training is performed using
    CUDA operations (GPU).

    """

    def __init__(self, model, data_loader, criterion, metric, use_cuda):
        self.model = model
        self.data_loader = data_loader
        self.criterion = criterion
        self.metric = metric
        self.use_cuda = use_cuda

    def run_epoch(self, iteration_loss=False):
        """Runs an epoch of validation.

        Keyword arguments:
        - iteration_loss (``bool``, optional): Prints loss at every step.

        Returns:
        - The epoch loss (float), and the values of the specified metrics

        """
        epoch_loss = 0.0
        self.metric.reset()
        for step, batch_data in enumerate(self.data_loader):
            # Get the inputs and labels
            inputs, labels = batch_data

            # Wrap them in a Varaible
            inputs, labels = Variable(inputs), Variable(labels)
            if self.use_cuda:
                inputs = inputs.cuda()
                labels = labels.cuda()

            # Forward propagation
            outputs = self.model(inputs)

            # Loss computation
            loss = self.criterion(outputs, labels)

            # Keep track of loss for current epoch
            epoch_loss += loss.data[0]

            # Keep track of evaluation the metric
            self.metric.add(outputs.data, labels.data)

            if iteration_loss:
                print("[Step: %d] Iteration loss: %.4f" % (step, loss.data[0]))

        return epoch_loss / len(self.data_loader), self.metric.value()
