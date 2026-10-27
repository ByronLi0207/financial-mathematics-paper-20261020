# CFTC TFF 官方来源核对（E2 数据访问前）

记录生成 UTC：`2026-10-24T22:08:17Z`。既有网页访问日期 UTC：`2026-10-24`。网页工具没有逐请求精确 UTC 时间，本记录保留日期精度，不补造时间戳。

**状态：只核官方说明、字段和索引链接。数据请求 0；数据下载 0；真实数据统计 0；未检查压缩包内实际表头、数据值或完整性。** 本记录不构成 E2 设计冻结，也不授权数据访问。双模型复审关闭。

本任务只新增本 Markdown 和同名 JSON，不修改设计文件、不提交。主代理另行决定并提交 E2；主代理告知将采用 Futures Only，2010 年 1 月起的候选覆盖方案是官方 2006–2016 历史包加 2017–2026 年度包，本记录不把候选方案写成已验证覆盖。

## 访问证据与证据边界

- 仅对官方历史索引 HTML 的 Python `urllib.request.urlopen` 请求返回 `HTTP Error 403: Forbidden`。该失败不是对 ZIP 发出的请求。
- 同一 URL 通过正常 IAB 浏览器成功显示 Historical Compressed 页面；只读 DOM 读取了两个 TFF 表的链接属性。没有点击、导航到或请求任何 ZIP。
- 官方说明、字段和公告通过 web 的搜索、打开、查找工具核对；搜索摘录不能证明压缩包内部内容。
- 官方 ZIP 链接以下仅供 E2 设计记录；本轮未下载，也没有验证 HTTP 成功状态、解压、表头、周数或缺失值。

## 已核官方来源

| 来源 | 直接 URL | 本次核对范围 |
|---|---|---|
| `history_index` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm) | 年度索引、2010 起始标签、2006–2016 历史包；只读取 href。 |
| `tff_fields` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalViewable/cotvariablestfm.html) | 传统逗号分隔文件的静态变量说明；不是实际包内 schema 验收。 |
| `tff_explanatory_notes` | [官方来源](https://www.cftc.gov/idc/groups/public/%40commitmentsoftraders/documents/file/tfmexplanatorynotes.pdf) | 分类、spreading、交易者计数、历史分类回溯及限制；说明文档不是数据文件。 |
| `cot_main_faq` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) | 周二/周五一般规则、少于20名报告交易者的退出机制、历史发布日期缺口。 |
| `cot_explanatory_notes` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes/index.htm) | OI 双边恒等、Combined 的 delta 换算及百分比分母。 |
| `release_schedule` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm) | 2026 暂定发布时间表与节假日顺延。 |
| `special_announcements` | [官方来源](https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalSpecialAnnouncements/index.htm) | 2018 Monday 观察日、2023 ION 延迟与微型合约整合、名称变更。 |
| `shutdown_2013` | [官方来源](https://www.cftc.gov/PressRoom/PressReleases/6745-13) | 2013 停摆后的补发。 |
| `shutdown_2018_2019` | [官方来源](https://www.cftc.gov/PressRoom/PressReleases/7864-19) | 2018–2019 停摆及 Monday 持仓、延迟发布。 |
| `shutdown_2025_updated` | [官方来源](https://www.cftc.gov/PressRoom/PressReleases/9147-25) | 2025-12-09 更新补发计划；取代11月旧计划。 |
| `web_policy` | [官方来源](https://www.cftc.gov/WebPolicy/index.htm) | 政府信息 public domain、请求注明 CFTC、第三方材料例外。 |

## 字段与测量对象

静态官方字段表给出以下准确变量名和位置。**实际数据表头尚未检查**，尤其日期列 `Report_Date_as_MM_DD_YYYY` 是说明页原文名称；不能提前认定每个历史包都严格使用该名称。下载授权后若有差异应记录和明确映射，不能静默丢列或把 API 字段名混入传统文件。

| 位置 | 官方静态字段名 | 用途 |
|---:|---|---|
| 1 | `Market_and_Exchange_Names` | `market_label` |
| 2 | `As_of_Date_In_Form_YYMMDD` | `position_date` |
| 3 | `Report_Date_as_MM_DD_YYYY` | `position_date_static_document_name` |
| 4 | `CFTC_Contract_Market_Code` | `market_identifier_preserve_as_string` |
| 5 | `CFTC_Market_Code` | `market_code` |
| 6 | `CFTC_Region_Code` | `region_code` |
| 7 | `CFTC_Commodity_Code` | `commodity_code` |
| 8 | `Open_Interest_All` | `market_open_interest` |
| 9 | `Dealer_Positions_Long_All` | `dealer_category_residual_long` |
| 10 | `Dealer_Positions_Short_All` | `dealer_category_residual_short` |
| 11 | `Dealer_Positions_Spread_All` | `dealer_category_spreading` |
| 59 | `Traders_Tot_All` | `total_reportable_trader_count` |
| 60 | `Traders_Dealer_Long_All` | `dealer_long_count_not_individual_identifiers` |
| 61 | `Traders_Dealer_Short_All` | `dealer_short_count_not_individual_identifiers` |
| 62 | `Traders_Dealer_Spread_All` | `dealer_spread_count_can_overlap_direction_counts` |
| 82 | `Contract_Units` | `contract_unit_label` |
| 83 | `CFTC_Contract_Market_Code_Quotes` | `quoted_contract_code` |
| 87 | `FutOnly_or_Combined` | `report_type_marker_actual_values_not_inspected` |

研究者可定义 `dealer_category_net_contracts = Dealer_Positions_Long_All - Dealer_Positions_Short_All`，但它不是官方直接提供的 net 列。本轮未计算。TFF 的配对方向仓计入 spreading，long/short 是剩余方向仓，净差中 spreading 抵消。[官方 TFF 说明](https://www.cftc.gov/idc/groups/public/%40commitmentsoftraders/documents/file/tfmexplanatorynotes.pdf)

TFF 是市场内按交易者类别汇总。Dealer/Intermediary 不能拆成可识别的独立 dealer 样本，long/short/spread 的交易者计数也不能直接相加为独立样本数。分类、主体及历史回溯均有边界。

Futures Only 的量是合约头寸。Combined 先把期权按 delta 换算成期货等价头寸再相加；若使用 Futures Only，可避免混入该换算变化。整个市场的 long OI 等于 short OI，OI不应理解成把两边相加的两倍量。原始合约数不是跨市场统一的美元风险；是否除以 OI 或另作标准化需由 E2 冻结。[官方 OI 说明](https://www.cftc.gov/MarketReports/CommitmentsofTraders/ExplanatoryNotes/index.htm)

与 NYFed 比较时，应说明这是 CFTC 类别聚合期货净持仓的外部检验；不是配对的同一 dealer 样本、个体双边头寸或完整资产负债表库存。本次没有查阅非 CFTC 来源，NYFed 的单位和覆盖主体必须由其自己的官方来源另行支持。

## 索引中的年度与历史链接（未下载）

以下所有年度链接均从官网已显示的 HTML 锚点核对。2010 的文字标签为 **Starting July 20, 2010**，因此2010年度包不能被当成已验证的全年覆盖。索引介绍文字与该标签并不完全一致，不能静默忽略。

| 年份 | Futures Only Text | Combined Text |
|---:|---|---|
| 2010 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2010.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2010.zip) |
| 2011 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2011.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2011.zip) |
| 2012 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2012.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2012.zip) |
| 2013 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2013.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2013.zip) |
| 2014 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2014.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2014.zip) |
| 2015 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2015.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2015.zip) |
| 2016 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2016.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2016.zip) |
| 2017 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2017.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2017.zip) |
| 2018 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2018.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2018.zip) |
| 2019 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2019.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2019.zip) |
| 2020 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2020.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2020.zip) |
| 2021 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2021.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2021.zip) |
| 2022 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2022.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2022.zip) |
| 2023 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2023.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2023.zip) |
| 2024 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2024.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2024.zip) |
| 2025 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2025.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2025.zip) |
| 2026 | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/fut_fin_txt_2026.zip) | [官方 ZIP 链接](https://www.cftc.gov/files/dea/history/com_fin_txt_2026.zip) |

Excel 链接同样已只读核对：`fut_fin_xls_{YYYY}.zip` 与 `com_fin_xls_{YYYY}.zip`；精确 URL 逐年保存在 JSON 中。

官网另列 2006–2016 的独立档案：

- futures_only / txt：[官方链接](https://www.cftc.gov/files/dea/history/fin_fut_txt_2006_2016.zip)。
- futures_only / xls：[官方链接](https://www.cftc.gov/files/dea/history/fin_fut_xls_2006_2016.zip)。
- combined / txt：[官方链接](https://www.cftc.gov/files/dea/history/fin_com_txt_2006_2016.zip)。
- combined / xls：[官方链接](https://www.cftc.gov/files/dea/history/fin_com_xls_2006_2016.zip)。

未发现覆盖2006至2026的单一完整历史包。历史包采用的早期交易者分类有回溯限制，不能把旧持仓视为完整逐期实时分类。是否采用该包及重叠年份去重规则由主代理在 E2 中独立冻结。

## 日期、缺失与范围变更限制

- 一般为周二持仓、周五美东15:30发布，节假日可以改变观察日或发布日期。2018年12月官方通知明确两周用Monday持仓；2025更新表也列出11月10日Monday报告日期。因此不能用“weekday必须Tuesday且日期差必须7天”定义连续周。
- 政府停摆与2023 ION事件会使持仓日和实际可得日相距多周。2013公告宣布从10月25日起补发原定10月4日发布的报告；2018年12月24日持仓的原12月28日发布报告，延至2019年2月1日的计划补发。2025应采用12月9日更新公告9147-25，而不是旧公告9138-25。
- COT FAQ 明确没有完整历史发布日期列表，官网仅有约13个月发布日期。年度包本身不能验证2010年以来每一期首次公开可得时间，也不能证明完整历史vintage回测。持仓日分析、发布日期分析和首次版本验证必须分开。
- 官网FAQ说历史数据发布后不再更新；特别公告又记录修正和重新分类。应保留获取字节、时间、哈希及相关公告，不能声称获得完整逐期vintage历史。
- **2023范围变化：** 2023年5月5日官方公告称，S&P 500（13874+）、Nasdaq100（20974+）、DJIA（12460+）Consolidated Reports 合并其相应 e-micro 合约。此类合并会改变经济覆盖；相同代码或标签不能被直接视为全期固定经济对象。
- `CFTC_Contract_Market_Code` 应保存为字符串，保留前导零和非数字字符。已核说明没有提供“代码的经济意义全历史恒定”的保证。名称、单位、合并范围和官方变更需一起审计，不能自动按相似名称拼接不同合约。
- CFTC 的20名reportable Large Traders是市场披露门槛：低于门槛可退出、恢复后可重进。这不保证20个合约满足研究设计。**冻结筛选后若少于20个合约，报告实际全部合格合约和不足，不降低门槛补数。**

预注册可考虑固定一个全局预期报告周日历，按官方观察日映射到报告周，记录Monday等例外；单个合约缺失仍是缺失，不把缺口两侧拼成相邻周。该项是来源核对产生的设计注意点，本文件没有冻结任何日期范围、连续长度、覆盖率或其他阈值。

## 使用权与后续来源记录

CFTC Web Policy 将其政府信息列为public domain，请求后续使用适当注明CFTC；第三方贡献或许可材料可能另有版权。引用CFTC不等于官方认可或独立验证。[官方版权条款](https://www.cftc.gov/WebPolicy/index.htm)

获准下载后，来源清单宜保留官方URL、抓取UTC、SHA-256、文件大小、报告类别、官方索引URL和来源说明。本轮没有生成数据下载清单，也没有检验任何真实样本、性能或统计结果。
