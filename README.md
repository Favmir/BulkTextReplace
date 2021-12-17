# BulkTextReplace
 Python script that replaces regex text for all `.txt` files in a folder


Note:
The `BulkReplacer.py` script needs a csv file named `BulkReplacer_List.csv` formatted in utf-8. It uses tab(\t) as delimiter, and quoting is disabled — meaning that you cannot have tab characters as input.

Example of `BulkReplacer_List.csv`:
```
([^…])…([^…])	\1……\2	Doulbe the Ellipses
([^\n "—])(—[\s])	\1 \2	Spacing for Em Dash
(\s)-(\s)	\1—\2	Turn Hyphen into Em Dash
([0-9])-([0-9])	\1–\2	For numbers, turn Hyphen into En Dash
```

first column is RegEx used to find text, second column the replacement RegEx, and the third is just for comments.
