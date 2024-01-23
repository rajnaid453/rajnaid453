from artifactory import ArtifactoryPath
import os

path = ArtifactoryPath(
    "https://artifact.swf.i.mercedes-benz.com/artifactory/avocadobscqal-delivery-release/i2/E307.0/deliverables/richos/dev/richos_backup.ext4.gz", auth=(
        "smuktha", "cmVmdGtuOjAxOjE3MzEwNTY0MDA6Qzl5d0F6b2YwMGhlZTBtRDRlSlFMcVpUM2Zr"))

# with path.open() as fd, open("richos_backup.ext4.gz", "wb") as out:
#     out.write(fd.read())
bpath = os.path.abspath(os.path.join("C:\\Workspace\\Gen20x\\builds\\SB_E307.0","richos_backup.ext4.gz"))
with open("richos_backup.ext4.gz", "wb") as out:
    path.writeto(out=bpath, chunk_size=256)