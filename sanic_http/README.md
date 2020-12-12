
```bash
 docker-compose up --build --force-recreate -d
```


### for testing 
```bash
echo -e "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && \
echo -e "POST on master I\nResponse: " && curl --location --request POST 'http://localhost:9000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 1",
    "w": 1
}' && \
echo -e "POST on master II\nResponse: " && curl --location --request POST 'http://localhost:9000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 2",
    "w": 2
}' && \
echo -e "GET on master\nResponse: " &&curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && \
echo -e "GET on secondary-1\nResponse: " &&curl --location --request GET 'http://localhost:9001/' \
--data-raw '' && \
echo -e "GET on secondary-2\nResponse: " &&curl --location --request GET 'http://localhost:9002/' \
--data-raw ''
```

### Recording
Will be added 
