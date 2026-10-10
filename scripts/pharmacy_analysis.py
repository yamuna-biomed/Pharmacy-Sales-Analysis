import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)


df = pd.read_csv('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\data\\salesdaily.csv')

print("=" * 80)
print("PHARMACY SALES & DRUG ANALYSIS")
print("=" * 80)
print(f"Total records: {len(df)}")
print(f"Date range: {df['datum'].min()} to {df['datum'].max()}")
print(f"Columns: {list(df.columns)}")
print()


df['datum'] = pd.to_datetime(df['datum'])

# Get medicine names from columns (all except metadata columns)
medicine_columns = ['M01AB', 'M01AE', 'N02BA', 'N02BE', 'N05B', 'N05C', 'R03', 'R06']

#  total sales per medicine
total_sales_per_medicine = df[medicine_columns].sum()

print("=" * 80)
print("TOTAL SALES BY MEDICINE")
print("=" * 80)
for medicine, sales in total_sales_per_medicine.sort_values(ascending=False).items():
    print(f"{medicine}: ${sales:,.2f}")
print()

#  CHART 1: TOP-SELLING MEDICINES 
print("Creating Chart 1: Top-Selling Medicines...")
plt.figure(figsize=(12, 6))
plt.barh(total_sales_per_medicine.index, total_sales_per_medicine.values, color='steelblue')
plt.xlabel('Total Sales Revenue ($)')
plt.ylabel('Medicine Code')
plt.title('Top-Selling Medicines - Total Revenue')
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\1_top_selling_medicines.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 1_top_selling_medicines.png\n")

#  CHART 2: MONTHLY SALES GROWTH 
print("Creating Chart 2: Monthly Sales Growth...")
df_monthly = df.groupby(df['datum'].dt.to_period('M'))[medicine_columns].sum().sum(axis=1)
df_monthly.index = df_monthly.index.to_timestamp()

plt.figure(figsize=(14, 6))
plt.plot(df_monthly.index, df_monthly.values, marker='o', linewidth=2, color='darkgreen', markersize=6)
plt.xlabel('Month')
plt.ylabel('Total Sales Revenue ($)')
plt.title('Monthly Sales Growth - Overall Trend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\2_monthly_sales_growth.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 2_monthly_sales_growth.png\n")

#  CHART 3: SALES BY DAY OF WEEK 
print("Creating Chart 3: Sales by Day of Week...")
weekday_sales = df.groupby('Weekday Name')[medicine_columns].sum().sum(axis=1)
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_sales = weekday_sales.reindex(weekday_order)

plt.figure(figsize=(12, 6))
plt.bar(range(len(weekday_sales)), weekday_sales.values, color='coral')
plt.xticks(range(len(weekday_sales)), weekday_sales.index, rotation=45)
plt.xlabel('Day of Week')
plt.ylabel('Total Sales Revenue ($)')
plt.title('Pharmacy Sales by Day of Week')
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\3_sales_by_weekday.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 3_sales_by_weekday.png\n")

#  CHART 4: MEDICINE COMPARISON (PIE CHART) 
print("Creating Chart 4: Medicine Sales Distribution...")
plt.figure(figsize=(10, 8))
colors = plt.cm.Set3(np.linspace(0, 1, len(medicine_columns)))
plt.pie(total_sales_per_medicine.values, labels=total_sales_per_medicine.index, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Sales Distribution Across Medicines')
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\4_medicine_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 4_medicine_distribution.png\n")

#  CHART 5: MEDICINE TRENDS OVER TIME 
print("Creating Chart 5: Medicine Sales Trends...")
df_monthly_by_medicine = df.set_index('datum').groupby(df.set_index('datum').index.to_period('M'))[medicine_columns].sum()
df_monthly_by_medicine.index = df_monthly_by_medicine.index.to_timestamp()

plt.figure(figsize=(16, 8))
for medicine in medicine_columns:
    plt.plot(df_monthly_by_medicine.index, df_monthly_by_medicine[medicine], marker='o', label=medicine, linewidth=2)
plt.xlabel('Month')
plt.ylabel('Sales Revenue ($)')
plt.title('Individual Medicine Sales Trends Over Time')
plt.legend(loc='best')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\5_medicine_trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 5_medicine_trends.png\n")

#  CHART 6: YEARLY COMPARISON 
print("Creating Chart 6: Yearly Sales Comparison...")
yearly_sales = df.groupby('Year')[medicine_columns].sum().sum(axis=1)

plt.figure(figsize=(10, 6))
plt.bar(yearly_sales.index, yearly_sales.values, color='mediumseagreen', width=0.6)
plt.xlabel('Year')
plt.ylabel('Total Sales Revenue ($)')
plt.title('Total Sales Revenue by Year')
plt.xticks(yearly_sales.index)
plt.tight_layout()
plt.savefig('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\6_yearly_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: 6_yearly_comparison.png\n")

#  DETAILED ANALYSIS REPORT 
print("=" * 80)
print("DETAILED ANALYSIS REPORT")
print("=" * 80)

print("\n1. TOP 3 BEST-SELLING MEDICINES:")
top3 = total_sales_per_medicine.sort_values(ascending=False).head(3)
for idx, (medicine, sales) in enumerate(top3.items(), 1):
    percentage = (sales / total_sales_per_medicine.sum()) * 100
    print(f"   {idx}. {medicine}: ${sales:,.2f} ({percentage:.1f}% of total sales)")

print("\n2. LOWEST SELLING MEDICINES:")
bottom3 = total_sales_per_medicine.sort_values(ascending=True).head(3)
for idx, (medicine, sales) in enumerate(bottom3.items(), 1):
    percentage = (sales / total_sales_per_medicine.sum()) * 100
    print(f"   {idx}. {medicine}: ${sales:,.2f} ({percentage:.1f}% of total sales)")

print("\n3. MONTHLY SALES STATISTICS:")
print(f"   Highest monthly sales: ${df_monthly.max():,.2f}")
print(f"   Lowest monthly sales: ${df_monthly.min():,.2f}")
print(f"   Average monthly sales: ${df_monthly.mean():,.2f}")

print("\n4. SALES BY DAY OF WEEK:")
for day in weekday_order:
    sales = weekday_sales[day]
    print(f"   {day}: ${sales:,.2f}")

print("\n5. YEARLY BREAKDOWN:")
for year, sales in yearly_sales.items():
    print(f"   {year}: ${sales:,.2f}")

print("\n6. TOTAL PHARMACY SALES:")
total_sales = total_sales_per_medicine.sum()
print(f"   Overall Total: ${total_sales:,.2f}")

# Save summary report to file
with open('C:\\Users\\Divya\\Documents\\GitHub\\Pharmacy-Sales-Analysis\\output\\Sales_Report.txt', 'w') as f:
    f.write("PHARMACY SALES & DRUG ANALYSIS REPORT\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("TOP-SELLING MEDICINES:\n")
    for medicine, sales in total_sales_per_medicine.sort_values(ascending=False).items():
        f.write(f"{medicine}: ${sales:,.2f}\n")
    
    f.write(f"\nTOTAL SALES: ${total_sales:,.2f}\n")
    f.write(f"Average Monthly Sales: ${df_monthly.mean():,.2f}\n")

print("\n✓ Report saved: Sales_Report.txt")

print("\n" + "=" * 80)
print("✓ ALL ANALYSES COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("\nOutput files saved in: output/ folder")
print("1. top_selling_medicines.png")
print("2. monthly_sales_growth.png")
print("3. sales_by_weekday.png")
print("4. medicine_distribution.png")
print("5. medicine_trends.png")
print("6. yearly_comparison.png")
print("7. Sales_Report.txt")