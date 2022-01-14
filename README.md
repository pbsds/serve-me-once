# [serve-me-once](https://pypi.org/project/fix-my-functions/)

Serves some data over HTTP, _once_.
Based on the built-in Python module `http.server`.


## Installation

	pip install serve-me-once.git

## Use

```python
from serve_me_once import serve_once, gen_random_port
serve_once(
	"Hello, World",
	timeout=2,
	mime_type="text/html",
	port=gen_random_port()
)
```

or

```python
from serve_me_once import serve_once_in_background, gen_random_port
import time

addr = serve_once_in_background(
	"Hello, World",
	timeout=2,
	mime_type="text/html",
	port=gen_random_port()
)
print("Hosting at:", addr)
time.sleep(3)
```


# ... Why?

The web version of [Netron](https://github.com/lutzroeder/netron) accepts an URL as a query parameter ([example](https://netron.app/?url=https://media.githubusercontent.com/media/onnx/models/master/vision/classification/squeezenet/model/squeezenet1.0-3.onnx)).
But serving temporary files is a chore.
Hence this.
