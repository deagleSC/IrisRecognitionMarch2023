open cmd at this path
----------------------

python -m venv venv

.\venv\Scripts\activate.bat

pip install -r requirements.txt

python createDB.py

python verifyDB.py --filename .\Dataset\1\001_2_1.jpg (or provide the path of the jpg image)
