from util import Util

direct_impact = True
indirect_impact = False

metrics_impacts = [
    ('LOC', indirect_impact), ('WMC', indirect_impact),
    ('DIT', indirect_impact), ('NOC', indirect_impact),
    ('DAC', indirect_impact), ('TCC', direct_impact),
    ('LOD', indirect_impact)
]

df = Util.get_df(min_package_size=16)

print(df['Package Name'].value_counts())

top_15_single_inverse_metrics_df = Util.compute_single_inverse_metrics(
    df=df, metrics_impacts=metrics_impacts,
    criteria=Util.mark_top_x, x=15
)

top_15_percent_single_inverse_metrics_df = Util.compute_single_inverse_metrics(
    df=df, metrics_impacts=metrics_impacts,
    criteria=Util.mark_top_x_percent, x=15
)

top_15_percent_in_range_single_inverse_metrics_df = Util.compute_single_inverse_metrics(
    df=df, metrics_impacts=metrics_impacts,
    criteria=Util.mark_top_x_percent_in_range, x=15
)

top_15_double_triple_inverse_metrics = Util.compute_double_triple_inverse_metrics(
    single_inverse_metrics_df=top_15_single_inverse_metrics_df,
    metrics_impacts=metrics_impacts
)

top_15_percent_double_triple_inverse_metrics = Util.compute_double_triple_inverse_metrics(
    single_inverse_metrics_df=top_15_percent_single_inverse_metrics_df,
    metrics_impacts=metrics_impacts
)

top_15_percent_in_range_double_triple_inverse_metrics = Util.compute_double_triple_inverse_metrics(
    single_inverse_metrics_df=top_15_percent_in_range_single_inverse_metrics_df,
    metrics_impacts=metrics_impacts
)


properties = [
    ('Re-Usability', [
        ('Understandability', [('LOC', 2), ('WMC', 2), ('DIT', 2), ('NOC', 2), ('DAC', 2), ('TCC', 2), ('LOD', 2)]),
        ('Learnability', [('LOC', 1), ('WMC', 2), ('DIT', 2), ('NOC', 2), ('DAC', 1), ('TCC', 1), ('LOD', 2)]),
        ('Operability', [('LOC', 1), ('WMC', 2), ('DIT', 2), ('NOC', 2), ('DAC', 1), ('TCC', 1), ('LOD', 2)]),
        ('Attractiveness', [('LOC', 2), ('WMC', 2), ('DIT', 2), ('NOC', 2), ('DAC', 2), ('TCC', 2), ('LOD', 1)]),
    ]),
    ('Maintainability', [
        ('Analyzability', [('LOC', 2), ('WMC', 2), ('DIT', 2), ('NOC', 1), ('DAC', 2), ('TCC', 2), ('LOD', 2)]),
        ('Changeability', [('LOC', 2), ('WMC', 2), ('DIT', 2), ('NOC', 2), ('DAC', 2), ('TCC', 2), ('LOD', 2)]),
        ('Stability', [('LOC', 1), ('WMC', 1), ('DIT', 1), ('NOC', 1), ('DAC', 2), ('TCC', 2), ('LOD', 1)]),
        ('Testability', [('LOC', 2), ('WMC', 2), ('DIT', 2), ('NOC', 1), ('DAC', 2), ('TCC', 2), ('LOD', 2)])
    ])
]

top_15_properties = Util.compute_properties(
    double_triple_inverse_metrics_df=top_15_double_triple_inverse_metrics, properties=properties
)

top_15_percent_properties = Util.compute_properties(
    double_triple_inverse_metrics_df=top_15_percent_double_triple_inverse_metrics, properties=properties
)

top_15_percent_in_range_properties = Util.compute_properties(
    double_triple_inverse_metrics_df=top_15_percent_in_range_double_triple_inverse_metrics, properties=properties
)

Util.save_data_frames(
    sheet_name_df=[
        ('top 15 1st inv mtr', top_15_single_inverse_metrics_df),
        ('top 15% 1st inv mtr', top_15_percent_single_inverse_metrics_df),
        ('top 15% in range 1st inv mtr', top_15_percent_in_range_single_inverse_metrics_df),
        ('top 15 2-3rd inv mtr', top_15_double_triple_inverse_metrics),
        ('top 15% 2-3rd inv mtr', top_15_percent_double_triple_inverse_metrics),
        ('top 15% in range 2-3rd inv mtr', top_15_percent_in_range_double_triple_inverse_metrics),
        ('top 15 properties', top_15_properties),
        ('top 15% properties', top_15_percent_properties),
        ('top 15% in range properties', top_15_percent_in_range_properties)
    ],
    file_name=' top_15.xlsx'
)

