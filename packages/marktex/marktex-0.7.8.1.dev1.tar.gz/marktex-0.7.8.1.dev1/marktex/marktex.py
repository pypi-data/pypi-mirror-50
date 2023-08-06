import argparse,sys,os


APP_DESC="""
MarkTex is used to convert markdown document into tex format.

You can choose the output dir from:
\n- output to the dir of every md file, the default option.
\n- output to a single dir use -o "path" option.
\n- assign every path use -e "path1" "path2" option.

e.g:
output to the dir the md file is:\n\tmarktex a.md ../b.md /dir/c.md ...

assign every path:\n\tmarktex a.md b.md ... -o "path"

assign every path (be sure the number of the dir options must be equal to markdown files ):\nmarktex a.md b.md ... -e "patha" "pathb" ...
    
"""
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser(description=APP_DESC)

parser.add_argument('mdfiles', metavar='mdfiles', type=str, nargs='+',
                    help='place markdown path')
parser.add_argument('-o','--output',type=str,default=None,help="指定统一路径")
parser.add_argument('-e','--every',help="为每个文件分配路径",nargs="*")
args = parser.parse_args()



every = args.every
mdfiles = args.mdfiles
output = args.output
output_paths = []

if every is not None:
    if len(every) != len(mdfiles):
        print("you ues -e option, the number of outputdirs must be equal to markdown files.")
        exit(1)
    output_paths = every
elif output is not None:
    output_paths = [output]*len(mdfiles)
else:
    for mdfile in mdfiles:
        mdfile = os.path.abspath(mdfile)
        mdpath,fname = os.path.splitext(mdfile)
        output_paths.append(mdpath)

from marktex.texrender.toTex import MarkTex
for mdfile,opath in zip(mdfiles,output_paths):
    _,fname = os.path.split(mdfile)
    fpre,_ = os.path.splitext(fname)
    doc = MarkTex.convert_file(mdfile,opath)
    doc.generate_tex(fpre)

print(f"[info*]convert finished.")
exit(0)
