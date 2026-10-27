# H8 ASMBI 最终构建与视觉核验

UTC：2026-10-27T05:32:44.188110+00:00。**结论：四份交付PDF与源码ZIP独立编译均通过；ZIP复编的8张主表页有轻微排版差异，已另行直接查看并明确披露。**

Canonical主文SHA：`b46b1ba919fe8d3f89306128aef0f610ad269ff3576d74412465834681b49fa3`。没有修改canonical、科学结果、QF或其他代理报告，没有运行研究计算、提交Git或另派代理；旧失败预视觉报告完整保留。

## 修复内容

- 三个确定叙述引用由Bib与已核实官方元数据推导作者显示名：Lee and Kim、Pagnottoni、Muddana et al.，接数字上标13/14/15。作者/DOI与canonical Bib严格核对；未知key或作者不符即失败。逆向转换必须恢复canonical引用语法，其他文字不变。
- 标题页改美式`license compliance`；自动叙述字数4,122、5关键词及范围说明完整一页。
- cover改为读取当前canonicalH6正文逐字保留，包含最新preprint政策、GitHub工作版本/PR披露和作者确认占位，实际为一页。

## 四份最终PDF

| 文件 | 页数 | SHA-256 |
|---|---:|---|
| [submission-package/ASMBI/manuscript.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/manuscript.pdf>) | 26 | `b394bd394b09345c73570e999d50839b6ca7293e14887b9266ebff07610b665d` |
| [submission-package/ASMBI/supplement.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/supplement.pdf>) | 54 | `15d52857f18e21d98222711f5f360cb4b67d3c44f069d79ebf0374b7b9142ba6` |
| [submission-package/ASMBI/title-page.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/title-page.pdf>) | 1 | `61dae5a525b2f33af74bd2abe4b1bb459afd573e661da807624f4ab394cbeda4` |
| [submission-package/ASMBI/cover-letter.pdf](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/cover-letter.pdf>) | 1 | `681162e8949f9f3b085ab3d03c8a7b5d5e7254183f64e80c0873599df3f0ff50` |

构建命令：`python3 notes/submission/build_asmbi_package.py`；编译仅用缓存`tectonic -X compile -C`。

## 最终PDF的逐页视觉覆盖

- 共82页。相对H5必要变化页为正文3、5，补充51，标题1，cover1，这5页全部实际原图直接查看。
- 另直接查看正文19以和ZIP独立编译比较。因此最终交付PDF为 **6页直接查看＋76页精确PNG继承**；77页本身与H5相同，其中p19额外直接看过。
- 主文其余页的继承来自此前实际直接查看的H5切片；补充继承保留H5报告及其H2原始直接查看的完整SHA链。绝不以相似外观代替精确字节身份。

| 文件/页 | 方式 | 观察或继承依据 | PNG SHA-256 |
|---|---|---|---|
| manuscript 1 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6a2aad8ad57d8bb2d107f9ef8cc24e44d752b8d29d221098f2e550b289c8760d` |
| manuscript 2 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `3b5fe2579fb60481d5d2cb6434bec4c00539af54925e5d1b42bc9ff3b4760c6e` |
| manuscript 3 | 直接原图 | Lee and Kim with superscript13 develop; Pagnottoni with superscript14 studies; Muddana et al. with superscript15 use. No author? or duplicated years; target equations and paragraph layout intact. | `c1ba3870ae2f84c1291b307d49b73ab17dc952545066934ee0cb2fd34f7e8826` |
| manuscript 4 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `ba58f84556b50b06f70bd7f7959219785648b535c6cfce3e5b0812fce0f0ae0c` |
| manuscript 5 | 直接原图 | GARCH expansion followed by and drawn is grammatical and readable; equation/menu/remaining method text intact without clipping. | `fd2d38e4ca76132d5d89f34bca2b5c2daa71f9be6f53a1e13a24295043d063dc` |
| manuscript 6 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `bbead846ac0016d1d2462a2257494ee8a91aabc17f7b85bede52ea730eae3ae0` |
| manuscript 7 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `935a1361cd5020713d017d3e2ac34f9e12908031521bf866653cf16e0f196eb1` |
| manuscript 8 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `b719dc776228f14fb607610fd901c0325afb693dd50ce8f07f15ed5ef7064cb6` |
| manuscript 9 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `467f072f431f6c4c3a1fc9220bdd466814e6e0bede686a81b53325d54c6b1bc8` |
| manuscript 10 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `3f1dda05af97bec34a6d793713492aab425af6c41442e565855a150b01560d5c` |
| manuscript 11 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `afb02564bc4ff38d0e8454bba7933a77143ffe0ae585c5564c42bf57385f5ff0` |
| manuscript 12 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `fc00b9ba4df9a5555d6bfe2ac86f82afed12031ded72e86d52a54d47c9d5581c` |
| manuscript 13 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `045a71eaab55af0252dd355c7c0a59cf07f12c711677c35d3eb7a8e4abd873f2` |
| manuscript 14 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `39a32df054f06b8f7c766bc58689970a1f3ae1a69a3ecb89821bbafa3e7a43e1` |
| manuscript 15 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `7f4305f32635f1b1963f25f3b78705722e13522d526614054f5622e8812f025a` |
| manuscript 16 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `ec8fb5c0b8f6aa67a5d358e4d441aa54ebc131273a4e478394308fe5874e25f9` |
| manuscript 17 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `794144dd1966429b6fbab78f4a3a313023a254f90a322ce0cc14c76470ff6e6e` |
| manuscript 18 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6480e80cdfd03e49b29c926bba126f92e67cdbd321775f2272c0ae34f5949561` |
| manuscript 19 | 直接原图 | Extra direct comparison with independently compiledZIP Table1: complete4study rows/4columns, all captions and wraps readable. Current final image also exactly equalsH5. | `b4c50eae72e2a331273bbef4dc29ad6a783ac2714c957dbd2c93b0269500011f` |
| manuscript 20 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `c299f57bbd75df127923e58451122c737bc890fd5e068f2ab424fbe0581c15bb` |
| manuscript 21 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `5956fb3b4dcea5a81968100dd28234dfc775a7f5854ab7500719473b0a571f09` |
| manuscript 22 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `42a80806eead1d0492a872b627675a21bb748fc87d3f16937b198eb7a8c86ad8` |
| manuscript 23 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `19999a14fcb5dd3dbd28dd4fa96d1c6a4da858e3089190d68c12c639d4b5d8e1` |
| manuscript 24 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `cf7c36d72d73d5ed2c50654ecb16091816c1ebdec6d3df9f71389e73ef6ffb59` |
| manuscript 25 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `37bdeccf97a94dde64b3c08a7cac7dd3e338eed3abe7c9b8fb315684db6f76f2` |
| manuscript 26 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `197162f98ea26a82a9018b0e73264ec60198d60ff5e7bc7027a07199a9057d2f` |
| supplement 1 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `57b0e6fd3bfdb94fdae8a30be6c81268e0cfe9aff28085d1c8ae139cddd1fd74` |
| supplement 2 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `27dc65cd1fa5c8f9a028fcd350261cdc6d297ec56907a0786e36ea06f7fbeae9` |
| supplement 3 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `714bfc8d7ef29e3d288b6d7f7674f0fb8dd92f0a3c1a56f4b3702c846bcee105` |
| supplement 4 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `221c4b81ad5233f5c9619c8abadb5f794b1ab86f8eb2ebbe0881f17f12e64567` |
| supplement 5 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `b03fd6d33709d63aa90c7b180589e161f5b4a9d71bb8b5f081ae0b66bfab4c6a` |
| supplement 6 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `65b972ac3bb20718ad6564fd4cb3806998feb25148242e733edae80f9f1a21c8` |
| supplement 7 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `27169eb5ed839919e976480e63fc51c999ed55d11d43ec55e6dc9558827aa8a6` |
| supplement 8 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `60fbfcad24f7e4719be25744a1d479d64b388d3dc5fb00086b60ab4e96424b22` |
| supplement 9 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `919751971da1d96740f620d98e6a31ede1b44519d656978e2c1935176a828405` |
| supplement 10 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `7406cb0a77351c6e17b1b5125ebce8c013c1a2be05a8f04f8f20a6107dd4f83b` |
| supplement 11 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `735e403ec0eb98ae69c4479b1e684e1c74704307e46402e378dc52f6486bf106` |
| supplement 12 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `64d27d6631139ff786fb29565796211b26b3bb4fa6c095f012a082dfde0278d9` |
| supplement 13 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `e47654f2a2c8d6d48fb06ea0a462bb45f9cc64fe55dd798d41e43b97d619d60a` |
| supplement 14 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `d7ee5bc04d9624a381631409c31784582d59fee7fbb50f1585479d09cabae22a` |
| supplement 15 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `17c3503642e05a5aa2ca1ba69dace4a334557f9016d83186de92d5972d8fb47c` |
| supplement 16 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `3ac2a4ca00b6609e898385e9236e127f791a2dd5230ddce946142bccabe2b293` |
| supplement 17 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `c3d66730c70b18d8fd7ed902a4b39d158411fba7a59b78ad346a0453d85f1cea` |
| supplement 18 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `9ad70ec194758f5b5761bceded5b46e28195a0740955d299d500682ab291055b` |
| supplement 19 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `e2e89c17bba5f3e531f5a668991831e61ed864a7c8fcd864bcb265c6433ead57` |
| supplement 20 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `0df154592da30d335974b225afe46fa4e927d3da6553b098ea70f1a5284f5a7d` |
| supplement 21 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `190f312213889e384898a41e6f8f542afcb6026e70c892f9da47d45a090ff24b` |
| supplement 22 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `e4eec0ea066deefb6816ebee62d3c6eda26faec7d3ab3a9a00906ffa21042dd3` |
| supplement 23 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `e82236e8d43a6e2f44e5aa01d0088991820ca97351dd895545cb5b28634c409d` |
| supplement 24 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `477afe8ca7fd199494dc7250341c05c65d64d3e81ead59b60f066624484cc6f5` |
| supplement 25 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `97c10bd3785d7bf140c65832451461f7ab0c4625fc4bf034a37141b6fa246c64` |
| supplement 26 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6367184c768e4afb20c4cf2acc80dffd99575d20c9100a53dfdbb4b0bb165b00` |
| supplement 27 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `852844a590b29afc39938d00a4f60b587c4f67b801600cafb97281869378bf88` |
| supplement 28 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `99e3ed7837125063efe730d976f853aea621a8ddfbfe3985867786127b50c4ad` |
| supplement 29 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `eac7fe07157584776c1376be7e676f02d7415404fd97b3aeeaa4a6f7b5167c36` |
| supplement 30 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `169cfa3813ce985e90aa16524debacaa91f2549108e44650e9a2b9003ca42fe6` |
| supplement 31 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `2260deff4ad51658b21c5ff91aa91772836ec84bb5975e8bb30b8edad8976813` |
| supplement 32 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `04c12cce95138ea1ce591e06b96cd6e505f1a3af185d7ee704ed28931a8e42e7` |
| supplement 33 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `9e7e7d44c83aaeaaf02800a8b56d33f439be12c3406dfaad1e1ad54a9a34ec43` |
| supplement 34 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `ce9ecfa107311b8cc7e1e27584cd8bf397b8ad7a873272e22fa69450d2492711` |
| supplement 35 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6954e6061a4698ebaf646e73296b5b232267b7cd209aee305b1e6ba56b5ab741` |
| supplement 36 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `0866ca1e18541ee08d7e4ed61adaecbe16cfa8d22f02b522e869c0792e6584ff` |
| supplement 37 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `4c343315bf7877fc556c1d0387c58c0fb35eb798a014e4f851993bdc9fa1a3e8` |
| supplement 38 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `44a917e6ad8f25239cfba3f002501fc272e781ef97b30e0f8a1ae776e485a1bc` |
| supplement 39 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6543804db77ff44854bf717d2a9c0783fc1c0ae6889dda9e6d2ac6a5b93f32a0` |
| supplement 40 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `b746ce45e2ec7f0bb282b11de7c9ccdc3c8c7b100345acab194d314adaf84445` |
| supplement 41 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `f15cd51f05ae72a02a37f239ae09cd89ac5510119e6c339b1b54fe005d6265bb` |
| supplement 42 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `bcc1a7f0ead9b3122bb805bb2c196f0384417cce35c508c1116b0e5e7f5c01c4` |
| supplement 43 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `1a98d52b65e2845b383d97fda73798e16b6ad66d54447085b8a4faee1ab9dacf` |
| supplement 44 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `4d33116b5563fb3e0d8f60d7d8a60c43f05c1fdd6aee5efda739faf0793da7bb` |
| supplement 45 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `6d4152d154a18ae6391d353637bc160c05dbec96940bbeb6c9107c9fc8acc22d` |
| supplement 46 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `087bb55fc0a8ef8d8041125efb6008a8d581f7fbee29a421069fd82869dbfb6a` |
| supplement 47 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `96e2099312182cea8c8dc16ad2d26b09df8ce679c0117f7a00c4a5086e1d1ad3` |
| supplement 48 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `cf3b50bcb945241d64aa8edc9df1ce47eb0e9a0294e1a5eaa370903785b77d40` |
| supplement 49 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `2e86df8bdf5bf14586fdf0246d91d72e47596364986392800e88267a5b8a0eb0` |
| supplement 50 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `e4c5ad3bb7ada57280d77182b735594feed55d68becc061e51e3211f7dfbd989` |
| supplement 51 | 直接原图 | S54 continuation retains final3WP2 and7QR4 rows, unsupported/undetermined statuses, then references. Old H2aux/H8-check production sentence absent; remaining provenance note and references clear. | `79560878df02f9c7b7a0242ac79993a709b4e816e54ba83f21eccb2cf2b2865a` |
| supplement 52 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `f8c387fbb3b1a49f2bd4800b7b727279397f495340aff0a4429d2f949f7490de` |
| supplement 53 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `9de21a01258727f5564ddbf31cf856be80a912e95cd9a1cfd16a0f08d7d648a9` |
| supplement 54 | 精确PNG继承 | 与H5原图逐字节相同，记录完整已实际查看的来源链。 | `22a26c1175226557f46be53685ceb465fc848de41e95e9352b33ac4230b48a46` |
| title-page 1 | 直接原图 | Onepage shows4,122 and frozen count scope,5keywords,American license compliance,all expected author/permission placeholders and data/code statement. | `824c7cac595a4ed847db528fc797306bed4b7b7e0d7ba725322794e036cacfac` |
| cover-letter 1 | 直接原图 | Onepage has3currentH6paragraphs: findings with adverse cases,officialscope quote,preprint policy/public-version inventory and author-confirmation disclosure. Links/line wraps/signature placeholder fit. | `1b4b4f05fc71bea0f1d967bc544cf78aad2b823860e0786bbdee8bb8cbeceec7` |

## 源码ZIP独立复编

- [submission-package/ASMBI/ASMBI-source-and-pdf.zip](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/submission-package/ASMBI/ASMBI-source-and-pdf.zip>)：51成员；CRC通过，全部成员与本地对应字节一致，包含的四个实际TeX目标全部独立缓存编译成功。ZIP SHA：`e215a64adb06e154f985ae2bab023af4b382b0fce60af98b5fc7a800f21a5c7f`。
- 独立编译页数仍为26/54/1/1，全部82页去空白文本与交付PDF完全一致。
- **74页PNG完全相同**；主文p19–26八张后置表存在轻微行距/垂直位置差异，不能声称82页像素相同。该8页已全部实际原图直接查看，表格、数字、正负号、NA、全部行列和注释完整，无裁切/重叠。其余74页按精确PNG身份继承最终PDF视觉覆盖。
- 独立编译与日志/渲染回执：[.scratch/submission/asmbi/h8-final-1793078627894/zip-recompile/verification.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/.scratch/submission/asmbi/h8-final-1793078627894/zip-recompile/verification.json>)；最终对比：[.scratch/submission/asmbi/h8-final-1793078627894/final-verification.json](</Users/bingyouli/Research/论文/金融数学论文-v10-20261024/.scratch/submission/asmbi/h8-final-1793078627894/final-verification.json>)。

## 关键验收与限制

- p3作者名和上标正确，Pagnottoni studies单数动词正确；四PDF均无`(author?)`。p5 GARCH and drawn并列语法显示正确。
- 补充p51制作阶段H2aux/H8-check句消失，S54失败/无法判定和QR4敏感性行保留，参考文献衔接清楚。
- 标题页4,122和American license；cover当前3段政策披露一页，均直接查看。
- 四最终日志均0overfull、0missing character、0undefined citation、0undefined reference。已有underfull和缓存字体尺寸/形状替代告警如实记录，未把它们写成零；图像可读性已经直接或精确继承核验。
- 原Wiley class/BST与官方模板字节保持一致。实际PDF是官方允许的FreeFormat＋官方AMA BST；原NJD离线缺依赖限制仍披露，不称原样NJD已编译。
- 作者/联系方式/声明/权限/DOI/软件许可确认仍是预期个人占位；本报告不等于外部投稿或远端发布验收。

## 封口记录

最终报告写入后停止写入。后续任何源、PDF或ZIP变化须绑定新SHA重新核验，不能无条件继承本PASS。
