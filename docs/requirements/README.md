# Đặc tả Excel

File `../../spec/smartlab_access_controller_spec.xlsx` là đầu vào chính cho Spec Verification Lab.

Hệ thống mô phỏng xác thực lệnh mở cửa phòng lab với hai worker dùng chung `access_guard`.

Workbook chứa fixture giáo dục theo yêu cầu của Spec Verification Lab: cụm khóa cố ý có `access_conflict`, bốn lỗi bộ nhớ C, một phép chia Python và một nhánh magic-value Python. Các phát hiện từ tool phải được mô tả là fixture, không phải hành vi chấp nhận được của hệ thống thật.

Thực nghiệm chính của Đề tài 4 nằm ở `src/slac_fuzz/`: `parse_override_packet` nhận gói bốn byte và dùng `SLAC` làm nhánh đích. Black-box và concolic/Z3 chạy trên cùng target này.

Quy tắc khi sửa đặc tả:

- Giữ nguyên đúng 10 sheet và tên các cột trong template.
- `CON-2` và `parse_badge_code.KichThuocBuffer` phải cùng là `20`.
- Nhãn trong CTL phải tồn tại trong `MoHinhTrangThai`.
- Dòng đầu của `LoaiTruLanNhau` phải là `access_locked` và `audit_locked`.
- Nếu đổi cặp mã mở cửa, cập nhật đồng thời `HamSinhMa`, `REQ-10` và `TC-7`.
- Không tạo workbook thứ hai cho bản vá; bản vá được kiểm chứng trong target Python riêng.

Các lỗi C được sinh có chủ đích để kiểm chứng static analysis trong bối cảnh học tập. Chúng không phải hành vi được chấp nhận của hệ thống.
