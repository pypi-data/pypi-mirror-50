## Example Usage

```python
def get_prefetch_queryset(self, instances, queryset=None):
    query = {'%s__in' % self.field.name: instances}

    from py_debug_inspect_utils import debug_print
    debug_print(query=query)
```  

Output:
```
/Users/Development/venv/lib/python3.7/site-packages/django/db/models/fields/related_descriptors.py:625 (get_prefetch_queryset)
()
{'query': {'attribute__in': [<Attribute: Flavor>]}}
```
