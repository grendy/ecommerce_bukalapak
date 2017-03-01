# ecommerce_bukalapak
Crawling bukalapak
##install scrapy on centos
1. sudo rpm -Uvh http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-5.noarch.rpm
2. yum update -y
3. yum install python-pip -y
4. yum install python-devel -y
5. yum install gcc gcc-devel -y
6. yum install libxml2 libxml2-devel -y
7. yum install libxslt libxslt-devel -y
8. yum install openssl openssl-devel -y
9. yum install libffi libffi-devel -y
10. CFLAGS="-O0" pip install lxml
11. pip install scrapy
