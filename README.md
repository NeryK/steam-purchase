# steam-purchase

Tool to export Steam purchase history to CSV or JSON, and also display some stats along the way.

## Usage

### Instructions

1. Log into your Steam account in a browser
2. Navigate to [https://store.steampowered.com/account/history]
3. Scroll to the bottom of the page and click the "LOAD MORE TRANSACTIONS" button
4. Repeat until all transactions are loaded (no more button displayed)
5. Save the HTML web page as a file (like `C:\Temp\NeryK's account.htm`)
6. Run the tool `python -m steampurch -i "C:\Temp\NeryK's account.htm" -c "C:\Temp\neryk_transactions.csv"`
7. Import CSV in your favorite spreadsheet software
8. Enjoy happy graph fun times

### Advanced

- Output JSON instead of CSV (or both) `python -m steampurch -i "C:\Temp\NeryK's account.htm" -j "C:\Temp\neryk_transactions.json"`
- Write stats to stdout `python -m steampurch -i "C:\Temp\NeryK's account.htm" -s`
  - This currently only works if the web page was displayed in English
