# Execute_QAT

## Execute Record
[Record](./execute_record/qat_record.env)  

## Use Timing Comparison


| 功能           | `val_trt.sh` 指令                                      | `trtexec` 指令                                         |
|----------------|------------------------------------------------------|-------------------------------------------------------|
| **模型輸入**   | ONNX 模型 (`qat_best_best.onnx`)                     | ONNX 模型 (`qat_best_yolov9-converted.onnx`)          |
| **功能**       | 驗證流程，可能包含推理、效能測試、精度計算             | 轉換模型為 TensorRT 引擎，並進行效能測試             |
| **數據集設定** | 使用 `data/coco.yaml`                                | 不涉及數據集驗證                                      |
| **動態輸入形狀** | 可能默認封裝設定                                    | 明確指定 `minShapes`, `optShapes`, `maxShapes`        |
| **精度選項**   | 未顯式提及 FP16/INT8 模式                            | 明確指定 `--fp16`, `--int8`                           |
| **額外功能**   | 生成計算圖 (`--generate-graph`)                      | 無此功能                                              |
| **執行細節**   | 封裝於腳本中，細節未展開                             | 直接執行 `trtexec`，所有參數顯式定義                 |
