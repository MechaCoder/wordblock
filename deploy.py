from git import Repo
from shutil import make_archive, copyfile
from requests import post
from json import loads
import os
import sys
import requests


class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 << 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                sys.stderr.write("\r{percent:3.0f}%".format(percent=percent))
                yield data

    def __len__(self):
        return self.totalsize


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
        base = str(self.repo.active_branch).split('/')[-1]
        return base

    def mkFileName(self):
        """ builds out the file name of the archive file """
        release = self.getMostRecentTag()
        branch = self.getCurrentBranchName()
        sha_msg = self.getMostRecentCommitHash()
        return f'wordblock_{branch}'

    def cpReadmeToBuild(self):
        """ copy across `readme.md` read me file"""
        return copyfile('./readme.md', './dist/readme.md')

    def compress(self, fileName: str):
        """ makes the archive file returns the absute path to the new archive"""
        zipFileAddr = make_archive(f'./{fileName}', 'zip', './dist/')
        return zipFileAddr

    def postFileToBitbucket(self, filePath: str):
        """ posts the file to the filepath """

        jsonFileObj = open('./devKeys.json')
        json = loads(jsonFileObj.read())
        jsonFileObj.close()

        BB_AUTH_STRING = json['BB_AUTH_STRING']
        BITBUCKET_REPO_OWNER = json['BITBUCKET_REPO_OWNER']
        BITBUCKET_REPO_SLUG = json['BITBUCKET_REPO_SLUG']
        url = f'https://{BB_AUTH_STRING}@api.bitbucket.org/2.0/repositories/{BITBUCKET_REPO_OWNER}/{BITBUCKET_REPO_SLUG}/downloads'
        


        # with open(filePath, 'rb') as fileObj:
        #     req = post(url, data=fileObj)

        req = post(url, data = upload_in_chunks(filePath, 10))

        return True

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
