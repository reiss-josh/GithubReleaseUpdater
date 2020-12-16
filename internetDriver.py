import json
import requests
import zipfile
import os

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