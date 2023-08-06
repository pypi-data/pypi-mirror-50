# Sidepanel

<!-- [![Build Status](https://travis-ci.org/jupyter-widgets/jupyterlab-sidecar.svg?branch=master)](https://travis-ci.org/jupyter-widgets/jupyterlab-sidecar)
[![codecov](https://codecov.io/gh/jupyter-widgets/jupyterlab-sidecar/branch/master/graph/badge.svg)](https://codecov.io/gh/jupyter-widgets/jupyterlab-sidecar) -->

A fork of jupyterlab/Sidecar with an additional Sidepanel

## Installation

```bash
pip install sidepanel
jupyter labextension install sidepanel
```

## Usage

The sidepanel widget is used as a context manager, just like ipywidgets' output
widget.

```python
from sidepanel import Sidepanel
from ipywidgets import IntSlider

sp = Sidepanel(title='Sidecar Output')
sl = IntSlider(description='Some slider')
with sp:
    display(sl)
```


<!-- ![sidecar](sidecar.gif) -->
