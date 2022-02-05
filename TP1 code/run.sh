python -m coverage run -m unittest test_email_analyzer.py
python -m coverage report
python -m coverage run -m --source=. --branch unittest test_email_analyzer.py
python -m coverage report

python -m coverage run -m unittest test_vocabulary_creator.py
python -m coverage report
python -m coverage run -m --source=. --branch unittest test_vocabulary_creator.py
python -m coverage report 

python -m coverage run -m unittest test_crud.py
python -m coverage report
python -m coverage run -m --source=. --branch unittest test_crud.py
python -m coverage report 