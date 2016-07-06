#TODO Make flac/ogg not have dup track tags (optional perhaps?)
import sys
supported_File_Types = []
DEBUG = 0
# Lets try to import all we can.  What we can import will be added to the supported list
# that is available from a static method.
try:
	import pyid3lib
	supported_File_Types.append("mp3")
except ImportError:
	print "You lack mp3 support"
try:
	import ogg.vorbis
	supported_File_Types.append("ogg")
except ImportError:
	print "You lack ogg support"
try:
	import flac.metadata as metadata
	supported_File_Types.append("flac")
except ImportError:
	print "You lack flac support"

class FileNotSupported(Exception):
	pass
class InvalidInput(Exception):
	pass

class tags:
	def __init__(self, file):
		self.filename = file
		if supported_File_Types.count(file[-3:]) < 1 and  supported_File_Types.count(file[-4:]) < 1:
			raise FileNotSupported, file + ' is not of supported type'

		if file[-4:] == '.mp3':
			self.type = 1
#			try:
			self.tag = pyid3lib.tag( file )
#			except eyeD3.tag.InvalidAudioFormatException:
#				raise FileNotSupported, file + ' is not of supported type'

			try:
				self.album = self.tag.album
			except AttributeError:
				self.album = None
			try:
				self.artist = self.tag.artist
			except AttributeError:
				self.artist = None

			self.vendor = None

			try:
				self.title = self.tag.title
			except AttributeError:
				self.title = None
			try:
				self.tracktotal = self.tag.track[1]
			except AttributeError:
				self.tracktotal = None
			try:
				self.tracknumber = self.tag.track[0]
			except AttributeError:
				self.tracknumber = None
			try:
				self.genre = self.tag[self.tag.index('TCON')]['text']
			except ValueError:
				self.genre = None

			try:
				self.date = self.tag.year
			except AttributeError:
				self.date = None
			try:
				self.discnum = self.tag[self.tag.index('TPOS')]['text']
			except ValueError:
				self.discnum = None
			try:
				self.comment = self.tag[self.tag.index('COMM')]['text']
			except ValueError:
				self.comment = None
			if DEBUG == 1:
				for i in self.tag:
					print i

		elif file[-4:] == '.ogg':
			self.type = 2
			try:
				self.tag = ogg.vorbis.VorbisFile(file)
			except ogg.vorbis.VorbisError:
				raise FileNotSupported, file + ' is not of supported type'				
			values = self.tag.comment().as_dict()
			if DEBUG == 1:
				print values
			try:
				self.album = values['ALBUM'].pop()
			except KeyError:
				self.album = None
			try:
				self.artist = values['ARTIST'].pop()
			except KeyError:
				self.artist = None
			try:
				self.vendor = values['VENDOR'].pop() #?
			except KeyError:
				self.vendor = None
			try:
				self.title = values['TITLE'].pop()
			except KeyError:
				self.title = None
			try:
				self.tracktotal = values['TRACKTOTAL'].pop()
			except KeyError:
				self.tracktotal = None
			try:
				self.tracknumber = values['TRACKNUMBER'].pop()
			except KeyError:
				self.tracknumber = None
			try:
				self.genre = values['GENRE'].pop()
			except KeyError:
				self.genre = None
			try:
				self.discnum = values['DISCNUMBER'].pop()
			except KeyError:
				self.discnum = None
			try:
				self.date = values['DATE'].pop()
			except KeyError:
				self.date = None
			try:
				self.comment = values['DESCRIPTION'].pop()
			except KeyError:
				self.comment = None				
		elif file[-5:] == '.flac':
			self.type = 3
			# MUCH of the following is taken from the python-flac example code
			# create a chain
			chain = metadata.Chain()
			chain.read(file)

			# get iterator, init
			it = metadata.Iterator()
			it.init(chain)

			while 1:
    				if it.get_block_type() == metadata.VORBIS_COMMENT:
					block = it.get_block()
					vc = metadata.VorbisComment(block)
					break
				if not it.next():
					break

			if vc:
				if DEBUG == 1:
					for c in vc.comments:
						print c
				try:
					self.album = vc.comments['ALBUM']
				except KeyError:
					self.album = None
				try:
					self.artist = vc.comments['ARTIST']
				except KeyError:
					self.artist = None
				try:
					self.vendor = vc.comments['VENDOR']
				except KeyError:
					self.vendor = None
				try:
					self.title = vc.comments['TITLE']
				except KeyError:
					self.title = None
				try:
					self.tracktotal = vc.comments['TRACKTOTAL']
				except KeyError:
					self.tracktotal = None
				try:
					self.tracknumber = vc.comments['TRACKNUMBER']
				except KeyError:
					self.tracknumber = None
				try:
					self.genre = vc.comments['GENRE']
				except KeyError:
					self.genre = None

				try:
					self.discnum = vc.comments['DISCNUMBER']
				except KeyError:
					self.discnum = None
				try:
					self.date = vc.comments['DATE']
				except KeyError:
					self.date = None
				try:
					self.comment = vc.comments['DESCRIPTION']
				except KeyError:
					self.comment = None
			self.chain = chain
			self.vc = vc

	def get_Supported_Formats():
		return supported_File_Types
	get_Supported_Formats = staticmethod(get_Supported_Formats)

	def get_Album(self):
			return self.album
	def get_Artist(self):
			return self.artist
	def get_Vendor(self):
			return self.vendor # ERROR
	def get_Title(self):
			return self.title
	def get_TrackTotal(self):
			return self.tracktotal
	def get_TrackNumber(self):
			return self.tracknumber
	def get_Genre(self):
			return self.genre
	def get_DiscNumber(self):
			return self.discnum
	def get_Date(self):
			return self.date
	def get_Comment(self):
			return self.comment

	def set_Album(self, newalbum):
		if self.type == 1:
			self.tag.album = newalbum
			self.tag.update()
			self.album = newalbum
		elif self.type == 2:
			self.write_Ogg_Tag('ALBUM',newalbum)
			self.album = newalbum
		elif self.type == 3:
			self.write_Flac_Tag('ALBUM',newalbum)
			self.album = newalbum

	def set_Artist(self, newartist):
		if self.type == 1:
			self.tag.artist = newartist
			self.tag.update()
			self.artist = newartist
		elif self.type == 2:
			self.write_Ogg_Tag('ARTIST',newartist)
			self.artist = newartist
		elif self.type == 3:
			self.write_Flac_Tag('ARTIST',newartist)
			self.artist = newartist

	def set_Title(self, newtitle):
		if self.type == 1:
			self.tag.title = newtitle
			self.tag.update()
			self.title = newtitle
		elif self.type == 2:
			self.write_Ogg_Tag('TITLE',newtitle)
			self.title = newtitle
		elif self.type == 3:
			self.write_Flac_Tag('TITLE',newtitle)
			self.title = newtitle

	def set_TrackTotal(self, newtracktotal):
		if self.type == 1:
			if self.tracknumber == None:
				a = 0
			else:
				a = self.tracknumber
			self.tag.track = (int(a), int(newtracktotal))
			self.tag.update()
			self.tracktotal = newtracktotal
		elif self.type == 2:
			self.write_Ogg_Tag('TRACKTOTAL',newtracktotal)
			self.tracktotal = newtracktotal
		elif self.type == 3:
			self.write_Flac_Tag('TRACKTOTAL',newtracktotal)
			self.tracktotal = newtracktotal

	def set_TrackNumber(self, newtracknumber):
		if self.type == 1:
			if self.tracktotal == None:
				a = 0
			else:
				a = self.tracktotal
			self.tag.track = (int(newtracknumber), int(a))
			self.tag.update()
			self.tracknumber = newtracknumber
		elif self.type == 2:
			self.write_Ogg_Tag('TRACKNUMBER',newtracknumber)
			self.tracknumber = newtracknumber
		elif self.type == 3:
			self.write_Flac_Tag('TRACKNUMBER',newtracknumber)
			self.tracknumber = newtracknumber

	def set_Genre(self, newgenre):
		if self.type == 1:
			self.set_Mp3_Fields('TCON', newgenre)
			self.genre = newgenre
		elif self.type == 2:
			self.write_Ogg_Tag('GENRE',newgenre)
			self.genre = newgenre
		elif self.type == 3:
			self.write_Flac_Tag('GENRE',newgenre)
			self.genre = newgenre

	def set_DiscNumber(self, newdiscnum):
		if self.type == 1:
			self.set_Mp3_Fields('TPOS', newdiscnum)
			self.discnum = newdiscnum
		elif self.type == 2:
			self.write_Ogg_Tag('DISCNUMBER',newdiscnum)
			self.discnum = newdiscnum
		elif self.type == 3:
			self.write_Flac_Tag('DISCNUMBER',newdiscnum)
			self.discnum = newdiscnum

	def set_Date(self, newdate):
		if len(str(newdate)) != 4:		
			raise InvalidInput, ' The Year must be 4 digits'	
		if self.type == 1:
			self.tag.year = newdate
			self.tag.update()
		elif self.type == 2:
			self.write_Ogg_Tag('DATE',newdate)
			self.date = newdate
		elif self.type == 3:
			self.write_Flac_Tag('DATE',newdate)
			self.date = newdate

	def set_Comment(self, newcomment):
		if self.type == 1:
			self.set_Mp3_Fields('COMM', newcomment)
			self.comment = newcomment
		elif self.type == 2:
			self.write_Ogg_Tag('DESCRIPTION',newcomment)
			self.comment = newcomment
		elif self.type == 3:
			self.write_Flac_Tag('DESCRIPTION',newcomment)
			self.comment = newcomment

	def write_Ogg_Tag(self, field, newdata):
		comment = self.tag.comment()
		try:
			if str(newdata).upper() in str(comment.as_dict()[field]).upper():
				# The Data Is Already In The Tag
				return
		except KeyError:
			# The File Doesn't Yet Have This Field
			pass
		# Add The Field
		comment.add_tag(field, unicode(newdata))
		# Write Out The File
		comment.write_to(self.filename)

	def write_Flac_Tag(self, field, newdata):
		does_exist = field + '=' + str(newdata).strip()
		if self.vc:
			# This loop checks to see if the tag already exists
			for c in self.vc.comments:
				if c == does_exist:
					return

			self.vc.comments[field] = newdata
			self.chain.write(True,True)

	def clear_Tag_Data(self):
		if self.type == 1:
			frames = []
			# make a list of all frames
			for i in self.tag:
				frames.append(i)
			# del all those frames
			for i in frames:
				self.tag.remove( i['frameid'] )
			self.tag.update()
		elif self.type == 2:
			self.tag.comment().clear()
			self.tag.comment().write_to(self.filename)
		elif self.type == 3:
			self.vc.block.vorbiscomment_remove_entries_matching('ARTIST')
			self.vc.block.vorbiscomment_remove_entries_matching('ALBUM')
			self.vc.block.vorbiscomment_remove_entries_matching('TITLE')
			self.vc.block.vorbiscomment_remove_entries_matching('DATE')
			self.vc.block.vorbiscomment_remove_entries_matching('DISCNUMBER')
			self.vc.block.vorbiscomment_remove_entries_matching('DESCRIPTION')
			self.vc.block.vorbiscomment_remove_entries_matching('TRACKTOTAL')
			self.vc.block.vorbiscomment_remove_entries_matching('TRACKNUMBER')
			self.vc.block.vorbiscomment_remove_entries_matching('GENRE')
			for c in self.vc.comments:
				print c
			self.chain.write(True,True)


	def set_Mp3_Fields(self, field, newdata):
		try:
			d = self.tag[self.tag.index(field)]        # get the frame
			d['text'] = str(newdata)       # update the dictionary
			self.tag[self.tag.index(field)] = d  # write back the dictionary
		except ValueError:
			# the item doesn't exist so just go ahead and add it
			self.tag.append( { 'frameid' : field, 'text' : str(newdata) } )
		self.tag.update()
