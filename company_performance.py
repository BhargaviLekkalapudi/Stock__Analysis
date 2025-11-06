import csv
from datetime import datetime

#Function: Read data from CSV file
#Purpose: To read stock data from a CSV file and return a list of valid stock entries.
#Notes: Handles missing or invalid data safely.

def read_csv_safe(filename):
    stocks = []
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)   #Using DictReader to read CSV into a dictionary

            for row in reader:
                try:       #To Extract and validate data
                    name = row['Stock'].strip()
                    sector = row['Sector'].strip()
                    start_price = row['PriceStart']
                    end_price = row['PriceEnd']

                    if not start_price or not end_price:
                        print("Skipping row due to missing prices:", row)
                        continue  # Skip if prices are zero or missing

                    start_price = float(start_price)
                    end_price = float(end_price)

                    if start_price > 0 and end_price > 0: #adds only valid rows with positive prices
                        stocks.append({
                            'Stock': name,
                            'Sector': sector,
                            'PriceStart': start_price,
                            'PriceEnd': end_price
                        })
                except (ValueError, KeyError):  # Skip invalid data
                    print("Skipping invalid row:", row)
                    continue
    except FileNotFoundError:
        print("File not found:", filename)
    return stocks


#Function: Calculate return for each stock
#Purpose: To compute the percentage return based on starting and ending prices.

def compute_return(stock):
    start = stock['PriceStart']
    end = stock['PriceEnd']
    change = ((end - start) / start) * 100
    stock['Return'] = round(change, 2)
    return stock


#Function: Sort stocks by return
#Purpose: To sort the list of stocks in descending order based on their return percentage.

def process_all(data):
    return sorted(data, key=lambda x: x['Return'], reverse=True)


#Function: Find average return by sector
#Purpose: To compute average return and count of stocks for each sector.

def aggregrate_by_sector(data):
    summary = {}
    for s in data:
        sector = s['Sector']
        if sector not in summary:
            summary[sector] = {'total': 0, 'count': 0}
        summary[sector]['total'] += s['Return']
        summary[sector]['count'] += 1

    for sec in summary: #Compute average return for each sector
        avg = summary[sec]['total'] / summary[sec]['count']
        summary[sec]['avg_return'] = round(avg, 2)
    return summary


#Function: Print report on screen
#Purpose: To display stock details, top performers, and sector summary.

def print_report(data, summary):
    print("\nAll Stock Details")
    print("-" * 60)
    print(f"{'Stock':<15}{'Sector':<20}{'Start':<10}{'End':<10}{'Return(%)':<10}")
    for s in data:
        print(f"{s['Stock']:<15}{s['Sector']:<20}{s['PriceStart']:<10}{s['PriceEnd']:<10}{s['Return']:<10}")

    print("\nTop 5 Stocks by Return")
    print("-" * 60)
    for s in data[:5]:
        print(f"{s['Stock']:<15}{s['Return']}%")

    print("\nSector Summary")
    print("-" * 60)
    best = max(summary.items(), key=lambda x: x[1]['avg_return'])
    for sec, val in summary.items():
        print(f"{sec:<20} Avg Return: {val['avg_return']}%   Count: {val['count']}")
    print(f"\nBest Sector: {best[0]} ({best[1]['avg_return']}%)")



#Function: Save results to CSV file
#Purpose: To write the processed stock data with returns into a new CSV file.

def export_csv(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_report_{timestamp}.csv"
    fields = ['Stock', 'Sector', 'PriceStart', 'PriceEnd', 'Return']
    try:
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
        print("\nData saved to", filename)
    except OSError:
        print("Error saving to file:", filename)    


#Function: Main program execution
#Purpose: To manage the overall flow of reading, processing, and reporting stock data.

if __name__ == "__main__":
    filename = input("Enter CSV filename: ").strip()   #Ask user for filename instead of hardcoding
    data = read_csv_safe(filename)

# Check if data is empty and exit if no valid data found

    if not data:
        print("No valid data found. Exiting program.")
        exit()

# Process data and generate report

    data = [compute_return(s) for s in data]
    data = process_all(data)
    summary = aggregrate_by_sector(data)

#Display report and save to CSV

    print_report(data, summary)
    export_csv(data)