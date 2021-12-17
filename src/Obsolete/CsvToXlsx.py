import csv
import sys
import openpyxl

def convert(input_path, output_path):
    """
    Read a csv file (with no quoting), and save its contents in an excel file.
    """
    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]

    with open(input_path) as f:
        reader = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row_index, row in enumerate(reader, 1):
            for col_index, value in enumerate(row, 1):
                ws.cell(row=row_index, column=col_index).value = value

    wb.save(output_path)


def main():
    try:
        input_path, output_path = sys.argv[1:]
    except ValueError:
        print('Usage: python %s input_path output_path' % (sys.argv[0],))
    else:
        convert(input_path, output_path)


if __name__ == '__main__':
    main()