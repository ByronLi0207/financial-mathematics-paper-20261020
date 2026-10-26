"""Pure layout/readback tests: no PDF authoring is performed by this module."""
from copy import deepcopy
import pytest
import v5_figure as fig


def test_verified_input_maps_all_scientific_values_without_reselection():
    data, binding = fig.load_figure_data()
    assert data['report'] == 73139
    assert data['floor'] == 42513
    assert data['peak'] == 74397
    assert data['endpoint'] == 48144
    assert data['date_labels'] == ['27 Jan', '03 Feb', '10 Feb', '17 Feb', '24 Feb', '03 Mar', '10 Mar']
    assert len(binding['scientific_bindings']) == 11
    layout = fig.figure_layout(data)
    assert layout['page_size'] == [467, 240]
    assert layout['point_coordinates'][0][0] == layout['plot_left']
    assert layout['point_coordinates'][-1][0] == layout['plot_right']
    assert layout['y_lower'] <= min(data['positions']) <= max(data['positions']) <= layout['y_upper']


def test_changed_path_peak_is_rejected_even_if_endpoint_still_valid():
    data, _ = fig.load_figure_data()
    broken = deepcopy(data)
    broken['peak'] = 75000
    with pytest.raises(ValueError, match='peak'):
        fig.figure_layout(broken)
