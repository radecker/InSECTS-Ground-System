FROM python:3.9

# working directory
WORKDIR /usr/src/app

# add the python application
ADD hal.py .

# copy requirements file to working directory
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "./hal.py"]
