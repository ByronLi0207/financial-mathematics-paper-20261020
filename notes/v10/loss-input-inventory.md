# v10 E0 saved loss/prediction input inventory

本轮只做既有逐点输入的元数据盘点，未下载新金融数据、重拟合、预测、派生或汇总 loss、运行 MCS、计算成本，未改旧目录或旧 Git。只写新 v10 的本说明与同名 JSON；未拷贝私有输入、未提交。

核心请求范围可用文件为 **407 个唯一完整 evaluation NPZ，58,430,911 字节**，精确原路径、SHA256、字节数与拟议 scratch 目标见 JSON 的 `minimum_core_private_copy_manifest`。全部旧产物扩展合集为 506 个唯一文件、63,245,545 字节；包含重叠全前缀、周度旧回溯与固定 λ 描述路径，仅供设计裁定，不能自动新增 MCS family。所有 1,006 条方法别名已核对完整 origin 区间和核心数组 shape，其中 782 条别名还与公开逐文件 trace hash 一致。其余仅记录当前文件 SHA256，不冒称已对没有公开的逐文件哈希完成比对。

必须保留 **12 个不可用方法槽**：D1 六个 NA、Treasury H24/W260 两个 ACI 验证不合格，以及 FX W720/H6、H24 在原评估与早期 2015 两个时期的四个 R3 失败。无 pinball 的已保存 C/B/Y 只记录设计后的派生计划；未实际派生。已有组合方法也只记录来源依赖。E3 与 E4 均须各自 design 单独提交后，才能开始各自运行。

Metadata only. This report records existing file paths, schema, hashes, origin indices and public receipt status. It does not contain new loss, performance, MCS, or cost results. Old files/Git were not modified. No financial data download or model refit occurred. E3 and E4 each require a separate committed design before running.

| Family | Complete saved method alias rows |
|---|---:|
| original | 90 |
| QR4 | 8 |
| Levy | 8 |
| mature_baselines | 18 |
| ACI_SAV | 22 |
| E3_extended_menu | 8 |
| panel_legacy | 192 |
| panel_E5 | 96 |
| E6_reference | 16 |
| E6_fixed_lambda_path | 12 |
| R6 | 512 |
| R6_original_structure | 4 |
| daily_FX | 12 |
| full_prefix_FX | 8 |

## Periods and clocks

- Original FX: source has 18576 records. Evaluation origins11927..18551 (6625), 2016-01-01 00:00..2017-01-23 00:00, H6/24, W720/2880. Source timezone unspecified; H means subsequent recorded observations.
- Early2015 FX: R6 evaluation8999..10438 (1440), 2015-07-15 00:00..2015-10-06 23:00, H6/24, W720/2880.
- Treasury and12 panels:706 aligned dates; eval405..681 (277), 2021-01-06..2026-04-22, H6/24,W52/260. Each panel raw CSV has707 rows and is aligned without imputation to the706-row Treasury grid.
- Existing R6 weekly retrospective:253..304 (52), 2018-02-07..2019-01-30, W52 only. Kept as a distinct old artifact.
- Same-record dailyFX:930 nonempty source days; eval405..905 (501), H6/24 subsequent nonempty day observations, W52/260. All12 F/QR33/QR4 slots complete.
- Existing WP5 full prefix:3071..10438 (7368), 2014-08-04..2015-10-06. F_matched/QR33/QR4 useW2880; F_rolling720 usesW720. This overlaps all early2015 R6 origins and is not a third independent period.

## Available vectors and recovery boundaries

- Original QR/KNN/SCALED_KNN and rolling/frozen F/S/K, with declared one_state variants, have stored per-origin pinball and C/Y/B.
- QR4 and Levy have saved C/Y/pinball but no floor. Their exact origin axes match original reference files; B can be read from saved frozen_F_floor after E4 design. No B is derived here.
- ACI/SAV store capacities/peak/floor. The12 legacy panel files store origins/peak/floor/frozen_F/Levy_L/QR33/C2_QR4; E5 additionally stores QR33_plus and I. These do not store per-origin pinball. Derive only after E3 design.
- E3 expanded-menu QR33_plus, E6 I/F references, fixed-lambda primary paths, R6 selected rules, dailyFX and WP5 all have immutable saved vectors. Public hashes were checked where supplied.
- E4 mapping: C=capacity or capacities or method-named prediction, B=floor=abs(N_t), Y=peak. R6 also stores strict_breach/overrun/unused. No headroom/excess/breach/cost computation or mean was performed.

## Explicit unavailable method slots

- D1 FX W720,H6/H24 FHS and PEAK_POT:4 NA slots. Each partial trace has240 origins11927..12166; GARCH convergence/admissibility failure. TreasuryW52,H6/H24 PEAK_POT:2 NA slots and zero-length partial trace; top-ten-percent has fewer than20 rows. Never score a partial subset or rerun.
- ACI_F and ACI_QR for TreasuryH24/W260:VALIDATION_INELIGIBLE and no evaluation vector. The other22 ACI/SAV slots are complete.
- R6 R3 for FXW720,H6 andH24 is FAILED/REQUIRED_VALIDATION_CANDIDATE_FAILED in BOTH early2015 and original evaluation:4 explicit failed slots. Other R6 rows and shared-trace aliases remain visible.
- Previously reported deterministic combinations have112 public rows:64 COMPLETE and48 NA. MEAN_F_QR can be recovered from existing C via F/2+QR/2; MEDIAN_F_QR_KNN needs original plain KNN, unavailable on panels. No per-point combination predictions/losses are saved. Inclusion/recovery must be specified by E3/E4 design and was not executed in E0.
- CFTC is NOT_ACQUIRED_NOT_EVALUATED. No original financial prediction may be rerun to fill a missing method.

## Minimum private copy proposal - not executed

The JSON minimum_private_copy_manifest provides exact source path, bytes, SHA256, and proposed NEW .scratch/v10/loss-inputs destination for every unique required complete evaluation NPZ. Copy only those files after root review. Do not copy all old scratch, R6 validation/inner-fold files, fixtures, or public summary archives. Raw FX/NYFed source copies are optional for date/provenance audit; saved C/B/Y and loss vectors suffice for E3/E4. Public receipts already belong to the inherited public tree and are listed by exact source path.

The JSON is the full machine inventory. Complete-grid eligibility requires receipt status, the original full origin grid and targets, available C/B/Y, finite full vectors checked only in the separately frozen run, and explicit missing statuses. Do not shrink grids or omit unfavourable methods. Repeated rule aliases sharing a trace hash are preserved.

Inventory counts: {"saved_method_alias_rows": 1006, "unique_complete_trace_files": 506, "unavailable_method_slots": 12, "reported_combination_rows": 112, "reported_complete_combination_rows": 64, "copy_bytes": 63245545, "file_hash_or_origin_structure_mismatches": 0}

Additional metadata checks: all1006 saved method aliases match their declared full origin interval and core array shapes. Public per-file trace hashes were checked for782 alias rows; the remaining files have their observed SHA256 inventoried but no per-file public hash supplied by the owning receipt. R6 series_key PDPOSGS-B is explicitly mapped to normalized_source nyfed_weekly without dropping either identity. Daily eval timestamps: 2015-05-24T23:59:59.999999 to 2016-12-27T23:59:59.999999.

Scope refinement: `minimum_core_private_copy_manifest` is the strict requested core copy subset (407 unique files, 58430911 bytes). The larger `minimum_private_copy_manifest` is the union including supplemental overlapping full-prefix and weekly-retro periods plus published fixed-lambda paths. Per-method/per-file scope tags distinguish these by declared period/method role; no performance-based filtering occurred. Supplemental records do not automatically authorize a new MCS family.
