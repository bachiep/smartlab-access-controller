# Kết quả thực nghiệm

`fuzz_experiment.json` và `fuzz_runs.csv` được tạo bằng `python tools\\run_fuzz_experiment.py`.

`ctl_liveness_check.json` được tạo bằng `python tools\\verify_ctl_liveness.py`; đây là kết quả kiểm chứng độc lập cho công thức CTL lồng mà tool giảng viên không nhận cú pháp.

- Năm hàng `black_box` dùng các seed 11, 23, 37, 53 và 71 với ngân sách 100.000 input mỗi lượt.
- Năm hàng `concolic` giải cùng điều kiện nhánh bằng Z3. Seed ở các hàng này chỉ định danh lần lặp vì bộ giải là xác định.
- `packet_hex=534c4143` biểu diễn gói ASCII `SLAC`.

Sau khi chạy Spec Verification Lab từ workbook trong `spec/`, lưu PDF/DOCX đã kiểm tra tại đây với tên `tool_pipeline_final.pdf` hoặc `tool_pipeline_final.docx`.
