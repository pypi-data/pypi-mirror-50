import csv


# from mld.file_parser import FileParser
# def main():
#     fileParser=FileParser("../single_drug.csv", "../mld/output.csv")
#     fileParser.parse()

class FileParser:

    def __init__(self, src_file, trgt_file):
        self._src_file = src_file
        self._trgt_file = trgt_file

    def parse(self):
        with open(self._src_file, newline='') as f:
            reader = csv.reader(f)

            with open(self._trgt_file, 'w', newline='') as t:

                fieldnames = ['id', 'drug', 'smiles']
                writer = csv.DictWriter(t, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    drugName = row[2][len('Drug: '):]
                    if row[0] and drugName and row[5]:
                        writer.writerow({'id': row[0], 'drug': drugName.lower(), 'smiles': row[5]})
