from matplotlib import pyplot as plt

# Five-number summary
min_val = 110.45
q1 = 120.31
median = 122.45
q3 = 124.21
max_val = 127.25

# Create boxplot using summary stats
fig, ax = plt.subplots()

ax.bxp([{
    'med': median,
    'q1': q1,
    'q3': q3,
    'whislo': min_val,
    'whishi': max_val,
    'fliers': []
}], showfliers=False)

ax.set_title("Boxplot (Datos agrupados)")
ax.set_ylabel("Valores")

plt.show()
