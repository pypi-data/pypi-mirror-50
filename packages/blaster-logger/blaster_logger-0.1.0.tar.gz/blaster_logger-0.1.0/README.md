## Blaster Logger
Turn-key logging solution based on [loguru](https://github.com/Delgan/loguru)

### Installation

```bash
pip install blaster_logger
```

### Usage

#### As logger
```python
from blaster_logger import log

log.debug('This is DEBUG level message')
log.info('This is INFO level message')
log.warning('This is a warning')
log.error('This is an error message')
log.critical('This is a critical level message')

try:
    raise RuntimeError('Error message')
except RuntimeError as e:
    log.trace(e) # This is a traceback log
```

#### As decorator
```python
from blaster_logger import log

@log.this
def some_func(x):
    return x * 2
```

