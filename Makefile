
build:
	docker build -t registry.edmodo.io/test-websocket .

run: build
	docker run -p 80:80 -t registry.edmodo.io/test-websocket
