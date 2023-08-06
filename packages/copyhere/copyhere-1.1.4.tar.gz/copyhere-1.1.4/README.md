# copyhere

Module for copy or unzip a file to cwd

## install

using `install.py`

for `requirements.txt`:

```text
git+git://github.com/an-dr/copyhere.git@1.1.4
```

## run

```bash
python -m copyhere
```

or

```python
import copyhere
copyhere.start()    # name=None (default) for using source file name
                    # name='' for user input a new name,
                    # name="any your new name"
```

to specify a folder to open in the selection window use `COPYHERE_SOURCEDIR` environment variable