import hashlib
from pathlib import Path
from v4_submission import compose,OUT

def test_v4_read_only_composition_preserves_current_revision():
 before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*-content.json')}
 compose(write_outputs=False)
 after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('*-content.json')}
 assert before==after
