# FINEME 서비스 README.md
![FINDME 포스터](https://user-images.githubusercontent.com/49577850/102770389-695a2380-43c7-11eb-98f6-cf81f62cd576.png)

# 본 프로젝트는 심리 상담과정에서의 다음과 같은 불편함들을 SW적으로 개선하주고자 기획하게 되었다
![문제점](https://user-images.githubusercontent.com/49577850/102770538-acb49200-43c7-11eb-8ea9-e8b085c0f4bf.png)


# 궁극적으로 다음과 같은 방식으로 상담의 효율을 높이고자 하였다
![해결방안,최종목표](https://user-images.githubusercontent.com/49577850/102770804-17fe6400-43c8-11eb-83af-68dadfebadd9.png)




# 프로젝트 설계 
 **프론트 - IOS / ANDROID 모두 구현하도록 크로스 플랫폼 ReactNaive 를 이용해서 구현하였다.
 백엔드 - 빠르고 안정되고 저렴한 서버를 구축하기 위해 Amazon AWS의 주요 서비스들을 적극 도입하였다. 감정 분석을 위해 Google AZURE 를 이용하였다. Docker 를 이용해 API 배포를 무중단화 시켰다.**
![계획,설계](https://user-images.githubusercontent.com/49577850/102771212-e0dc8280-43c8-11eb-9f21-f5faa62cd1c6.png)

# TDD 활용
 **90% 이상의 Test Coverage를 가져가며 서비스의 안정성을 향상시켜 개발하였다.
 Django에서는 Python 의 Unit Teet 기반의 TestCase클래스를 제공한다. 이를 상속시켜 FindMe 서비스를 개발하며 테스를 자동화 하였다**
 
