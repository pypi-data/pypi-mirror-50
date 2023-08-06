from __future__ import print_function

# import json
import os
# import re
import subprocess

from IPython.core import magic_arguments as m_args
from IPython.core.magic import (Magics, magics_class, cell_magic, line_magic, line_cell_magic)
from IPython.utils.tempdir import TemporaryDirectory


PicatPredicates = {}


@magics_class
class PicatMagics(Magics):

    @m_args.magic_arguments()
    # @m_args.argument('-b', '--bind', nargs='+', help='Bind the return to variable `result`')
    @m_args.argument('-d', '--delete', nargs=1, help='Delete a predicate')
    @m_args.argument('-e', '--execute', help='Execute a Picat program')
    # @m_args.argument('-i', '--input', nargs='+', help='Input variables')
    @m_args.argument('-l', '--list', action='store_true', help='List all predicates')
    @m_args.argument('-n', '--new', nargs=1, help='Define a new predicate from a cell. If it already exists, it will be updated.')
    # @m_args.argument('-o', '--output', nargs='+', help='Output variables')
    # @m_args.argument('-p', '--predicate', nargs=1, help='Predicate to start to execute')
    
    @line_cell_magic
    def picat(self, line, cell=None):
        '''Picat magic'''

        picat_proc = ["picat"]

        args = m_args.parse_argstring(self.picat, line)
        
        #
        # Delete a predicate
        #
        if args.delete:
            PicatPredicates.pop(args.delete[0], '')
            return
        
        #
        # Add or Update a predicate
        #
        if args.new:
            PicatPredicates.update({args.new[0]: cell})
            return

        #
        # List all predicates
        #
        if args.list:
            with TemporaryDirectory() as tmpdir:
                with open(tmpdir + "/prg.pi", "w") as prgf:
                    for predicate in PicatPredicates.keys():
                        prgf.write(PicatPredicates.get(predicate))
                    if cell is not None:
                        prgf.write(cell)
                    prgf.close()
                    # For debuging only!!!
                    with open(tmpdir + "/prg.pi") as prgf:
                        p = prgf.readlines()
                        print(''.join(p))
                        return   

        #
        # Executes a script in the same directory
        #
        if args.execute:
            picat_test = picat_proc[:]
            my_env = os.environ.copy()

            pipes = subprocess.Popen(
                picat_test + [args.execute],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
            (output, erroutput) = pipes.communicate()
            if pipes.returncode != 0:
                print(erroutput.rstrip().decode())
                return
            print(output.decode('utf-8'))       
            return
        #
        # Get variables from Python
        #
        # inputs = {}
        # # inputs = []
        # if args.input:
        #     for var in args.input:
        #         if var in self.shell.user_ns.keys():
        #             inputs[var] = self.shell.user_ns[var]
        #             # inputs.append(self.shell.user_ns[var])
        #             return inputs
        #         else:
        #             return var + " is undefined"
        
        #
        # Execute the program in the cell
        #
        picat_test = picat_proc[:]

        with TemporaryDirectory() as tmpdir:
            with open(tmpdir + "/prg.pi", "w") as prgf:
                for predicate in PicatPredicates.keys():
                    prgf.write(PicatPredicates.get(predicate))
                if cell is not None:
                    prgf.write(cell)
                prgf.close()
                pipes = subprocess.Popen(
                    picat_test + [tmpdir + "/prg.pi"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=os.environ.copy())
                (output, erroutput) = pipes.communicate()
                if pipes.returncode != 0:
                    print(erroutput.rstrip().decode())
                    return
                print(output.decode('utf-8'))
        return


def check_picat():
    '''This function checks if Picat exists and it is in the path
    '''
    try:
        pipes = subprocess.Popen(["picat", "--version"],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, erroutput) = pipes.communicate()
        if pipes.returncode != 0:
            print("Error while initialising extension: cannot run picat. "
                  "Make sure it is on the PATH when you run the Jupyter server.")
            return False
        print(output.rstrip().decode())
    except OSError as _:
        print("Error while initialising extension: cannot run picat. "
              "Make sure it is on the PATH when you run the Jupyter server.")
        return False
    return True
