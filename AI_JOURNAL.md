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
