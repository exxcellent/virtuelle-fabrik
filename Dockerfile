FROM python:3.10

# System deps:
RUN pip install "poetry==1.4.1"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --without dev,test,docs --no-interaction --no-ansi --no-root

# Creating folders, and files for a project:
COPY . /code

CMD ["uvicorn", "API.app.main:app", "--host", "0.0.0.0", "--port", "8000"]