# E2 CFTC：已保存回执报告草稿

本草稿只读取 saved summary、eligibility、splits 与来源 provenance 元数据，不读取 raw observations，不运行筛选、校准、预测或新增检验。

已保存的选中合约数为 17，按 eligibility 的原顺序保留字面 code；不补成20个合约。

T1：支持。完整精度操作数：`{"status": "SUPPORTED", "required_cells": 34, "complete_operand_cells": 34, "simple_better_cells": 29, "fraction": 0.8529411764705882, "minimum_inclusive_fraction": 0.6, "unknown_cells": []}`。
T2：不支持。完整精度操作数：`{"status": "NOT_SUPPORTED", "median_pct_by_window": {"52": 19.334715757564624, "260": 10.34828178946443}, "lower_inclusive_pct": -10.0, "upper_inclusive_pct": 10.0}`。
T3：支持。完整精度操作数：`{"status": "SUPPORTED", "W52_median_pct": 10.280676300222424, "W260_median_pct": 0.2174917571722501, "W260_minus_W52_pct_points": -10.063184543050173}`。

全部所选合约在图轴及主表各保留一行。主表展示 I、QR4、QR33、ACI_F、ACI_QR33 在两 W 相对其自身 F 的变化；F 原始均值、所有绝对评分、breach、惩罚、gamma 和失败槽仍在完整 cells/CSV 中。

图只显示逐合约 QR33/F 的两 W 对照，失败或非正 F 显示 NA；没有成功合约子集的汇总线。所有数字由 saved cells/across_contracts/predictions 直接引用。显示舍入不改变完整精度门槛。

来源状态：ALL_REQUIRED_FILES_DOWNLOADED。下载 vintage 的经济头寸日期与 Monday 模型时钟分开；Monday 标签不代表当时已公开信息。来源是独立于 NYFed 的报告系统，但 futures dealer 类别是聚合数据，contract counts 不是美元敞口。

OI 全历史排名是事后 universe 选择；相关市场不构成独立交易员样本，不进行合并独立性检验，也不作跨合约美元或原始损失聚合。

保存的 split 元数据（原样引用，不推算缺失日期）：

```json
{
  "N": 877,
  "horizon": 6,
  "indices": {
    "validation_first": 553,
    "validation_last": 604,
    "evaluation_first": 611,
    "evaluation_last": 870,
    "validation_n": 52,
    "evaluation_n": 260,
    "unissued_gap_n": 6
  },
  "model_clock": {
    "validation": {
      "first": "2020-08-10",
      "last": "2021-08-02",
      "last_label_end": "2021-09-13"
    },
    "evaluation": {
      "first": "2021-09-20",
      "last": "2026-09-07",
      "last_label_end": "2026-10-19"
    }
  },
  "actual_dates": {
    "validation": {
      "first": "2020-08-11",
      "last": "2021-08-03",
      "last_label_end": "2021-09-14"
    },
    "evaluation": {
      "first": "2021-09-21",
      "last": "2026-09-08",
      "last_label_end": "2026-10-20"
    }
  },
  "training": {
    "validation": [
      {
        "window": 52,
        "first_origin": 496,
        "last_origin": 547,
        "latest_label_end": 553,
        "training_count": 52
      },
      {
        "window": 260,
        "first_origin": 288,
        "last_origin": 547,
        "latest_label_end": 553,
        "training_count": 260
      }
    ],
    "evaluation": [
      {
        "window": 52,
        "first_origin": 554,
        "last_origin": 605,
        "latest_label_end": 611,
        "training_count": 52
      },
      {
        "window": 260,
        "first_origin": 346,
        "last_origin": 605,
        "latest_label_end": 611,
        "training_count": 260
      }
    ]
  },
  "per_contract": {
    "044601": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "043602": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "042601": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "045601": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "020601": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "099741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "1170E1": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "097741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "096742": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "095741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "090741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "232741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "33874A": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "240743": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "092741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "098662": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    },
    "112741": {
      "N": 877,
      "horizon": 6,
      "indices": {
        "validation_first": 553,
        "validation_last": 604,
        "evaluation_first": 611,
        "evaluation_last": 870,
        "validation_n": 52,
        "evaluation_n": 260,
        "unissued_gap_n": 6
      },
      "model_clock": {
        "validation": {
          "first": "2020-08-10",
          "last": "2021-08-02",
          "last_label_end": "2021-09-13"
        },
        "evaluation": {
          "first": "2021-09-20",
          "last": "2026-09-07",
          "last_label_end": "2026-10-19"
        }
      },
      "actual_dates": {
        "validation": {
          "first": "2020-08-11",
          "last": "2021-08-03",
          "last_label_end": "2021-09-14"
        },
        "evaluation": {
          "first": "2021-09-21",
          "last": "2026-09-08",
          "last_label_end": "2026-10-20"
        }
      },
      "training": {
        "validation": [
          {
            "window": 52,
            "first_origin": 496,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 288,
            "last_origin": 547,
            "latest_label_end": 553,
            "training_count": 260
          }
        ],
        "evaluation": [
          {
            "window": 52,
            "first_origin": 554,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 52
          },
          {
            "window": 260,
            "first_origin": 346,
            "last_origin": 605,
            "latest_label_end": 611,
            "training_count": 260
          }
        ]
      }
    }
  },
  "date_axis_note": "Weekly Monday00:00 labels for build_features; retain actual economic position dates for provenance and displayed splits. Monday labels are feature/time indices, NOT public decision or availability times.",
  "information_time": "Economic-position-date replay of downloaded vintage, same structural limitation as Treasury. Normally Tuesday positions publishedFriday15:30ET, with documented holiday/shutdown/ION delays; exact full historical first-release dates unavailable. Not a tradable first-release-vintage backtest."
}
```

输入路径、bytes、SHA256 和逐合约完整精度绑定见 report-values.json。此稿不产生 E3/MCS 或 E4 成本结果。
