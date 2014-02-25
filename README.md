tiny_uwsgi
==========

english 
-------

very thin python web framework for uwsgi

suitalble for http service, restful api server
very small code size
web service architecture education
not suitable ( but not impossiable ) for web site

use uwsgi specific feature
    like @postfork
and configuration settings
    like max-requests

requirement
nginx(optional - recommended)
uwsgi , uwsgidecorators
python 2.7.x
python simplejson

support per worker initialize
get parameter
form post data
josn post data
cookie
http header process and http error
can use gluon.dal(web2py) for db access

multi-service support and automatic function mapping

request is mapped to serviceName.@exposeToURL function name
http://hostname/serviceName/@exposeToURL functionname

see test_service.py

korean
------

아주 간단한 파이썬 http 서비스 프레임웍 입니다. 

http 서비스나 restful 서비스를 만들때 유용하며 
( 웹 사이트를 만들기는 적합하지 않습니다. )
아주 작은 코드 크기로 웹서비스의 구조를 교육할때도 유용하게 사용할 수 있습니다. 

nginx 와 uWSGI 를 사용하여 서비스를 구성하는 것을 가정하고 만들어져 있으며

get 인자 , html 폼 데이터 전송 , json 포스트 전송을 모두 지원 합니다. 

web2py에 일부인 gluon.dal 을 사용하여 DB를 사용하는 것에도 적합합니다. 

web2py 와 유사하게 
http://hostname/서비스이름/함수이름?인자들 + post data
형태로 서비스를 구성하기 편하도록 되어 있습니다. 

예제코드인 test_service.py를 보시면 도움이 될것 입니다. 
