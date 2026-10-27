# H0 导入审计与决定

基线 `revision-v13`：`8c4b2b1572eea9b8fa6aabf9074a1aa86c2008f6`。只读来源 `final-jof` / PR #6：`6192ec370d131c60d05e9fb103150e0e9db6aa23`。远端开工指向见 [remote-before.txt](remote-before.txt)。

## 通过并导入

- CFTC 历史长度 WP2：设计提交 effa537 先于正式开始 13.372451 秒；739 个保存结果文件与原结果提交 3396aed 全部相同，153 个评价 trace 的 SHA 与回执一致。完整审计与逐字段数字对照见 [wp2-import-audit.md](wp2-import-audit.md) 和 [JSON](wp2-import-audit.json)。
- 17 个原始 CFTC source arrays 已在 v13，字节一致；7 个代码/协议路径原先不存在，其中两项是非原始数据继承依赖。为避免缺失依赖，按审计闭包只读复制 747 文件到 `evidence/submission/final-jof/`，不覆盖既有结果。
- 正文在 FX 历史曲线之后仅加一段；完整判定屏、25 条反例记录及解释在补充 S39；118 个显示字段直接绑定保存 JSON/SHA，见 [imported-number-bindings.json](imported-number-bindings.json)。H2 按实际编译辅助文件核对为 S39，修正了初稿按文本计数误记的 S40。
- 五位候选审稿人机构/方向通过，冲突与是否提名全部待作者确认。名单与十条问答只作为投稿材料；见 [reviewer-audit.md](reviewer-audit.md)、[candidate-reviewers.md](candidate-reviewers.md)、[author-qa.md](author-qa.md)。无人被联系。

## 不导入和解释边界

- 不导入 PR #6 的标题、摘要、改写主线和其他文稿/图；v13 的题名及摘要文本保持逐字符一致。
- WP2 判决保持 PARTLY：P1 为 15/17 与 29/34；P2 为 10/17，未达到 60%；P3 为 6/17，未达到 70%；QR33 高区保持 NOT_TESTABLE。
- 设计只是本地先提交，公开上传晚于运行；不能称为公开外部预注册。W52/W260 已看过，不能称为未见时期前瞻复现。
- 共享核心数字 1,288 项定位/字段、54 个共享来源文件全部 exact；22 个非共同项单列，不把 v13 新增 G 结果说成 PR #6 共有。

## 验证

v13 的原目录和科学结果不覆写。新 canonical 源在 `submission-final/`。H0 正文与补充已用缓存离线 LaTeX 编译；科学档案在 `frozen-science.json` 保存 2,527 个原始字节封条，后续逐项复核。初次完整测试失败一项线程快照；提前固定单线程环境后，1,928 测试及 1,184 子测试通过，原失败完整保留。新分支链接引起的一处正文 URL 越界已改为可点击文字标签。

## 待用户决定

- PR #6 的备选题名 “When Is History Long Enough?”：本轮不采用。
- 审稿人是否提名、与所有作者的关系和机构邮箱仍待作者确认。
