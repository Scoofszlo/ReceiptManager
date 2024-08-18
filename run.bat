@REM Creates virtual environment or some sort of isolated space so that 
@REM installation of external dependencies will only be installed in this
@REM folder
IF NOT EXIST .venv (
    python -m venv .venv
)

@REM Runs the program
python -m src.receiptmanager
