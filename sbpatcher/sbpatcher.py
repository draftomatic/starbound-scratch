import sys, glob, os, shutil, fnmatch

if len(sys.argv) != 5:
  print('Usage:   python sbpatcher.py <input folder> <output folder> <patch file> <pattern>')
  sys.exit(1)

indir = sys.argv[1]
outdir = sys.argv[2]
patch = sys.argv[3]
pattern = sys.argv[4]

if not os.path.isdir(indir):
  print(indir + ' is not a directory; exiting')
  sys.exit(1)

if not os.path.isdir(outdir):
  print(outdir + ' is not a directory; exiting')
  sys.exit(1)

if not os.path.exists(patch):
  print(patch + ' is not a file; exiting')
  sys.exit(1)


###########

indir = os.path.realpath(indir)
outdir = os.path.realpath(outdir)
searchpath = indir + '/' + pattern

print('Searching ' + searchpath)

#files = glob.glob(searchpath)
files = []
for root, dirnames, filenames in os.walk(indir):
  for filename in fnmatch.filter(filenames, pattern):
    files.append(os.path.join(root, filename))

print(str(len(files)) + ' files found\n')

if len(files) == 0:
  sys.exit(1)

filedict = {}

for f in files:
  realpath = os.path.realpath(f)
  patchout = realpath.replace(indir, outdir)
  print('  ' + realpath + ' => ' + patchout)
  filedict[realpath] = patchout

print('\nProceed? (Y/y)')
proceed = raw_input()

if proceed.lower() != 'y':
  sys.exit(0)

for key, value in filedict.iteritems():
  if os.path.exists(value):
    print('Patch file ' + value + ' already exists; skipping')
    continue
  print('creating patch file: ' + value)
  #shutil.copyfile(patch, out)
