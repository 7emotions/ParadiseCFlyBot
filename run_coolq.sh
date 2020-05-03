sudo systemctl start docker

docker run -ti --rm --name cqhttp-test \
             -v /home/qnurye/.cache/coolq/data:/home/qnurye/.cache/coolq \
             -p 9000:9000 \
             -p 5700:5700 \
             -e COOLQ_ACCOUNT=1934426641 \
             -e CQHTTP_POST_URL=http://172.17.0.1:5000 \
             -e CQHTTP_SERVE_DATA_FILES=yes \
             -e VNC_PASSWD=12345678 \
             richardchien/cqhttp:latest

sudo systemctl stop docker

