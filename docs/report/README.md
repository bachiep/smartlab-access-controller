# Bằng chứng báo cáo

Sau khi chạy tool giảng viên, lưu các artefact đã chọn vào `results/` và giữ nguyên log gốc.

Tối thiểu cần có:

1. Report tool sinh từ Excel.
2. Kết quả Kripke/CTL và mutual exclusion.
3. Kết quả static checker cho CWE-120, CWE-401, CWE-415 và CWE-416, có chú thích đây là fault injection.
4. Ít nhất một model Z3 SAT cho kiểm tra tràn số.
5. Năm lượt black-box và năm lượt white-box/concolic, lưu seed, số lần thử, thời gian, input đạt đích và log.
6. Bảng tổng hợp mean/median; nếu black-box không đạt nhánh đích trong giới hạn, ghi rõ `not reached`.

Không thay số liệu chạy thực tế bằng ước lượng. Mọi kết luận phải chỉ tới log, bảng hoặc ảnh chụp tương ứng.
