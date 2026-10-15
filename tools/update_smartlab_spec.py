"""Populate the single SmartLab workbook used by Spec Verification Lab.

The workbook remains in the teacher-provided 10-sheet format.  This script
changes only specification values; it deliberately preserves the workbook's
existing sheet names, order, formatting, and dimensions where possible.
"""

from pathlib import Path

from openpyxl import load_workbook


WORKBOOK = Path(__file__).resolve().parents[1] / "spec" / "smartlab_access_controller_spec.xlsx"


def replace_rows(ws, rows):
    """Replace data rows while retaining the template header row and its style."""
    for row in range(2, ws.max_row + 1):
        for column in range(1, ws.max_column + 1):
            ws.cell(row, column).value = None
    for row_index, values in enumerate(rows, start=2):
        for column_index, value in enumerate(values, start=1):
            ws.cell(row_index, column_index).value = value
    final_row = len(rows) + 1
    if ws.max_row > final_row:
        ws.delete_rows(final_row + 1, ws.max_row - final_row)


def main():
    workbook = load_workbook(WORKBOOK)

    workbook["ThongTin"]["B3"] = (
        "Bộ điều khiển mở cửa SmartLab xác thực thẻ và mã mở khóa khẩn cấp. "
        "Access worker và audit worker dùng chung access_guard; hệ thống ghi "
        "nhận sự kiện truy cập và dùng các fixture lỗi có chủ đích cho thực hành."
    )

    replace_rows(
        workbook["YeuCauChucNang"],
        [
            ("REQ-1", "Access worker và audit worker không được đồng thời giữ access_guard.", "safety", "HIGH"),
            ("REQ-2", "Cụm access_guard không được deadlock khi hai worker tranh chấp khóa.", "liveness", "HIGH"),
            ("REQ-3", "Một phiên xét duyệt thông thường phải hoàn tất sau khi cấp quyền hoặc từ chối.", "liveness", "HIGH"),
            ("REQ-4", "Hàm phân tích mã thẻ không được sao chép quá bộ đệm 20 ký tự ASCII.", "memory", "HIGH"),
            ("REQ-5", "Hàm tạo audit record phải giải phóng vùng nhớ đã cấp phát.", "memory", "MEDIUM"),
            ("REQ-6", "Hàm đóng phiên không được giải phóng cùng một con trỏ nhiều hơn một lần.", "memory", "HIGH"),
            ("REQ-7", "Hàm xóa badge cache không được truy cập vùng nhớ sau khi giải phóng.", "memory", "HIGH"),
            ("REQ-8", "Bộ đếm sự kiện truy cập không được tràn int32 khi cộng các bộ đếm đầu vào.", "safety", "MEDIUM"),
            ("REQ-9", "Hàm tỷ lệ truy cập hợp lệ phải xử lý mẫu số bằng 0 có kiểm soát.", "functional", "MEDIUM"),
            ("REQ-10", "Fixture magic-value của tool dùng cặp số nguyên 16-bit và phải được kiểm thử bằng black-box cùng concolic fuzzing.", "functional", "HIGH"),
            ("REQ-11", "Parser riêng parse_override_packet chỉ cấp quyền cho đúng gói 4 byte SLAC; bản vá phải chặn nhánh bypass này.", "functional", "HIGH"),
        ],
    )

    replace_rows(
        workbook["YeuCauPhiChucNang"],
        [
            ("NFR-1", "Mỗi lượt black-box phải xét tối đa đúng 100000 input trên target SLAC.", "HIGH"),
            ("NFR-2", "Mỗi record fuzzing phải lưu đủ 5 trường: seed, attempts, duration_seconds, packet_hex, reached_target.", "HIGH"),
            ("NFR-3", "So sánh phải có đúng 5 lượt mỗi kỹ thuật với seed 11, 23, 37, 53 và 71.", "HIGH"),
            ("NFR-4", "Kết quả phải tách tối thiểu 2 nhóm: fixture giáo dục của pipeline và target SLAC của Nhóm 11.", "HIGH"),
            ("NFR-5", "Thành viên còn lại phải tái lập thực nghiệm bằng tối đa 3 lệnh không cần sửa mã nguồn.", "MEDIUM"),
        ],
    )

    replace_rows(
        workbook["MoHinhTrangThai"],
        [
            ("access_free", "x", "safe", "access_holds, audit_holds, entry_idle"),
            ("access_holds", None, "access_locked", "access_conflict"),
            ("audit_holds", None, "audit_locked", "access_conflict"),
            ("access_conflict", None, "access_locked, audit_locked, violation", "entry_idle"),
            ("entry_idle", None, "entry_ready, door_locked", "credential_review, override_review"),
            ("credential_review", None, "normal_entry_active", "access_granted, access_denied"),
            ("override_review", None, "override_entry_active", "access_granted, access_denied"),
            ("access_granted", None, "door_unlocked", "session_closed"),
            ("access_denied", None, "door_locked", "session_closed"),
            ("session_closed", None, "complete", "session_closed"),
        ],
    )

    replace_rows(
        workbook["ThuocTinhAnToan"],
        [
            ("AG(!violation)",),
            ("EF(access_locked)",),
            ("AF(complete)",),
        ],
    )

    replace_rows(
        workbook["LoaiTruLanNhau"],
        [
            ("access_locked", "audit_locked"),
            ("violation", "safe"),
            ("access_locked", "safe"),
            ("audit_locked", "safe"),
            ("normal_entry_active", "override_entry_active"),
        ],
    )

    replace_rows(
        workbook["HamSinhMa"],
        [
            ("parse_badge_code", "c", "buffer_copy", "raw_badge", 20, "buffer-overflow", None, None),
            ("create_audit_record", "c", "alloc_release", None, 32, "memory-leak", None, None),
            ("close_access_session", "c", "alloc_release", None, 8, "double-free", None, None),
            ("reset_badge_cache", "c", "alloc_release", None, 16, "use-after-free", None, None),
            ("access_event_total", "c", "arithmetic", "granted_events, pending_events", 16, None, None, None),
            ("valid_access_ratio", "python", "divide", "granted, attempted", 16, None, None, None),
            ("unlock_override_code", "python", "magic_value", "override_a, override_b", 16, None, 5813, 2649),
        ],
    )

    replace_rows(
        workbook["KiemTraSoHoc"],
        [
            (
                "access_event_total",
                "granted_events, pending_events",
                "granted_events >= 0 and pending_events >= 0 and granted_events + pending_events > 2000000000",
                "granted_events + pending_events",
            ),
            (
                "audit_byte_total",
                "written_bytes, buffered_bytes",
                "written_bytes >= 0 and buffered_bytes >= 0 and written_bytes + buffered_bytes > 2000000000",
                "written_bytes + buffered_bytes",
            ),
            (
                "daily_badge_total",
                "accepted_today, queued_today",
                "accepted_today >= 0 and queued_today >= 0 and accepted_today + queued_today > 32767",
                "accepted_today + queued_today",
            ),
            (
                "active_session_total",
                "active_sessions, closing_sessions",
                "active_sessions >= 0 and closing_sessions >= 0 and active_sessions + closing_sessions > 65535",
                "active_sessions + closing_sessions",
            ),
            (
                "denied_attempt_total",
                "denied_today, delayed_denials",
                "denied_today >= 0 and delayed_denials >= 0 and denied_today + delayed_denials > 32767",
                "denied_today + delayed_denials",
            ),
        ],
    )

    replace_rows(
        workbook["TestCase"],
        [
            ("TC-1", "REQ-1, REQ-2", "Cụm khóa access_guard cố ý có xung đột", "Hệ thống ở access_free", "Chạy kiểm chứng mô hình\nKiểm tra trạng thái access_conflict", "AG(!violation) vi phạm và mutex phát hiện trạng thái nguy hiểm có chủ đích", "HIGH"),
            ("TC-2", "REQ-3", "Vòng đời một phiên xét duyệt", "Hệ thống ở access_free", "Chạy kiểm chứng mô hình\nKiểm tra CTL liveness", "AF(complete) đúng từ trạng thái khởi tạo", "HIGH"),
            ("TC-3", "REQ-4, CON-2", "Tràn bộ đệm mã thẻ", "parse_badge_code có fixture buffer-overflow", "Sinh mã C\nChạy check_c_source()", "Phát hiện CWE-120 trên fixture", "HIGH"),
            ("TC-4", "REQ-5", "Rò rỉ audit record", "create_audit_record có fixture memory-leak", "Sinh mã C\nChạy check_c_source()", "Phát hiện CWE-401 trên fixture", "HIGH"),
            ("TC-5", "REQ-6", "Giải phóng kép phiên", "close_access_session có fixture double-free", "Sinh mã C\nChạy check_c_source()", "Phát hiện CWE-415 trên fixture", "HIGH"),
            ("TC-6", "REQ-7", "Dùng bộ nhớ sau khi giải phóng", "reset_badge_cache có fixture use-after-free", "Sinh mã C\nChạy check_c_source()", "Phát hiện CWE-416 trên fixture", "HIGH"),
            ("TC-7", "REQ-8", "Bộ đếm access_event_total vượt ngưỡng int32", "Hai biến đầu vào không âm", "Chạy check_int32_overflow() bằng Z3", "SAT: có thể tràn int32", "MEDIUM"),
            ("TC-8", "REQ-8", "Bộ đếm audit_byte_total vượt ngưỡng int32", "Hai biến đầu vào không âm", "Chạy check_int32_overflow() bằng Z3", "SAT: có thể tràn int32", "MEDIUM"),
            ("TC-9", "REQ-8", "Bộ đếm daily_badge_total vượt ngưỡng int16", "Hai biến đầu vào không âm", "Chạy check_int32_overflow() bằng Z3", "SAT: có thể vượt ngưỡng nghiệp vụ int16", "MEDIUM"),
            ("TC-10", "REQ-8", "Bộ đếm active_session_total vượt ngưỡng uint16", "Hai biến đầu vào không âm", "Chạy check_int32_overflow() bằng Z3", "SAT: có thể vượt ngưỡng nghiệp vụ uint16", "MEDIUM"),
            ("TC-11", "REQ-8", "Bộ đếm denied_attempt_total vượt ngưỡng int16", "Hai biến đầu vào không âm", "Chạy check_int32_overflow() bằng Z3", "SAT: có thể vượt ngưỡng nghiệp vụ int16", "MEDIUM"),
            ("TC-12", "REQ-9", "Mẫu số tỷ lệ truy cập bằng 0", "valid_access_ratio đã được sinh", "Chạy blackbox_fuzz() 300 lần", "Có ít nhất một ZeroDivisionError trên fixture", "MEDIUM"),
            ("TC-13", "REQ-10, CON-3", "Tìm mã mở cửa khẩn cấp fixture", "unlock_override_code có cặp test 5813, 2649", "Chạy concolic_fuzz() tối đa 15 vòng", "Tìm đúng cặp và đạt nhánh test oracle", "HIGH"),
            ("TC-14", "REQ-11, NFR-1, NFR-2, NFR-3, NFR-4, NFR-5", "So sánh fuzzing trên target SLAC của Nhóm 11", "Đã chốt seed, ngân sách và môi trường", "Chạy 5 seed black-box x 100000 input\nChạy 5 lượt concolic cùng nhánh SLAC\nLưu CSV, JSON và log CTL", "Bảng có attempts, mean, median, thời gian, input đạt đích và trạng thái bản vá", "HIGH"),
        ],
    )

    workbook.save(WORKBOOK)


if __name__ == "__main__":
    main()
