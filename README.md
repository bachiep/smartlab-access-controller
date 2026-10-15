# SmartLab Access Controller

Đồ án Nhóm 11 cho học phần CSE703093 - An toàn phần mềm.

Hệ thống mô phỏng bộ điều khiển xác thực lệnh mở cửa phòng lab. Trọng tâm là so sánh black-box và white-box/concolic fuzzing trên cùng nhánh xác thực mã mở cửa khẩn cấp.

## Phạm vi kỹ thuật

- Đặc tả Excel tương thích Spec Verification Lab.
- Mô hình Kripke/CTL, static analysis, kiểm tra SMT và fuzzing.
- Target Python riêng để so sánh black-box và concolic/Z3 trên cùng nhánh `SLAC`.
- Mã vulnerable/patched và kiểm thử hồi quy.
- Log và số liệu tái lập được.

## Cấu trúc

- `spec/`: file Excel đặc tả của nhóm.
- `src/`: target fuzzing của nhóm.
- `tests/`: kiểm thử hồi quy.
- `results/`: log và bảng số liệu thực nghiệm đã chọn.
- `docs/`: yêu cầu, hướng dẫn chạy và nguồn báo cáo.

## Chạy lại thực nghiệm

Yêu cầu: Python 3.11+ và `z3-solver`.

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python tools\run_fuzz_experiment.py
```

Script tạo `results/fuzz_experiment.json` và `results/fuzz_runs.csv`. Mỗi kỹ thuật có năm lượt được lập chỉ mục bằng cùng các seed; concolic là xác định nên seed chỉ nhận diện lần lặp, không làm thay đổi ràng buộc Z3.

## Chạy Spec Verification Lab

1. Mở `SpecVerificationLab.exe` của giảng viên.
2. Chọn `Nạp từ file Excel khác (.xlsx)` và nạp `spec/smartlab_access_controller_spec.xlsx`.
3. Chọn `3) Chạy TOÀN BỘ Pipeline` rồi xuất PDF/DOCX tích hợp.
4. Lưu bản PDF đã kiểm tra vào `results/tool_pipeline_final.pdf`.

Các CWE/CTL vi phạm sinh từ fixture trong workbook là bằng chứng công cụ học phần, không phải tuyên bố về hệ thống triển khai thật.

Spec Verification Lab chỉ nhận công thức CTL đơn giản với một nhãn nguyên tử. Vì vậy workbook dùng `AF(complete)` để kiểm tra trực tiếp từ trạng thái khởi tạo; mô hình bảo đảm mọi nhánh, gồm `access_denied`, đều đến `session_closed` mang nhãn `complete`.
