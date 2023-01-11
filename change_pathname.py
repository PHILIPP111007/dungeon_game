import pathlib
from pathlib import Path


path = Path(__file__).parent

if __name__ == '__main__':
	print(path)
	print('The file contains the "path" variable, which is responsible for setting the path')
