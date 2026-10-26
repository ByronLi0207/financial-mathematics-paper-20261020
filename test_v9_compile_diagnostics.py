"""Document guard must detect actual TeX problems without package-info false flags."""
import importlib.util
from pathlib import Path

def module():
 p=Path(__file__).parent/'notes/revision-v9/compile_documents.py';s=importlib.util.spec_from_file_location('v9_compile_guard',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def test_benign_infwarerr_info_is_not_a_build_error():
 assert module().diagnostics('Package: infwarerr 2019/12/03 v1.5 Providing info/warning/error messages (HO)')==[]

def test_actual_tex_failure_and_bad_reference_are_not_suppressed():
 lines=['! Undefined control sequence.',"LaTeX Warning: Reference `missing' on page 1 undefined",'Overfull \\hbox (8.0pt too wide)','Missing character: There is no Ω in font','error: compilation halted','LaTeX Error: Missing document.']
 assert module().diagnostics('\n'.join(lines))==lines
