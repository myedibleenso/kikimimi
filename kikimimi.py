import praw
import nltk
import re
import os


###regex
url_pattern = r'(\s*https?:\/\/.*[\r\n]*)'


###celebrities
politicians =["PresidentObama", "hooshangamirahmadi", "GovSchwarzenegger"]

muscle_guys = ["GovSchwarzenegger", "IamDolphLundgren"]

astronauts = ["ColChrisHadfield"]

chefs = ["iamAnthonyBourdain"]

comedians =["_WillFerrell", "iamlouisck", "MrJohnCReilly", "_Seinfeld", "_BillMurray",
		    "JoeRoganForReals", "RobinWilliamsHere", "BatemanJason", "ThatKevinSmith"]

actors = ["iamdavidblaine", "thebryancranston", "RealMarkHamill", "Terry_Gilliam", 
          "Al_the_hologram", "williamshatner", "GovSchwarzenegger", "IamDolphLundgren"]

musicians = ["alyankovic", "Here_Comes_The_King"]

writers = ["RL__Stine", "stephenkinghere", "RASalvatore", "JohnKricfalusi", "DavidXCohen_"]

scientists = ["neiltyson", "sundialbill", "DrMichioKaku"]

technologists = ["salman_khan_academy", "thisisbillgates", "StephenWolfram-Real"]

celebrities = list(set(politicians + muscle_guys + astronauts + chefs + 
				  comedians + actors + musicians + writers + scientists + technologists))

celeb_lookup = {"thisisbillgates":"Bill Gates",
				"PresidentObama":"Barack Obama",
				"RL__Stine":"R.L. Stine",
				"Terry_Gilliam":"Terry Gilliam",
				"RobinWilliamsHere":"Robin Williams",
				"JoeRoganForReals":"Joe Rogan",
				"Al_the_hologram":"Dean Stockwell",
				"_Seinfeld":"Jerry Seinfield",
				"iamAnthonyBourdain":"Anthony Bourdain",
				"IamDolphLundgren":"Dolph Lundgren",
				"iamlouisck":"Louis C.K.",
				"RealMarkHamill":"Mark Hamill",
				"JohnKricfalusi":"John Kricfalusi",
				"_WillFerrell":"Will Ferrell",
				"ColChrisHadfield":"Chris Hadfield",
				"hooshangamirahmadi":"Hooshang Amirahmadi",
				"MrJohnCReilly":"John C. Reilly",
				"RASalvatore":"R.A. Salvatore",
				"ThatKevinSmith":"Kevin Smith",
				"_BillMurray":"Bill Murray",
				"williamshatner":"William Shatner",
				"neiltyson":"Neil deGrasse Tyson",
				"thebryancranston":"Bryan Cranston",
				"alyankovic":"Al Yankovic",
				"DrMichioKaku":"Michio Kaku",
				"StephenWolfram-Real":"Stephen Wolfram",
				"sundialbill":"Bill Nye",
				"GovSchwarzenegger":"Arnold Schwarzenegger",
				"salman_khan_academy":"Salman Khan",
				"Here_Comes_The_King":"Snoop Dogg",
				"BatemanJason":"Jason Batemen",
				"iamdavidblaine":"David Blaine",
				"stephenkinghere":"Stephen King",
				"DavidXCohen_":"David Cohen"}


class RedditBot(object):
	"""
	"""
	def __init__(self, bot_name='az_ling_bot', verbose=False):
		print "creating bot..."
		self.bot = praw.Reddit(bot_name)
		self.user_comments = dict()
		self.verbose = verbose
		self.chunk_size = 20
		self.out_dir = "REDDIT_USERS"
		self.log_file = os.path.join(self.out_dir, "contents.txt")

	def yap(self, msg):
		"""
		wrapper for std out
		"""
		if self.verbose:
			print msg

	def create_directory(self, p):
		"""
		"""
		if not os.path.exists(p):
			os.makedirs(p)

	def logger(self, msg, log_file=None):
		"""
		"""
		if not log_file: 
			log_file = self.log_file

		if not os.path.exists(log_file):
			log_dir = os.path.join(os.path.split(log_file)[:-1])
			self.create_directory(*log_dir)
			open(log_file, 'w').close()
		
		with open(log_file, 'a') as f:
			f.write(msg)

	def get_comments(self, username, comment_limit=None, clean=True):
		"""
		"""
		try:
			user = self.bot.get_redditor(username)
			comments = list()
			for comment in user.get_comments(limit=comment_limit):
				body = comment.body
				if len(body.split()) > 1:
					if clean:
						body = self.clean_comment(body)
					comments.append(body)
					self.yap(body)
				else:
					self.yap("!!!short comment found: \n\t\"{0}\"".format(body))
		except Exception, e:
			print e
			print "problem with {0}".format(username)
		if comments:
			self.user_comments[username]=comments

	def num_comments(self, username):
		"""
		"""
		try:
			user = self.bot.get_redditor(username)
			print "user: {0}".format(username)
			print "comments: {0}\n".format(len(list(user.get_comments(limit=None))))
		except Exception, e:
			print e
			print "problem with {0}".format(username)

	def clean_comment(self, comment):
		"""
		"""
		clean_comment = re.sub(url_pattern, 'URL', comment, flags=re.MULTILINE)
		return clean_comment

	def tokenize_stuff(self, comments):
		"""
		"""
		tokenized_comments = [nltk.tokenize.wordpunct_tokenize(sent) for comment in comments \
							  for sent in nltk.tokenize.sent_tokenize(comment)]
		return tokenized_comments

	def run_all(self):
		"""
		"""
		for celeb in celebrities:
			self.get_comments(celeb)
			tokenized_comments = poo.tokenize_stuff(self.user_comments[celeb])
			self.user_comments[celeb] = tokenized_comments
			print "username: {0}".format(celeb)
			print "real name: {0}".format(celeb_lookup[celeb])
			print "sentences: {0}\n".format(len(tokenized_comments))
			self.yap("making files...")
			self.make_files(celeb, tokenized_comments)

	def make_files(self, username, comments, chunk_size=None, log_data=True):
		"""
		"""
		if not chunk_size:
			chunk_size = self.chunk_size

		last_name = celeb_lookup[username].split()[-1]
		last_name = last_name.replace('.','')
		size_designator = "COMPLETE" if len(comments) > 1000 else "SMALL"

		author_dir = os.path.join(os.getcwd(), self.out_dir, size_designator, last_name)
		self.create_directory(author_dir)
		
		if log_data:
			self.logger("username: {0}\n".format(username))
			self.logger("real name: {0}\n".format(celeb_lookup[username]))
			self.logger("sentences: {0}\n".format(len(comments)))
			self.logger("location: {0}\n\n".format(os.path.join(self.out_dir, size_designator)))
		
		file_id = 0
		for i in xrange(0, len(comments), chunk_size):
			chunk = '\n'.join([' '.join(c) for c in comments[i:i+chunk_size]])
			fname = os.path.join(author_dir, "{0}_{1}".format(last_name, file_id))
			
			with open(fname, 'w') as f:
				f.write(chunk.encode('utf8'))
			
			file_id += 1

if __name__ == "__main__":
	print "gathering comments for celebrities..."
	poo = RedditBot()
	poo.run_all()
