import logging

import numpy as np
import torch


def count_parameters(model):
    weight_sizes = [np.prod(param.size()) for param in model.parameters()]
    return sum(weight_sizes)


def show_detail_parameters(model):
    params = [(n, np.prod(v.size())) for n, v in model.named_parameters()]
    out = ['Param: %s contributes %s weights' % (n, c) for n, c in params]
    out.append('Total: %s' % sum([c for n, c in params]))
    out = '\n'.join(out)
    logging.info(out)


def length_to_mask(length, max_len=None, dtype=None):
    """length: B.
    return B x max_len.
    If max_len is None, then max of length will be used.
    """
    max_len = max_len or length.max().item()
    mask = torch.arange(max_len, device=length.device,
                        dtype=length.dtype).expand(len(length), max_len) < length.unsqueeze(1)
    if dtype is not None:
        mask = torch.as_tensor(mask, dtype=dtype, device=length.device)
    return mask


def length_to_mask_np(length, max_len=None, dtype=None):
    """length: B.
    return B x max_len.
    If max_len is None, then max of length will be used.
    """
    max_len = max_len or length.max().item()
    mask = np.arange(max_len).repeat(max_len-len(length), ) < length.unsqueeze(1)
    if dtype is not None:
        mask = torch.as_tensor(mask, dtype=dtype, device=length.device)
    return mask


def register_buffer(model, name, value):
    """
    Register value as buffer of module, in case of value is not a Tensor
    :param model:
    :param name:
    :param value:
    :return:
    """
    model.register_buffer(name, torch.tensor([value]))


def tile(input, size, dim):
    """
    >>> x = torch.tensor([[1,2], [3, 4], [5,6]])
    >>> x
    tensor([[1, 2],
            [3, 4],
            [5, 6]])
    >>> tile(x, 3, dim=1)
    tensor([[1, 1, 1, 2, 2, 2],
            [3, 3, 3, 4, 4, 4],
            [5, 5, 5, 6, 6, 6]])
    :param self:
    :param input:
    :param size:
    :param dim:
    :return:
    """
    assert input.dim() == 2
    assert dim == 1
    batch_size = input.size(0)
    return input.view(-1, 1).repeat(1, size).view(batch_size, -1)

