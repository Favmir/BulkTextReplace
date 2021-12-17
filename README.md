# BulkTextReplace
 Python script that replaces regex text for all files in a folder


Notes:
The replacer needs a csv file named "BulkReplacer_List.csv" formatted in utf-8. It uses tab(\t) as delimiter, and quoting is disabled — meaning that you cannot have tab characters as input.

first column is regex used to find text, second column the replacement regex, and third is just for comments.