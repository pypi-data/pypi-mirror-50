def print_f(the_list,level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_f(each_item,level+1)
		else:
                        for each_level in range(level):
                                print("\t")
                        print(each_item)

