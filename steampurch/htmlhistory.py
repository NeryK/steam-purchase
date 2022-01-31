"""Parse Steam purchase history HTML file"""
from bs4 import BeautifulSoup
import json
from collections import namedtuple

Transaction = namedtuple("Transaction", "date, items, type, payment, total, wallet_change, wallet_balance")

def parse_row(row):
    transaction_data = []
    # Raw Date
    cursor = row.find("td", {"class": "wht_date"})
    if not cursor:
        return None
    transaction_data.append(cursor.get_text().strip())
    # Multiple items
    cursor = row.find("td", {"class": "wht_items"})
    items = [item.get_text().strip().split("\t", 1)[0] for item in cursor.find_all("div")]
    if not items:
        # Single item
        items = [cursor.get_text().strip()]
    transaction_data.append(items)
    # Transaction type
    transaction_data.append(row.find("td", {"class": "wht_type"}).div.get_text().strip())
    # Payment means
    transaction_data.append(row.find("td", {"class": "wht_type"}).find("div", {"class": "wth_payment"}).get_text().strip().replace("\t", " "))
    # Amount
    transaction_data.append(row.find("td", {"class": "wht_total"}).get_text().strip().replace("\t", "").replace("\n", " "))
    # Wallet amount change
    transaction_data.append(row.find("td", {"class": "wht_wallet_change"}).get_text().strip())
    # Wallet balance
    transaction_data.append(row.find("td", {"class": "wht_wallet_balance"}).get_text().strip())
    return Transaction._make(transaction_data)

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    main_table = soup.find("table", {"class": "wallet_history_table"})
    if main_table:
        return [parse_row(row) for row in main_table.tbody.find_all("tr", recursive=False)]
    return []

def read_html_file(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        return parse_html(html_file.read())

def write_json_file(json_file_path, data):
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps([transaction._asdict() for transaction in data if transaction is not None]))