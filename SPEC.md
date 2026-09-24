# ĐẶC TẢ YÊU CẦU PHẦN MỀM (SPEC)
# CÔNG CỤ PHÂN TÍCH DÒNG TIỀN VÍ ON-CHAIN (ETH CASHFLOW ANALYZER)

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Nhóm thực hiện:** Nhóm maibalinh089-crypto
- **Vai trò đảm nhiệm:** Chuyên viên phân tích nghiệp vụ (Business Analyst - BA)
- **Phiên bản tài liệu:** v1.0 (Lab 5 — Không viết mã nguồn trong buổi này)

---

## 1. Mục đích

Xây dựng công cụ phân tích tự động dòng tiền on-chain đối với đồng tiền gốc (Native ETH) của một địa chỉ ví Ethereum trong 90 ngày gần nhất, phục vụ công tác kiểm toán, đối soát kế toán và giám sát tuân thủ (AML/CFT) thông qua bảng dữ liệu chi tiết, các chỉ số tài chính tổng hợp và biểu đồ biến động số dư theo thời gian.

---

## 2. Đầu vào (Inputs)

1. **Địa chỉ ví mục tiêu (`address`):**
   - Kiểu dữ liệu: Chuỗi ký tự (String).
   - Định dạng: Bắt buộc dài đúng 42 ký tự, bắt đầu bằng tiền tố `0x`, là chuỗi thập lục phân (Hexadecimal) hợp lệ theo chuẩn Ethereum (chấp nhận cả chữ thường hoặc định dạng Checksum EIP-55).
   - Nguồn cung cấp: Người dùng nhập từ dòng lệnh (CLI argument) hoặc giao diện nhập liệu.
2. **Khóa truy cập API Etherscan (`ETHERSCAN_API_KEY`):**
   - Kiểu dữ liệu: Chuỗi ký tự bí mật (Secret String).
   - Nguồn cung cấp: Đọc từ biến môi trường hệ thống (`os.environ.get("ETHERSCAN_API_KEY")`), tuyệt đối không ghi cứng (hardcode) trong mã nguồn (tuân thủ quy ước `AGENTS.md`).
3. **Số ngày cần phân tích (`days`):**
   - Kiểu dữ liệu: Số nguyên dương (Integer).
   - Giá trị mặc định: `90` ngày.
   - Miền giá trị hợp lệ: $1 \le \text{days} \le 365$.

---

## 3. Quy tắc nghiệp vụ (Business Rules)

- **R1 (Nhận diện Dòng tiền vào - Inflow):**  
  Một giao dịch được xác định là Dòng tiền vào khi và chỉ khi:
  - Trường `to` trùng khớp với địa chỉ ví đang xét (so khớp không phân biệt chữ hoa/thường).
  - Trường `from` KHÁC địa chỉ ví đang xét.
  - Trạng thái giao dịch thành công (`isError == "0"`).  
  *Ghi nhận:* Giá trị dòng tiền vào $= +\text{Value}$. Người nhận không phải trả phí gas mạng lưới.

- **R2 (Nhận diện Dòng tiền ra - Outflow):**  
  Một giao dịch được xác định là Dòng tiền ra khi và chỉ khi:
  - Trường `from` trùng khớp với địa chỉ ví đang xét (so khớp không phân biệt chữ hoa/thường).
  - Trường `to` KHÁC địa chỉ ví đang xét.
  - Trạng thái giao dịch thành công (`isError == "0"`).  
  *Ghi nhận:* Số tiền thực tế bị trừ khỏi ví $= -(\text{Value} + \text{Gas Fee})$.

- **R3 (Công thức tính Phí giao dịch - Gas Fee):**  
  Phí mạng lưới thực trả cho mỗi giao dịch được tính theo công thức:
  $$\text{Gas Fee (ETH)} = \frac{\text{gasUsed} \times \text{gasPrice}}{10^{18}}$$
  Trong đó `gasUsed` và `gasPrice` được trích xuất trực tiếp từ phản hồi của API Etherscan.

- **R4 (Xử lý Giao dịch thất bại - Failed Transactions):**  
  Nếu giao dịch xuất phát từ ví đang xét (`from == address`) nhưng có trạng thái thất bại (`isError == "1"`):
  - Giá trị chuyển đi: $\text{Value} = 0$ (tiền gốc không rời khỏi ví do EVM hoàn tác).
  - Phí gas: Ví vẫn bị mạng lưới khấu trừ khoản $\text{Gas Fee}$.  
  *Ghi nhận:* Hạch toán khoản phí này vào Dòng tiền ra với phân loại riêng `"OUT (Phí giao dịch thất bại)"`.

- **R5 (Xử lý Giao dịch tự chuyển cho chính mình - Self-transfer):**  
  Nếu giao dịch có cả `from` và `to` đều trùng với địa chỉ ví đang xét:
  - Giá trị chuyển $\text{Value}$ triệt tiêu (chuyển đi rồi lại nhận về cùng một số dư).
  - Ví bị trừ khoản $\text{Gas Fee}$.  
  *Ghi nhận:* Hạch toán vào Dòng tiền ra với số tiền đúng bằng $\text{Gas Fee}$, phân loại `"OUT (Tự chuyển - Phí gas)"` để tránh bị nhân đôi doanh số.

- **R6 (Quy đổi đơn vị đo lường):**  
  Mọi giá trị tiền tệ trích xuất từ API đều ở đơn vị cơ sở nhỏ nhất là `wei`. Hệ thống bắt buộc phải chia cho $10^{18}$ trước khi thực hiện cộng trừ số học và hiển thị sang đơn vị `ETH` (lấy độ chính xác tối thiểu 6 chữ số thập phân).

- **R7 (Lọc khung thời gian khảo sát):**  
  Hệ thống chỉ xử lý các giao dịch có nhãn thời gian `timeStamp` thỏa mãn điều kiện:
  $$(\text{Timestamp}_{\text{hiện tại}} - \text{days} \times 86,400) \le \text{timeStamp} \le \text{Timestamp}_{\text{hiện tại}}$$
  Các giao dịch trước mốc thời gian này sẽ bị loại khỏi bảng tính trong kỳ.

- **R8 (Trật tự sắp xếp và Tính số dư lũy kế):**  
  Toàn bộ giao dịch hợp lệ trong kỳ phải được sắp xếp theo thời gian tăng dần (`timeStamp` tăng dần; nếu trùng thời gian thì xếp theo `nonce` hoặc `transactionIndex` tăng dần).  
  Số dư biến động lũy kế tại thời điểm giao dịch thứ $i$ ($B_i$) được tính tuần tự từ mốc $B_0 = 0$:
  $$B_i = B_{i-1} + \Delta_i$$
  Trong đó $\Delta_i = +\text{Value}$ (đối với dòng tiền vào) hoặc $\Delta_i = -(\text{Value} + \text{Gas Fee})$ (đối với dòng tiền ra).

---

## 4. Đầu ra (Outputs)

1. **Bảng kê dữ liệu dòng tiền chi tiết (Data Table):**  
   Hiển thị danh sách giao dịch gồm 6 cột thông tin chuẩn hóa:
   - `Thời gian`: Định dạng chuẩn quốc tế `YYYY-MM-DD HH:MM:SS UTC`.
   - `Mã băm giao dịch (Tx Hash)`: Chuỗi rút gọn (ví dụ `0x955d...4dab`).
   - `Loại phát sinh`: Nhãn rõ ràng gồm `IN` (Tiền vào), `OUT` (Tiền ra), `OUT (Failed Fee)` (Phí giao dịch lỗi).
   - `Số tiền chuyển (ETH)`: Giá trị gốc của giao dịch.
   - `Phí mạng lưới (ETH)`: Phí gas thực trả.
   - `Số dư lũy kế biến động (ETH)`: Số dư tích lũy sau giao dịch.

2. **Ba chỉ số tài chính tổng hợp (Summary Metrics):**
   - **Tổng tiền vào (Total Inflow):** Tổng các khoản ETH nhận được trong 90 ngày.
   - **Tổng tiền ra (Total Outflow):** Tổng ETH đã chuyển đi + Tổng toàn bộ phí gas đã trả.
   - **Dòng tiền ròng trong kỳ (Net Cashflow):** $\text{Net Cashflow} = \text{Tổng tiền vào} - \text{Tổng tiền ra}$.

3. **Biểu đồ trực quan hóa (Balance Chart):**
   - Loại biểu đồ: Biểu đồ đường (Line Chart).
   - Trục hoành ($X$): Trục thời gian (ngày/tháng).
   - Trục tung ($Y$): Số dư lũy kế (ETH).
   - Thể hiện trực quan các đỉnh chi tiêu và các mốc nhận tiền lớn.

---

## 5. Xử lý ngoại lệ và Tình huống biên (Exception Handling & Edge Cases)

- **E1 (Địa chỉ ví không hợp lệ):**  
  Nếu tham số `address` không bắt đầu bằng `0x`, độ dài khác 42 ký tự hoặc chứa ký tự không thuộc bảng mã Hex $\rightarrow$ Hệ thống dừng thực thi, hiển thị thông báo lỗi rõ ràng:  
  `"Lỗi E1: Địa chỉ ví không đúng định dạng chuẩn Ethereum (cần 42 ký tự bắt đầu bằng 0x)."`
- **E2 (Thiếu khóa API Etherscan):**  
  Nếu biến môi trường `ETHERSCAN_API_KEY` chưa được thiết lập hoặc để trống $\rightarrow$ Hệ thống dừng thực thi, báo lỗi:  
  `"Lỗi E2: Biến môi trường ETHERSCAN_API_KEY chưa được cấu hình. Vui lòng thiết lập khóa API."`
- **E3 (Lỗi phản hồi từ API / Vượt hạn mức gọi):**  
  Nếu Etherscan trả về mã trạng thái lỗi (ví dụ HTTP 429 - Rate Limit hoặc API Key không hợp lệ) $\rightarrow$ Hệ thống in chi tiết mã lỗi và thông điệp của Etherscan, dừng chương trình an toàn, không để ứng dụng bị crash.
- **E4 (Ví không có giao dịch trong kỳ khảo sát):**  
  Nếu API trả về mảng kết quả rỗng trong 90 ngày gần nhất $\rightarrow$ Hệ thống không báo lỗi, in thông báo thân thiện:  
  `"Thông báo: Ví không phát sinh bất kỳ giao dịch nào trong 90 ngày gần nhất."`  
  Hiển thị bảng tổng hợp: Tổng vào = 0 ETH, Tổng ra = 0 ETH, Dòng tiền ròng = 0 ETH.
- **E5 (Xử lý ví có khối lượng giao dịch lớn > 10.000 txs):**  
  Etherscan giới hạn tối đa 10.000 giao dịch cho một lần truy vấn API $\rightarrow$ Hệ thống bắt buộc phải triển khai thuật toán phân trang tự động (Pagination: gọi trang tiếp theo hoặc tịnh tiến tham số `startblock`) để thu thập trọn vẹn 100% dữ liệu của kỳ khảo sát.
- **E6 (Lỗi gián đoạn mạng / Timeout):**  
  Nếu kết nối mạng bị ngắt hoặc quá thời gian chờ (10 giây) $\rightarrow$ Tự động thử lại tối đa 3 lần với cơ chế lùi thời gian lũy thừa (Exponential Backoff: 1s, 2s, 4s) trước khi thông báo gián đoạn mạng cho người dùng.

---

## 6. Ngoài phạm vi (Out of Scope)

1. **Không phân tích giao dịch Token:** Không bao gồm các token tiêu chuẩn ERC-20 (như USDT, USDC), ERC-721 (NFT) hay ERC-1155; công cụ này chỉ tập trung duy nhất vào đồng tiền cơ sở Native ETH.
2. **Không phân tích giao dịch nội bộ (Internal Transactions):** Tạm thời không bóc tách các dòng tiền ETH được chuyển gián tiếp thông qua việc kích hoạt hợp đồng thông minh (Smart Contract Internal Calls) để đảm bảo độ phức tạp ở mức kiểm soát được.
3. **Không quy đổi tỷ giá tiền pháp định (Fiat):** Không tích hợp API giá (như CoinGecko hay Binance) để quy đổi ra USD hoặc VNĐ; toàn bộ số liệu thể hiện độc quyền bằng ETH.
4. **Không hỗ trợ chuỗi khối khác:** Chỉ áp dụng cho Ethereum Mainnet và Sepolia Testnet, không áp dụng cho các mạng Layer 2 (Arbitrum, Optimism) hay mạng tương thích EVM khác trong phạm vi phiên bản này.

---

## 7. Biên bản Kiểm tra chéo (Peer Review Feedback) từ Nhóm bạn

| STT | Vấn đề mơ hồ nhóm bạn chỉ ra trong bản thảo | Đánh giá của nhóm tác giả | Giải pháp làm rõ đã bổ sung vào đặc tả |
| :---: | :--- | :--- | :--- |
| **1** | **Chưa xử lý tình huống ví tự gửi cho chính mình (Self-transfer):**<br>Nếu một người chuyển 1 ETH cho chính ví của mình, theo quy tắc R1 sẽ cộng 1 ETH, theo R2 lại trừ 1 ETH + Gas Fee $\rightarrow$ Doanh số vào và ra bị đội lên 1 ETH ảo dù số dư thực tế không đổi. | **Hoàn toàn xác đáng.** Đây là lỗ hổng logic kế toán dòng tiền rất phổ biến khi phân tích on-chain. | **Bổ sung Quy tắc R5 riêng biệt:** Khẳng định giao dịch có `from == to` thì giá trị tiền gốc triệt tiêu, chỉ hạch toán duy nhất khoản phí Gas Fee vào Dòng tiền ra. |
| **2** | **Mơ hồ về mốc bắt đầu của Số dư lũy kế:**<br>Bản thảo ghi "Số dư lũy kế" nhưng không nói rõ là số dư tuyệt đối của ví (cần số dư tại thời điểm 90 ngày trước) hay là chênh lệch dòng tiền ròng bắt đầu từ 0. | **Rất chính xác.** Công cụ AI khi đọc yêu cầu cũ có thể tự bịa ra lệnh gọi `eth_getBalance` ở quá khứ gây lỗi. | **Làm rõ tại Quy tắc R8 và Mục 4:** Định nghĩa rõ đây là *"Số dư biến động lũy kế trong kỳ (Cumulative Net Flow)"* bắt đầu từ mốc 0, phản ánh dòng tiền thuần của kỳ khảo sát 90 ngày. |
