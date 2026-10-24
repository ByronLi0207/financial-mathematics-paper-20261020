"""Regression for the observed postrun JSON scalar failure; no study rerun."""
import importlib
import json
import numpy as np


def test_exact_numpy_scalar_conversion_makes_frozen_prediction_serializable():
    from run_v9_nonstationarity import prediction_status
    from test_v9_nonstationarity_driver import cells,diagnostics
    raw=prediction_status(cells(),diagnostics(),[f's{i}' for i in range(13)])
    # Reproduce the observed production failure before checking the repair.
    try:json.dumps(raw)
    except TypeError:pass
    else:raise AssertionError('observed NumPy scalar failure was not reproduced')
    m=importlib.import_module('finalize_v9_archive')
    native=m.native_scalars(raw)
    assert json.loads(json.dumps(native))==native
    assert type(native['N1']['holm_rejections']) is int
    assert native['N1']['holm_rejections']==raw['N1']['holm_rejections']
    assert native['N2']==raw['N2'] and native['N3']==raw['N3']


def test_scalar_conversion_never_rounds_or_discards_nested_values():
    m=importlib.import_module('finalize_v9_archive')
    a={'values':[np.float64(1.2345678901234567),np.int64(7),np.bool_(False)],'missing':None}
    b=m.native_scalars(a)
    assert b=={'values':[1.2345678901234567,7,False],'missing':None}
