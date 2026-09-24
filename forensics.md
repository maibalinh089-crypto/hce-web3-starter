# Báo cáo Thực hành Lab 3: Đọc giao dịch và hợp đồng trên Etherscan

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** maibalinh089-crypto
- **Địa chỉ ví cá nhân:** `0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3`
- **Mã băm giao dịch phân tích (Tx Hash):** `0x955dfe5904cf06bc8ec52dc54fbdaf75238a4190b317d789a10c43cef3804dab`
- **Mạng thử nghiệm:** Sepolia Testnet

---

## Bước 1: Mổ xẻ chi tiết 8 trường trong giao dịch on-chain

Dưới đây là bảng trích xuất trực tiếp từ Blockchain Explorer (Etherscan / Blockscout) đối với giao dịch thực tế của sinh viên:

| STT | Tên trường | Giá trị thực tế trích xuất | Ý nghĩa kỹ thuật | Vì sao người làm nghiệp vụ (Kế toán / Tuân thủ) cần |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Status** | `Success` (Thành công) | Trạng thái thực thi giao dịch do máy ảo EVM trả về sau khi hoàn tất các lệnh mã máy. | **Xác định tính pháp lý và hạch toán:** Giao dịch `Failed` vẫn bị trừ phí gas mạng lưới. Kế toán phải kiểm tra Status để biết tài sản đã thực sự chuyển giao thành công hay chỉ mới tốn phí giao dịch. |
| **2** | **Block** | `9915717` (Block Height) | Số thứ tự của khối chứa giao dịch đã được các validator kiểm tra và liên kết vào chuỗi khối. | **Xác định tính hoàn tất (Finality):** Số khối càng tăng, số lượt xác nhận (confirmations) càng cao, giảm rủi ro bị tái tổ chức chuỗi (reorg). Kế toán ghi nhận thời điểm tài sản chuyển đổi quyền sở hữu. |
| **3** | **Timestamp** | Dec-26-2025 03:30:00 AM UTC (1766719800) | Dấu thời gian do validator ghi lại khi đóng khối giao dịch theo chuẩn UTC. | **Mốc ghi nhận kế toán & quy đổi tỷ giá:** Làm căn cứ hạch toán doanh thu, chi phí, và áp tỷ giá hối đoái (ETH/USD hoặc ETH/VND) chính xác tại thời điểm phát sinh nghĩa vụ tài chính. |
| **4** | **From / To** | **From:** `0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3`<br>**To:** `0x9e4dc2f178b5f9c38beba5010fb06e21d21b4445` | Địa chỉ ví gửi (bắt đầu bằng private key ký) và ví nhận tài sản/tương tác hợp đồng. | **Xác minh danh tính (KYC/AML & Travel Rule):** Đối soát danh tính các bên liên quan, rà soát địa chỉ ví đối ứng có thuộc danh sách đen (OFAC), ví sàn giao dịch hay ví cá nhân không lưu ký (unhosted). |
| **5** | **Value** | `0.01 Sepolia ETH` (10,000,000,000,000,000 Wei) | Giá trị tài sản gốc (Native ETH) thực tế được chuyển giao giữa hai địa chỉ ví. | **Ghi nhận nguyên giá nghiệp vụ:** Số liệu cơ sở để ghi tăng/giảm số dư tài khoản thanh toán và theo dõi tài sản của doanh nghiệp. |
| **6** | **Transaction Fee** | `0.0000315 ETH` (`21,000` Gas Used × `1.50` Gwei) | Tổng chi phí thực tế mà người gửi phải trả cho mạng lưới để xử lý giao dịch. | **Hạch toán chi phí tài chính:** Phí gas là chi phí hoạt động (OpEx) thực tế. Kế toán bắt buộc phải hạch toán riêng khoản phí này, không được gộp vào nguyên giá tài sản chuyển đi. |
| **7** | **Gas Price** | `1.500000013 Gwei` (0.0000000015 ETH) | Đơn giá cho mỗi đơn vị tính toán gas (gồm Base Fee + Priority Fee/Tip theo chuẩn EIP-1559). | **Kiểm soát và tối ưu ngân sách:** Giúp chuyên viên giải thích nguyên nhân biến động chi phí giữa các thời điểm (do mạng nghẽn hay đặt mức ưu tiên cao), phục vụ chính sách tối ưu hóa phí giao dịch. |
| **8** | **Nonce** | `11` | Số thứ tự giao dịch xuất phát từ ví gửi (đếm tuần tự từ 0: đây là giao dịch thứ 12). | **Phát hiện gian lận và kiểm soát dòng tiền:** Nonce đảm bảo giao dịch không bị phát lại (Replay Attack). Giúp kế toán phát hiện giao dịch bị bỏ sót (nonce gap) hoặc giao dịch bị chèn/thay thế (Speed Up/Cancel). |

---

## Bước 2: Đọc và phân tích hợp đồng Tether USD (USDT) trên Ethereum Mainnet

- **Tên hợp đồng:** `TetherToken` (Ký hiệu: `USDT`)
- **Địa chỉ hợp đồng trên Mainnet:** `0xdAC17F958D2ee523a2206206994597C13D831ec7`
- **Đường dẫn kiểm tra:** [https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7](https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7)

---

## Bước 3: Trả lời 3 câu hỏi bắt buộc

### Câu 1: Hợp đồng bạn xem có công bố mã nguồn đã xác thực không?
- **Trả lời:** **CÓ, hợp đồng USDT đã được xác thực mã nguồn (Contract Source Code Verified).**
- **Ý nghĩa đối với chuyên viên tuân thủ:** 
  - Trên Etherscan, mục **Contract** có dấu tích xanh (*Verified*). Mã nguồn Solidity công khai khớp 100% với chuỗi bytecode máy đang chạy trên blockchain.
  - Phân biệt:
    + **Bytecode:** Chuỗi mã nhị phân dạng hex (máy EVM thực thi), con người không thể đọc hiểu logic nghiệp vụ.
    + **Source Code (Verified):** Mã nguồn cấp cao (Solidity) được nhà phát triển công bố và trình biên dịch xác nhận tính đồng nhất với bytecode.
  - *Nguyên tắc tuân thủ:* Nếu một dự án tiền điện tử không công bố mã nguồn đã xác thực, đây là **Cờ đỏ (Red Flag)** cảnh báo rủi ro cao về mã độc, cửa sau (backdoor) hoặc dự án lừa đảo (scam).

---

### Câu 2: Tổng cung của đồng đó là bao nhiêu? Đọc ra từ hàm nào?
- **Hàm đọc dữ liệu:** Gọi hàm `totalSupply()` trong tab **Read Contract** (không tốn gas, không cần kết nối ví).
- **Giá trị thô trả về (Raw value):** `88,304,342,264,551,152`
- **Độ chia lẻ (Decimals):** `6` (đọc từ hàm `decimals()`)
- **Tổng cung thực tế đã quy đổi:**
  $$\text{Total Supply} = \frac{88,304,342,264,551,152}{10^6} \approx \mathbf{88,304,342,264.55\text{ USDT}}$$
  *(Hơn 88.3 tỷ USD giá trị USDT đang lưu hành trên mạng lưới Ethereum).*

---

### Câu 3: Trong tab Write Contract, có hàm nào cho phép một địa chỉ đặc biệt đóng băng tài khoản người khác không? Nếu có, tên hàm là gì?
- **Trả lời:** **CÓ, hợp đồng USDT có cơ chế đóng băng tài khoản trực tiếp.**
- **Tên các hàm trong tab Write Contract:**
  1. `addBlackList(address _evilUser)`: Đưa địa chỉ ví mục tiêu vào danh sách đen. Khi bị đưa vào danh sách này, ví mục tiêu bị khóa cứng: không thể chuyển USDT đi và không thể nhận thêm USDT (`require(!isBlackListed[_from])`).
  2. `removeBlackList(address _clearedUser)`: Gỡ bỏ địa chỉ khỏi danh sách đen khi có yêu cầu hợp lệ.
  3. `destroyBlackFunds(address _blackListedUser)`: Hàm cưỡng chế tiêu hủy toàn bộ số dư USDT của ví trong blacklist, giảm tổng cung lưu thông tương ứng.
- **Ai có quyền gọi hàm này:** Chỉ duy nhất địa chỉ nắm giữ vai trò chủ sở hữu (**Owner**) của hợp đồng (thuộc quyền kiểm soát của Tether Limited) thông qua modifier `onlyOwner`.

---

## Bài học và Thảo luận mở rộng: Mức độ phi tập trung thực tế của Stablecoin

Phát hiện ở Câu 3 là điểm mấu chốt đối với mọi chuyên viên phân tích on-chain và tuân thủ tài sản số:

1. **Thực tế về tính phi tập trung (Decentralization Paradox):**
   Mặc dù USDT và USDC vận hành trên hạ tầng blockchain phi tập trung (Ethereum), nhưng tầng ứng dụng tiền tệ của chúng mang tính **tập trung tuyệt đối (Centralized Control)**.
2. **Tuân thủ pháp lý và yêu cầu thực thi pháp luật:**
   Cơ chế `addBlackList` là điều kiện bắt buộc để Tether và Circle tuân thủ quy định của các cơ quan quản lý (như OFAC Hoa Kỳ, DOJ, FBI, FinCEN). Khi nhận được lệnh của tòa án hoặc yêu cầu trừng phạt quốc tế, tổ chức phát hành có thể đơn phương đóng băng hàng triệu USD trong các ví của tội phạm mạng, tin tặc hoặc thực thể bị cấm vận chỉ bằng một giao dịch gọi hàm trên blockchain.
3. **Ý nghĩa rủi ro đối với người dùng và doanh nghiệp:**
   Nắm giữ stablecoin tập trung đồng nghĩa với việc chấp nhận rủi ro đối tác (Counterparty Risk) và rủi ro bị đóng băng tài sản kiểm duyệt. Đây là lý do ra đời của các stablecoin phi tập trung không có quyền admin (như DAI, LUSD).
