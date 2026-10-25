# v12 复现与检查

权威入口为 revision-v12；四份可编辑文件在 `submission-v10/`。原生源ZIP经独立解包编译，正文20页、补充36页、标题页/附信各1页。编译无需私有金融输入或原始本地Git历史。全部58页以逐张实际查看，或与已看PNG精确逐字节相同的方式完成视觉核验，见 `final-visual-qa.json`。

## 设计和数值运行

F1、F2、F3各有独立本地设计提交，并在第一次数值计算前各自公开为一文件提交；精确字节、提交时刻见 `design-publication.jsonl`。执行器源码在运行前本地封存，三个运行目录的 `code-seal.json` 保留相同六份源码SHA。计算没有下载新数据，没有改旧结果，没有重试失败格。F1有限菜单oracle排除无穷惩罚，只作事后诊断。

实际研究命令使用临时uv环境，固定NumPy2.3.5和线程数1，入口为 `python -B run_v12_studies.py F1`、`F2`、`F3`。不要在已封存输出目录重新执行：目录和失败缓存是单次不可覆盖的记录。金融重放需要原始私有FX文件和记录的其他输入字节；数据指纹与原路径见协议、`input-preflight.json`及`v12_inputs.py`。此处没有提供跨机器自动定位私有文件的承诺。

描述统计入口为 `report_v12_descriptives.py --run`，在F3完成后只运行一次；原样脚本副本和输出保存在 `results/v12/descriptives/`。该副本可以显式指定 `--root`，输出必须选未存在目录。均值、样本SD、经验秩和汇总口径见metadata；它不拟合模型，也不重跑预测。

## 测试和文件完整性

`final-tests.json` 保留完整实际命令、线程环境、时间、返回码及日志摘要：1904 passed,1184 subtests passed。入口为固定临时环境下的 `python -B -m pytest -q -p no:cacheprovider`；不往系统Python安装依赖。该全套测试在保有旧原始Git对象的工作库通过。原有三份历史对象仍是legacy检查的必要条件；不要把此结果说成不含历史对象的全新公共clone已通过。

`final-source-integrity.json`核对2095份既有科学文件、18项执行代码封印、50项新正文事实/数字和1324项描述数字绑定。三个旧表的数值行、菜单原文、七段局限原文和移动的FX段均保持字节。数据表的排版副本仅加宽一个列宽；旧菜单完整表仅缩小行距并将原样表注移到表前。

## 原生投稿包

实际命令为 `notes/v12/build_native_package.py --run native-pass4`（临时uv/pypdf环境）；Tectonic编译四份源，Poppler逐页渲染。结果见 `final-native-build.json`；编译器在视觉确认前的原回执另存 `native-pass4-build-before-visual.json`。正文新增低频文字已内联，使未修改的写法统计器能计入全部段落。最终指标见 `writing-acceptance.json`。

旧版本构稿器会覆盖人工修订，禁止用来重建当前正文。本文没有执行投稿，也没有填写作者、ORCID、资金和利益冲突信息；按用户最后要求删除当前AI声明。

## 发布方式

终端Git推送没有可用凭据，GitHub连接器写入返回403，因此使用已登录的本机GitHub页面，只提交revision-v12。每批均从远端Git读回字节核对；设计提交在计算前已经单独公开。原本地研究提交历史保留为本机 `.scratch/v12/original-local-history.bundle`，不上传可能含本地身份信息的历史包。浏览器提交保留内容，不保留原本地研究提交的ID/时间；两套身份在回执中分别标注。最终以完整Git树和分支HEAD一致为接收条件，不声称普通git push命令成功。
