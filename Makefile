all: image

image:
	docker build -t indoman .

run-prod:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -p 127.0.0.1:4636:4636 --name indoman indoman python3 -m indoman

run:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -p 127.0.0.1:4636:4636 --name indoman indoman python3 -m indoman --debug --disable-cors --host=0.0.0.0

attach:
	docker exec -it indoman /bin/sh
