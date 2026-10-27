# WP3 heatmap display development evidence

This display tool reads only a terminated saved summary. During development it used a constructed scalar 216-row fixture, with no study DGP draws, model fits, forecast calculations or original-result reads. The fixture deliberately includes unavailable 7/32 cells and an extreme +1750.5% display value, not an empirical or simulated study finding.

## Scope and fixed presentation

- Six PDFs plus six PNG previews: QR33 and QR4, each relative loss, strict breach rate and strict win rate.
- Six panels per figure: H rows (6,24), level phi columns (0.7,0.9,0.98). Within panel, W rows (52,260,720,2880), variance persistence columns (0,0.9,0.98).
- Complete factorial inventory is required; duplicate, absent or unexpected cell identities are rejected.
- Only all 32 planned paired repetitions complete with finite estimate/MC SE can be colored. Other full-procedure cells show hatched NA and completed/planned counts. Available-pair values remain audit fields, never plotted as complete data.
- Fixed grayscale limits were chosen before seeing any study results: loss[-100,100]%, breach and win[0,100]%. Outliers keep the original numeric annotation even when shading clips. Each eligible cell shows estimate and MC SE (parentheses).
- Probability-to-percentage conversion is presentation only; the source summary is hash-checked unchanged. Source/hash, drawn-cell counts, scalar panels, captions and every PDF/PNG hash are written in display-receipt.json.
- Output directory must be new; existing output is refused rather than replaced. No file is deleted.

## RED before implementation

Actual command (the following shell `cat` meant the compound shell returned 0; the pytest output itself records failures, and a separate pytest exit code was not captured):

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_plots.py -q
```

```text
WARN `--no-project` was provided, but no project was found
FFFFFFFFFFFFFFF                                                          [100%]
=================================== FAILURES ===================================
____________ test_display_module_is_standard_library_only_at_import ____________

    def test_display_module_is_standard_library_only_at_import():
        command = "import runpy,sys; runpy.run_path(%r); assert not any(x in sys.modules for x in ('numpy','matplotlib','conditional_study','v8_mechanism_mc'))" % str(MODULE)
        result = subprocess.run([sys.executable,'-c',command],capture_output=True,text=True)
>       assert result.returncode == 0, result.stderr
E       AssertionError: Traceback (most recent call last):
E           File "<string>", line 1, in <module>
E           File "<frozen runpy>", line 286, in run_path
E           File "<frozen runpy>", line 254, in _get_code_from_file
E         FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['/Users/bingyouli/.cache/uv/builds-v0/.tmpDfZzR8/bin/python', '-c', "import runpy,sys; runpy.ru...o 2] No such file or directory: \'/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py\'\n').returncode

test_v8_wp3_plots.py:35: AssertionError
_____________ test_grid_has_six_facets_and_exactly_72_unique_cells _____________

    def test_grid_has_six_facets_and_exactly_72_unique_cells():
>       module = load_module(); panels = module.prepare_grids(fixture_summary(),'QR33','loss')
                 ^^^^^^^^^^^^^

test_v8_wp3_plots.py:39: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a8ce2a0>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
________ test_partial_available_pair_value_is_na_never_zero_or_colored _________

    def test_partial_available_pair_value_is_na_never_zero_or_colored():
>       module = load_module(); summary = fixture_summary()
                 ^^^^^^^^^^^^^

test_v8_wp3_plots.py:49: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a825f40>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
___________ test_complete_status_cannot_override_missing_repetitions ___________

    def test_complete_status_cannot_override_missing_repetitions():
>       module = load_module(); summary = fixture_summary()
                 ^^^^^^^^^^^^^

test_v8_wp3_plots.py:60: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a826e40>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
________ test_probability_display_only_converts_units[breach-6.25-0.5] _________

metric = 'breach', expected = 6.25, expected_se = 0.5

    @pytest.mark.parametrize('metric,expected,expected_se',[('breach',6.25,.5),('win',75.,7.)])
    def test_probability_display_only_converts_units(metric,expected,expected_se):
>       cell = load_module().prepare_grids(fixture_summary(),'QR4',metric)[0]['cells'][0][0]
               ^^^^^^^^^^^^^

test_v8_wp3_plots.py:68: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a960c80>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
__________ test_probability_display_only_converts_units[win-75.0-7.0] __________

metric = 'win', expected = 75.0, expected_se = 7.0

    @pytest.mark.parametrize('metric,expected,expected_se',[('breach',6.25,.5),('win',75.,7.)])
    def test_probability_display_only_converts_units(metric,expected,expected_se):
>       cell = load_module().prepare_grids(fixture_summary(),'QR4',metric)[0]['cells'][0][0]
               ^^^^^^^^^^^^^

test_v8_wp3_plots.py:68: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a960c50>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
_____________ test_full_factorial_inventory_is_required[duplicate] _____________

mutation = 'duplicate'

    @pytest.mark.parametrize('mutation',['duplicate','missing','unexpected'])
    def test_full_factorial_inventory_is_required(mutation):
        summary = fixture_summary()
        if mutation=='duplicate': summary['cells'].append(dict(summary['cells'][72]))
        elif mutation=='missing': summary['cells'].pop(72)
        else: summary['cells'][72]['phi']=.8
>       with pytest.raises(ValueError): load_module().prepare_grids(summary,'QR33','loss')
                                        ^^^^^^^^^^^^^

test_v8_wp3_plots.py:79: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a837620>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
______________ test_full_factorial_inventory_is_required[missing] ______________

mutation = 'missing'

    @pytest.mark.parametrize('mutation',['duplicate','missing','unexpected'])
    def test_full_factorial_inventory_is_required(mutation):
        summary = fixture_summary()
        if mutation=='duplicate': summary['cells'].append(dict(summary['cells'][72]))
        elif mutation=='missing': summary['cells'].pop(72)
        else: summary['cells'][72]['phi']=.8
>       with pytest.raises(ValueError): load_module().prepare_grids(summary,'QR33','loss')
                                        ^^^^^^^^^^^^^

test_v8_wp3_plots.py:79: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a9a4620>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
____________ test_full_factorial_inventory_is_required[unexpected] _____________

mutation = 'unexpected'

    @pytest.mark.parametrize('mutation',['duplicate','missing','unexpected'])
    def test_full_factorial_inventory_is_required(mutation):
        summary = fixture_summary()
        if mutation=='duplicate': summary['cells'].append(dict(summary['cells'][72]))
        elif mutation=='missing': summary['cells'].pop(72)
        else: summary['cells'][72]['phi']=.8
>       with pytest.raises(ValueError): load_module().prepare_grids(summary,'QR33','loss')
                                        ^^^^^^^^^^^^^

test_v8_wp3_plots.py:79: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a9a6600>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
________ test_nonfinite_complete_value_is_na_with_explicit_reason[None] ________

bad = None

    @pytest.mark.parametrize('bad',[None,math.nan,math.inf])
    def test_nonfinite_complete_value_is_na_with_explicit_reason(bad):
        summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=bad
>       cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
             ^^^^^^^^^^^^^

test_v8_wp3_plots.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a960a40>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
________ test_nonfinite_complete_value_is_na_with_explicit_reason[nan] _________

bad = nan

    @pytest.mark.parametrize('bad',[None,math.nan,math.inf])
    def test_nonfinite_complete_value_is_na_with_explicit_reason(bad):
        summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=bad
>       cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
             ^^^^^^^^^^^^^

test_v8_wp3_plots.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a827cb0>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
________ test_nonfinite_complete_value_is_na_with_explicit_reason[inf] _________

bad = inf

    @pytest.mark.parametrize('bad',[None,math.nan,math.inf])
    def test_nonfinite_complete_value_is_na_with_explicit_reason(bad):
        summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=bad
>       cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
             ^^^^^^^^^^^^^

test_v8_wp3_plots.py:85: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a825910>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
_ test_fixed_color_limits_do_not_depend_on_results_and_annotations_retain_outliers _

    def test_fixed_color_limits_do_not_depend_on_results_and_annotations_retain_outliers():
>       module=load_module();summary=fixture_summary();summary['cells'][72]['relative_loss_percent']=1750.5
               ^^^^^^^^^^^^^

test_v8_wp3_plots.py:91: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a7ba300>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
____________________ test_zero_is_a_valid_complete_estimate ____________________

    def test_zero_is_a_valid_complete_estimate():
        summary=fixture_summary();summary['cells'][72].update(relative_loss_percent=0.,relative_loss_mcse=0.)
>       cell=load_module().prepare_grids(summary,'QR33','loss')[0]['cells'][0][0]
             ^^^^^^^^^^^^^

test_v8_wp3_plots.py:101: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a9a56a0>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
__________________ test_unknown_method_or_metric_is_rejected ___________________

    def test_unknown_method_or_metric_is_rejected():
>       module=load_module()
               ^^^^^^^^^^^^^

test_v8_wp3_plots.py:106: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
test_v8_wp3_plots.py:18: in load_module
    spec.loader.exec_module(module)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <_frozen_importlib_external.SourceFileLoader object at 0x10a9a55b0>
path = '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

>   ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023/notes/revision-v8/plot_wp3.py'

<frozen importlib._bootstrap_external>:1190: FileNotFoundError
=========================== short test summary info ============================
FAILED test_v8_wp3_plots.py::test_display_module_is_standard_library_only_at_import
FAILED test_v8_wp3_plots.py::test_grid_has_six_facets_and_exactly_72_unique_cells
FAILED test_v8_wp3_plots.py::test_partial_available_pair_value_is_na_never_zero_or_colored
FAILED test_v8_wp3_plots.py::test_complete_status_cannot_override_missing_repetitions
FAILED test_v8_wp3_plots.py::test_probability_display_only_converts_units[breach-6.25-0.5]
FAILED test_v8_wp3_plots.py::test_probability_display_only_converts_units[win-75.0-7.0]
FAILED test_v8_wp3_plots.py::test_full_factorial_inventory_is_required[duplicate]
FAILED test_v8_wp3_plots.py::test_full_factorial_inventory_is_required[missing]
FAILED test_v8_wp3_plots.py::test_full_factorial_inventory_is_required[unexpected]
FAILED test_v8_wp3_plots.py::test_nonfinite_complete_value_is_na_with_explicit_reason[None]
FAILED test_v8_wp3_plots.py::test_nonfinite_complete_value_is_na_with_explicit_reason[nan]
FAILED test_v8_wp3_plots.py::test_nonfinite_complete_value_is_na_with_explicit_reason[inf]
FAILED test_v8_wp3_plots.py::test_fixed_color_limits_do_not_depend_on_results_and_annotations_retain_outliers
FAILED test_v8_wp3_plots.py::test_zero_is_a_valid_complete_estimate - FileNot...
FAILED test_v8_wp3_plots.py::test_unknown_method_or_metric_is_rejected - File...
15 failed in 0.07s
```

## GREEN after implementation and visual-layout correction

Same pytest command, current output:

```text
WARN `--no-project` was provided, but no project was found
...............                                                          [100%]
15 passed in 0.08s
```

## Actual constructed-fixture render and QA

Temporary-only uv environment: `--with matplotlib --with pypdf --with pillow --with pytest`; offline cached packages, no global/system installation. An initial pre-render attempt omitted pytest needed only to import the test fixture. A second attempt was correctly refused because the macOS /var temporary path includes a symlink. Resolving the real temporary directory allowed output. Neither failed attempt generated study observations.

Six fixture PDFs were generated and independently opened with pypdf, each one page. Reusing the existing output directory raised FileExistsError as intended. The first visual fixture revealed an overlapping colorbar label and footer. Increasing bottom spacing corrected that display problem; no source scalar, metric or color limit changed. The six figures were then rendered to a new output directory (original fixture files retained):

```json
{"constructed_fixture_only": true, "rendered_pdfs": 6, "pdf_page_counts": [1, 1, 1, 1, 1, 1], "preview": "/private/var/folders/4g/4pc4x_0x10dcd_t1wwhqss980000gn/T/v8-wp3-plot-fixture-9neyqsdo/figures-layout2/v8-wp3-qr33-loss.png"}
```

Actual image inspection: QR33-loss and QR4-win previews show all H/phi titles, W/p tick labels, gray/hatched cells, uncapped +1750.5 annotation, separate colorbar label/footer; no clipping or overlap after correction. pypdf extraction additionally finds six H titles and two history labels in loss, breach and win PDF samples. This is fixture-display QA, not acceptance of any future formal result or manuscript page.

`python3 -B notes/revision-v8/plot_wp3.py --help` runs using standard library only and exits successfully. For formal rendering after the study has terminated and summary exists:

```text
uv run --offline --no-project --no-env-file --python BUNDLED_PYTHON --with matplotlib python -B notes/revision-v8/plot_wp3.py --summary results/revision-v8/wp3/summary.json --outdir NEW_OUTPUT_DIRECTORY
```

The parent must visually inspect the actual result figures separately before publication. No formal output was read or rendered by this task.

## Follow-up: interpreting the win-rate Monte Carlo SE

Only the display caption and its scalar text test changed. No sealed scientific core/driver, protocol or study output was read or modified. The caption now explains that the plug-in binomial Monte Carlo SE can equal zero when all 32 repetitions win or none wins. This is not certainty from a finite set of repetitions. It refers to the worst-case bound already reported in the saved summary, `0.5/√32`; no new interval, inferential test or financial calculation was added.

Actual command for both RED and GREEN:

```text
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /Users/bingyouli/.local/bin/uv run --offline --no-project --no-env-file --python /Users/bingyouli/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 --with pytest python -B -m pytest -p no:cacheprovider test_v8_wp3_plots.py -q
```

RED, exit 1:

```text
WARN `--no-project` was provided, but no project was found
...............F                                                         [100%]
=================================== FAILURES ===================================
_ test_win_caption_distinguishes_zero_plugin_se_from_finite_repetition_certainty _

    def test_win_caption_distinguishes_zero_plugin_se_from_finite_repetition_certainty():
        module=load_module();text=module.caption('QR4','win')
>       assert 'plug-in binomial Monte Carlo SE' in text
E       AssertionError: assert 'plug-in binomial Monte Carlo SE' in 'Four-feature quantile regression: repetitions with lower mean loss than matched f (%). Rows of panels show horizons H...ic annotation. The finite grid describes these specified processes and does not establish a universal regime boundary.'

test_v8_wp3_plots.py:113: AssertionError
=========================== short test summary info ============================
FAILED test_v8_wp3_plots.py::test_win_caption_distinguishes_zero_plugin_se_from_finite_repetition_certainty
1 failed, 15 passed in 0.09s
```

GREEN, exit 0:

```text
WARN `--no-project` was provided, but no project was found
................                                                         [100%]
16 passed in 0.08s
```

The test also confirms this win-specific explanation is not inadvertently inserted into the loss caption. Formal result figures have not been read or rerendered by this follow-up.
