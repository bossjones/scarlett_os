1. Convert ruamel usage from old api to the newer one:

## Before 0.15.0:

```
from pathlib import Path
from ruamel import yaml
data = yaml.safe_load("abc: 1")
out = Path('/tmp/out.yaml')
with out.open('w') as fp:
yaml.safe_dump(data, fp, default_flow_style=False)
```

## after:

```
from pathlib import Path
from ruamel.yaml import YAML
yaml = YAML(typ='safe')
yaml.default_flow_style = False
data = yaml.load("abc: 1")
out = Path('/tmp/out.yaml')
yaml.dump(data, out)
```
