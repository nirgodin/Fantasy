from Code.old_versions.v1.Functions import PreProcessing, Insights

ins = Insights(last_gw=38,
               season=21)

pp = PreProcessing(first_gw=5,
                   last_gw=38,
                   season=21)

fpl_data = pp.fpl_concat()
plt_data = pp.plt_concat()
schedule = pp.schedule_melt()

FPL_subtract = ['Pts.', 'Minutes played', 'Goals scored', 'Assists', 'Clean sheets',
                'Goals conceded', 'Own goals', 'Penalties saved', 'Penalties missed',
                'Yellow cards', 'Red cards', 'Saves', 'Bonus', 'Bonus Points System',
                'Times in Dream Team', 'Transfers in', 'Transfers out']


# Manipulate fpl data
ts_data = pp.subtracting(fpl_data, FPL_subtract)

# Create stable players df
stability_data = ins.stability_scores(ts_data=ts_data,
                                      pts_thresh=3.5,
                                      minutes_thresh=30)

value_data = ins.value_for_money(ts_data, role_relative=False)

team_pts = ins.team_pts(ts_data)

seizure = ins.opportunity_seizure(ts_data, role_relative=False)
