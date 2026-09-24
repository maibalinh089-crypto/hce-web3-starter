# NHẬT KÝ LÀM VIỆC VỚI AI - ECO2432

---

## Lab 4: Nhận diện Hợp đồng có Rủi ro (ClubTokens.sol)

### 1. Thông tin phiên làm việc
- **Ngày thực hiện:** 24/09/2026
- **Sinh viên:** maibalinh089-crypto
- **Công cụ AI:** Antigravity (Gemini 3.8 Flash)

---

### 2. Chi tiết Prompt & Phản hồi

**Prompt nguyên văn:**
> "Bạn là chuyên viên thẩm định rủi ro tài sản số. Dưới đây là mã nguồn một hợp đồng token. Hãy liệt kê mọi quyền đặc biệt mà chủ sở hữu hợp đồng có thể thực hiện, và với mỗi quyền, nêu rõ:
> - Tên hàm và số dòng
> - Người nắm giữ token chịu rủi ro gì
> Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy.
> [Dán mã nguồn contracts/lab04/ClubTokens.sol]"

**AI trả về:**
- Xác định `ClubTokenA` an toàn, không có quyền admin.
- Xác định `ClubTokenB` có hàm `mint` (dòng 18-20) cho phép chủ sở hữu đúc token không giới hạn.
- Xác định `ClubTokenC` có hàm `setRestricted` (dòng 30-32) và hàm `_update` (dòng 34-37) kiểm tra danh sách chặn, gây rủi ro Honeypot/đóng băng tài sản.

**Đánh giá:** Dùng được ngay sau khi đối chiếu số dòng mã thực tế.

---

### 3. So sánh đối chiếu (Bắt buộc theo yêu cầu Lab 4)

| Tiêu chí | Chi tiết ghi nhận |
| :--- | :--- |
| **Đọc thủ công tìm ra gì?** | Khi tự đọc mã nguồn 15 phút đầu tiên: <br>1. Phát hiện `ClubTokenA` không kế thừa `Ownable`.<br>2. Phát hiện `ClubTokenB` có hàm `mint` đi kèm modifier `onlyOwner`.<br>3. Phát hiện `ClubTokenC` có mảng `restricted` và hàm `setRestricted` chỉ dành cho `owner`. |
| **AI tìm thêm được gì?** | AI cung cấp góc nhìn sâu hơn về mặt kỹ thuật kiến trúc OpenZeppelin 5.x:<br>1. AI chỉ ra chính xác số dòng mã của từng hàm (`mint`: Dòng 18–20; `setRestricted`: Dòng 30–32; `_update`: Dòng 34–37).<br>2. AI giải thích cơ chế hàm nội bộ `_update` ghi đè (override) ở Dòng 34–37 là chốt chặn can thiệp vào toàn bộ luồng chuyển tiền (`transfer` và `transferFrom`). Dòng 35 `require(!restricted[from])` biến hợp đồng thành mô hình lừa đảo Honeypot kinh điển (cho phép mua nhưng cấm bán ra ngoài). |
| **AI có nói sai chỗ nào không?** | **Có rủi ro suy diễn (Hallucination) nếu prompt lỏng lẻo:**<br>- Khi không có câu ràng buộc cuối, AI có xu hướng cảnh báo thêm các lỗi phổ biến như "có thể điều chỉnh phí giao dịch (tax)" hoặc "hàm tự hủy (selfdestruct)" vốn hoàn toàn KHÔNG tồn tại trong mã `ClubTokens.sol`.<br>- **Cách khắc phục:** Thêm câu chốt của giảng viên: *"Chỉ trả lời dựa trên mã nguồn tôi cung cấp. Nếu không tìm thấy, nói là không tìm thấy"*. Sau câu này, AI trả về kết quả chuẩn xác 100% khớp với mã nguồn. |

**Ai phát hiện:** Sinh viên phát hiện khi đối chiếu giữa mã nguồn thực tế và câu trả lời ban đầu của AI.

---
---

## Lab 6: Sinh mã bằng AI và Kiểm tra Kết quả (Cashflow Analyzer)

### 1. Thông tin phiên làm việc
- **Ngày thực hiện:** 24/09/2026
- **Sinh viên:** maibalinh089-crypto
- **Tệp mã nguồn xây dựng:** `scripts/cashflow_analyzer.py`
- **Tệp đặc tả làm căn cứ:** `SPEC.md`
- **Tệp quy ước ràng buộc:** `AGENTS.md`

---

### 2. Bảng kiểm tra bắt buộc 6 điểm (Checklist Đánh giá)

| STT | Hạng mục kiểm tra | Cách kiểm tra thực tế | Kết quả đánh giá |
| :---: | :--- | :--- | :--- |
| **1** | **Đơn vị tiền tệ** | Kiểm tra số dư hiển thị: có chia cho $10^{18}$ không? | **ĐẠT.** Mọi trường `value`, `gasPrice` đều được chia $10^{18}$ để chuyển từ `wei` sang `ETH` chuẩn xác. |
| **2** | **Khóa API** | Tìm chuỗi khóa bí mật trong mã nguồn | **ĐẠT.** Tuyệt đối không ghi cứng khóa API. Đọc thông qua `os.environ.get("ETHERSCAN_API_KEY")`. |
| **3** | **Phân trang (Pagination)** | Kiểm tra ví có nhiều hơn 1.000 giao dịch | **ĐẠT.** Đã xây dựng vòng lặp `while True` với `page += 1` và `offset = 1000` để quét cạn toàn bộ giao dịch. |
| **4** | **Giao dịch thất bại** | Kiểm tra giao dịch có `isError == "1"` | **ĐẠT.** Không bỏ qua giao dịch thất bại; vẫn trích xuất `gasUsed * gasPrice` để trừ phí gas vào dòng tiền ra. |
| **5** | **Xử lý lỗi (Exception)** | Thử ngắt mạng hoặc nhập địa chỉ sai / API Key sai | **ĐẠT.** Bắt ngoại lệ `URLError`, kiểm tra `status != "1"`, in thông báo thân thiện và dừng an toàn, không crash. |
| **6** | **Phiên bản API** | Đối chiếu tài liệu Etherscan v1/v2 và Sepolia | **ĐẠT.** Hỗ trợ endpoint hiện hành kèm cơ chế Fallback sang Blockscout khi môi trường chưa kịp nạp API Key. |

---

### 3. Ghi nhận 2 lỗi cụ thể do công cụ AI sinh ra (Bắt buộc theo chuẩn đầu ra)

#### LỖI 1: Bỏ qua phí gas của giao dịch thất bại (Lỗi nghiệp vụ dòng tiền Blockchain)
- **Prompt đưa vào:** *"Hãy viết hàm phân tích dòng tiền vào ra từ danh sách giao dịch trả về của Etherscan theo SPEC.md."*
- **Mã nguồn AI sinh ra ban đầu (Chỗ sai):**
  ```python
  # Ma nguon sai do AI sinh ra ban dau:
  for tx in txs:
      if tx.get("isError") == "1":
          continue  # AI tu y bo qua vi cho rang giao dich loi khong phat sinh dong tien
  ```
- **Hậu quả nghiệp vụ:** Trên thực tế blockchain Ethereum, dù giao dịch thất bại thì mạng lưới validator vẫn khấu trừ khoản phí gas thực tế (`gasUsed * gasPrice`) từ ví người gửi. Việc AI dùng `continue` bỏ qua toàn bộ giao dịch thất bại đã làm **bỏ sót 7 khoản phí gas** trong lịch sử ví của sinh viên (giao dịch `0x2094...aaaf`, `0xbeb9...15d4`, `0xd93f...3410`,...), dẫn đến Số dư lũy kế bị chênh lệch so với số dư thực tế trên Etherscan.
- **Cách sửa của sinh viên:**
  ```python
  # Sinh vien sua lai theo quy tac R4 trong SPEC.md:
  if is_error:
      loai_phat_sinh = "OUT (That bai - Phi gas)"
      bien_dong = -gas_fee_eth   # Chi tru phi gas, khong tru tien chuyen
      tong_ra += gas_fee_eth
  ```
- **Ai phát hiện:** **Sinh viên phát hiện** khi đối chiếu với Quy tắc R4 trong `SPEC.md` và kiểm tra thấy số dư cuối kỳ không khớp với Etherscan.

---

#### LỖI 2: Thiếu cơ chế phân trang (Pagination), chỉ lấy trang dữ liệu đầu tiên
- **Prompt đưa vào:** *"Viết hàm gọi API Etherscan lấy danh sách giao dịch của ví."*
- **Mã nguồn AI sinh ra ban đầu (Chỗ sai):**
  ```python
  # Ma nguon sai do AI sinh ra ban dau:
  url = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&page=1&offset=100&apikey={api_key}"
  res = urllib.request.urlopen(url)
  data = json.loads(res.read())
  return data["result"]  # Chi goi dung 1 lan duy nhat
  ```
- **Hậu quả kỹ thuật:** API Etherscan giới hạn số bản ghi mỗi lần trả về. Khi ví có lịch sử hoạt động dày (hoặc ví sàn, ví dự án có hàng nghìn giao dịch), hàm của AI chỉ lấy được tối đa trang đầu tiên và bỏ sót toàn bộ các giao dịch còn lại. Dữ liệu dòng tiền bị đứt đoạn, biểu đồ số dư bị cụt.
- **Cách sửa của sinh viên:** Thay bằng vòng lặp `while True`, khởi tạo `page = 1`, liên tục nối dữ liệu vào mảng tổng `all_txs.extend(result)`, và chỉ dừng lại khi `len(result) < offset` hoặc hết dữ liệu theo quy định ngoại lệ E5 trong `SPEC.md`.
- **Ai phát hiện:** **Sinh viên phát hiện** khi kiểm tra ví thực tế và đối chiếu với danh mục kiểm tra số 3 của giảng viên.

---

### 4. Kết quả nghiệm thu
- Chương trình [cashflow_analyzer.py](file:///c:/Users/Admin/Downloads/hce-web3-starter/scripts/cashflow_analyzer.py) chạy mượt mà, phân tích trọn vẹn 59 giao dịch on-chain của ví sinh viên.
- Biểu đồ [cashflow_chart.png](file:///c:/Users/Admin/Downloads/hce-web3-starter/cashflow_chart.png) được vẽ và xuất tự động, phản ánh đúng chu kỳ nhận 1 ETH từ vòi Faucet và các khoản chi tiêu/phí gas kế tiếp.
