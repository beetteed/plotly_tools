import datetime
import dateutil
import re

    
def add_range_selector(layout, axis_name='xaxis', ranges=None, default=None):    
    """Add a rangeselector to the layout if it doesn't already have one.
    
    :param ranges: which ranges to add, e.g. ['3m', '1y', 'ytd']
    :param default_range: which range to choose as the default, e.g. '3m'
    """
    axis = layout.setdefault(axis_name, dict())
    axis.setdefault('type', 'date')
    axis.setdefault('rangeslider', dict())
    if ranges is None:
        # Make some nice defaults
        ranges = ['1m', '6m', 'ytd', '1y', 'all']
    re_split = re.compile('(\d+)')
    def range_split(range):
        split = re.split(re_split, range)
        assert len(split) == 3
        return (int(split[1]), split[2])
    # plotly understands m, but not d or y!
    step_map = dict(d='day', m='month', y='year')
    def make_button(range):
        range = range.lower()
        if range == 'all':
            return dict(step='all')
        elif range == 'ytd':
            return dict(count=1,
                label='YTD',
                step='year',
                stepmode='todate')
        else:
            (count, step) = range_split(range)
            step = step_map.get(step, step)
            return dict(count=count,
                label=range,
                step=step,
                stepmode='backward')
    axis.setdefault('rangeselector', dict(buttons=[make_button(r) for r in ranges]))
    if default is not None and default != 'all':
        end_date = datetime.datetime.today()
        if default.lower() == 'ytd':
            start_date = datetime.date(end_date.year, 1, 1)
        else:
            (count, step) = range_split(default)
            step = step_map[step] + 's'  # relativedelta needs plurals
            start_date = (end_date - dateutil.relativedelta.relativedelta(**{step: count}))
        axis.setdefault('range', [start_date, end_date])