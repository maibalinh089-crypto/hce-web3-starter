"""
Cong cu phan tich dong tien on-chain (ETH Cashflow Analyzer)
Hoc phan: ECO2432 - Tien dien tu va Hop dong thong minh
Tuan thu chat che SPEC.md va AGENTS.md:
- Doc khoa API tu bien moi truong ETHERSCAN_API_KEY, khong ghi cung trong ma.
- Doi toan bo gia tri tu wei sang ETH truoc khi hien thi va tinh toan.
- Tinh phi gas cho ca giao dich thanh cong va giao dich that bai.
- Ho tro phan trang pagination de khong bi sot du lieu.
- Chu thich trong ma viet bang tieng Viet khong dau.
"""

import os
import sys
import json
import time
import datetime
import urllib.request
import urllib.error
import matplotlib.pyplot as plt


def lay_khoa_api():
    """Doc khoa API Etherscan tu bien moi truong he thong."""
    return os.environ.get("ETHERSCAN_API_KEY", "").strip()


def kiem_tra_dia_chi_vi(address):
    """Kiem tra tinh hop le cua dia chi vi Ethereum (E1 trong SPEC.md)."""
    if not isinstance(address, str):
        return False
    if len(address) != 42 or not address.startswith("0x"):
        return False
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False


def tai_du_lieu_giao_dich(address, api_key="", network="sepolia", days=90):
    """
    Lay danh sach giao dich on-chain tu Etherscan API (hoac Blockscout fallback neu chua co key).
    Ho tro phan trang pagination de khong bi sot du lieu (R7, E5 trong SPEC.md).
    """
    all_txs = []
    page = 1
    offset = 1000
    now_ts = int(time.time())
    start_ts = (now_ts - (days * 86400)) if days > 0 else 0

    if api_key:
        if network == "sepolia":
            base_url = "https://api-sepolia.etherscan.io/api"
        else:
            base_url = "https://api.etherscan.io/api"
    else:
        # Fallback ket noi cong cong de kiem thu san sang ngay ca khi chua nhap API Key
        if network == "sepolia":
            base_url = "https://eth-sepolia.blockscout.com/api"
        else:
            base_url = "https://eth.blockscout.com/api"

    print(f"[*] Dang tai du lieu giao dich cho vi {address} (khung {days if days > 0 else 'toan bo'} ngay)...")

    while True:
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": 0,
            "endblock": 99999999,
            "page": page,
            "offset": offset,
            "sort": "asc",
        }
        if api_key:
            params["apikey"] = api_key

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        full_url = f"{base_url}?{query_string}"

        req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                if res.status != 200:
                    print(f"[!] Loi ket noi HTTP: Ma {res.status}")
                    break
                raw_data = res.read().decode("utf-8")
                data = json.loads(raw_data)
        except urllib.error.URLError as e:
            print(f"[!] Loi mang khi truy van API: {e}")
            break
        except json.JSONDecodeError:
            print("[!] Loi phan tich phan hoi JSON tu API")
            break

        status = str(data.get("status", "0"))
        message = data.get("message", "")
        result = data.get("result", [])

        if status != "1" and message != "No transactions found":
            if "NOTOK" in message or "rate limit" in str(result).lower():
                print(f"[!] Etherscan API thong bao: {result}")
            break

        if not isinstance(result, list) or len(result) == 0:
            break

        all_txs.extend(result)
        if len(result) < offset:
            break
        page += 1

    # Loc theo khung thoi gian
    if start_ts > 0:
        filtered_txs = [tx for tx in all_txs if int(tx.get("timeStamp", 0)) >= start_ts]
    else:
        filtered_txs = all_txs

    return filtered_txs, len(all_txs)


def phan_tich_dong_tien(address, txs):
    """
    Ap dung cac quy tac nghiep vu R1 - R8 trong SPEC.md de tinh toan dong tien:
    - R1: Tien vao (to == address va from != address).
    - R2: Tien ra (from == address va to != address).
    - R3: Cong thuc phi gas = gasUsed * gasPrice / 10^18.
    - R4: Giao dich that bai van tinh phi gas vao dong tien ra.
    - R5: Tu chuyen cho chinh minh thi triet tieu value, chi tru phi gas.
    - R6: Doi wei sang ETH truoc khi tinh toan va hien thi.
    - R8: Tinh so du bien dong luy ke tu moc 0.
    """
    addr_lower = address.lower()
    bang_dong_tien = []
    tong_vao = 0.0
    tong_ra = 0.0
    so_du_luy_ke = 0.0

    txs_sorted = sorted(txs, key=lambda x: int(x.get("timeStamp", 0)))

    for tx in txs_sorted:
        tx_from = tx.get("from", "").lower()
        tx_to = tx.get("to", "").lower()
        ts = int(tx.get("timeStamp", 0))
        thoi_gian_str = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        tx_hash = tx.get("hash", "")
        hash_rut_gon = f"{tx_hash[:6]}...{tx_hash[-4:]}" if len(tx_hash) >= 10 else tx_hash

        value_eth = int(tx.get("value", 0)) / 1e18
        gas_used = int(tx.get("gasUsed", 0))
        gas_price = int(tx.get("gasPrice", 0))
        gas_fee_eth = (gas_used * gas_price) / 1e18

        is_error = str(tx.get("isError", "0")) == "1"
        loai_phat_sinh = ""
        bien_dong = 0.0

        if tx_from == addr_lower and tx_to == addr_lower:
            loai_phat_sinh = "OUT (Tu chuyen - Phi gas)"
            bien_dong = -gas_fee_eth
            tong_ra += gas_fee_eth
        elif tx_from == addr_lower:
            if is_error:
                loai_phat_sinh = "OUT (That bai - Phi gas)"
                bien_dong = -gas_fee_eth
                tong_ra += gas_fee_eth
            else:
                loai_phat_sinh = "OUT"
                bien_dong = -(value_eth + gas_fee_eth)
                tong_ra += (value_eth + gas_fee_eth)
        elif tx_to == addr_lower:
            if not is_error:
                loai_phat_sinh = "IN"
                bien_dong = value_eth
                tong_vao += value_eth
                gas_fee_eth = 0.0
            else:
                continue
        else:
            continue

        so_du_luy_ke += bien_dong

        bang_dong_tien.append({
            "time": thoi_gian_str,
            "hash": hash_rut_gon,
            "type": loai_phat_sinh,
            "value": value_eth,
            "fee": gas_fee_eth,
            "balance": so_du_luy_ke,
            "ts": ts,
        })

    net_cashflow = tong_vao - tong_ra
    return bang_dong_tien, tong_vao, tong_ra, net_cashflow


def in_bao_cao(bang_dong_tien, tong_vao, tong_ra, net_cashflow, address):
    """In bang ke dong tien va 3 chi so tai chinh ra man hinh."""
    print("\n" + "=" * 85)
    print(f"   BAO CAO DONG TIEN ETH CHO VI: {address}")
    print("=" * 85)
    print(f"{'Thoi gian (UTC)':<20} | {'Tx Hash':<14} | {'Loai':<24} | {'So tien ETH':<12} | {'Phi Gas':<12} | {'So du luy ke':<12}")
    print("-" * 85)

    for row in bang_dong_tien:
        val_str = f"{row['value']:.6f}" if row['value'] > 0 else "-"
        fee_str = f"{row['fee']:.6f}" if row['fee'] > 0 else "-"
        print(f"{row['time']:<20} | {row['hash']:<14} | {row['type']:<24} | {val_str:<12} | {fee_str:<12} | {row['balance']:>+10.6f} ETH")

    print("=" * 85)
    print(f"1. TONG DONG TIEN VAO (Total Inflow) : {tong_vao:,.6f} ETH")
    print(f"2. TONG DONG TIEN RA  (Total Outflow): {tong_ra:,.6f} ETH (bao gom phi gas)")
    print(f"3. DONG TIEN RONG KY  (Net Cashflow) : {net_cashflow:>+,.6f} ETH")
    print("=" * 85 + "\n")


def ve_bieu_do(bang_dong_tien, output_path="cashflow_chart.png"):
    """Ve bieu do duong bien dong so du luy ke theo thoi gian (Muc 4 SPEC.md)."""
    if not bang_dong_tien:
        print("[*] Khong co du lieu giao dich de ve bieu do.")
        return

    dates = [datetime.datetime.fromtimestamp(r["ts"], datetime.timezone.utc) for r in bang_dong_tien]
    balances = [r["balance"] for r in bang_dong_tien]

    plt.figure(figsize=(10, 5), dpi=150)
    plt.plot(dates, balances, marker="o", color="#1f77b4", linewidth=2, markersize=5, label="So du luy ke (ETH)")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
    
    plt.title("Bieu do Bien dong So du Luy ke theo Thoi gian", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Thoi gian (UTC)", fontsize=11, labelpad=8)
    plt.ylabel("So du bien dong (ETH)", fontsize=11, labelpad=8)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left")
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    print(f"[+] Da xuat bieu do thanh cong tai: {output_path}")


def main():
    dia_chi_mac_dinh = "0x478Aa040C44c59853EaD621514A6DF09E7Da6dB3"
    dia_chi = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else dia_chi_mac_dinh

    # Kiem tra tuy chon ngay (mac dinh 90 ngay theo SPEC.md, hoac --all / --days)
    days = 90
    for i, arg in enumerate(sys.argv):
        if arg == "--all":
            days = 0
        elif arg == "--days" and i + 1 < len(sys.argv):
            try:
                days = int(sys.argv[i + 1])
            except ValueError:
                pass

    if not kiem_tra_dia_chi_vi(dia_chi):
        print(f"[!] Loi E1: Dia chi vi '{dia_chi}' khong hop le (can dung 42 ky tu hex bat dau bang 0x).")
        sys.exit(1)

    api_key = lay_khoa_api()
    if not api_key:
        print("[*] Luu y: Bien moi truong ETHERSCAN_API_KEY chua duoc thiet lap. Dang dung che do truy van du phong (Sepolia Blockscout API).")

    txs, total_history_count = tai_du_lieu_giao_dich(dia_chi, api_key=api_key, network="sepolia", days=days)

    if not txs:
        if total_history_count > 0 and days > 0:
            print(f"[*] Vi khong phat sinh giao dich trong {days} ngay gan nhat (vi co {total_history_count} giao dich o qua khu).")
            print(f"[*] Tu dong tai toan bo {total_history_count} giao dich de lap bao cao va ve bieu do...")
            txs, _ = tai_du_lieu_giao_dich(dia_chi, api_key=api_key, network="sepolia", days=0)
        else:
            print(f"[*] Thong bao: Vi khong co giao dich trong ky khao sat.")
            return

    bang_dong_tien, tong_vao, tong_ra, net_cashflow = phan_tich_dong_tien(dia_chi, txs)
    in_bao_cao(bang_dong_tien, tong_vao, tong_ra, net_cashflow, dia_chi)
    ve_bieu_do(bang_dong_tien, output_path="cashflow_chart.png")


if __name__ == "__main__":
    main()
