import tarfile

with tarfile.open('prjcode.tar.gz','w:gz') as tar:
    tar.add('source.py')
    tar.add('TestCases.py')
    tar.add('README.txt')
    tar.add('report.pdf')