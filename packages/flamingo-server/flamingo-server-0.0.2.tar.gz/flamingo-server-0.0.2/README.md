# Flamingo



## Installing

```bash
pip install flamingo
```



## Example

simple http server

```python
import json
from flamingo import Flamingo, Response

app = Flamingo()

def homepage():
    return "Hello world"

app.register("/", homepage)
app.register("/text", "this is just a line of text")

data = json.dumps({"code":200, "msg":"hello world"})
app.register("/json", Response(200, data, content_type="application/json"))

app.run()
```