import pandas as pd

file_path = "c:/Users/Pedro Luis/Downloads/Clase 2811/Data/inventario_andina.csv"
df = pd.read_csv(file_path)

# Total sum of the column (Historical sum)
total_sum = df['valor_inventario_cop'].sum()

# Convert date
df['fecha_corte'] = pd.to_datetime(df['fecha_corte'])

# Sum by date
sum_by_date = df.groupby('fecha_corte')['valor_inventario_cop'].sum().sort_index()

print(f"Total Sum of ALL rows (Historical): ${total_sum:,.0f}")
print("\nSum by Date (Snapshots):")
print(sum_by_date)

latest_date = df['fecha_corte'].max()
latest_sum = df[df['fecha_corte'] == latest_date]['valor_inventario_cop'].sum()
print(f"\nLatest Snapshot ({latest_date.date()}) Sum: ${latest_sum:,.0f}")
