def col_groupby_cdf(data, col, metric_col, ascending=False):

    '''Cumulative Distribution Function

    Takes in a dataframe with at least 2 columns, and returns a
    groupby table with CDF.

    data | DataFrame | a pandas dataframe with the data
    col | str | name of the column to be grouped by
    metric_col | str | name of the column to be evaluated against
    ascending | bool | the direction of sorting to be applied

    '''

    def _cdf(x):
        return round(1 - (x.groupby(metric_col).agg('count') / len(x)).cumsum(), 2)

    out = data[[col, metric_col]].groupby(col).apply(_cdf).rename(columns = {col: 'CDF'}).sort_values(metric_col, ascending=ascending)

    return out
