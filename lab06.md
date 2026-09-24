# Báo cáo Thực hành Lab 6: Sinh mã bằng AI và Kiểm tra Kết quả

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** maibalinh089-crypto
- **Tệp mã nguồn:** [`scripts/cashflow_analyzer.py`](scripts/cashflow_analyzer.py)
- **Tệp biểu đồ đầu ra:** [`cashflow_chart.png`](cashflow_chart.png)
- **Tệp nhật ký AI:** [`AI_JOURNAL.md`](AI_JOURNAL.md)

---

## 1. Chuẩn đầu ra và Kết quả nghiệm thu

1. **Chương trình chạy được:** Kịch bản Python [`scripts/cashflow_analyzer.py`](scripts/cashflow_analyzer.py) thực thi hoàn hảo, kết nối API on-chain để trích xuất và phân tích toàn bộ lịch sử 59 giao dịch của ví `0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3`.
2. **Biểu đồ trực quan:** Đã sinh tự động tệp biểu đồ đường [`cashflow_chart.png`](cashflow_chart.png) thể hiện diễn biến số dư lũy kế theo thời gian từ mốc nhận 1.0 Sepolia ETH đến số dư hiện tại (+0.881302 ETH).
3. **Bắt lỗi công cụ AI:** Ghi nhận và khắc phục thành công **2 lỗi nghiêm trọng** do AI sinh ra trong tệp [`AI_JOURNAL.md`](AI_JOURNAL.md).

---

## 2. Kết quả kiểm tra theo Danh mục 6 điểm bắt buộc

| STT | Điểm kiểm tra | Yêu cầu đối soát | Kết quả thực tế của chương trình |
| :---: | :--- | :--- | :--- |
| **1** | **Đơn vị tiền tệ** | Số dư hiển thị có hợp lý không? Có chia $10^{18}$ không? | **ĐẠT.** Mọi giá trị `value`, `gasPrice` đều được chia $10^{18}$ chuyển từ Wei sang ETH chính xác. |
| **2** | **Khóa API** | Có chuỗi khóa cứng trong mã không? | **ĐẠT.** Tuyệt đối không ghi cứng khóa; đọc từ `os.environ.get("ETHERSCAN_API_KEY")`. |
| **3** | **Phân trang** | Ví có nhiều giao dịch có lấy đủ không? | **ĐẠT.** Có vòng lặp phân trang `page += 1` quét hết toàn bộ 59 giao dịch, không bỏ sót. |
| **4** | **Giao dịch thất bại** | Có tính phí gas của giao dịch thất bại không? | **ĐẠT.** Các giao dịch `isError == "1"` vẫn được bóc tách phí gas và cộng vào Tổng tiền ra. |
| **5** | **Xử lý lỗi** | Thử nhập địa chỉ sai hoặc API Key sai | **ĐẠT.** Bắt ngoại lệ HTTP/Network, in thông báo rõ ràng và thoát an toàn, không bị crash. |
| **6** | **Phiên bản API** | Đối chiếu tài liệu Etherscan hiện hành | **ĐẠT.** Hỗ trợ endpoint hiện hành và có cơ chế Fallback truy vấn dữ liệu dự phòng. |

---

## 3. Tóm tắt 2 lỗi do AI sinh ra được ghi trong `AI_JOURNAL.md`

1. **Lỗi 1 (Bỏ qua phí gas của giao dịch thất bại):**  
   - *Hành vi của AI:* Dùng `if tx.get("isError") == "1": continue` vì cho rằng giao dịch thất bại thì không có tiền di chuyển.
   - *Hậu quả:* Bỏ sót phí gas mà validator đã trừ khỏi ví người gửi, làm sai lệch số dư lũy kế.
   - *Cách sinh viên sửa:* Vẫn trích xuất `(gasUsed * gasPrice) / 10^18` để trừ phí gas vào dòng tiền ra.
   - *Ai phát hiện:* **Sinh viên phát hiện**.

2. **Lỗi 2 (Thiếu phân trang, chỉ lấy 1 trang đầu):**  
   - *Hành vi của AI:* Chỉ gọi API 1 lần với `page=1&offset=100`.
   - *Hậu quả:* Bỏ sót toàn bộ các giao dịch ở các trang sau đối với ví có lịch sử hoạt động lớn.
   - *Cách sinh viên sửa:* Dùng vòng lặp `while True` với `page += 1` cho đến khi hết dữ liệu.
   - *Ai phát hiện:* **Sinh viên phát hiện**.

---

## 4. Cách chạy chương trình

Chạy trực tiếp từ thư mục gốc của dự án:
```bash
python scripts/cashflow_analyzer.py
```
*(Hoặc truyền thêm tham số địa chỉ ví bất kỳ và số ngày cần phân tích:)*
```bash
python scripts/cashflow_analyzer.py 0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3 --days 300
```
Biểu đồ sẽ tự động được lưu tại `cashflow_chart.png`.
