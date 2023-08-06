Productivity
============

##### August 2019: This driver is in very early stages of development.

Python ≥3.5 driver and command-line tool for [AutomationDirect Productivity Series PLCs](https://www.automationdirect.com/adc/overview/catalog/programmable_controllers/productivity_series_controllers).

<p align="center">
  <img src="https://www.automationdirect.com/images/overviews/p-series-cpus_400.jpg" />
</p>

Installation
============

```
pip install productivity
```

Usage
=====

### PLC Configuration

This driver uses Modbus TCP/IP for communication. Unlike the ClickPLC, modbus
addresses need to be manually configured in the PLC firmware.

To do this, go to `Write Program → Tag Database`, scroll down to the values you
care about, and click the `Mod Start` cell of each value. This will assign
Modbus addresses (e.g. `300001`) to the values.

### Command Line

```
$ productivity the-plc-ip-address
```

Per [the manual](https://cdn.automationdirect.com/static/manuals/p2userm/p2userm.pdf),
this will print a sample of Modbus registers. You can pipe this as needed.
However, you'll likely want the python functionality below.

### Python

This uses Python ≥3.5's async/await syntax to asynchronously communicate with
a ClickPLC. For example:

```python
import asyncio
from productivity import ProductivityPLC

async def get():
    async with ProductivityPLC('the-plc-ip-address') as plc:
        print(await plc.get())

asyncio.run(get())
```

<!-- The entire API is `get` and `set`, and takes a range of inputs:

```python
>>> await plc.get('df1')
0.0
>>> await plc.get('df1-df20')
{'df1': 0.0, 'df2': 0.0, ..., 'df20': 0.0}
>>> await plc.get('y101-y316')
{'y101': False, 'y102': False, ..., 'y316': False}

>>> await plc.set('df1', 0.0)  # Sets DF1 to 0.0
>>> await plc.set('df1', [0.0, 0.0, 0.0])  # Sets DF1-DF3 to 0.0.
>>> await plc.set('y101', True)  # Sets Y101 to true
```

Currently, only X, Y, and DF are supported. I personally haven't needed to
use the other categories, but they are straightforward to add if needed. -->
