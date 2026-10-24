# v9 reproduction and document boundaries

The owning source is the isolated `revision-v9` tree. Only this branch is published. Earlier branches, PR3/4/5 and the two earlier local directories are outside this task's write scope.

## Documents

From repository root, compile `submission-jof/manuscript.tex`, `submission-jof/supplement.tex` and `submission-jof/title-page.tex` with an existing Tectonic/XeLaTeX installation into distinct new directories. From the submission ZIP, select `main.tex` for the main article and compile the other two targets separately. Current PDFs use native TeX. Preview aliases are byte copies. The package manifest and embedded snapshots bind their exact source dependencies; old content builders must not overwrite this revision.

## Saved study integrity

`python3 -B restore_v9_archive.py restore results/v9/nonstationarity/formal/archive-parts.json` reconstructs the intact formal archive from its two public parts at a new destination according to the helper's command help. Existing untracked destinations are not to be overwritten. The part manifest supplies the full archive SHA; `audit_v9_nonstationarity.py` and `results/v9/nonstationarity/audit/` describe byte/receipt checks. These read saved output, not raw financial series. The report scripts reconstruct aggregate displays, not new forecasts. The original report-layer error, partial write and separate exact-scalar serialization provenance remain under `postrun/`.

The original local design-only commit is `5decccb0a13ef1969629cfec695dd3459c412c4e` at 2026-10-24T18:38:37UTC. First study diagnosis was 19:08:52.012080UTC; formal computation began 19:10:05.397496UTC. These local objects and prior sealed historical objects are not carried by browser file-tree commits. Protocol hashes and execution receipts are public; this is a different claim from preserving original Git object history remotely.

## Local full tests and replay

Final test receipt records the actual command and output. The numerical environment is a temporary uv run with arch8.0.0, NumPy2.3.5, scikit-learn1.9.1, pytest9.1.1, matplotlib3.11.2, pypdf and pillow. Native thread counts are each set to one. No system Python package was installed. Tests use artificial fixtures and saved archives; they do not rerun C2 financial diagnostics or forecasts. Historical document checks point to exact frozen PR5 snapshots while retaining their original assertions.

The full local suite has the original private historical commit objects needed by unchanged guards. They were imported solely into the new clone; they are not v9 ancestors and are not published through a bundle, ref or mirror. A fresh public clone therefore does not have an independently verified full historical replay environment. It can compile native documents and inspect the archives. A safe public history/provenance route remains AUTHOR-TODO T6; required restricted FX inputs remain separately unavailable. Passing local tests is not independent dealer validation or prospective evidence.
