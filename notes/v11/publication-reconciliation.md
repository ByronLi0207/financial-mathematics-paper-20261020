# Publication readback and progress-log reconciliation

The first complete public content tree is `8ba7a9529203958fe2e2a75b7d77c4aeb00e5b20` at `b3390eed6734276ee2176e71b0b3eb40fbc49749`. It exactly matches the local editorial source `d72bc90ead1494b2ab8cf58ab764dbf6794fdf2f`; see [first-whole-tree.json](first-whole-tree.json).

The large notes upload did not finish its GitHub commit before the first immediate fetch. No second upload or commit was submitted; the published head was subsequently read back. Among its 67 files, 66 exactly matched the earlier frozen snapshot. `publication-batches.jsonl` contained the actual later three batch receipts rather than the older five-entry cut. Its eight entries exactly matched the local append-only log and the already observed publication operations. The complete eight-entry log was retained and committed locally; the subsequent **entire Git tree** comparison passed. No paper, result, protocol, figure or scientific source value differed.

Original local editorial history is preserved in the author's local `.scratch/v11/local-editorial-history.bundle`, with the public v10b base as its prerequisite. Browser publication preserves exact file contents rather than original editorial commit identities. The original research-design history has its separate explicit provenance proofs; neither publication dates nor editorial metadata are represented as public preregistration.

Future batches use explicit frozen-file paths, with the source cut stated in their receipts. Final delivery metadata necessarily follows the first complete tree. The final local/remote equality is checked after that metadata is published; no progress-log self-reference is used to manufacture a final commit hash.
