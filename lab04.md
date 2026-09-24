# Báo cáo Thực hành Lab 4: Nhận diện Hợp đồng có Rủi ro

- **Học phần:** ECO2432 — Tiền điện tử và Hợp đồng thông minh
- **Giảng viên phụ trách:** TS. Hà Ngọc Long
- **Sinh viên thực hiện:** maibalinh089-crypto
- **Tệp mã nguồn thẩm định:** `contracts/lab04/ClubTokens.sol`

---

## 1. Bảng kết luận thẩm định rủi ro mã nguồn

| Hợp đồng | Kết luận | Tên hàm | Số dòng | Rủi ro cho người nắm giữ |
| :---: | :--- | :--- | :---: | :--- |
| **ClubTokenA** | **An toàn / Không có vấn đề** | Không có hàm đặc quyền | N/A | **Không có rủi ro từ quyền admin.** Token không kế thừa `Ownable`. Tổng cung được đúc cố định 1 lần duy nhất trong hàm `constructor` ($1,000,000 \times 10^{18}$ wei). Không ai có thể tạo thêm token hay can thiệp vào tài khoản người khác. |
| **ClubTokenB** | **Rủi ro lạm phát vô hạn (Unlimited Mint / Dilution Risk)** | `mint(address to, uint256 amount)` | **Dòng 18 – 20** | **Pha loãng giá trị nghiêm trọng.** Hợp đồng cấp quyền `onlyOwner` cho phép chủ sở hữu đúc thêm token tùy ý không giới hạn số lượng và không có mức trần (cap). Chủ sở hữu có thể tự đúc hàng tỷ token rồi xả ra thị trường (dump), làm giá trị token của người nắm giữ lao dốc về 0. |
| **ClubTokenC** | **Rủi ro đóng băng tài sản / Bẫy thanh khoản (Honeypot / Blacklist)** | 1. `setRestricted(address user, bool status)`<br>2. `_update(address from, address to, uint256 value)` | **Dòng 30 – 32**<br><br>**Dòng 34 – 37** | **Mất thanh khoản, không thể bán lại.** Chủ sở hữu có thể gọi `setRestricted` để đưa ví người mua vào danh sách đen. Khi người dùng muốn chuyển đi hoặc bán trên sàn DEX, hàm nội bộ `_update` kiểm tra `require(!restricted[from])` tại **Dòng 35** sẽ lập tức revert giao dịch. Đây là cơ chế lừa đảo Honeypot kinh điển (cho mua nhưng cấm bán). |

---

## 2. Bằng chứng trích xuất từ mã nguồn (`contracts/lab04/ClubTokens.sol`)

### 2.1. Phân tích ClubTokenA (Dòng 7 – 11)
```solidity
7: contract ClubTokenA is ERC20 {
8:     constructor() ERC20("Club Token A", "CTA") {
9:         _mint(msg.sender, 1_000_000 * 10 ** decimals());
10:    }
11: }
```
- **Đánh giá:** Mã nguồn tối giản, tuân thủ đúng chuẩn ERC-20 bất biến. Không có biến trạng thái quản trị, không có hàm can thiệp số dư sau triển khai.

---

### 2.2. Phân tích ClubTokenB (Dòng 13 – 21)
```solidity
13: contract ClubTokenB is ERC20, Ownable {
14:     constructor() ERC20("Club Token B", "CTB") Ownable(msg.sender) {
15:         _mint(msg.sender, 1_000_000 * 10 ** decimals());
16:     }
17: 
18:     function mint(address to, uint256 amount) external onlyOwner {
19:         _mint(to, amount);
20:     }
21: }
```
- **Cơ chế rủi ro:** Dòng 18 có modifier `onlyOwner`. Hàm `mint` nhận tham số `amount` kiểu `uint256` nhưng hoàn toàn không có điều kiện ràng buộc như `require(totalSupply() + amount <= MAX_SUPPLY)`. Chủ dự án nắm toàn quyền kiểm soát nguồn cung tiền tệ.

---

### 2.3. Phân tích ClubTokenC (Dòng 23 – 38)
```solidity
23: contract ClubTokenC is ERC20, Ownable {
24:     mapping(address => bool) public restricted;
...
30:     function setRestricted(address user, bool status) external onlyOwner {
31:         restricted[user] = status;
32:     }
33: 
34:     function _update(address from, address to, uint256 value) internal override {
35:         require(!restricted[from], "Dia chi bi han che");
36:         super._update(from, to, value);
37:     }
38: }
```
- **Cơ chế rủi ro:** 
  - Dòng 24 khai báo bảng tra cứu trạng thái hạn chế: `mapping(address => bool) public restricted;`.
  - Dòng 30–32 cho phép `owner` đơn phương thay đổi trạng thái của bất kỳ người dùng nào thành `true`.
  - Dòng 34–37: Trong OpenZeppelin Contracts 5.x, hàm `_update` là chốt chặn trung tâm điều phối mọi hoạt động chuyển tiền (thay thế cho `_beforeTokenTransfer` ở bản 4.x). Tại Dòng 35, điều kiện `require(!restricted[from], "Dia chi bi han che")` ngăn cản mọi luồng tiền chuyển đi từ ví bị đánh dấu. Người nắm giữ hoàn toàn bị giam vốn.

---

## 3. Bài học thực tiễn cho Chuyên viên Thẩm định Dự án Web3

1. **Thẩm định phân quyền (Privilege Audit):** Sự xuất hiện của `Ownable` không đồng nghĩa với an toàn. Kiểm toán viên luôn phải rà soát tất cả các hàm gắn `onlyOwner` để xem quyền hạn đó có thể can thiệp đến dòng tiền và số dư của người dùng hay không.
2. **Quy tắc trần tổng cung (Hard Cap):** Nếu hợp đồng có chức năng mint, bắt buộc phải có giới hạn trần bất biến (Hard Cap) hoặc lịch trình lạm phát được mã hóa cố định trong thuật toán, không được để hàm mint tùy tiện.
3. **Cơ chế Blacklist / Honeypot:** Bất kỳ cơ chế can thiệp vào hàm `transfer` hoặc `_update` để lọc địa chỉ gửi đều là rủi ro tập trung hóa cực lớn. Trong các dự án ẩn danh (meme coin, DeFi nhỏ), đây là dấu hiệu 99% của bẫy lừa đảo rút thanh khoản (Rug Pull / Honeypot).
