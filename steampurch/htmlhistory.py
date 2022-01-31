"""Parse Steam purchase history HTML file"""
from collections import namedtuple
from bs4 import BeautifulSoup

Transaction = namedtuple("Transaction", "date, items, type, payment, total, wallet_change, wallet_balance")

def parse_row(row):
    """Parse a row of Steam purchase history table into a named tuple"""
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
    payment_means = row.find("td", {"class": "wht_type"}).find("div", {"class": "wth_payment"}).get_text().strip()
    transaction_data.append([
        [payment for payment in payment_mean.strip().split("\t") if payment != ""]
            for payment_mean in payment_means.split("\n")
            if payment_mean != ""])
    # Amount
    transaction_data.append(
        row.find("td", {"class": "wht_total"}).get_text().strip().replace("\t", "").replace("\n", " "))
    # Wallet amount change
    transaction_data.append(row.find("td", {"class": "wht_wallet_change"}).get_text().strip())
    # Wallet balance
    transaction_data.append(row.find("td", {"class": "wht_wallet_balance"}).get_text().strip())
    return Transaction._make(transaction_data)

def parse_html(html):
    """Parse a string containing an entire HTML document"""
    soup = BeautifulSoup(html, "html.parser")
    main_table = soup.find("table", {"class": "wallet_history_table"})
    if main_table:
        return [
            parsed_row
            for row in main_table.tbody.find_all("tr", recursive=False)
            if (parsed_row := parse_row(row)) is not None]
    return []

def read_html_file(html_file_path):
    """Open and parse an HTML document provided by file path"""
    with open(html_file_path, "r", encoding="utf-8") as html_file:
        return parse_html(html_file.read())
