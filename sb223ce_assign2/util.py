import pandas as pd


class Util:

    @staticmethod
    def get_df(min_package_size):
        try:
            return pd.read_excel('filtered_data.xlsx')
        except FileNotFoundError:
            df = pd.read_excel('data.xlsx')

            packages_names = []
            for full_qualified_name in df.get('FullQualifiedName'):
                name = full_qualified_name.split('.java')[0]
                packages_names.append(name[0: name.rindex('.')])
            df.insert(loc=0, column='Package Name', value=packages_names)

            packages_count = df['Package Name'].value_counts()
            for package_name, count in zip(packages_count.index, packages_count):
                if count < min_package_size:
                    df = df.replace(to_replace=package_name, value='others')

            df = df.drop(columns=[
                'Maintainability', 'CBO', 'CYC_Classes', 'ILCOM', 'LCOM', 'LD',
                'LEN', 'MPC', 'NAM', 'NOM', 'RFC', 'FullQualifiedName'
            ])

            df = df.rename(index=str, columns={
                'name': 'Class Name',
                'LOD_Class': 'LOD'
            })

            df.to_excel(excel_writer='filtered_data.xlsx', index=False)
            return pd.read_excel('filtered_data.xlsx')

    @staticmethod
    def compute_single_inverse_metrics(df, metrics_impacts, x, criteria):
        temp_df = df.copy()
        for metric, impact in metrics_impacts:
            inverse_metrics = [0 for _ in range(len(temp_df))]
            for package_name in temp_df['Package Name'].unique():
                package_df = temp_df.loc[temp_df['Package Name'] == package_name]
                package_df = package_df.sort_values(by=metric, ascending=impact)
                criteria(df=package_df, x=x, inverse_metrics=inverse_metrics, metric=metric, impact=impact)
            temp_df.insert(loc=temp_df.columns.get_loc(metric) + 1, column=metric + "'", value=inverse_metrics)
        return temp_df

    @staticmethod
    def compute_double_triple_inverse_metrics(single_inverse_metrics_df, metrics_impacts):
        temp_df = pd.DataFrame(data=single_inverse_metrics_df['Package Name'].unique(), columns=['Package Name'])
        for metric, impact in metrics_impacts:
            double_inverse_metrics, triple_inverse_metrics = [], []
            for package_name in single_inverse_metrics_df['Package Name'].unique():
                package_df = single_inverse_metrics_df.loc[single_inverse_metrics_df['Package Name'] == package_name]
                double_inverse_metric = package_df[metric + "'"].sum()
                double_inverse_metrics.append(double_inverse_metric)
                triple_inverse_metrics.append(double_inverse_metric / len(package_df))
            temp_df.insert(loc=len(temp_df.columns), column=metric + "''", value=double_inverse_metrics)
            temp_df.insert(loc=len(temp_df.columns), column=metric + "'''", value=triple_inverse_metrics)
        return temp_df

    @staticmethod
    def compute_properties(double_triple_inverse_metrics_df, properties):
        temp_df = pd.DataFrame(data=double_triple_inverse_metrics_df['Package Name'], columns=['Package Name'])
        for property_name, sub_properties, in properties:
            property_df = pd.DataFrame(data=[0 for _ in range(len(temp_df))], columns=[property_name])
            for sub_property_name, sub_property_metrics_weights, in sub_properties:
                sub_properties_values = []
                for package_name in double_triple_inverse_metrics_df['Package Name']:
                    sub_property_value, sub_property_weights = 0, 0
                    package_df = double_triple_inverse_metrics_df.loc[
                        double_triple_inverse_metrics_df['Package Name'] == package_name
                    ]
                    for metric, weight in sub_property_metrics_weights:
                        sub_property_value += weight * package_df[metric + "'''"].get_values()[0]
                        sub_property_weights += weight
                    sub_properties_values.append(sub_property_value / sub_property_weights)
                temp_df.insert(loc=len(temp_df.columns), column=sub_property_name, value=sub_properties_values)
                property_df[property_name] += temp_df[sub_property_name]
            temp_df.insert(loc=len(temp_df.columns), column=property_name, value=property_df[property_name])
        return temp_df

    @staticmethod
    def mark_top_x(df, x, inverse_metrics, **_):
        for index, row_index in enumerate(df.index):
            inverse_metrics[row_index] = 1 if index < x else 0

    @staticmethod
    def mark_top_x_percent(df, x, inverse_metrics, **_):
        top_x_percent = round((x / 100) * len(df))
        for index, row_index in enumerate(df.index):
            inverse_metrics[row_index] = 1 if index < top_x_percent else 0

    @staticmethod
    def mark_top_x_percent_in_range(df, x, inverse_metrics, metric, impact):
        min_val = min(df[metric])
        max_val = max(df[metric])
        if impact:
            max_val = min_val + ((x / 100) * (max_val - min_val))
        else:
            min_val = max_val - (x / 100) * (max_val - min_val)
        for row_index, metric_val in zip(df.index, df[metric]):
            if min_val <= metric_val <= max_val:
                inverse_metrics[row_index] = 1
            else:
                inverse_metrics[row_index] = 0

    @staticmethod
    def save_data_frames(sheet_name_df, file_name):
        with pd.ExcelWriter(file_name) as writer:
            for sheet_name, df in sheet_name_df:
                df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False)
