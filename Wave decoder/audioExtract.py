import numpy as np

class RIFF:
	def __init__(self):
		self.Chunk_ID = None
		self.Chunk_Size = None
		self.Format = None	

class FMT:
	def	__init__(self):
		self.SubChunk1_ID = None
		self.SubChunk1_Size = None
		self.Audio_Format = None
		self.Num_Channels = None
		self.Sample_Rate = None
		self.Byte_Rate = None
		self.Block_Align = None
		self.Bitsper_Sample = None

class DATA:
	def __init__(self):
		self.SubChunk2_ID = None
		self.SubChunk2_Size = None
		self.data = None

class WAV:
	def __init__(self,path):
		self.offset = 0
		self.file = path
		self.RIFF = RIFF()
		self.FMT = FMT()
		self.DATA = DATA()

	def RIFF_CHUNK(self):
		fd = open(self.file,'rb')		
		self.RIFF.Chunk_ID = (fd.read(4))
		self.RIFF.Chunk_Size = readLE(fd.read(4))
		self.RIFF.Format = (fd.read(4))
		self.offset += 12
		fd.close()
		return self.RIFF

	def FMT_CHUNK(self):
		fd = open(self.file,'rb')
		fd.seek(self.offset)
		self.FMT.SubChunk1_ID = (fd.read(4))
		self.FMT.SubChunk1_Size = readLE(fd.read(4))
		self.FMT.Audio_Format = readLE(fd.read(2))
		self.FMT.Num_Channels = readLE(fd.read(2))
		self.FMT.Sample_Rate = readLE(fd.read(4))
		self.FMT.Byte_Rate = readLE(fd.read(4))
		self.FMT.Block_Align = readLE(fd.read(2))
		self.FMT.Bitsper_Sample = readLE(fd.read(2))
		fd.close()
		self.offset += 24		
		return self.FMT

	def DATA_CHUNK(self):		
		fd = open(self.file,'rb')
		fd.seek(self.offset)
		music_data = []
		self.DATA.SubChunk2_ID = (fd.read(4))
		self.DATA.SubChunk2_Size = readLE(fd.read(4))
		music_data = list(fd.read(self.DATA.SubChunk2_Size))
		fd.close()
		self.DATA.data = music_data
		return self.DATA	

def readLE(string):
	string = string.hex()
	reverse_string = ''
	length = len(string)
	while length:
		reverse_string += string[length-2:length]
		length -= 2
	return int(reverse_string,16)

def readBE(string):
	string = string.hex()	
	return int(string,16)

if __name__=="__main__":
	obj = WAV('mozart.wav')
	print(obj.RIFF_CHUNK().__dict__)
	print(obj.FMT_CHUNK().__dict__)
	data = obj.DATA_CHUNK()
	file_data = data.data
	file = open('raw','wb')
	file.write(bytearray(file_data))
	file.close()