from titanic.controller import Controller
from titanic.view import View
if __name__ == '__main__':
    def print_menu():
        print('0. Exit')
        print('1. 시각화')
        print('2. 모델링')
        print('3. 머신러닝')
        print('4. 머신생성')
        return input('메뉴 입력\n')
    app = Controller()
    while 1:
        menu = print_menu()
        if menu == '1':
            view = View('train.csv')
            menu = input('차트 내용 선택 \n'
                         '1. 생존자 vs 사망자 \n'
                         '2. 생존자 성별 대비')
            if menu == '1':
                view.plot_survived_dead()
            if menu == '2':
                view.plot_sex()
        if menu == '2':
            app.modeling('train.csv','test.csv')
        if menu == '3':
            app.learning('train.csv','test.csv')
        if menu == '4':
            app.submit('train.csv','test.csv')
        elif menu == '0':
            break