from .fileinfo import FileInfo
from . import ifileinfo, filewriter, CsvFileInfo, utils
import numpy as np
import os
import soundfile as sf
import math.ceil

class Splitter():
    """
            Splitter allows splitting an existing file.

            Args:
                channels: Number of channels the files parsed should have.
                path: the path where the new merger file should be created.
                samplerate: samplerate to write on the file.
                max_length: Maximum file length in minutes.
                
    """
    def __init__(self, channels, path, samplerate, max_length):
        #need to figure out if either max_length by time or by size
        self._channels = channels
        self._init_samples()
        if(isinstance(samplerate,int)):
            self._samplerate = samplerate
        else:
            raise TypeError("Samplerate not integer")

        #if(not(isinstance(max_length,int))):
        #    raise TypeError("max_length not integer")
        
        self.path = path
        #max_length = minutes * seconds
        self.max_num_samples = math.ceil((max_length * 60) * samplerate)
        #if the file exists already, then there's no need to create it(FileInfo)
        #if theres no file, we need to create it (array)
        self.file_exists = (os.path.isfile(self.path))


    def _init_samples(self):
        self._samples = np.empty(shape=(0,self._channels))

    def __enter__(self):
        return self

    def __exit__(self,type,value,traceback):
        pass

    def add(self, *files):
        """
            Adds new samples to the buffer array.

            When ``create_file`` method is executed the buffer gets emptied.

        Args:
            *files: An array, containing several pathes to files or IFileInfos specializations,
                although the latter is preferred.
        """
        tmp = None
        for f in files:
            if(issubclass(type(f),ifileinfo.IFileInfo)):
                tmp = f.getSamples()
            else:
                with FileInfo(f) as this:
                    tmp = this.getSamples()
            self._samples = np.append(self._samples,tmp,axis=0)

    def create_file(self, samplerate = None):
        """
            Creates a new file with the filename, converts based on extension given in ``new_filename``
            
            When executed the sample buffer will be emptied,
            so ``create_file`` should be executed frequently.

            Args:
                samplerate: Samplerate of the file.

        """
        if(len(self._samples) == 0):
            raise TypeError("No samples are queued!")
        if(samplerate == None):
            samplerate = self._samplerate
        path = utils.path_splitter(self.path)
        if(path['file_name'] == None):
            raise TypeError("It doesn't contain an extension")
        #tries to create the directory
        try: 
            import os
            os.mkdir(path['path'])
        except (OSError,FileNotFoundError) as e:
            #import errno
            pass
            #if(e.errno != errno.EEXIST):
            #   raise #if there's an error thats not eexits(file/directory exists)
        samples_left = len(self._samples)
        files_index = 0
        
        while(samples_left > 0):
            samples_to_write = self._samples[self.max_num_samples*files_index:self.max_num_samples*(files_index+1)]
            samples_left -= self.max_num_samples
            with CsvFileInfo(samples_to_write,self._samplerate) as infofile:
                with filewriter.FileWriter(infofile) as fw:
                    fw.create_file(path['path']+path['file_name']+'_'+str(files_index)+'.'+path['extension'], self._samplerate)
            files_index+=1
        self._init_samples()