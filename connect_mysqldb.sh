docker run --platform linux/x86_64 \
-it \
--rm \
mysql:latest \
mysql \
-h${MYSQL_HOST} \
-u${MYSQL_USER} \
-p${MYSQL_PASSWORD}
