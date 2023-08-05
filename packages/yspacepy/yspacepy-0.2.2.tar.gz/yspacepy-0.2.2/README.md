
# yspacepy

## Synopsis

```python
>>> from yspacepy.objects import sun, earth
>>> sun.radius.value
695508.0
>>> sun.radius.unit
Unit("km")
>>> sun.radius.to('au').value
0.004649183820234682
>>> sun.radius.to('au').unit
Unit("AU")
>>> sun.radius
<Quantity 695508. km>
>>> sun.dist('earth')
<Quantity 1.496e+08 km>
```

## Using the API interface

Using the interface for the [y-space API](http://y-space.pw/api):

```python
>>> from yspacepy.api import ysapi
>>> api = ysapi()
>>> api.messier.list()
['m1', 'm2', 'm3', 'm4', 'm5', ...
>>> api.messier.id('m1')
{'con': 'Tau', 'dec': '+22° 01′', 'dist': '6300', ...
```

## Installation

    $ pip install yspacepy

