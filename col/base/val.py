class GlobalConstValue(object):
    """ DocString for GlobalConstValue"""
    gui_show_second = 10
    gui_show_num_per_second = 250
    gui_show_num_all = gui_show_second * gui_show_num_per_second

if __name__ == '__main__':
    g = GlobalConstValue()
    print(g.gui_show_num_all)

