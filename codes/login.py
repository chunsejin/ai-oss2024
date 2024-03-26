def login(usernme, password):  # 오타: 'username'이 올바른 매개변수 이름입니다.
    # 사용자 이름과 비밀번호를 검증하는 함수
    expected_username = "user1"
    expected_password = "passw0rd"

    if usernme == expected_username and password == expected_password
        print("로그인 성공!")
    else:
        print("로그인 실패!")  # 들여쓰기 누락
    # if 문에서 콜론 누락

login("user1", "passw0rd")