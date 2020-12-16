from internetDriver import *
import sys, getopt

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

#generate parameters via text input if no commandline input
def GenerateParameters():
  repouser = input("\nEnter the username of the repository owner:\n")
  reponame = input("\nEnter the name of the repository:\n")
  dst = input("\nEnter the destination for your downloaded file:\n(Optional, hit Enter to skip)\n(Ex: C:/Downloads)\n")
  myuser = input("\nEnter your github username:\n(Optional, hit Enter to skip)\n")

  return repouser,reponame,dst,myuser

def GetParameters():
  #get parameters
  params = []
  if (len(sys.argv) > 1):
    for i in sys.argv[1:]:
      params += [i]

  #verify enough params, else have entry manually
  if(len(params) < 2):
    print("Not enough parameters!")
    print("main.py <repo owner> <repo name> <destination (optional)> <your username (optional)>")
    return GenerateParameters()
  
  #add dst if not found
  if(len(params) < 3):
    params += [""]

  #add myuser if not found
  if(len(params) < 4):
    params += [None]

  #return parameters
  return params[0],params[1],params[2],params[3]
  

def main():
  repouser, reponame, dst, myuser = GetParameters()
  
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

if __name__ == "__main__":
  main()