# Config Injection

A decorator for injecting config from files and other sources.

Example use-case:

```yaml
# conf/config.yml
target_device: /path/to/device
n_runs: 12
use_gpu: false
```

```python
from inject_config import inject_config
from start_simulation import start_simulation

@inject_config.from_yaml('conf/config.yml')
def run_simulation(sim_config: dict) -> dict:
    start_simulation(sim_config)
```

For more examples look at the tests :)
