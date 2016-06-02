__author__ = 'Corey Petty'
import file_parse.database as db
import sys


def main(filename: str):
    if not filename:
        root_dir = input("Please enter root directory of job files: ")
    else:
        root_dir = filename

    outfile_name = input("Please input desired output JSON filename: ")

    print("\n----> Collecting data from job files")
    df = db.make_dataframe(root_dir=root_dir)
    df.to_json(outfile_name, date_unit='s', double_precision=15)
    print("DataFrame converted to JSON format: {}".format(outfile_name))


if __name__ == "__main__":
    main(sys.argv[1])
