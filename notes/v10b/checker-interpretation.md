# 冻结写法计数的解释

沿用notes/v9/measure_writing.py与writing_check.py原代码，不改词表、分句或分母。用户本轮要求的三项是flagged<=8%、mean<=20、0>40；按原字段原样报告。

精确Supplement引用使旧v9额外FORBIDDEN列表的S1/S2/S3触发。这些均为“Supplement Sections S1–S2 / Figures S1–S2 / Sections S3–S5”文献内定位，非已禁止的实验成功标准代号；本轮用户明确要求精确节表图。旧额外no_forbidden_body因此不能静默标PASS，也不能为消警报删掉正确定位。最终JSON保留原raw报告，另按上下文逐项注明合法crossref，三写法门槛独立验收。
