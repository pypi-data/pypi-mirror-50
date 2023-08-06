import argparse
import ctypes
import sys

from . import codegen
from . import driver
from . import parser
from . import tokenization


def parse_args():
    parser = argparse.ArgumentParser()
    sub_parsers = parser.add_subparsers(help='sub commands', dest='cmd')
    parser_build = sub_parsers.add_parser('build', help='compile packages and dependencies')
    parser_build.add_argument('src')
    parser_build.add_argument('-o')
    parser_run = sub_parsers.add_parser('run', help='compile and run Douz program')
    parser_run.add_argument('src')
    parser_run.add_argument('-o')
    return parser.parse_args()


args = parse_args()

if args.cmd == 'build':
    driver = driver.User()
    driver.compile(args.src, args.o)

if args.cmd == 'run':
    with open(args.src, 'r') as f:
        t = tokenization.Tokenization(f)
        p = parser.Parser(t)
        c = codegen.CodeGen()
        for e in p.iter():
            c.code_base(e)
        llvm_ir = c.text()

    driver = driver.Lite()
    driver.compile_ir(llvm_ir)

    func_ptr = driver.engine.get_function_address('main')
    cfunc = ctypes.CFUNCTYPE(ctypes.c_uint)(func_ptr)
    status = cfunc()
    print(f'Exit: {status}')
    sys.exit(status)
