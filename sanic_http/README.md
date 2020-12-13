
```bash
 docker-compose up --build --force-recreate -d
```


### for testing

Testing POST on master with write concerns: 1, 2, 3
```bash
docker-compose up --build --force-recreate -d master secondary-1 
echo -e "Now introduce 10 seconds delay in secondary-2 and run in docker\n" # edit in the secondary.py file
docker-compose up --build --force-recreate -d secondary-2

echo -e "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && echo
echo -e "GET on secondary-1\nResponse: " && curl --location --request GET 'http://localhost:9001/' \
--data-raw '' && echo
echo -e "GET on secondary-2\nResponse: " && curl --location --request GET 'http://localhost:9002/' \
--data-raw '' && echo -e "\n \t\t\tAll nodes should be new (empty message memory list).\n\n" \
echo -e "POST on master with write-concern = 1\nResponse: " && curl --location --request POST 'http://localhost:9000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 1",
    "w": 1
}' && \
echo -e "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && echo -e "\n\n" \
echo -e "POST on master with write-concern = 2\nResponse: " && curl --location --request POST 'http://localhost:9000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 2",
    "w": 2
}' && \
echo -e "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && \
echo -e "GET on secondary-1\nResponse: " &&curl --location --request GET 'http://localhost:9001/' \
--data-raw '' && \
echo -e "GET on secondary-2\nResponse: " &&curl --location --request GET 'http://localhost:9002/' \
--data-raw '' && echo -e "\n\n"  \
echo -e "POST on master with write-concern = 3\nResponse: " && curl --location --request POST 'http://localhost:9000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message": "test 3",
    "w": 3
}' && \
echo -e "GET on master\nResponse: " && curl --location --request GET 'http://localhost:9000/' \
--data-raw '' && \
echo -e "GET on secondary-1\nResponse: " && curl --location --request GET 'http://localhost:9001/' \
--data-raw '' && \
echo -e "GET on secondary-2\nResponse: " && curl --location --request GET 'http://localhost:9002/' \
--data-raw '' && echo -e "\n\n" 
```

### Recording
Will be shared on request, please contact us