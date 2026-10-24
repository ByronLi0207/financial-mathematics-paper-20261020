"""Change only Figure 1 y-tick display strings; preserve frozen coordinates.

Reads the old source and seven-point selection read-only. It does not invoke
the old figure builder, reselect a window, calculate forecasts or alter data.
"""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[2]
OLD_SOURCE = ROOT / 'notes/v7/figure-sources/v7-endpoint-peak-example.tex'
OLD_DATA = ROOT / 'notes/v7/example-selection.json'
OLD_PDF = ROOT / 'submission-jof/figures/v7-endpoint-peak-example.pdf'
NEW_SOURCE = ROOT / 'notes/v8/figure-sources/endpoint-peak.tex'
NEW_PDF = ROOT / 'submission-jof/figures/v8-endpoint-peak-example.pdf'
CHECK = ROOT / 'notes/v8/figure1-format-check.json'
WORK = ROOT / '.scratch/v8/figure1-format'
TECTONIC = Path('/Applications/ChatGPT.app/Contents/Resources/tectonic/tectonic')
TICK = re.compile(r'(\\put\(58\.00,[-0-9.]+\)\{\\makebox\(0,0\)\[r\]\{)([^{}]+)(\}\})')


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def main():
    old_bytes = OLD_SOURCE.read_bytes()
    old = old_bytes.decode()
    data_bytes = OLD_DATA.read_bytes()
    old_pdf_bytes = OLD_PDF.read_bytes()
    expected = json.loads((ROOT / 'notes/v7/s9-figure-source-check.json').read_text())
    pin = next(row for row in expected['figure_sources']
               if row['source'] == str(OLD_SOURCE.relative_to(ROOT)))
    if sha(old_bytes) != pin['sha256']:
        raise ValueError('Original figure source differs from frozen v7 source')
    ticks = []

    def ordinary(match):
        before = match[2]
        if not re.fullmatch(r'\d+(?:\.\d+)?e[+-]\d+', before):
            raise ValueError('Expected original scientific y-tick')
        after = format(Decimal(before), ',.0f')
        ticks.append(dict(before=before, after=after))
        return match[1] + after + match[3]

    new, count = TICK.subn(ordinary, old)
    if count != 5:
        raise ValueError('Expected exactly five y-tick strings')
    normalize = lambda source: TICK.sub(lambda m: m[1] + '<Y_TICK>' + m[3], source)
    if normalize(new) != normalize(old):
        raise ValueError('Unexpected source change outside tick strings')
    old_bezier = '\n'.join(line for line in old.splitlines() if '\\qbezier' in line)
    new_bezier = '\n'.join(line for line in new.splitlines() if '\\qbezier' in line)
    coordinate_pattern = r'\\(?:put|qbezier)\([^\n{]*'
    old_coordinates = re.findall(coordinate_pattern, old)
    new_coordinates = re.findall(coordinate_pattern, new)
    if old_coordinates != new_coordinates or old_bezier != new_bezier:
        raise ValueError('Graphic coordinates changed')
    for target in (NEW_SOURCE, NEW_PDF, CHECK):
        if target.exists():
            raise FileExistsError('New task output already exists: ' + str(target))
    NEW_SOURCE.parent.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=False)
    NEW_SOURCE.write_text(new)
    command = [str(TECTONIC), '--keep-logs', '--outdir', str(WORK), str(NEW_SOURCE)]
    compiled = subprocess.run(command, capture_output=True, text=True, check=False)
    (WORK / 'compile-stdout.txt').write_text(compiled.stdout)
    (WORK / 'compile-stderr.txt').write_text(compiled.stderr)
    if compiled.returncode:
        raise RuntimeError('Tectonic compilation failed; inspect task compile logs')
    shutil.copyfile(WORK / 'endpoint-peak.pdf', NEW_PDF)
    render_commands = []
    for name, pdf in (('before', OLD_PDF), ('after', NEW_PDF)):
        command = ['pdftoppm', '-r', '180', '-singlefile', '-png', str(pdf), str(WORK / name)]
        subprocess.run(command, capture_output=True, text=True, check=True)
        render_commands.append(command)
    if OLD_SOURCE.read_bytes() != old_bytes or OLD_DATA.read_bytes() != data_bytes or OLD_PDF.read_bytes() != old_pdf_bytes:
        raise ValueError('An original source/data/PDF changed')
    selection = json.loads(data_bytes)['selection']
    check = dict(
        status='STRUCTURAL_PASS_VISUAL_PENDING', created_utc=datetime.now(timezone.utc).isoformat(),
        source=str(OLD_SOURCE.relative_to(ROOT)), output_source=str(NEW_SOURCE.relative_to(ROOT)),
        source_sha256=sha(old_bytes), output_source_sha256=sha(new.encode()),
        normalized_source_sha256=sha(normalize(old).encode()),
        normalized_output_sha256=sha(normalize(new).encode()),
        source_unchanged_except_five_y_tick_strings=True,
        coordinates_identical=old_coordinates == new_coordinates,
        coordinate_sha256=sha(json.dumps(old_coordinates).encode()),
        qbezier_commands_identical=old_bezier == new_bezier,
        qbezier_sha256=sha(old_bezier.encode()), qbezier_count=old_bezier.count('\\qbezier'),
        frozen_data_source=str(OLD_DATA.relative_to(ROOT)), frozen_data_sha256=sha(data_bytes),
        frozen_positions=selection['positions'], frozen_absolute_positions=selection['absolute_positions'],
        frozen_report=selection['report'], frozen_dates=selection['dates'],
        frozen_data_unchanged=True, original_source_unchanged=True, original_pdf_unchanged=True,
        original_pdf_sha256=sha(old_pdf_bytes), output_pdf=str(NEW_PDF.relative_to(ROOT)),
        output_pdf_sha256=sha(NEW_PDF.read_bytes()), tick_changes=ticks,
        compile_exit_code=compiled.returncode,
        compile_command=[str(TECTONIC), '--keep-logs', '--outdir', str(WORK.relative_to(ROOT)), str(NEW_SOURCE.relative_to(ROOT))],
        render_commands=render_commands, visual_qa='PENDING',
        data_selection_changed=False, forecasts_computed=0, models_fitted=0, new_scores=0,
    )
    CHECK.write_text(json.dumps(check, indent=2) + '\n')
    print(json.dumps(dict(status=check['status'], tick_changes=ticks,
                          output_pdf=check['output_pdf'], check=str(CHECK.relative_to(ROOT))), indent=2))


if __name__ == '__main__':
    main()
