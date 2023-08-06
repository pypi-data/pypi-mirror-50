# pltshow-python
python sdk for pltshow


## Example

```python
import pandas as pd
import pltshow
plt = pltshow.Client('username', 'password')

df = pd.DataFrame(....)
plt.show('chart_name', df)
```
then open pltshow.com in browser, login and then your chart will be there
