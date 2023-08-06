import os
import regex
import json
import subprocess
from ethereum.utils import decode_hex

def compile_solidity(sourcecode, name=None, cwd=None, solc='solc', optimize=True, optimize_runs=None):

    process = subprocess.Popen([solc, '--version'], cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderrdata = process.communicate()
    try:
        m = regex.match(r"^Version: (?P<version>\d+\.\d+\.\d+).*$",
                        output.decode('utf-8').split('\n')[1])
        version = tuple([int(i) for i in m.group('version').split('.')])
    except:
        raise Exception("Unable to parse solc version")

    args = [solc, '--allow-paths', '.', '--combined-json', 'bin,abi']

    #if version > (0, 5, -1):
    #    pass #optimize_runs = 200
    #elif version > (0, 4, -1):
    if optimize_runs is None:
        optimize_runs = 1000000000

    if optimize:
        args.append('--optimize')
    if optimize_runs:
        args.extend(['--optimize-runs', str(optimize_runs)])
    #print(' '.join(args))

    if cwd is None:
        cwd = "."
    cwd = os.path.abspath(cwd)

    if os.path.exists(os.path.join(cwd, sourcecode)):
        filename = sourcecode
        sourcecode = None
    else:
        filename = '<stdin>'

    args.append(filename)

    process = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderrdata = process.communicate(input=sourcecode)
    try:
        #print(output.decode('utf-8'))
        output = json.loads(output)
    except json.JSONDecodeError:
        if output and stderrdata:
            output += b'\n' + stderrdata
        elif stderrdata:
            output = stderrdata
        raise Exception("Failed to compile source: {}\n{}\n{}".format(filename, ' '.join(args), output.decode('utf-8')))

    contract = None
    try:
        for key in output['contracts']:
            if key.startswith(filename + ':'):
                if name is not None and not key.endswith(':' + name):
                    continue
                contract = output['contracts'][key]
                break
    except KeyError:
        raise
    if contract is None:
        raise Exception("Unexpected compiler output: unable to find contract in result")

    abi = json.loads(contract['abi'])
    data = decode_hex(contract['bin'])

    return abi, data
