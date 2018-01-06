import json
data_file = '../FineJaeger16 Replication/pilot_raw_results.txt'


data = []
verbs = ['dropped', 'hit', 'phoned', 'were', 'declared', 'worked', 'moved', 'got',
		'rushed', 'offered', 'told', 'had', 'signalled', 'pecked','advised', 'decided',
		'dangled', 'landed','licked', 'ran','washed', 'set', 'warned', 'coached', 'became',
		'recognized', 'committed','helped', 'would','heard', 'served', 'went','guaranteed','knew',
		'denied', 'caught','pushed', 'asked','conducted','stopped', 'rested','wound','called','returned',
		'fed','sat', 'fell','cooked', 'sent', 'hurried',"hadn't", 'taught', 'scrubbed','splashed', 'assured',
		'burnt','rinsed','watched','played','unloaded','found', 'bathed', 'read','remembered','quickly','begged',
		'answered','cheated', 'left', 'shoved', 'complained']

bad_participants = [
 			('5a26b1338766a400019007a2', 5),
 			('5a26b1338766a400019007a2', 7),
 			('5a26b1338766a400019007a2', 8),
 			('5a26b1338766a400019007a2', 9),
 			('5a26b1338766a400019007a2', 10),
 			('5a270017e2d20d00013207ff', 14),
 			('Tal Linzen', 6),
 			('das', 6),
 			]

#Note: Three things to note
	# 1. It has 'were' as a disambiguating verb. But 'were' is also used in 'who were'. So need to have some form of conditional to avoid this
	# 2. It uses 'quickly' (the adverb) instead of the verb because the adverb starts the VP?
	# 3. Does not take into consideration sentences disambiguated at PP. Still uses second verb as beginning of disambiguating region

def split_data(participant):
	clean_data = []
	lextale_data = []
	for item in participant[3]:
		sent_type = item[3][1]
		if sent_type in ['filler', 'ambiguous', 'unambiguous']:
			clean_data.append(item)
		if sent_type == 'LexTale':
			lextale_data.append(item)
	return (clean_data,lextale_data)

def get_disambig_region(verbs, words):
	indices = []
	prev = words[0]
	verb_count = 0
	pos = 0
	for word in words:
		#if (prev != 'who') and word == 'were' and word in verbs: verb_count+=1
		if word in verbs and not (prev == 'who' and word == 'were'): verb_count+=1
		if verb_count >= 2: pos+=1
		indices.append(pos)
		prev = word

	return indices
		
def process_participant(participant_data, verbs):
	sent_type = ''
	i = 0
	# for item in participant_data:
	# 	sent_type = item[3][1]
	all_words = []
	all_sentences = []
	all_rt = []
	all_resps = []
	all_indices = []
	all_sent_types = []

	while i < len(participant_data):
		sent_just_ended = False
		words = []
		rt = []
		sentence = []
		resps = []
		sent_type = []
		sent = ''  # having this because every row (in long form) needs to have the sentence it is associated with. This information is not noted for the question. SO keeping track

		while not sent_just_ended:
			curr = participant_data[i]
			sent_type.append(curr[3][1])
			
			if not curr[0][1] == 'Question':
				words.append(curr[6][1])
				rt.append(curr[7][1])
				sent = curr[9][1]
				sentence.append(sent)
				resps.append('na')
			else:
				words.append(curr[5][1])
				rt.append(curr[8][1])
				sentence.append(sent)
				if curr[7][1]==1: resps.append('correct')
				elif curr[7][1]==0: resps.append('wrong')
				else: print 'Found a response that is not 1 or 0'
				sent_just_ended = True
			i+=1

		disambig_region_indices = get_disambig_region(verbs, words)
			
		all_words.extend(words)
		all_sentences.extend(sentence)
		all_rt.extend(rt)
		all_resps.extend(resps)
		all_indices.extend(disambig_region_indices)
		all_sent_types.extend(sent_type)

	return(all_words, all_sentences, all_rt, all_indices, all_resps, all_sent_types)

def process_participant_lextale(lextale_data):
	words = []
	resps = []
	for item in lextale_data:
		words.append(item[5][1])
		if item[7][1]==1: resps.append('correct')
		elif item[7][1]==0: resps.append('wrong')
		else: print 'Found a response that is not 1 or 0'

	return(words,resps)



def process_all_data(data, bad_participants, spr_filename, lextale_filename,verbs):
	all_words = []
	all_sentences = []
	all_rt = []
	all_indices = []
	all_resps = []
	all_sent_types = []
	participant_ids = []
	participant_lists = []
	all_lextale_words = []
	all_lextale_resps = []
	all_lextale_participant_ids =[]

	for participant in data:
		participant_id = participant[3][0][6][1]
		participant_list = participant[1]
		#print type(participant_list)
		#print type(participant_id)

		if not (str(participant_id),participant_list) in bad_participants:
			clean_data,lextale_data = split_data(participant)
			words, sentences, rt, indices, resps, sent_types = process_participant(clean_data, verbs)
			lextale_words, lextale_resps = process_participant_lextale(lextale_data)
			#print lextale_data
			if not all(len(lst) == len(words) for lst in [words, sentences, rt, indices, resps]):
				print 'for participant %s, not all lists are equal' %(participant_id)
				print 'Overall not all lists are equal'
				print 'words: %s' %(len(words)) 
				print 'sentences: %s' %(len(sentences))
				print 'rt: %s' %(len(rt))
				print 'indices: %s' %(len(indices))
				print 'resps: %s' %(len(resps))
				print

			all_words.extend(words)
			all_sentences.extend(sentences)
			all_rt.extend(rt)
			all_indices.extend(indices)
			all_resps.extend(resps)
			all_sent_types.extend(sent_types)
			participant_ids.extend([participant_id]*len(words))
			participant_lists.extend([participant_list]*len(words))

			all_lextale_words.extend(lextale_words)
			all_lextale_resps.extend(lextale_resps)
			all_lextale_participant_ids.extend([participant_id]*len(lextale_words))


	if not all(len(lst) == len(all_words) for lst in [all_words, all_sentences, all_rt, all_indices, all_resps, participant_ids, participant_lists]):
				print 'Overall not all lists are equal'
				print 'words: %s' %(len(all_words)) 
				print 'sentences: %s' %(len(all_sentences))
				print 'rt: %s' %(len(all_rt))
				print 'indices: %s' %(len(all_indices))
				print 'resps: %s' %(len(all_resps))
				print 'participant_ids: %s' %(len(participant_ids))
				print 'participant_lists: %s' %(len(participant_lists))
				print


	with open(spr_filename, "wb") as f:
		#writer = csv.writer(f)
		for i in range(len(all_words)):
			#print i
			row = '%s,%s,%s,%s,%s,%s,%s, %s\n' %(all_sentences[i], all_words[i], all_sent_types[i], all_rt[i], all_indices[i], all_resps[i], participant_ids[i], participant_lists[i])
			f.write(row)
	f.close()

	with open(lextale_filename, "wb") as g:
		#writer = csv.writer(f)
		for i in range(len(all_lextale_words)):
			#print i
			row = '%s,%s,%s\n' %(all_lextale_words[i], all_lextale_resps[i], all_lextale_participant_ids[i])
			g.write(row)
	g.close()



with open(data_file, "r") as file:
	for line in file:
		if not line[0] == '#':
			results = json.loads(line.replace('\n', ''))
			data.append(results)

print len(data)

process_all_data(data, bad_participants, 'test.csv', 'lextale_test.csv', verbs)










"""


rt = ''
sent_type = ''
sent = ''
word = ''
resp = ''
pos_in_sent = ''  #first word in disambiguating region is 1 and so on

list_number = data[0][1]   #the list of the first participant rn
participant = data[0][3][0][6][1]  #participant id of the first participant rn

for item in data[0][3]:
	sent_type = item[3][1]

	if sent_type in ['filler', 'ambiguous', 'unambiguous']:
		#rt = item[9][1]
		#sent = item[9][1]
		if item[0][1] == 'Question':
			word = item[5][1]
			rt = item[8][1]
			#resp = item[7]
			if item[7][1]==1: resp = 'correct'   
			elif item[7][1]==0: resp = 'wrong'
			#sent = item[9]
		else: 
			word = item[6][1]
			rt = item[7][1]
			sent = item[9][1]
			resp = 'na'
	# for thing in item:
	# 	print thing
	# if item[0][1] == 'Question': print '_____________________________________________________________'
	#print
		#sent_type = thing[3]
		#print sent_type
	#print (sent_type, rt, word,resp)
	#if item[0][1] == 'Question': print

# print list_number
# print participant

#print len(data[0][3])


words = ['An', 'impatient', 'shopper','shoved', 'blah', 'were', 'had', 'blah','blah' ]
print get_disambig_region(verbs, words)

"""
"""
To do: 
	- Mark pos in sent by figuring out when the disambiguating regions starts
	- 


"""

