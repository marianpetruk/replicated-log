
```bash
 docker-compose up --build --force-recreate -d
```


### for testing 
```bash
echo "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/message' \
--data-raw '' && \
echo "POST on master I\nResponse: " && curl --location --request POST 'http://localhost:9000/message' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 1"
}' && \
echo "POST on master II\nResponse: " && curl --location --request POST 'http://localhost:9000/message' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 2"
}' && \
echo "GET on master\nResponse: " &&curl --location --request GET 'http://localhost:9000/message' \
--data-raw '' && \
echo "GET on secondary-1\nResponse: " &&curl --location --request GET 'http://localhost:9001/secondary' \
--data-raw '' && \
echo "GET on secondary-2\nResponse: " &&curl --location --request GET 'http://localhost:9002/secondary' \
--data-raw ''
```

### Recording
[![asciicast](https://asciinema.org/a/AtreUgp89sZnZ9wfwgwBO7fdh.svg)](https://asciinema.org/a/AtreUgp89sZnZ9wfwgwBO7fdh)