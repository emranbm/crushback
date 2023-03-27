FROM python:3.8.13
RUN pip install pipenv==2022.7.4
WORKDIR /app/
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --dev
COPY . .
CMD bash run.sh
