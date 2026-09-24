# Báo cáo Thực hành Lab 5: Viết Đặc tả cho Công cụ Phân tích Dòng tiền

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** maibalinh089-crypto
- **Tệp sản phẩm chính của buổi học:** [`SPEC.md`](SPEC.md)

---

## 1. Mục tiêu và Vai trò nghiệp vụ

- Buổi này sinh viên đóng vai trò là **Chuyên viên Phân tích Nghiệp vụ (Business Analyst - BA)**.
- **Quy tắc bắt buộc:** **KHÔNG VIẾT MÃ NGUỒN** trong buổi học này.
- Mục đích là tạo ra một bản đặc tả yêu cầu kỹ thuật (Software Requirement Specification - SRS) hoàn chỉnh, tường minh, không có điểm mơ hồ để lập trình viên hoặc công cụ AI có thể sinh mã chính xác 100% trong buổi tiếp theo mà không cần phải hỏi lại.

---

## 2. Toàn văn Bản Đặc tả Yêu cầu

Toàn bộ bản đặc tả chi tiết gồm 7 mục chuẩn hóa đã được lưu trữ và cập nhật tại:
👉 **[Xem tệp đặc tả chi tiết SPEC.md](SPEC.md)**

### Tóm tắt các nội dung cốt lõi trong `SPEC.md`:
1. **Mục đích:** Xây dựng công cụ phân tích tự động dòng tiền on-chain ETH trong 90 ngày.
2. **Đầu vào:** Địa chỉ ví hex 42 ký tự, khóa `ETHERSCAN_API_KEY` đọc từ biến môi trường (tuân thủ `AGENTS.md`), tham số số ngày (mặc định 90).
3. **Quy tắc nghiệp vụ (R1 - R8):**
   - R1: Tiền vào (`to == address` và `from != address`).
   - R2: Tiền ra (`from == address` và `to != address`), số trừ = Value + Phí gas.
   - R3: Phí gas thực tế = $(\text{gasUsed} \times \text{gasPrice}) / 10^{18}$.
   - R4: Giao dịch thất bại vẫn bị trừ phí gas mạng lưới, hạch toán vào tiền ra.
   - R5: Tự chuyển cho chính mình (`from == to`), giá trị chuyển triệt tiêu, chỉ trừ phí gas.
   - R6: Đổi toàn bộ đơn vị từ `wei` sang `ETH` (chia $10^{18}$).
   - R7: Lọc chặt chẽ khoảng thời gian trong 90 ngày theo `timeStamp`.
   - R8: Sắp xếp thời gian tăng dần, tính số dư biến động lũy kế ($B_i = B_{i-1} + \Delta_i$).
4. **Đầu ra:** Bảng kê 6 cột chi tiết, 3 chỉ số tài chính tổng hợp (Tổng vào, Tổng ra, Dòng tiền ròng) và Biểu đồ đường (Line Chart).
5. **Ngoại lệ (E1 - E6):** Xử lý ví sai định dạng, thiếu API key, API lỗi/rate limit, ví rỗng trong kỳ (không crash), ví lớn hơn 10.000 giao dịch (phân trang pagination) và gián đoạn mạng (retry backoff).
6. **Ngoài phạm vi:** Không phân tích token ERC-20, không phân tích giao dịch nội bộ, không đổi ra tiền pháp định.
7. **Nhận xét kiểm tra chéo (Peer Review):** Ghi nhận 2 điểm mơ hồ lớn do nhóm bạn phản biện (xử lý ví tự chuyển tiền và mốc bắt đầu của số dư lũy kế) cùng phương án làm rõ triệt để.
