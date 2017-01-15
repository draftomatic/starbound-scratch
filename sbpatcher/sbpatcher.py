import sys, glob, os, shutil, fnmatch, json, commentjson

def main():

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

  if len(files) == 0:
    print('No files found in ' + indir + ' matching pattern ' + pattern)
    sys.exit(1)

  filedict = {}

  for f in files:
    realpath = os.path.realpath(f)
    patchout = realpath.replace(indir, outdir) + '.patch'
    if filematcher(realpath):
      print('  ' + realpath + ' => ' + patchout)
      filedict[realpath] = patchout

  print('\n' + str(len(filedict)) + ' files matched')
  print('Proceed? [Y/y]')
  proceed = raw_input()

  if proceed.lower() != 'y':
    sys.exit(0)

  patchcount = 0
  for inpath, outpath in filedict.iteritems():
    if os.path.exists(outpath):
      print('Patch file ' + outpath + ' already exists; skipping')
      continue

    print('Creating patch file: ' + outpath)

    try:
      os.makedirs(os.path.dirname(outpath))
    except OSError as e:
      if e.errno != 17:
        raise e

    shutil.copyfile(patch, outpath)
    patchcount += 1
  
  print('\nCreated ' + str(patchcount) + ' patch files')

def filematcher(path):
  try:
    with open(path) as file:
      jsoncontent = commentjson.load(file)

      if 'smashable' in jsoncontent and jsoncontent['smashable'] == True:
        return True
      else:
        return False
  except:
    print('Failed to read file ' + path)




main()

print('Finished!')