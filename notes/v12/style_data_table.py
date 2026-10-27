"""Display width only; statistical table bodies remain byte-for-byte unchanged."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[2];source=R/'results/v12/descriptives/data-table.tex';target=R/'submission-v10/generated/v12-data-table.tex'
a=source.read_text();b=a.replace(r'p{.08\linewidth}',r'p{.09\linewidth}',1);assert a!=b
if target.exists():
 i=0;backup=target.with_name(target.name+'.v12-width.bak')
 while backup.exists():i+=1;backup=target.with_name(target.name+f'.v12-width.{i}.bak')
 shutil.copyfile(target,backup)
target.write_text(b)
sha=lambda x:hashlib.sha256(x).hexdigest()
record=dict(operation='One frequency-column width: .08 to .09 linewidth; no text or number changes.',source_sha256=sha(source.read_bytes()),display_sha256=sha(target.read_bytes()),inverse_identity=b.replace(r'p{.09\linewidth}',r'p{.08\linewidth}',1)==a)
p=R/'notes/v12/data-table-style.json';assert not p.exists();p.write_text(json.dumps(record,indent=2)+'\n');print(record)
