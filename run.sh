docker build -t chatbot .
docker run -it  -v ./mem/:/mem/  --rm chatbot