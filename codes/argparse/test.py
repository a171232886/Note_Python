import argparse

"""
针对某些版本python传入bool型参数，args将其认为是str问题的解决方案
"""
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')
    
def parse_args():
    parser = argparse.ArgumentParser(description="Test")
    parser.add_argument('-d1','--debug1',
                        type=str2bool,
                        default=False,
                        help='DeBUG')
    parser.add_argument('-d2','--debug2',
                    type=bool,
                    default=False,
                    help='DeBUG')
    parser.add_argument('-t','--test',
                    type=int,
                    default=0,
                    help='DeBUG')
    args = parser.parse_args()
    return args

args = parse_args()
print(type(args.test))
print(type(args.debug1))
print(type(args.debug2))

