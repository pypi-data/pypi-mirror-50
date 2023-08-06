def print_loll(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_loll(each_item)
        else:
            print(each_item)
