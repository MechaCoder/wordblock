# Todo;
# 1) get the most recent tag
# 2) get the most recent branch
# 3) make a FileName 
# 4) compress a build/
from git import Repo
from shutil import make_archive, copyfile

class Deploy:

    def __init__(self):
        self.repo = Repo('./')
    
    def getMostRecentTag(self):
        return str(self.repo.tags[0]).replace('.','')

    def getMostRecentCommitHash(self):
        return str(self.repo.refs[0].commit.hexsha)[-15:]

    def getCurrentBranchName(self):
        return str(self.repo.active_branch)[8:]

    def mkFileName(self):
        release = self.getMostRecentTag()
        branch = self.getCurrentBranchName()
        sha_msg = self.getMostRecentCommitHash()
        return f'wordblock_{release}_{branch}_{sha_msg}'

    def cpReadmeToBuild(self):
        return copyfile('./readme.md', './build/readme.md')

    def compress(self, fileName:str):
        zipFileAddr = make_archive(f'./{fileName}', 'zip', './build/')
        return zipFileAddr

    def main(self):
        self.cpReadmeToBuild()
        filename = self.mkFileName()
        return self.compress(filename)

if __name__ == '__main__':
    x = Deploy().main()
    print('A Deployment .zip has been created;')
    print(f'---- {x}')