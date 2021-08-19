from typing import *
from torch import Tensor

from . import preproc

def accuracy(config: preproc.Config, y_pred: Tensor, y: Tensor) -> Tuple[int, int]:
  (n, _) = y_pred.size()
  total_count = 0
  accurate_count = 0
  for i in range(n):
    ty_pred = config.type_set.tensor_to_type(y_pred[i])
    ty = config.type_set.tensor_to_type(y[i])
    total_count += 1
    if ty_pred == ty:
      accurate_count += 1
  return (accurate_count, total_count)

def topk_accuracy(config: preproc.Config, k: int, y_pred: Tensor, y: Tensor) -> Tuple[int, int]:
  (n, _) = y_pred.size()
  total_count = 0
  accurate_count = 0
  for i in range(n):
    ty_preds = config.type_set.tensor_to_topk_types(y_pred[i], k)
    ty = config.type_set.tensor_to_type(y[i])
    total_count += 1
    if ty in ty_preds:
      accurate_count += 1
  return (accurate_count, total_count)
