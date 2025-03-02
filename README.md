# upload-mobi
Upload mobi file to your kindle
```shell
cd
cd  upload-mobi
docker rm -f web
docker build -t kindle .
docker run -d --name web -p 80:80 -v /home/ubuntu/uploads:/opt/uploads kindle
```