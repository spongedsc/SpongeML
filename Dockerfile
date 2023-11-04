FROM anibali/pytorch:1.13.1-nocuda

WORKDIR /app

# get the really big model done with
RUN pip install transformers[torch]

# rest of the dependencies
COPY ["requirements.txt", "./"]
RUN pip install -r requirements.txt

# the code
COPY . .

CMD [ "python3", "main.py" ]

EXPOSE 6000

ENV TRANSFORMERS_CACHE=/modelcache
VOLUME [ "/modelcache" ]