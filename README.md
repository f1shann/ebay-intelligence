FlipIQ: eBay UK Resale Tool

Finds eBay UK listings priced below the median for a product.

How it works
1. Fetches listings from the eBay Browse API.
2. Removes junk titles (faulty, box only, for parts, and similar).
3. Removes price outliers using the IQR method.
4. Compares each listing's price plus shipping to the median and flags deals.

Run it
1. Install Python 3.10 or newer.
2. Clone the repo: `git clone https://github.com/f1shann/ebay-intelligence`
3. `cd ebay-intelligence`
4. Install the packages: `pip install requests python-dotenv`
5. Run `python main.py`, then type `find iphone 15 pro max`.

With no `.env` file, the tool uses `sample_data.json`, so no eBay keys are needed.

Live mode (optional)
Create a `.env` file with `APP_ID`, `CERT_ID` and `EBAY_ENV` from your eBay developer account. Without it, the sample data is used.

Status
Work in progress. Discover and Hunt are not built yet
