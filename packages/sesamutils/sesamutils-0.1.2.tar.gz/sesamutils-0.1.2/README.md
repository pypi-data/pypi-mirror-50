# SesamUtils

**Python module to simplify common tasks when developing microservices for the Sesam integration platform.**


### Usage examples

```bash
from sesamutils import VariablesConfig

required_env_vars = ["username", "password", "hostname"]
optional_env_vars = ["debug"]

config = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

if not config.validate():
    sys.exit(1)


print(config.username)

```



### Installation

```bash
pip install sesamutils
```