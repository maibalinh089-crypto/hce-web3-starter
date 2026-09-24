# Báo cáo Thực hành Lab 7: Tính Chi phí Vận hành Thực tế

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** maibalinh089-crypto
- **Chủ đề nghiên cứu:** Phân tích mô hình kinh tế dòng tiền (Unit Economics) và tính khả thi của ứng dụng Web3 trên hạ tầng Blockchain.

---

## 1. Cấu trúc Phí Giao dịch trên Blockchain

Công thức tổng quát xác định chi phí của một giao dịch on-chain:
$$\text{Chi phí giao dịch (ETH)} = \text{Lượng Gas tiêu thụ (Gas Used)} \times \text{Đơn giá Gas (Gas Price in Gwei)} \times 10^{-9}$$
$$\text{Chi phí giao dịch (USD)} = \text{Chi phí giao dịch (ETH)} \times \text{Giá ETH (USD)}$$

### Phân rã lượng gas tiêu thụ cho thao tác cộng điểm thành viên:
Trong một Smart Contract quản lý điểm thưởng (ví dụ `ClubPoint` / ERC-20 Loyalty), một giao dịch cộng điểm cho sinh viên bao gồm các thành phần chi phí gas cơ bản:
1. **Chi phí khởi tạo giao dịch cơ sở (Base Transaction Cost):** Cố định `21,000 gas`.
2. **Chi phí lưu trữ trạng thái lâu dài (`SSTORE`):** Cập nhật biến số dư điểm của sinh viên trong bảng tra cứu `mapping(address => uint256)`:
   - Nếu cộng điểm lần đầu (ghi từ 0 lên giá trị mới): tốn khoảng `20,000 gas`.
   - Nếu cập nhật điểm đã có (sửa từ giá trị khác 0 sang giá trị mới): tốn khoảng `5,000 gas`.
3. **Thực thi mã lệnh logic (Execution & Arithmetic):** Kiểm tra quyền sở hữu (`onlyOwner`), kiểm tra tính hợp lệ: `~2,000 – 3,000 gas`.
4. **Phát sự kiện (Emit Event `PointAdded`):** Ghi nhật ký vào log của khối để ứng dụng giao diện lắng nghe: `~1,500 – 2,000 gas`.

$\rightarrow$ **Lượng gas tiêu thụ chuẩn chọn để tính toán:** **`45,000 gas / lượt cộng điểm`** (mức trung bình thực tế khi tương tác hợp đồng thông minh).

---

## 2. Giải bài toán: Thẻ tích điểm CLB sinh viên (1.000 lượt/tháng)

- **Quy mô hoạt động:** $1,000$ lượt cộng điểm / tháng.
- **Lượng gas cho 1 giao dịch cộng điểm:** $45,000$ gas.
- **Đơn giá gas giả định (Gas Price):** $20$ Gwei ($20 \times 10^{-9}$ ETH).
- **Tỷ giá giả định:** $1 \text{ ETH} = 3,000 \text{ USD}$ (Tỷ giá quy đổi: $1 \text{ USD} \approx 25,500 \text{ VNĐ}$).

---

### a) Chi phí trên mạng Ethereum Layer 1 (Mainnet)

1. **Phí cho 1 giao dịch cộng điểm:**
   $$\text{Fee}_{\text{ETH}} = 45,000 \times 20 \times 10^{-9} = 0.0009 \text{ ETH}$$
   $$\text{Fee}_{\text{USD}} = 0.0009 \times 3,000 \text{ USD} = \mathbf{2.70\text{ USD / giao dịch}} \approx \mathbf{68,850\text{ VNĐ / giao dịch}}$$

2. **Tổng chi phí vận hành trong 1 tháng (1.000 giao dịch):**
   $$\text{Total}_{\text{Tháng}} = 1,000 \times 2.70 \text{ USD} = \mathbf{2,700\text{ USD / tháng}} \approx \mathbf{68,850,000\text{ VNĐ / tháng}}$$

---

### b) Chi phí trên mạng Layer 2 (Đơn giá rẻ hơn 100 lần)

Khi di chuyển hợp đồng thông minh lên các giải pháp Layer 2 (như Base, Arbitrum, Optimism), chi phí thực thi được giảm thiểu khoảng 100 lần:

1. **Phí cho 1 giao dịch cộng điểm trên Layer 2:**
   $$\text{Fee}_{\text{L2 / tx}} = \frac{2.70 \text{ USD}}{100} = \mathbf{0.027\text{ USD / giao dịch}} \approx \mathbf{688.5\text{ VNĐ / giao dịch}}$$

2. **Tổng chi phí vận hành 1 tháng trên Layer 2:**
   $$\text{Total}_{\text{L2 / tháng}} = \frac{2,700 \text{ USD}}{100} = \mathbf{27\text{ USD / tháng}} \approx \mathbf{688,500\text{ VNĐ / tháng}}$$

> **Ghi chú thực tiễn:** Sau bản nâng cấp Ethereum Dencun (EIP-4844 blobs), phí giao dịch thực tế trên Layer 2 (như mạng Base hoặc Arbitrum One) thường giảm sâu từ 200 – 500 lần so với L1, dao động chỉ khoảng $0.005 – 0.01$ USD/giao dịch. Khi đó, tổng chi phí một tháng cho CLB chỉ còn khoảng **5 – 10 USD/tháng** (~125,000 – 250,000 VNĐ).

---

### c) Phân tích chủ thể chịu phí (Ai trả tiền? Sinh viên có chấp nhận không?)

#### Kịch bản 1: Sinh viên tự trả phí
- **Trên Layer 1:** Mỗi lần uống một cốc trà sữa hay tham gia một hoạt động CLB để được tích 1 điểm (giá trị quy đổi thực tế của điểm thường chỉ tương đương $2,000 – 5,000$ VNĐ quà tặng), sinh viên phải bỏ ra **$68,850$ VNĐ tiền phí gas**.
  $\rightarrow$ **Phản ứng của sinh viên:** **TỪ CHỐI 100%**. Đây là nghịch lý kinh tế: *"Chi phí giao dịch cao gấp 15 – 30 lần giá trị phần thưởng nhận được"*. Ứng dụng sẽ chết ngay ngày đầu ra mắt.
- **Trên Layer 2:** Mức phí ~`688 VNĐ / lần`. Sinh viên có thể miễn cưỡng chấp nhận nếu giá trị điểm thưởng lớn hơn (ví dụ tích điểm đổi học bổng, quà tặng giá trị). Tuy nhiên, rào cản lớn nhất là sinh viên phải tự mua ETH và nạp vào ví cá nhân để làm phí gas (ma sát trải nghiệm rất cao).

#### Kịch bản 2: Câu lạc bộ chi trả phí
- **Trên Layer 1:** Ngân sách $2,700$ USD/tháng (~$68.8$ triệu VNĐ) vượt xa toàn bộ ngân sách hoạt động trong cả một năm học của hầu hết các CLB sinh viên $\rightarrow$ **CLB chắc chắn phá sản**.
- **Trên Layer 2:** Chi phí $27$ USD/tháng (~$688,500$ VNĐ) hoàn toàn nằm trong khả năng tài trợ từ quỹ câu lạc bộ hoặc trích từ quỹ nhà tài trợ sự kiện.

#### Giải pháp tối ưu mô hình kinh doanh (Best Practice):
CLB triển khai trên **Layer 2** kết hợp cơ chế **Account Abstraction (ERC-4337)** với hợp đồng **Paymaster**:
- CLB nạp trước 27 USD vào quỹ Paymaster hàng tháng để **tài trợ 100% phí gas** cho thành viên (*Gasless Transactions*).
- Sinh viên chỉ việc quét mã QR tích điểm mà không cần phải sở hữu sẵn đồng ETH nào trong ví, đem lại trải nghiệm mượt mà giống như các ứng dụng Web2 (Grab, Momo).

---

### d) Kết luận về tính khả thi của mô hình Thẻ tích điểm

| Môi trường triển khai | Chi phí / giao dịch | Chi phí / tháng | Khả thi kỹ thuật | Khả thi kinh tế | Quyết định đầu tư |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ethereum Layer 1 (Mainnet)** | $2.70$ USD | $2,700$ USD | Có | **KHÔNG (0% Viable)** | **BÁC BỎ HOÀN TOÀN** |
| **Mạng Layer 2 (Base / Arbitrum)** | $0.027$ USD | $27$ USD | Có | **RẤT CAO (Highly Viable)** | **LỰA CHỌN TỐI ƯU** |

$\rightarrow$ **KẾT LUẬN:** Mô hình thẻ tích điểm chỉ khả thi trên **Mạng Layer 2 (hoặc Layer 3 / Appchain)**. Việc triển khai trực tiếp trên Ethereum Layer 1 là hoàn toàn phi thực tế về mặt kinh tế đối với các ứng dụng có tần suất giao dịch vi mô (Micro-transactions).

---

## 3. Mở rộng Khung tính toán cho Ý tưởng Đồ án Nhóm

- **Tên ý tưởng đồ án:** **Hệ thống Bình chọn & Cấp Chứng chỉ Hoạt động Sinh viên bằng Soulbound Token (SBT / POAP)**.
- **Quy mô hoạt động:** 
  - $500$ sinh viên tham gia trong một học kỳ.
  - Tổng số lượng giao dịch: $2,000$ giao dịch / kỳ (gồm $1,500$ lượt bỏ phiếu tín nhiệm ban cán sự và $500$ lượt đúc chứng chỉ số không thể chuyển nhượng SBT).
- **Lượng gas ước tính cho 1 giao dịch mint/bình chọn:** **`80,000 gas`** (do logic kiểm tra chữ ký mật mã ECDSA và ghi dữ liệu phức tạp hơn).

### Bảng tính phân tích độ nhạy chi phí đồ án nhóm:

| Chỉ số kinh tế | Triển khai trên Ethereum Layer 1 | Triển khai trên Layer 2 (Base / Arbitrum) |
| :--- | :---: | :---: |
| **Lượng gas / giao dịch** | $80,000$ gas | $80,000$ gas |
| **Đơn giá gas trung bình** | $20$ Gwei | $0.2$ Gwei (giảm 100 lần) |
| **Giá ETH giả định** | $3,000$ USD | $3,000$ USD |
| **Chi phí / 1 lượt tương tác (USD)** | **$4.80$ USD** (~$122,400$ VNĐ) | **$0.048$ USD** (~$1,224$ VNĐ) |
| **Tổng chi phí cho cả kỳ (2.000 txs)** | **$9,600$ USD** (~$244,800,000$ VNĐ) | **$96$ USD** (~$2,448,000$ VNĐ) |
| **Tính khả thi của đồ án** | **Bất khả thi** (chi phí cao hơn cả giải thưởng cuộc thi) | **Hoàn toàn khả thi** (khoảng 2.4 triệu VNĐ cho một kỳ tổ chức) |

### Kết luận phân tích kinh doanh (Unit Economics):
1. **Lựa chọn hạ tầng:** Nhóm thống nhất lựa chọn mạng **Base (hoặc Arbitrum One)** làm nền tảng triển khai đồ án thực hành.
2. **Chiến lược phân bổ ngân sách:** Dự toán ngân sách $96$ USD cho phí gas sẽ được tính vào chi phí tổ chức sự kiện của khoa/trường hoặc đề xuất hỗ trợ từ các quỹ vườn ươm Web3 (Web3 Grants).
