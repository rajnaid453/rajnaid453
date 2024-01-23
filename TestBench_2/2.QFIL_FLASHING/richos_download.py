
from artifactory import *

richosBuild = int(sys.argv[4])
userName = str(sys.argv[5])
artifactoryToken = str(sys.argv[6])
X = r"https://artifact.swf.daimler.com:443/artifactory/apricotbscqal/build/yocto.apricot-manifests.dunfell.downstream/"+str(richosBuild)
path = ArtifactoryPath(X, auth=(userName, artifactoryToken))
print("richos download started")
path.archive().writeto(out=r"C:\WorkSpace\Gen20X\builds\\"+str(richosBuild)+ ".zip", chunk_size=100 * 1024 * 1024)
print("richos download completed")
#path.archive().writeto(out=r"\\53.127.143.112\\oms_testing\\testing\\Sreekanth\\"+str(richosBuild)+ ".zip", chunk_size=100 * 1024 * 1024)
