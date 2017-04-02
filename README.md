An XML comparer (CLI and library) written in Python.

CLI usage (TODO):

Compare two xml files directly:
```$ xmlcompare file1.xml file2.xml```

shows the diff between the two xml files using your configured diff tool (e.g. vimdiff). Exactly the same
as just running `yourtool file1.xml file2.xml`

Actions
---
Options that fall in the "actions" category are:

--ignore-order: will ignore the order of all the elements
--ignore-text: will ignore the text inside the elements matched
--ignore-element: ignores the entire element (and all of its descendants)
--ignore-attr-order: ignores the order of the attributes

These do either work on the entire documents or part of them (see Selectors)

Example: Compare two xml files, ignoring sort order of elements
```$ xmlcompare --ignore-order file1.xml file2.xml```

Selectors
---
You can use "selectors" to limit the scope of the actions:

Ignore the order, but only for depth=1 (where the root element is at depth 0):
```$ xmlcompare --depth=1 --ignore-order file1.xml file2.xml``` 

Ignore the order of the elements selected by the xpath
```$ xmlcompare --select="xpath" --ignore-order```


