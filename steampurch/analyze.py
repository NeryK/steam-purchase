"""Interpret Steam purchase history data"""
from collections import namedtuple
import dateparser
import price_parser

ConvertedTransaction = namedtuple(
    "ConvertedTransaction", [
        "isodate", "is_refund", "is_credit", "items", "type", "payment", "total_amount_numeric", "total_currency",
        "total_additional", "wallet_change", "wallet_balance_numeric", "wallet_balance_currency"])

def convert(data):
    """Read strings into objects"""
    converted_data = []
    for transaction in data:
        isodate = dateparser.parse(transaction.date).date().isoformat()
        total_price = price_parser.Price.fromstring(transaction.total_amount)
        wallet_balance_price = price_parser.Price.fromstring(transaction.wallet_balance)
        if wallet_balance_price.amount is not None:
            wallet_balance_price_amount = float(wallet_balance_price.amount)
        else:
            wallet_balance_price_amount = None
        converted_data.append(ConvertedTransaction(
            isodate, transaction.is_refund, transaction.is_credit, transaction.items, transaction.type,
            transaction.payment, float(total_price.amount), total_price.currency, transaction.total_additional,
            transaction.wallet_change, wallet_balance_price_amount, wallet_balance_price.currency))
    return converted_data

def sum_transactions(transactions, currency):
    """Sum debit and credit transactions for a given currency"""
    total_debit = sum([
        transaction.total_amount_numeric
        for transaction in transactions
        if not transaction.is_refund
        and not transaction.wallet_change.startswith("-")
        and transaction.total_currency == currency])
    total_credit = sum([
        transaction.total_amount_numeric
        for transaction in transactions
        if (transaction.is_refund or transaction.is_credit)
        and transaction.total_currency == currency])
    return currency, round(total_debit - total_credit, 2)

def stats(converted_data):
    """Print yearly stats"""
    transaction_by_year = {}
    for transaction in converted_data:
        year = dateparser.parse(transaction.isodate).year
        if year in transaction_by_year:
            transaction_by_year[year].append(transaction)
        else:
            transaction_by_year[year] = [transaction]
    currencies = {transaction.total_currency for transaction in converted_data}
    totals_by_year = {}
    for year, transactions in transaction_by_year.items():
        for currency in currencies:
            if year in totals_by_year:
                totals_by_year[year].append(sum_transactions(transactions, currency))
            else:
                totals_by_year[year] = [sum_transactions(transactions, currency)]
    for year, totals in totals_by_year.items():
        print(f"Spent in {year}:")
        for currency, amount in totals:
            if amount > 0:
                print(f"\t{amount} {currency}")
    totals_all_time = []
    for currency in currencies:
        totals_all_time.append(sum_transactions(converted_data, currency))
    print("Total spent:")
    for currency, amount in totals_all_time:
        if amount > 0:
            print(f"\t{amount} {currency}")
