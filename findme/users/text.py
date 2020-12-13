def message(domain, uidb64, token):
    return f"안녕하세요 FINDME 입니다.\n\n아래 링크를 클릭해서 회원 인증을 완료하세요 \n\n클릭 : {domain}/users/activate/{uidb64}/{token}"
