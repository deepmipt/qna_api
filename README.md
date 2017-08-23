# qna_api
QnA REST microservice
```sh
docker run -d -h qna_api                                              \
           --name qna_api                                             \
           -p 5000:80                                                 \
           -e "AMQP_URI=amqp://user:password@host"                    \
           -v /data/qna:/data                                         \
           seliverstov/qna_api:latest
```
