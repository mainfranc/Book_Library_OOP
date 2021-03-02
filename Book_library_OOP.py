from Interface_code_OOP import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run_mode')
    parser.add_argument('-d', action="store_true", dest="run_mode")
    args = parser.parse_args()
    debug_mode = False
    if args.run_mode:
        debug_mode = True
    main_window = Interface(debug_mode)
    main_window.main()
