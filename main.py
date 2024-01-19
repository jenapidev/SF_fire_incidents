from os import name

from ParseData import ParseData

from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    parser = ParseData()
    parser.extract_data()
    parser.transform_data()
    parser.load_data()
