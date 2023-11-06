class cal:
    def calminus():
        a=3
        b=2
        result= a-b
        print("메인으로 호출안되면 내가 발생")
        return result
    def cal( ):
        a=3
        b=3
        result= a+b
        print("매인으로 호출되면 내가 발생",result)
        return result
        
if __name__ == '__main__':
    cal()
