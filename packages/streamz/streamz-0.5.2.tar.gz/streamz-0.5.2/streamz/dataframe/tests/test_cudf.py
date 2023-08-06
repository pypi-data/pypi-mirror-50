"""
Tests for cudf DataFrames:
All tests have been cloned from the test_dataframes module in the same folder.
Some of these tests pass with cudf, and others are marked with xfail
where a pandas-like method is not yet implemented in cudf.
But these tests should pass as and when cudf rolls out more pandas-like methods.
"""
from __future__ import division, print_function

import operator

import pytest
from dask.dataframe.utils import assert_eq
import numpy as np
import pandas as pd

from streamz import Stream
from streamz.dataframe import DataFrame, Series, DataFrames, Aggregation
from streamz.dask import DaskStream

from distributed import Client


cudf = pytest.importorskip("cudf")


@pytest.fixture(scope="module")
def client():
    client = Client(processes=False, asynchronous=False)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture(params=['core', 'dask'])
def stream(request, client):  # flake8: noqa
    if request.param == 'core':
        return Stream()
    else:
        return DaskStream()


def test_identity(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)
    L = sdf.stream.gather().sink_to_list()

    sdf.emit(df)

    assert L[0] is df
    assert list(sdf.example.columns) == ['x', 'y']

    x = sdf.x
    assert isinstance(x, Series)
    L2 = x.stream.gather().sink_to_list()
    assert not L2

    sdf.emit(df)
    assert isinstance(L2[0], cudf.Series)
    assert assert_eq(L2[0], df.x)


def test_dtype(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)

    assert str(sdf.dtypes) == str(df.dtypes)
    assert sdf.x.dtype == df.x.dtype
    assert sdf.index.dtype == df.index.dtype


def test_attributes():
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df)

    assert getattr(sdf,'x',-1) != -1
    assert getattr(sdf,'z',-1) == -1

    sdf.x
    with pytest.raises(AttributeError):
        sdf.z


def test_exceptions(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)
    with pytest.raises(TypeError):
        sdf.emit(1)

    with pytest.raises(IndexError):
        sdf.emit(cudf.DataFrame())


@pytest.mark.parametrize('func', [
    pytest.param(lambda x: x.sum(),
                 marks=pytest.mark.xfail(
                     reason="'Series' object does not support item assignment")),
    pytest.param(lambda x: x.mean(),
                 marks=pytest.mark.xfail(
                     reason="'Series' object does not support item assignment")),
    lambda x: x.count(),
    pytest.param(lambda x: x.size,
                 marks=pytest.mark.xfail(reason="Not implemented"))
])
def test_reductions(stream, func):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    for example in [df, df.iloc[:0]]:
        sdf = DataFrame(example=example, stream=stream)

        df_out = func(sdf).stream.gather().sink_to_list()

        x = sdf.x
        x_out = func(x).stream.gather().sink_to_list()

        sdf.emit(df)
        sdf.emit(df)

        assert_eq(df_out[-1], func(cudf.concat([df, df])))
        assert_eq(x_out[-1], func(cudf.concat([df, df]).x))


@pytest.mark.parametrize('op', [
    operator.add,
    operator.and_,
    operator.eq,
    operator.floordiv,
    operator.ge,
    operator.gt,
    operator.le,
    operator.lshift,
    operator.lt,
    operator.mod,
    operator.mul,
    operator.ne,
    operator.or_,
    operator.pow,
    operator.rshift,
    operator.sub,
    operator.truediv,
    operator.xor,
])
@pytest.mark.parametrize('getter', [lambda df: df, lambda df: df.x])
def test_binary_operators(op, getter, stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    try:
        left = op(getter(df), 2)
        right = op(2, getter(df))
    except Exception:
        return

    a = DataFrame(example=df, stream=stream)
    li = op(getter(a), 2).stream.gather().sink_to_list()
    r = op(2, getter(a)).stream.gather().sink_to_list()

    a.emit(df)

    assert_eq(li[0], left)
    assert_eq(r[0], right)


@pytest.mark.parametrize('op', [
    operator.abs,
    operator.inv,
    operator.invert,
    operator.neg,
    lambda x: x.map(lambda x: x + 1),
    lambda x: x.reset_index(),
    lambda x: x.astype(float),
])
@pytest.mark.parametrize('getter', [lambda df: df, lambda df: df.x])
def test_unary_operators(op, getter):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    try:
        expected = op(getter(df))
    except Exception:
        return

    a = DataFrame(example=df)
    b = op(getter(a)).stream.sink_to_list()

    a.emit(df)

    assert_eq(b[0], expected)


@pytest.mark.parametrize('func', [
    lambda df: df.query('x > 1 and x < 4'),
    pytest.param(lambda df: df.x.value_counts().nlargest(2),
                 marks=pytest.mark.xfail(reason="`cudf.Series.add` is'nt implemented"))
])
def test_dataframe_simple(func):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    expected = func(df)

    a = DataFrame(example=df)
    L = func(a).stream.sink_to_list()

    a.emit(df)

    assert_eq(L[0], expected)


def test_set_index():
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

    a = DataFrame(example=df)

    b = a.set_index('x').stream.sink_to_list()
    a.emit(df)
    assert_eq(b[0], df.set_index('x'))

    b = a.set_index(a.y + 1).stream.sink_to_list()
    a.emit(df)
    assert_eq(b[0], df.set_index(df.y + 1))


def test_binary_stream_operators(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

    expected = df.x + df.y

    a = DataFrame(example=df, stream=stream)
    b = (a.x + a.y).stream.gather().sink_to_list()

    a.emit(df)

    assert_eq(b[0], expected)


def test_index(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    a = DataFrame(example=df, stream=stream)
    b = a.index + 5
    L = b.stream.gather().sink_to_list()

    a.emit(df)
    a.emit(df)

    assert_eq(L[0], df.index + 5)
    assert_eq(L[1], df.index + 5)


def test_pair_arithmetic(stream):
    df = cudf.DataFrame({'x': list(range(10)), 'y': [1] * 10})

    a = DataFrame(example=df.iloc[:0], stream=stream)
    L = ((a.x + a.y) * 2).stream.gather().sink_to_list()

    a.emit(df.iloc[:5])
    a.emit(df.iloc[5:])

    assert len(L) == 2
    assert_eq(cudf.concat(L), (df.x + df.y) * 2)


def test_getitem(stream):
    df = cudf.DataFrame({'x': list(range(10)), 'y': [1] * 10})

    a = DataFrame(example=df.iloc[:0], stream=stream)
    L = a[a.x > 4].stream.gather().sink_to_list()

    a.emit(df.iloc[:5])
    a.emit(df.iloc[5:])

    assert len(L) == 2
    assert_eq(cudf.concat(L), df[df.x > 4])


@pytest.mark.xfail(reason="`cudf.DataFrame.add` is not implemented")
@pytest.mark.parametrize('agg', [
    lambda x: x.sum(),
    lambda x: x.mean(),
    lambda x: x.count(),
    lambda x: x.var(ddof=1),
    lambda x: x.std(),
    pytest.param(lambda x: x.var(ddof=0),
                 marks=pytest.mark.xfail(reason="unknown"))
])
@pytest.mark.parametrize('grouper', [lambda a: a.x % 3,
                                     lambda a: 'x',
                                     lambda a: a.index % 2,
                                     lambda a: ['x']])
@pytest.mark.parametrize('indexer', [lambda g: g.y,
                                     lambda g: g,
                                     lambda g: g[['y']],
                                     pytest.param(lambda g: g[['x', 'y']],
                                                  marks=pytest.mark.xfail(
                                                        reason="Indexer column matches grouper"))
                                     ])
def test_groupby_aggregate(agg, grouper, indexer, stream):
    df = cudf.DataFrame({'x': (np.arange(10) // 2).astype(float), 'y': [1.0, 2.0] * 5})

    a = DataFrame(example=df.iloc[:0], stream=stream)

    def f(x):
        return agg(indexer(x.groupby(grouper(x))))

    L = f(a).stream.gather().sink_to_list()

    a.emit(df.iloc[:3])
    a.emit(df.iloc[3:7])
    a.emit(df.iloc[7:])

    first = df.iloc[:3]
    assert assert_eq(L[0], f(first))
    assert assert_eq(L[-1], f(df))


@pytest.mark.xfail(reason="`cudf.Series.add` is not implemented")
def test_value_counts(stream):
    s = cudf.Series([1, 2, 1])

    a = Series(example=s, stream=stream)

    b = a.value_counts()
    assert b._stream_type == 'updating'
    result = b.stream.gather().sink_to_list()

    a.emit(s)
    a.emit(s)

    assert_eq(result[-1], cudf.concat([s, s]).value_counts())


@pytest.mark.xfail(reason="'Series' object does not support item assignment")
def test_setitem(stream):
    df = cudf.DataFrame({'x': list(range(10)), 'y': [1] * 10})

    sdf = DataFrame(example=df.iloc[:0], stream=stream)
    stream = sdf.stream

    sdf['z'] = sdf['x'] * 2
    sdf['a'] = 10
    sdf[['c', 'd']] = sdf[['x', 'y']]

    L = sdf.mean().stream.gather().sink_to_list()

    stream.emit(df.iloc[:3])
    stream.emit(df.iloc[3:7])
    stream.emit(df.iloc[7:])

    df['z'] = df['x'] * 2
    df['a'] = 10
    df[['c', 'd']] = df[['x', 'y']]

    assert_eq(L[-1], df.mean())


def test_setitem_overwrites(stream):
    df = cudf.DataFrame({'x': list(range(10))})
    sdf = DataFrame(example=df.iloc[:0], stream=stream)
    stream = sdf.stream

    sdf['x'] = sdf['x'] * 2

    L = sdf.stream.gather().sink_to_list()

    stream.emit(df.iloc[:3])
    stream.emit(df.iloc[3:7])
    stream.emit(df.iloc[7:])

    assert_eq(L[-1], df.iloc[7:] * 2)


@pytest.mark.parametrize('kwargs,op', [
    ({}, 'sum'),
    ({}, 'mean'),
    pytest.param({}, 'min'),
    pytest.param({}, 'median', marks=pytest.mark.xfail(reason="Not implemented for rolling objects")),
    pytest.param({}, 'max'),
    pytest.param({}, 'var', marks=pytest.mark.xfail(reason="Not implemented for rolling objects")),
    pytest.param({}, 'count'),
    pytest.param({'ddof': 0}, 'std', marks=pytest.mark.xfail(reason="Not implemented for rolling objects")),
    pytest.param({'quantile': 0.5}, 'quantile', marks=pytest.mark.xfail(reason="Not implemented for rolling objects")),
    pytest.param({'arg': {'A': 'sum', 'B': 'min'}}, 'aggregate', marks=pytest.mark.xfail(reason="Not implemented"))
])
@pytest.mark.parametrize('window', [
    pytest.param(2),
    7,
    pytest.param('3h'),
    pd.Timedelta('200 minutes')
])
@pytest.mark.parametrize('m', [
    2,
    pytest.param(5)
])
@pytest.mark.parametrize('pre_get,post_get', [
    (lambda df: df, lambda df: df),
    (lambda df: df.x, lambda x: x),
    (lambda df: df, lambda df: df.x)
])
def test_rolling_count_aggregations(op, window, m, pre_get, post_get, kwargs,
        stream):
    index = pd.DatetimeIndex(start='2000-01-01', end='2000-01-03', freq='1h')
    df = cudf.DataFrame({'x': np.arange(len(index))}, index=index)

    expected = getattr(post_get(pre_get(df).rolling(window)), op)(**kwargs)

    sdf = DataFrame(example=df, stream=stream)
    roll = getattr(post_get(pre_get(sdf).rolling(window)), op)(**kwargs)
    L = roll.stream.gather().sink_to_list()
    assert len(L) == 0

    for i in range(0, len(df), m):
        sdf.emit(df.iloc[i: i + m])

    assert len(L) > 1

    assert_eq(cudf.concat(L), expected)


def test_stream_to_dataframe(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    source = stream
    L = source.to_dataframe(example=df).x.sum().stream.gather().sink_to_list()

    source.emit(df)
    source.emit(df)
    source.emit(df)

    assert L == [6, 12, 18]


def test_to_frame(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)

    assert sdf.to_frame() is sdf

    a = sdf.x.to_frame()
    assert isinstance(a, DataFrame)
    assert list(a.columns) == ['x']


@pytest.mark.parametrize('op', ['cumsum', 'cummax', 'cumprod', 'cummin'])
@pytest.mark.parametrize('getter', [lambda df: df, lambda df: df.x])
def test_cumulative_aggregations(op, getter, stream):
    df = cudf.DataFrame({'x': list(range(10)), 'y': [1] * 10})
    expected = getattr(getter(df), op)()

    sdf = DataFrame(example=df, stream=stream)

    L = getattr(getter(sdf), op)().stream.gather().sink_to_list()

    for i in range(0, 10, 3):
        sdf.emit(df.iloc[i: i + 3])
    sdf.emit(df.iloc[:0])

    assert len(L) > 1

    assert_eq(cudf.concat(L), expected)


def test_display(stream):
    pytest.importorskip('ipywidgets')
    pytest.importorskip('IPython')

    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)

    s = sdf.x.sum()

    s._ipython_display_()


def test_tail(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)

    L = sdf.tail(2).stream.gather().sink_to_list()

    sdf.emit(df)
    sdf.emit(df)

    assert_eq(L[0], df.tail(2))
    assert_eq(L[1], df.tail(2))


def test_example_type_error_message():
    try:
        DataFrame(example=[123])
    except Exception as e:
        assert 'DataFrame' in str(e)
        assert '[123]' in str(e)


def test_dataframes(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrames(example=df, stream=stream)
    L = sdf.x.sum().stream.gather().sink_to_list()

    sdf.emit(df)
    sdf.emit(df)

    assert L == [6, 6]


def test_aggregate_updating(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)

    assert sdf.x.sum()._stream_type == 'updating'
    assert (sdf.x.sum() + 1)._stream_type == 'updating'


def test_window_sum(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)
    L = sdf.window(n=4).x.sum().stream.gather().sink_to_list()

    sdf.emit(df)
    assert L == [6]
    sdf.emit(df)
    assert L == [6, 9]
    sdf.emit(df)
    assert L == [6, 9, 9]


@pytest.mark.xfail(reason="'Series' object does not support item assignment")
def test_window_sum_dataframe(stream):
    df = cudf.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
    sdf = DataFrame(example=df, stream=stream)
    L = sdf.window(n=4).sum().stream.gather().sink_to_list()

    sdf.emit(df)
    assert_eq(L[0], cudf.Series([6, 15], index=['x', 'y']))
    sdf.emit(df)
    assert_eq(L[0], cudf.Series([6, 15], index=['x', 'y']))
    assert_eq(L[1], cudf.Series([9, 21], index=['x', 'y']))
    sdf.emit(df)
    assert_eq(L[0], cudf.Series([6, 15], index=['x', 'y']))
    assert_eq(L[1], cudf.Series([9, 21], index=['x', 'y']))
    assert_eq(L[2], cudf.Series([9, 21], index=['x', 'y']))


@pytest.mark.parametrize('func', [
    lambda x: x.sum(),
    lambda x: x.mean(),
    lambda x: x.count(),
    lambda x: x.var(ddof=1),
    lambda x: x.std(ddof=1),
    lambda x: x.var(ddof=0),
])
@pytest.mark.parametrize('n', [2, 4])
@pytest.mark.parametrize('getter', [
    lambda df: df.x,
])
def test_windowing_n(func, n, getter):
    df = cudf.DataFrame({'x': list(range(10)), 'y': [1, 2] * 5})

    sdf = DataFrame(example=df)
    L = func(getter(sdf).window(n=n)).stream.gather().sink_to_list()

    for i in range(0, 10, 3):
        sdf.emit(df.iloc[i: i + 3])
    sdf.emit(df.iloc[:0])

    assert len(L) == 5

    assert_eq(L[0], func(getter(df).iloc[max(0, 3 - n): 3]))
    assert_eq(L[-1], func(getter(df).iloc[len(df) - n:]))


def test_window_full():
    df = cudf.DataFrame({'x': np.arange(10, dtype=float), 'y': [1.0, 2.0] * 5})

    sdf = DataFrame(example=df)

    L = sdf.window(n=4).apply(lambda x: x).stream.sink_to_list()

    sdf.emit(df.iloc[:3])
    sdf.emit(df.iloc[3:8])
    sdf.emit(df.iloc[8:])

    assert_eq(L[0], df.iloc[:3])
    assert_eq(L[1], df.iloc[4:8])
    assert_eq(L[2], df.iloc[-4:])


def test_custom_aggregation():
    df = cudf.DataFrame({'x': np.arange(10, dtype=float), 'y': [1.0, 2.0] * 5})

    class Custom(Aggregation):
        def initial(self, new):
            return 0

        def on_new(self, state, new):
            return state + 1, state

        def on_old(self, state, new):
            return state - 100, state

    sdf = DataFrame(example=df)
    L = sdf.aggregate(Custom()).stream.sink_to_list()

    sdf.emit(df)
    sdf.emit(df)
    sdf.emit(df)

    assert L == [0, 1, 2]

    sdf = DataFrame(example=df)
    L = sdf.window(n=5).aggregate(Custom()).stream.sink_to_list()

    sdf.emit(df)
    sdf.emit(df)
    sdf.emit(df)

    assert L == [1, -198, -397]
