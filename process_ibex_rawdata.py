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

#Note: Three things to note
	# 1. It has 'were' as a disambiguating verb. But 'were' is also used in 'who were'. So need to have some form of conditional to avoid this
	# 2. It uses 'quickly' (the adverb) instead of the verb because the adverb starts the VP?
	# 3. Does not take into consideration sentences disambiguated at PP. Still uses second verb as beginning of disambiguating region

def remove_unwanted(participant):
	clean_data = []
	for item in participant[3]:
		sent_type = item[3][1]
		if sent_type in ['filler', 'ambiguous', 'unambiguous']:
			clean_data.append(item)
	return clean_data

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

	while i < len(participant_data):
		sent_just_ended = False
		words = []
		rt = []
		sentence = []
		resps = []
		sent_type = []

		while not sent_just_ended:
			curr = participant_data[i]
			sent_type.append(curr[3][1])
			sent = ''  # having this because every row (in long form) needs to have the sentence it is associated with. This information is not noted for the question. SO keeping track
			
			if not curr[0][1] == 'Question':
				words.append(curr[6][1])
				rt.append(curr[7][1])
				sent = curr[9][1]
				sentence.append(sent)
				resps.append('na')
			else:
				words.append(curr[5][1])
				rt.append(curr[8][1])
				if curr[7][1]==1: resps.append('correct')
				elif curr[7][1]==1: resps.append('wrong')
				else: print 'Found a response that is not 1 or 0'
				sent_just_ended = True
			i+=1

		disambig_region_indices = get_disambig_region(verbs, words)
			
		all_words.extend(words)
		all_sentences.extend(sentence)
		all_rt.extend(rt)
		all_resps.extend(resps)
		all_indices.extend(disambig_region_indices)

	return(all_words, all_sentences, all_rt, all_indices, all_resps)

			
def process_all_data(data, bad_participants, filename, verbs):
	all_words = []
	all_sentences = []
	all_rt = []
	all_indices = []
	all_resps = []
	participant_ids = []
	participant_lists = []

	for participant in data:
		participant_id = participant[3][0][6][1]
		participant_list = participant[1]

		if not participant_id in bad_participants:
			clean_data = remove_unwanted(participant)
			words, sentences, rt, indices, resps = process_participant(clean_data, verbs)
			
			if not all(len(lst) == len(words) for lst in [words, sentences, rt, indices, resps]):
				print 'for participant %s, not all lists are equal' %(participant_id)

			all_words.extend(words)
			all_sentences.extend(sentences)
			all_rt.extend(rt)
			all_indices.extend(indices)
			all_resps.extend(resps)
			participant_ids.extend([participant_id]*len(words))
			participant_lists.extend([participant_list]*len(words))


	if not all(len(lst) == len(all_words) for lst in [all_words, all_sentences, all_rt, all_indices, all_resps, participant_ids, participant_lists]):
				print 'Overall not all lists are equal' 


	with open(filename, "wb") as f:
		#writer = csv.writer(f)
		for i in range(len(all_words)):
			print i
			row = '%s,%s,%s,%s,%s,%s,%s' %(all_words[i], all_sentences[i], all_rt[i], all_indices[i], all_resps[i], participant_ids[i], participant_lists[i])
			f.write(row)


with open(data_file, "r") as file:
	for line in file:
		if not line[0] == '#':
			results = json.loads(line.replace('\n', ''))
			data.append(results)

process_all_data(data, [], 'test.csv', verbs)










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

