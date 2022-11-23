# Bulk Text Replacer
#### Python script that find & replace for all `.txt` files in a folder using multiple regular expressions.

I made this for my own translation work. Very useful when you're changing a million lines of dialog for games like Baldurs Gate 3, or for fictions like HPMOR.

The `BulkReplacer.py` script needs a csv file named `BulkReplacer_List.csv`.
Requirements for the csv file:
* formatted in `utf-8-sig`
* use ` `(Tab key) as delimiter (multiple tabs in a row are considered as one tab)

The program will generate a csv file for you if there isn't one.

Example of `BulkReplacer_List.csv`:
```
Your fine.          You're fine.    Fixes grammar
([^…])…([^…])       \1……\2          Doulbe the Ellipses
([^\n ""—])(—[\s])  \1 \2           Spacing for Em Dash
(\s)-(\s)           \1—\2           Turn Hyphen into Em Dash
([0-9])-([0-9])     \1–\2           For numbers, turn Hyphen into En Dash 
```
This translates to:
| BEFORE            | AFTER         | COMMENT                               |
|:-----------------:|:-------------:|:--------------------------------------|
| Your fine.        | You're fine.  | Fixes grammar                         |
| ([^…])…([^…])     | \1……\2        | Doulbe the Ellipses                   |
| ([^\n "—])(—[\s]) | \1 \2         | Spacing for Em Dash                   |
| (\s)-(\s)         | \1—\2         | Turn Hyphen into Em Dash              |
| ([0-9])-([0-9])   | \1–\2         | For numbers, turn Hyphen into En Dash |

First column is the RegEx used to find text, second column the replacement RegEx. The third column does nothing — it's just for comments.
