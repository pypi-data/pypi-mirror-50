from dotcpp.dotcpp_ext import DoubleList

if __name__ == '__main__':
    double_list = DoubleList()
    double_list.add(1.2)
    print(double_list.contains(1.2))
    print(double_list.contains(1.3))
