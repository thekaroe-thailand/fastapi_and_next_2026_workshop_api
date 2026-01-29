# run project
uvicorn main:app --reload

# init
alembic init alembic

# version for migrate
alembic revision --autogenerate -m "first migrate"

# updata database
alembic upgrade head

# uv sync
uv sync

# deactivete
deactivate

# activate
.venv\Scripts\activate

# .venv
py -m venv .venv

# py version
py --version

# upgrade
py -m ensurepip --upgrade

# pip version
py -m pip --version

# setup uv all user
py -m pip install --user uv
py -m pip install uv

# show uv
py -m pip show uv

# where uv
where uv

