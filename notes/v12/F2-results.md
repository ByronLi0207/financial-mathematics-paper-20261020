# F2：验证期长度结果

实际计算 17.460 秒；136 个计划方法格，132 成功、4 数值失败；全部 17 合约均通过事先资格审查，无资源删减。已完成的 F1 预测缓存直接复用，不重新估计。

|方法|历史长度|完整配对|52周中位超额损失|156周中位超额损失|两中位数之差/百分点|只有截距选择数（52→156）|V1|V2|
|---|---:|---:|---:|---:|---:|---|---|---|
|QR33|52|17/17|+19.335%|+4.031%|-15.304|4→10|SUPPORTED|SUPPORTED|
|QR33|260|17/17|+10.348%|+0.525%|-9.823|4→5|SUPPORTED|SUPPORTED|
|QR4|52|16/17|—%|—%|—|2→7|UNDETERMINED|UNDETERMINED|
|QR4|260|16/17|—%|—%|—|2→4|UNDETERMINED|UNDETERMINED|

主模型 QR33 的 V1=SUPPORTED，V2=SUPPORTED；两种历史长度均达到预写阈值。QR4 存在失败，固定总体判断为无法确定，不能用16对成功子集替代17对合约。

失败格：
- `F2-cftc-042601-original-H6-W52-V52-tau0.95` / QR4: NONCONVERGENCE。
- `F2-cftc-042601-original-H6-W52-V156-tau0.95` / QR4: NONCONVERGENCE。
- `F2-cftc-240743-original-H6-W260-V52-tau0.95` / QR4: NONCONVERGENCE。
- `F2-cftc-240743-original-H6-W260-V156-tau0.95` / QR4: NONCONVERGENCE。

延长验证期同时改变其历史覆盖，不能把结果解释为增加独立样本数的因果效应；验证标签仍然重叠。此结果属于已看过评估期上的事后诊断。

来源：`results/v12/validation-length/predictions.json` 的 `/methods/*/by_window/*`；逐格 `rows.json`，原设计 `protocol/v12/validation-length-design.md`。
