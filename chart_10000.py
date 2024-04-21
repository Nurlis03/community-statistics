import matplotlib.pyplot as plt

# Data
labels = ['With Discord', 'Without Discord']
sizes = [2630, 7370]
colors = ['#1f77b4', '#ff7f0e']  # Using blue and orange colors
explode = (0.1, 0)  # explode the 1st slice (With Discord)

# Plot
plt.figure(figsize=(8, 6))
patches, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Communities with and without Discord')

# Adding community counts to the legend
plt.legend(patches, [f'{label}: {size}' for label, size in zip(labels, sizes)], loc="best")

# Adding description
description = "This chart illustrates the distribution of Discord and non-Discord communities among the top 10,000 most popular communities."
plt.figtext(0.5, 0.01, description, wrap=True, horizontalalignment='center', fontsize=12)

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
