class GlobalConstValue(object):
    """ DocString for GlobalConstValue"""
    gui_show_second = 10
    gui_show_num_per_second = 250
    gui_show_num_all = gui_show_second * gui_show_num_per_second

    flag_trigger = [bytes(512*[0x00]), bytes(512*[0x01]),
                    bytes(512*[0x02]), bytes(512*[0x03]),
                    bytes(512*[0xFF])]


if __name__ == '__main__':
    g = GlobalConstValue()
    print(g.gui_show_num_all)

