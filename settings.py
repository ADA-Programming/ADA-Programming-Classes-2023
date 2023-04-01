"""Project configuration settings (PROJECT_DIR, format strings, etc.).
"""


from pathlib import Path

PREFERRED_DATE_FORMAT = '%b %d, %Y'

# Define PROJECT_DIR as Path(__file__).parent

PROJECT_DIR = Path(__file__).parent
# print(PROJECT_DIR)
DATA_DIR = PROJECT_DIR / 'data'
# print(DATA_DIR)

# # Demonstrate __file__, type(__file__), Path(__file__), Path(__file__).parent and Path.cwd()
# print(__file__)
# print(Path(__file__))
# print(Path(__file__).parent)
