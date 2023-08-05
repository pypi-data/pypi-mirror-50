# reportlib
Generator HTML from pandas via Jinja2

##  Changelog for version 3.0.0

- Styler now cannot access via df.style. Use Styler(df) instead

- Renamed Generator -> Report, EnvironParser -> ConfigParser

- Add default options (provided via Styler.set_option or Styler.__init__) for Styler.format_number() 

- Add html_ouput, email_config, email_env in Report constructor instead of hidden environ variables

- Add reportlib.add_template_dir

# Usage
## Project structure
```
root/ (or root/src/)
 |-+-templates/
 | |-styles.css
 |-report.py
 |-email_config.yml
 |-metadata.yml
 ...
```

## Basic usage
```bash
# Setup environ before running code
export REPORT_DATE='2019-06-30'
export EMAIL_ENV='dev'
```


```python
"""report.py"""

import os
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from reportlib import Report, ConfigParser, Styler

# Parse options from env
config = ConfigParser(config=os.environ)
report_date = config.date('REPORT_DATE', default='yesterday')

# Prepare data
df = pd.DataFrame(np.random.randn(8, 4), index=['index'], columns=['a', 'b', 'c', 'd'])

# Config report
reportlib.add_template_dir('templates')
Styler.set_option('precision', 2)
Styler.set_option('fillna', '-')
Styler.set_option('fillinf', '-')
Styler.set_option('fillzero', '-')

# Initial generator
generator = Generator(
  styles='styles.css',
  title='Report Demo',
  context={
    'report_date': report_date
  },
  html_output='report_output.html',
  email_config='email_config.yml',
  email_env=config.get('EMAIL_ENV'),
)

# Styling data
style = (
  Styler(df)
  .add_class('bold highlight', subset=pd.IndexSlice[0:1, style.data.columns])  # Bold and Highlight some row by using class `highlight`
  .add_class('text-right', columns=style.data.columns)  # Align right columns
)

# Add tables
generator.add_table(style)

# Run generator
generator.run()
```


```yaml
# This is `dev` env
dev: 
  smtp:
    username: 'your.email@your.domain'
    pwd: 'yourpassword'
  from: 'From'  
  subject: 'Report Demo - {report_date:%d/%m/%Y}'  # Report Demo - 30/06/2019
  to: 
    - 'you@your.domain'
  cc:
    - 'your.boss@your.domain'
  bcc:
    - 'some.body@other.domain'
  files:
    - 'relative_path/some_attachtments.txt'
    - '/home/users/you/absolute_path/attactment.txt'
# ... Your other env
```