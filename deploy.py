# Todo;
# 1) get the most recent tag
# 2) get the most recent branch
# 3) make a FileName
# 4) compress a build/
from git import Repo
from shutil import make_archive, copyfile
from requests import post
from json import loads


class Deploy:

    def __init__(self):
        """ deployment class """
        self.repo = Repo('./')

    def getMostRecentTag(self):
        """returns the most recent tag which should the release"""
        return str(self.repo.tags[0]).replace('.', '')

    def getMostRecentCommitHash(self):
        """returns a sha1 of has of the most recent the last fiveteen chars"""
        return str(self.repo.refs[0].commit.hexsha)[-15:]

    def getCurrentBranchName(self):
        """gets the active Branch"""
        return str(self.repo.active_branch)[8:]

    def mkFileName(self):
        """ builds out the file name of the archive file """
        release = self.getMostRecentTag()
        branch = self.getCurrentBranchName()
        sha_msg = self.getMostRecentCommitHash()
        return f'wordblock_{release}_{branch}_{sha_msg}'

    def cpReadmeToBuild(self):
        """ copy across `readme.md` read me file"""
        return copyfile('./readme.md', './build/readme.md')

    def compress(self, fileName: str):
        """ makes the archive file returns the absute path to the new archive"""
        zipFileAddr = make_archive(f'./{fileName}', 'zip', './build/')
        return zipFileAddr

    def postFileToBitbucket(self, filePath: str):
        """ posts the file to the filepath """

        jsonFileObj = open('./devKeys.json')
        json = loads(jsonFileObj.read())
        jsonFileObj.close()

        BB_AUTH_STRING = json['BB_AUTH_STRING']
        BITBUCKET_REPO_OWNER = json['BITBUCKET_REPO_OWNER']
        BITBUCKET_REPO_SLUG = json['BITBUCKET_REPO_SLUG']

        fileObj = {'files': open(f'{filePath}', 'rb')}
        url = f'https://{BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/{BITBUCKET_REPO_OWNER}/{BITBUCKET_REPO_SLUG}/downloads'
        req = post(url, files=fileObj)
        fileObj['files'].close()

        return req.status_code

    def main(self):
        self.cpReadmeToBuild()
        filename = self.mkFileName()

        print('compressing file.')
        pathname = self.compress(filename)
        rObj = {
            'path': pathname,
            'sentToBb': False

        }
        print('sending file to bitbucket.')
        if self.postFileToBitbucket(pathname) is 200:
            rObj['sentToBb'] = True

        return rObj


if __name__ == '__main__':
    x = Deploy().main()
    print('A Deployment .zip has been created;')
    print(f'>>> {x["path"]}')
    if x['sentToBb']:
        print('Deployment has been sent Bitbucket')
