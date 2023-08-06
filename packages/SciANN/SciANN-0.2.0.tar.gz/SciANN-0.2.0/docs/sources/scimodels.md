# SciModels


---

<span style="float:right;">[[source]](https://github.com/sciann/sciann/tree/master/sciann/models/model.py#L18)</span>
### SciModel

```python
sciann.models.model.SciModel(inputs=None, targets=None, loss_func='mse', plot_to_file=None)
```

Configures the model for training.

__Arguments__

- __inputs__: Main variables (also called inputs, or independent variables) of the network, `xs`.
    They all should be of type `Variable`.

targets: list all targets (also called outputs, or dependent variables)
to be satisfied during the training. Expected list members are:
- Entries of type `Constraint`, such as Data, Tie, etc.
- Entries of type `Functional` can be:
. A single `Functional`: will be treated as a Data constraint.
The object can be just a `Functional` or any derivatives of `Functional`s.
An example is a PDE that is supposed to be zero.
. A tuple of (`Functional`, `Functional`): will be treated as a `Constraint` of type `Tie`.
- If you need to impose more complex types of constraints or
to impose a constraint partially in a specific part of region,
use `Data` or `Tie` classes from `Constraint`.

plot_to_file: A string file name to output the network architecture.

__Raises__

- __ValueError__: `inputs` must be of type Variable.
            `targets` must be of types `Functional`, or (`Functional`, data), or (`Functional`, `Functional`).
    
----

### solve


```python
solve(x_true, y_true, weights=None, epochs=10, batch_size=256, shuffle=True, callbacks=None, stop_after=100, default_zero_weight=1e-10)
```


Performs the training on the model.

__Arguments__

- __x_true__: list of `Xs` associated to targets of `Y`.
    Expecting a list of np.ndarray of size (N,1) each,
    with N as the sample size.
- __y_true__: list of true `Ys` associated to the targets defined during model setup.
    Expecting the same size as list of targets defined in `SciModel`.
        - To impose the targets at specific `Xs` only,
            pass a tuple of `(ids, y_true)` for that target.

weights (np.ndarray): A global sample weight to be applied to samples.
    Expecting an array of shape (N,1), with N as the sample size.
    Default value is `one` to consider all samples equally important.
epochs (Integer): Number of epochs to train the model.
    An epoch is an iteration over the entire `x` and `y`
    data provided.
batch_size (Integer): or 'None'.
    Number of samples per gradient update.
    If unspecified, 'batch_size' will default to 128.

- __shuffle__: Boolean (whether to shuffle the training data).
    Default value is True.
- __callbacks__: List of `keras.callbacks.Callback` instances.
- __stop_after__: To stop after certain missed epochs.
    Defaulted to 100.
- __default_zero_weight__: a small number for zero sample-weight.

__Returns__

A 'History' object after performing fitting.
    
