import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../flaskr'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
print(os.path.abspath(os.path.join(testdir, srcdir)))

print(sys.path)

