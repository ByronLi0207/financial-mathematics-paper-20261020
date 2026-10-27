# v10 final protection check

最终全套测试为 PASS；保护核对整体为 FAIL，原因是旧修订 v3 目录相对 E0 出现8个文件差异，并且 HEAD/tree 推进。差异来源本次核对未确定，未恢复或写入旧目录。NEW v10 的3454个继承文件中3452个字节相同，仅 README.md 和 .gitignore 为允许的非研究改动；14个受保护远端 refs 及1036项四阶段封存代码/输入指纹全部通过。

测试独立回执：notes/v10/final-tests.json；原始输出：.scratch/v10/final-pytest.txt。实际UTC 2026-10-25T00:16:13.170030+00:00 至 2026-10-25T00:18:04.789112+00:00，wall 111.61913116599999秒，输出末行：`1715 passed, 1181 subtests passed in 110.99s (0:01:50)`。本回执不代替 root 的 native PDF/visual/publication 检查。

Overall: **FAIL**. UTC: 2026-10-25T00:19:00.087982+00:00 to 2026-10-25T00:19:03.290169+00:00. Elapsed 3.202s.

This audit only read files and Git objects/refs, using GIT_OPTIONAL_LOCKS=0. No status/fetch/index-write command, scientific driver, read_design, financial recomputation, restoration or old-directory write occurred.

| Scope | Result | Evidence |
|---|---|---|
| E0 old tracked files | FAIL | 10419/10427 identical; HEAD/tree/branch checked |
| Protected remote refs | PASS | 14/14 equal to E0 |
| Base tracked tree in NEW | PASS | 3452 identical; 2 permitted README/.gitignore changes; 0 unexpected; 0 missing |
| Scientific source/input pins | PASS | 1036/1036 SHA/byte checks |

## Old directories

- /Users/bingyouli/Research/论文/金融数学论文-修订v3-20261023: FAIL; 3321/3329 identical, 8 changed, 0 missing, 0 mode changes; Git identity unchanged=False.
  Differences: {"changed_files": [{"path": "EXTENDED_RESULTS.md", "expected_sha256": "afabb348ca1a31d273c1e895637a4cabc2a701361be6e649a89fe9636fc471bd", "actual_sha256": "e52fef2ead04968f1494a63b960e551b7fc484d93580e4ab269b66d58bf308a0", "expected_bytes": 6762, "actual_bytes": 7929}, {"path": "REVISION_V9_CHANGELOG.md", "expected_sha256": "c7228642fa9d5b973eb3e285c4cce31e58bc38243c7bc506ff95f90a465c309e", "actual_sha256": "6c4cb77c8be3d69e218e57596c33edba5f998009bb6f9675dde2599f424a701a", "expected_bytes": 6717, "actual_bytes": 89058}, {"path": "submission-jof/manuscript.pdf", "expected_sha256": "472787ca9638a43b57ba4ff637fd1f53e88c310f578d25e63e01199b9c7ec6b0", "actual_sha256": "bdca38069ed46ff5ccc552d96637a65cd9686263d9dea0dda7868cfa4ca71e8b", "expected_bytes": 187817, "actual_bytes": 211957}, {"path": "submission-jof/manuscript.tex", "expected_sha256": "66287e0d3b192affe04a4c974a1d0141fe3a3be8eda4da074552be5828bead40", "actual_sha256": "54be6466f3d00ea794b7b8917f95c5caf9f17aaf257d476fae5e16b9de11af1d", "expected_bytes": 61307, "actual_bytes": 69215}, {"path": "submission-jof/references.bib", "expected_sha256": "3e02559cce9fc22c796a4f9a2a4e1b590020a451c983b8ae447728fed79250d5", "actual_sha256": "6691a06dd9052834dd0260544e83288a4b84a76dbab4c384cc717649db695ea3", "expected_bytes": 10149, "actual_bytes": 11200}, {"path": "submission-jof/supplement.pdf", "expected_sha256": "25d547a67daf4e8a1b915ec0ff6870b9a6d44ce0d5aa1a651e2925d8f21b4c89", "actual_sha256": "8d2023aa9f31fad66823f679cff39f8e4996e001c0ddb1e0d9fa2fedb18d111a", "expected_bytes": 199857, "actual_bytes": 237087}, {"path": "submission-jof/supplement.tex", "expected_sha256": "2fb0b5fee233265cfdd968282beba43143b1a8fa92cbf62a81e090c941d5a3db", "actual_sha256": "ae9d9cbe5d4100a6cb35abddafeaf49441181e953f176623e5d37728b41f4fb9", "expected_bytes": 90602, "actual_bytes": 82186}, {"path": "test_v8_main_numbers.py", "expected_sha256": "7c7d86a4a5f75c30b7f054056f7f9075f249898c65524ff9394cf89974a87182", "actual_sha256": "096d15b26a6189e0eff4d662ac8a3d213fa5fac6545f200f3e4e8fea0127eccf", "expected_bytes": 4821, "actual_bytes": 4984}], "missing_files": [], "mode_changes": [], "actual_git": {"head": "32ee58688bac260de322c31cb8945adbf3b53154", "tree": "205f1863acc973c494078e1d21ba69f965d54a74", "branch": "revision-v8-goal"}, "expected_git": {"head": "7f0fee8f1cfdeed584098bbc27570e88eafaea43", "tree": "e1b0d584900d1671e326e53fc7a5324f58c184e1", "branch": "revision-v8-goal"}, "read_errors": []}
- /Users/bingyouli/Research/论文/金融数学论文-v8-20261024: PASS; 2780/2780 identical, 0 changed, 0 missing, 0 mode changes; Git identity unchanged=True.
- /Users/bingyouli/Research/论文/金融数学论文-v9-20261024: PASS; 3454/3454 identical, 0 changed, 0 missing, 0 mode changes; Git identity unchanged=True.
- /Users/bingyouli/Research/论文/金融数学论文-导师修订-20261023: PASS; 864/864 identical, 0 changed, 0 missing, 0 mode changes; Git identity unchanged=True.

The fifth E0-listed directory was recorded as non-Git and has no supplied per-file baseline; this report makes no content-unchanged claim for it.

## NEW inherited tree

All base tracked entries were compared by Git blob identity against their current working-file bytes. Only README.md and .gitignore are allowed nonresearch changes. Research source, data, results and submission-jof are included without exclusions.

Allowed changes: [{"path": ".gitignore", "category": "other_inherited", "expected_git_blob": "2640159a1357978fce2a8a243faed8fb16d6cfcb", "actual_git_blob": "73ba8fb4d4f385e9abed8bbb3e5c18b41180e0be", "bytes": 1454}, {"path": "README.md", "category": "other_inherited", "expected_git_blob": "6f84700a9688720e74ff2db3e90d26474ec10728", "actual_git_blob": "f19f5ea939b7fd4b320a0aeca5f081f1b1cbba1d", "bytes": 30457}]
Unexpected changes: []
Missing files: []

## Seals

Checked four manifests and 1036 referenced code/design/source/metadata/private-copy/group pins using SHA256 and bytes only. NPZs/ZIPs were hashed as opaque bytes, never parsed as financial arrays.
Seal failures: []

All full path/blob/pin/ref details are retained in final-protection.json. External differences, if present, are evidence only and were not rolled back. Native PDF compilation/visual checks/publication are outside this task.
