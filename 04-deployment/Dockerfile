FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

COPY score.py /app/
COPY Pipfile /app/Pipfile 
COPY Pipfile.lock /app/Pipfile.lock  
WORKDIR /app/
RUN pip install pipenv && pipenv install
ENTRYPOINT ["pipenv", "run", "python", "/app/score.py"]