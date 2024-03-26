def cal_avg(number_list):
    # 이 함수는 숫자 리스트의 평균을 계산합니다
    sum = 0

    for number in number_list:
        sum += number  
    average = sum / len(number_list)
    return average

# 숫자 리스트
numbers = [10, 20, 30, 40, 50]

# 평균 출력
print("평균:", cal_avg(numbers))
