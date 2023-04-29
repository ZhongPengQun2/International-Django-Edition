# international
to be international


docker build -t international:1.0 -f Dockerfile .
docker run --net="host" --name international international:1.0


-- DB migrate
python app.py db init
python app.py db migrate
python app.py db upgrade
