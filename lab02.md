# Báo cáo Thực hành Lab 2: Ví và Giao dịch đầu tiên

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Sinh viên:** maibalinh089-crypto
- **Địa chỉ ví cá nhân (Sepolia):** `0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3`

---

## 1. Bảng đối chiếu giao dịch

| Trường thông tin | Giao dịch thành công (Bước 1) | Giao dịch thất bại có chủ đích (Bước 2) |
| :--- | :--- | :--- |
| **Mã băm giao dịch (Tx Hash)** | *(Điền mã tx hash sau khi chuyển 0.01 ETH)* | *(Điền mã tx hash nếu thất bại on-chain, hoặc ghi: Bị chặn bởi MetaMask Client)* |
| **Số tiền chuyển** | 0.01 Sepolia ETH | *(Ví dụ: 0.01 Sepolia ETH hoặc toàn bộ số dư)* |
| **Phí giao dịch thực trả (Gas Fee)** | *(Ví dụ: ~0.0000315 ETH = 21,000 gas × Gas Price)* | 0 ETH (nếu MetaMask từ chối trước) hoặc Gas đã tiêu tốn |
| **Trạng thái (Status)** | Confirmed / Success (Block confirmed) | Rejected (MetaMask) / Failed (Reverted on-chain) |
| **Nguyên nhân (nếu thất bại)** | Không có (Giao dịch hợp lệ) | **Tình huống A:** Sai Checksum địa chỉ ví (EIP-55) làm MetaMask báo lỗi định dạng.<br>**Tình huống B:** Không đủ số dư trả phí Gas (Insufficient funds for gas). |

---

## 2. Câu hỏi lý thuyết nghiệp vụ

> **Câu hỏi:** *Nếu bạn chuyển nhầm cho người lạ, có lấy lại được không? Vì sao?*

**Trả lời (3 câu chuẩn nguyên lý Blockchain):**

1. **Không thể tự ý lấy lại hay đảo ngược số tiền đã chuyển nhầm.**
2. **Nguyên nhân là do blockchain vận hành theo cơ chế phân tán với tính bất biến (Immutability):** một khi giao dịch đã được các validator xác thực và đóng khối, không một cá nhân, tổ chức hay quản trị viên nào có thẩm quyền can thiệp vào sổ cái để hoàn tác giao dịch.
3. **Cách duy nhất để nhận lại tài sản là liên hệ và trông đợi người nhận tự nguyện thực hiện một giao dịch mới để chuyển trả lại cho bạn.**

---

## 3. Bài học thực tiễn cho Kế toán và Chuyên viên tuân thủ tài sản số

1. **Cơ chế Checksum (EIP-55):** Địa chỉ Ethereum phân biệt chữ hoa/chữ thường thông qua mã băm để phát hiện lỗi gõ nhầm ký tự, nhưng hệ thống không thể biết địa chỉ đó có đúng ý định người gửi hay không.
2. **Nguyên lý phí mạng lưới (Gas):** Phí giao dịch luôn được trả bằng đồng tiền bản địa (ETH trên mạng Ethereum/Sepolia) và trừ trực tiếp vào số dư khả dụng, không trừ vào số tiền dự định chuyển đi. Do đó tài khoản luôn cần duy trì một lượng ETH dự phòng để làm phí gas.
