import zipfile
from os.path import join, isdir

import builder


class CreateSourceArchive(builder.Task):
    description = "Build source archive"

    def DoTask(self):
        """
        Create a zip archive off all versioned files in the working copy.
        """
        import pysvn
    
        filename = join(
            self.buildSetup.outDir,
            "%(appName)s_%(appVersion)s_Source.zip" % self.buildSetup.__dict__
        )
        client = pysvn.Client()
        workingDir = self.buildSetup.sourceDir
        zipFile = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        for status in client.status(workingDir, ignore=True):
            if status.is_versioned:
                path = status.path
                if not isdir(path):
                    arcname = path[len(workingDir) + 1:]
                    zipFile.write(path, arcname)
        zipFile.close()
    
