# Puzzle

## Setup with pip
python: 3.6 

package: pytest, pytest-html
```bash
pip install pytest -U
pip install pytest-html -U 
```

## Setup with conda

```bash
conda env create -f environment.yml
```

## Execute the script

Test a 15x15 game board
```bash
python puzzle.py check_words 15
```

Create a 15x15 game board
```bash
python puzzle.py get_board 15
```

## Run test without html report

```bash
pytest test_puzzle.py
```

## Run test with html report

```bash
pytest test_puzzle.py --html=report.html --self-contained-html
```
