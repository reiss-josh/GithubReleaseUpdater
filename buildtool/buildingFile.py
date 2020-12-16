import json
import requests
import zipfile
import os
import sys, getopt

def ConstructUrl(username, reponame):
  return "https://api.github.com/repos/" + username + "/" + reponame + "/releases/latest"

def GetJsonData(url, username = None):
  if(username):
    response = requests.get(url, auth = (username,'token'))
  else:
    response = requests.get(url)
  loaded = json.loads(response.text)
  return loaded

def GetAssetDownloads(jsonData):
  assets = jsonData["assets"]
  out = []
  for i in assets:
    out += [i['browser_download_url']]
  return out

def RetrieveDownloadLinks(repoUsername, reponame, downloaderUsername = None):
  builtUrl = ConstructUrl(repoUsername, reponame)
  jsonData = GetJsonData(builtUrl, downloaderUsername)
  assetLinks = GetAssetDownloads(jsonData)
  return assetLinks

def GetFileNamesFromUrls(downloadLinks):
  out = []
  for currLink in downloadLinks:
    fileName = (currLink.split('/')[-1:][0])
    out += [fileName]
  return out

def CreateDirIfInvalid(dst):
  isDir = os.path.isdir(dst)
  if(not isDir):
    os.mkdir(dst)

def AbsPathConstructor(fileName, dst):
  if(not dst):
    return fileName
  if(dst[-1] != '/' and dst[-1] != "\\"):
    dst += '/'
  CreateDirIfInvalid(dst)
  return dst+fileName

def DownloadFile(url, fileName):
  fileObject = requests.get(url)
  with open(fileName, 'wb') as localFile:
    localFile.write(fileObject.content)

def UnzipToLocation(src, dst, deleteSrc = False):
  with zipfile.ZipFile(src, 'r') as zip_ref:
    zip_ref.extractall(dst)
  os.remove(src)

def CheckIfZip(fileName):
  return zipfile.is_zipfile(fileName)

def BeautifyStringArray(items):
  out = []
  for i in range(len(items)):
    out += [("["+str(i)+"]: " + items[i])]
  return out

def chooseFile(linkFileNames):
  beautified = BeautifyStringArray(linkFileNames)
  print("\nAVAILABLE FILES")
  for i in beautified:
    print(i)

  chosenInd = input("Enter number of the file you want to download:\n")
  return(int(chosenInd))

def main():
  #repouser, reponame, dst, myuser = GetParameters()
  repouser = "yamashi"
  reponame = "PerformanceOverhaulCyberpunk"
  dst = "/bin/x64"
  myuser = None

  append = input("Enter the directory where Cyberpunk is:\n(Ex: D:/Games/Steam/steamapps/common/Cyberpunk 2077\n")
  dst = append + dst
  print()

  downloadLinks = RetrieveDownloadLinks(repouser, reponame, myuser)
  linkFileNames = GetFileNamesFromUrls(downloadLinks)

  if(len(linkFileNames) < 2):
    chosenInd = 0
  else:
    chosenInd = chooseFile(linkFileNames)

  chosenUrl = downloadLinks[chosenInd]
  chosenFile = AbsPathConstructor(linkFileNames[chosenInd], dst)

  print("\nDownloading " + chosenFile + "...")
  DownloadFile(chosenUrl, chosenFile)
  print("Done!")

  if(CheckIfZip(chosenFile) == True):
    print("\nUnzipping " + chosenFile + " to " + dst + "...")
    UnzipToLocation(chosenFile, dst, True)
    print("Done!")

  input("Press Enter to continue...")

if __name__ == "__main__":
  main()