import pandas as pd
import matplotlib.pyplot as plt

csv = pd.read_csv('data.csv')


def plot(x_col, y_col, x_max, y_max, x_label, y_label, title):
    plt.figure()

    for x, y, name in zip(csv.get(x_col), csv.get(y_col), csv.get('name')):
        if x > x_max or y > y_max:
            plt.scatter(x, y, color='red')
            plt.text(x, y, name, horizontalalignment='left', verticalalignment='top')
        else:
            plt.scatter(x, y, color='green')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.show()


def compute_global_statistics():
    packages = []

    for package in csv.get('FullQualifiedName'):
        package = package.split('.java')[0].split('.')

        if package not in packages:
            packages.append(package)

    return {
        'packages': len(packages),
        'methods': sum(csv.get('NOM')),
        'lines_of_code': sum(csv.get('LOC'))
    }


plot(
    x_col='LOC', y_col='WMC',
    x_max=800, y_max=80,
    x_label='Lines of Code (LOC)', y_label='Weighted Method Count (WMC)',
    title='Size vs Complexity'
)

plot(
    x_col='TCC', y_col='DAC',
    x_max=1, y_max=15,
    x_label='Tight Package Cohesion (TCC)', y_label='Data Abstract Coupling (DAC)',
    title='Cohesion vs Coupling'
)

plot(
    x_col='DIT', y_col='CBO',
    x_max=4, y_max=15,
    x_label='Depth of Inheritance (DIT)', y_label='Coupling Between Objects (CBO)',
    title='Inheritance vs Coupling'
)

plot(
    x_col='NOC', y_col='WMC',
    x_max=4, y_max=80,
    x_label='Number of Children (NOC)', y_label='Weighted Method Count (WMC)',
    title='No. of Children vs Complexity'
)

print(compute_global_statistics())
