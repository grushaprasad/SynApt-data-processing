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

def get_disambig_region(verbs, words):
	indices = []
	prev = words[0]
	verb_count = 0
	pos = 0
	for word in words:
		if not prev == 'who' and word == 'were' and word in verbs: verb_count+=1
		if verb_count >= 2: pos+=1
		indices.append(pos)
		prev = word

	return indices
		




num = 0
with open(data_file, "r") as file:
	for line in file:
		#print line
		if not line[0] == '#':
			#print line
			# new = line.replace('\n', '')
			# new = new.replace('/', '')

			num+=1
			print num
			results = json.loads(line.replace('\n', ''))
			#results = json.loads(new)
			#print (len(results), type(results))
			data.append(results)
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
	print (sent_type, rt, word,resp)
	if item[0][1] == 'Question': print

# print list_number
# print participant

#print len(data[0][3])


words = ['An', 'impatient', 'shopper', 'shoved', 'blah', 'had', 'blah','blah' ]
#print get_disambig_region(verbs, words)

"""
To do: 
	- Mark pos in sent by figuring out when the disambiguating regions starts
	- 


"""

