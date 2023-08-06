# Log Redactor

Redacts data in python logs based on regex filters passed in by the user.  
This will work with json logging formats as well and also with nested data in the `extra` argument. 


# Examples

```python
import re
import logging
import logredactor

# Create a logger
logger = logging.getLogger()
# Add the redact filter to the logger with your custom filters
redact_patterns = [re.compile(r'\d+')]

# if no `default_mask` is passed in, 4 asterisks will be used
logger.addFilter(logredactor.RedactingFilter(redact_patterns, default_mask='xx'))

logger.warning("This is a test 123...")
# Output: This is a test xx...
```

Python only applies the filter on that logger, so any other files using logging will not get the filter applied. To have this filter applied to all loggers do the following
```python
import re
import logging
import logredactor
from pythonjsonlogger import jsonlogger

# Create a pattern to hide api key in url. This uses a _Positive Lookbehind_
redact_patterns = [re.compile(r'(?<=api_key=)[\w-]+')]

# Override the logging handler that you want redacted
class RedactStreamHandler(logging.StreamHandler):
    def __init__(self, *args, **kwargs):
        logging.StreamHandler.__init__(self, *args, **kwargs)
        self.addFilter(logredactor.RedactingFilter(redact_patterns))

root_logger = logging.getLogger()

sys_stream = RedactStreamHandler()
# Also set the formatter to use json, this is optional and all nested keys will get redacted too
sys_stream.setFormatter(jsonlogger.JsonFormatter('%(name)s %(message)s'))
root_logger.addHandler(sys_stream)

logger = logging.getLogger(__name__)

logger.error("Request Failed", extra={'url': 'https://example.com?api_key=my-secret-key'})
# Output: {"name": "__main__", "message": "Request Failed", "url": "https://example.com?api_key=****"}
```
