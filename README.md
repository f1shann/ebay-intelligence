eBay MarketPlace FLipping Project: eBay UK Resale Tool

Finds eBay UK listings priced below the median resale value for a product. It compares live listings against a sold-price baseline, filters out junk and outliers, and estimates profit after shipping and eBay’s buyer protection fee.

Download

Grab the latest FlipIQ.exe from the Releases page and run it on Windows. It comes with bundled sample data, so you can try it without any keys.

To use live listings and sold data, create a .env file next to the exe with:

APP_ID, CERT_ID and EBAY_ENV from your eBay developer account (live listings)
APIFY_API_TOKEN (sold baseline)

Then run it and type find iphone 15 pro max.

How it works
Fetch: pulls live listings from the eBay Browse API, and recent sold listings through an Apify actor. Without keys, it uses bundled sample data.
Filter junk: removes titles with fault or non-item words (faulty, broken, box only, for parts, locked, and similar), matched by whole word or phrase.
Filter models and variants: keeps only listings containing every number from the query, and removes multi-model or multi-storage titles like “16/15” or “128GB/256GB”.
Split by condition: groups listings as New, Opened, Refurbished or Used, and analyses each separately.
Remove outliers: drops prices outside 1.5 × IQR, for both live and sold data.
Set the baseline: uses the median of sold prices, with the coefficient of variation (CV) showing how tight the market is. A condition with fewer than 15 sold sales is reported as unreliable rather than given a median.
Flag deals: calculates total cost (item price plus first shipping option), deviation from the baseline, and estimated profit after shipping and buyer protection fees. Listings above the minimum profit are printed with their link.

Example Output(not real deals just an example):
> find iphone 15 pro max
baseline median: 486.95
cv: 10.2
iPhone 15 Pro Max Blue Titanium 256GB, total cost (including shipping): 408.15, deviation: 16.2, profit: 61.0 https://www.ebay.co.uk/itm/960115016216
Apple iPhone 15 Pro Max - 256GB - Black Titanium (Unlocked), total cost (including shipping): 410.95, deviation: 15.6, profit: 58.14 https://www.ebay.co.uk/itm/198742945865

Known limitations
The tool does not separate by conditions yet which it should do as different codnitions have different value.  I will work on this next
Work in progress. Discover (sold data analysis and saved baselines) and Hunt (live search and alerts) are not built yet.
