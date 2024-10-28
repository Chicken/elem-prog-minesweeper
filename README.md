# Minesweeper for Elementary Programming (521141P)

Overkill minesweeper project because I felt like procrastinating other things.

## Get started

`python -m venv .venv`  
`source .venv/bin/activate` (for windows `.venv\Scripts\activate.bat` or `.venv\Scripts\Activate.ps1`)  
`pip install -r requirements.txt`  
`python src/main.py`

## Known problems

- The first click after a window resize (such as starting or ending a game) isn't registered
  - **Really** damn annoying btw
  - No idea how to fix
    - Getting mouse position on focus event didn't work as such was never triggered, might be platform dependant
