# Báo cáo Thực hành Lab 2: Ví và Giao dịch đầu tiên

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên:** maibalinh089-crypto
- **Địa chỉ ví cá nhân (Sepolia):** `0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3`

---

## 1. Bảng đối chiếu giao dịch

| Trường thông tin | Giao dịch thành công (Bước 1) | Giao dịch thất bại có chủ đích (Bước 2) |
| :--- | :--- | :--- |
| **Mã băm giao dịch (Tx Hash)** | `0x955dfe5904cf06bc8ec52dc54fbdaf75238a4190b317d789a10c43cef3804dab` | `0xd93fcd480e9760201cae22071fcf1b4a07f777f3551f02f5ba1d7c81d2ee3410` |
| **Số tiền chuyển** | `0.01 Sepolia ETH` | `0.00 Sepolia ETH` (Thử rút/chuyển vượt quá số dư cho phép) |
| **Phí giao dịch thực trả** | `0.0000315 ETH` (21,000 Gas × 1.50 Gwei) | `0.000093081 ETH` (29,785 Gas × 3.125 Gwei) |
| **Trạng thái (Status)** | **Confirmed / Success** (Đã đóng khối thành công) | **Failed / Reverted** (Giao dịch bị từ chối/hoàn tác) |
| **Nguyên nhân (nếu thất bại)** | Giao dịch hợp lệ, tài khoản đủ số dư chuyển và đủ phí gas. | Hợp đồng / EVM trả về mã lỗi hoàn tác: `KHONG_DU_SO_DU` do số dư không đáp ứng điều kiện giao dịch. |

---

## 2. Phân tích chi tiết hai tình huống giao dịch thất bại

### Tình huống A — Địa chỉ sai (Lỗi ở tầng giao diện / Client - Checksum EIP-55)
- **Hành vi thực nghiệm:** Thử sửa một ký tự chữ hoa thành chữ thường hoặc đổi một ký tự bất kỳ trong địa chỉ người nhận trên MetaMask.
- **Hiện tượng:** MetaMask lập tức vô hiệu hóa nút gửi và báo lỗi `"Invalid address"` hoặc không khớp mã kiểm tra (checksum).
- **Phí giao dịch:** `0 ETH` (Không phát sinh giao dịch trên blockchain, không tốn phí gas vì giao dịch chưa được ký và broadcast).
- **Bài học kế toán / tuân thủ:** Địa chỉ ví Ethereum áp dụng chuẩn EIP-55 (dùng chữ hoa/chữ thường để kiểm tra tính toàn vẹn) giúp phát hiện lỗi gõ nhầm ký tự. Tuy nhiên, hệ thống **chỉ kiểm tra định dạng hợp lệ chứ không kiểm tra người nhận có đúng chủ thể bạn mong muốn hay không**.

### Tình huống B — Không đủ phí / Vi phạm số dư (Lỗi ở tầng EVM / Blockchain)
- **Hành vi thực nghiệm:** Chuyển số tiền vượt quá số dư khả dụng hoặc không chừa lại ETH để trả phí gas.
- **Hiện tượng:** 
  - Nếu gửi trên giao diện MetaMask thông thường: Báo lỗi *"Insufficient funds for gas"*.
  - Nếu giao dịch được đóng gói đưa lên mạng lưới (như mã băm ở bảng trên): EVM tiến hành thực thi đến khi gặp điều kiện kiểm tra số dư không thỏa mãn sẽ kích hoạt lệnh `revert` với lý do `KHONG_DU_SO_DU`.
- **Phí giao dịch:** Vẫn phải trả `0.000093081 ETH` (phí gas cho các bước tính toán của node xác thực trước khi giao dịch bị hoàn tác).
- **Bài học kế toán / tuân thủ:** Phí giao dịch (Gas) luôn phải trả bằng đồng tiền gốc của mạng (ETH), không trừ vào số tiền chuyển, và **người gửi vẫn bị trừ phí gas ngay cả khi giao dịch thất bại**.

---

## 3. Câu hỏi lý thuyết nghiệp vụ

> **Câu hỏi:** *Nếu bạn chuyển nhầm cho người lạ, có lấy lại được không? Vì sao?*

**Trả lời (3 câu chuẩn nguyên lý Blockchain):**

1. **Không thể tự ý lấy lại hay đảo ngược số tiền đã chuyển nhầm trên mạng lưới blockchain.**
2. **Nguyên nhân là do blockchain vận hành theo cơ chế phi tập trung với tính bất biến (Immutability):** một khi giao dịch đã được các validator xác thực và đóng khối, không có bất kỳ tổ chức, ngân hàng hay quản trị viên nào có thẩm quyền can thiệp vào sổ cái để hủy bỏ giao dịch.
3. **Cách duy nhất để nhận lại tài sản là liên hệ trực tiếp với chủ sở hữu của địa chỉ ví nhận nhầm và trông đợi họ tự nguyện thực hiện một giao dịch mới để hoàn trả lại cho bạn.**

---

## 4. Tổng kết cho vị trí Kế toán & Tuân thủ tài sản số

1. **Nguyên tắc "Zero-Trust" trong chuyển tiền:** Luôn thực hiện giao dịch thử nghiệm với số tiền tối thiểu (ví dụ 0.001 ETH) trước khi chuyển khoản tiền lớn.
2. **Quản lý dòng tiền phí Gas:** Mọi nghiệp vụ chuyển tài sản (kể cả chuyển token ERC-20 hay tương tác Smart Contract) đều đòi hỏi số dư ETH native riêng biệt để trả phí mạng lưới.
3. **Đối soát giao dịch qua Explorer:** Trạng thái giao dịch thực tế phải luôn được kiểm chứng chéo thông qua Transaction Hash trên Blockchain Explorer (như Sepolia Etherscan / Blockscout), không chỉ dựa vào thông báo giao diện ví.
