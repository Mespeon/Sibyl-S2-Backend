def preparePayload():
	descriptors = [
	"A 16-year-old, second-year high school student and founder of µ's. She is always smiling, and her redeeming feature is her energy. She acts on impulse and always runs head-first into things once she's made up her mind. Any and all problems are overcome with her inherent optimism, making her the engine and driving force behind µ's.",
	"A 16-year-old, second-year high school student and Honoka's closest friend. They've been together since kindergarten. In contrast to Honoka, she has a kind and gentle personality, focuses on her studies, and is a model student. Although she's so gentle, she's also confident and reliable.",
	"A 16-year-old, second-year high school student and the childhood friend of Honoka and Kotori. Raised in a family that runs a school of traditional Japanese dance, she is a refined girl with perfect manners and has a dignified air around her. She has also practiced archery ever since she was little. She is strict with herself and with others and hates misconduct and laziness.",
	"A 15-year-old, first-year high school student. She's a quiet girl who doesn't stand out much in class and loves white rice. She lacks self-esteem and is quick to give up on almost anything she does. Admiring µ's, she joins the group along with Rin, her closest friend and the person she's always together with, and Maki.",
	"A 15-year-old, first-year high school student and the daughter of a wealthy family—her parents run a large hospital. Her singing is top-notch and she can also play the piano. Haughty and proud, she doesn't reveal her true emotions often. Her courageous nature allows her to argue with older students, but there is also a side to her which desires company.",
	"A 15-year-old, first-year high school student and an energetic girl who's fond of sports. She would rather move her body than worry about things. She ends up participating in everything just because they sound interesting. Most likely due to her involvement in sports, she is very helpful and often looks after her childhood friend, Hanayo. Her responses are always full of energy and she puts her all into practices.",
	"A 17-year-old, third-year high school student and a true idol otaku. As an upperclassman who's trying her hardest around the clock to become an idol, she frequently comes into contact with Honoka and the others while acting like a big shot. However, it turns out that she often makes mistakes and is unexpectedly clumsy. Her favorite saying is 'Nico Nico Smile'.",
	"A 17-year-old, third-year high school student and the student council president. She is one-quarter Russian. With a sharp mind and superb athletic abilities, she does everything thrown at her flawlessly. Popular throughout the school and having a strong sense of responsibility, she performs her duties as the student council president well.",
	"A 17-year-old, third-year high school student and the student council vice-president. Her relatively carefree personality is the complete opposite of Eli's, and she speaks with a peculiar mix of a Kansai accent and regular Japanese. She makes a good team with the cool Eli. She has a big heart and is the oldest of all the members. While she appears to be indifferent to most things, she is also quite the schemer.",
	"The second-year student at Uranohoshi Girls' High School who launched Aqours. The youngest of three sisters, she comes from a family that runs a traditional Japanese inn and is proud of their open-air, ocean-view bath. She's sociable and hates giving up. Her positive, pushy attitude gradually affects everyone around her.",
	"A second-year from Akihabara who transferred into Chika's class. An average girl with a reserved personality who would rather stay indoors than go out. While she seems mature and collected, she is actually quite careless, frequently jumping to conclusions and making mistakes.",
	"A second-year student and Chika's classmate. Good enough at the high dive to qualify for the national team. A sporty type whose hobby is weight training, she tends to take action without thinking matters over first. Her father captains a ferry, and her dream is to have his job someday.",
	"A first-year student who's almost always with her good friend Hanamaru. She is cowardly and tends to cry a lot, but she still has a tough interior, forged by her role as the daughter of a rich, well-known family. She has always looked up to idols and needlework is the only thing she's really great at.",
	"A first-year student who likes the \"little devil\" look and proclaims to be \"Fallen Angel Jeanne\". Born in the urban side of Numazu city, she's bright, fearless, smart, and thoughtful. However, she has extremely bad luck, running into all kinds of unforeseen trouble wherever she goes.",
	"A first-year student and the daughter of a family that has run a nearby temple for several generations. An avid reader, she has a deep fondness for Japanese literature. She's also a gifted singer, earning her a spot in a choir. She is gentle and cares for those around her, but is prone to running around in circles.",
	"A third-year student at Uranohoshi Girls' High School. She lives with her grandfather, who runs a diving shop on a nearby island. A mature but laid-back person, she rarely sweats the details and usually maintains a calm, cool demeanor.",
	"A third-year student. Her mother is Japanese, while her father is Italian-American and manages a hotel chain. She has a cheerful personality, she often acts independently. She always keeps her chin up when faced with hardship and ready to try her hand at anything.",
	"A third-year student and president of the student council. Hails from an old fishing family whose name is well-known around the area. Prideful and a perfectionist, she can't sit still when things are done sloppily or incorrectly."
	]

	# muse = [
	# {'name': "Kosaka Honoka", 'description': descriptors[0], 'cardPhoto': cardPhotos[0], 'avatar': avatars[0], 'voice': voices[0]},
	# {'name': "Minami Kotori", 'description': descriptors[1], 'cardPhoto': cardPhotos[1], 'avatar': avatars[1], 'voice': voices[1]},
	# {'name': "Sonoda Umi", 'description': descriptors[2], 'cardPhoto': cardPhotos[2], 'avatar': avatars[2], 'voice': voices[2]},
	# {'name': "Koizumi Hanayo", 'description': descriptors[3], 'cardPhoto': cardPhotos[3], 'avatar': avatars[], 'voice': voices[3]},
	# {'name': "Nishikino Maki", 'description': descriptors[4], 'cardPhoto': cardPhotos[4], 'avatar': avatars[4], 'voice': voices[4]},
	# {'name': "Hoshizora Rin", 'description': descriptors[5], 'cardPhoto': cardPhotos[5], 'avatar': avatars[5], 'voice': voices[5]},
	# {'name': "Yazawa Nico", 'description': descriptors[6], 'cardPhoto': cardPhotos[6], 'avatar': avatars[6], 'voice': voices[6]},
	# {'name': "Ayase Eli", 'description': descriptors[7], 'cardPhoto': cardPhotos[7], 'avatar': avatars[7], 'voice': voices[7]},
	# {'name': "Tojo Nozomi", 'description': descriptors[8], 'cardPhoto': cardPhotos[8], 'avatar': avatars[8], 'voice': voices[8]}
	# ]
	#
	# #Aqours sample payload
	# aqours = [
	# {'name': "Takami Chika", 'description': descriptors[9], 'cardPhoto': cardPhotos[9], 'avatar': avatars[9], 'voice': voices[9]},
	# {'name': "Riko Sakurauchi", 'description': descriptors[10], 'cardPhoto': cardPhotos[10], 'avatar': avatars[10], 'voice': voices[10]},
	# {'name': "You Watanabe", 'description': descriptors[11], 'cardPhoto': cardPhotos[11], 'avatar': avatars[11], 'voice': voices[11]},
	# {'name': "Ruby Kurosawa", 'description': descriptors[12], 'cardPhoto': cardPhotos[12], 'avatar': avatars[12], 'voice': voices[12]},
	# {'name': "Yoshiko Tsushima", 'description': descriptors[13], 'cardPhoto': cardPhotos[13], 'avatar': avatars[13], 'voice': voices[13]},
	# {'name': "Hanamaru Kunikida", 'description': descriptors[14], 'cardPhoto': cardPhotos[14], 'avatar': avatars[14], 'voice': voices[14]},
	# {'name': "Kanan Matsura", 'description': descriptors[15], 'cardPhoto': cardPhotos[15], 'avatar': avatars[15], 'voice': voices[15]},
	# {'name': "Mari Ohara", 'description': descriptors[16], 'cardPhoto': cardPhotos[16], 'avatar': avatars[16], 'voice': voices[16]},
	# {'name': "Kurosawa Dia", 'description': descriptors[17], 'cardPhoto': cardPhotos[17], 'avatar': avatars[17], 'voice': voices[17]}
	# ]

	cardPhotos = [
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	''
	]

	# muse = [
	# {'name': "Kosaka Honoka", 'description': descriptors[0], 'cardPhoto': cardPhotos[0], 'avatar': avatars[0], 'voice': voices[0]},
	# {'name': "Minami Kotori", 'description': descriptors[1], 'cardPhoto': cardPhotos[1], 'avatar': avatars[1], 'voice': voices[1]},
	# {'name': "Sonoda Umi", 'description': descriptors[2], 'cardPhoto': cardPhotos[2], 'avatar': avatars[2], 'voice': voices[2]},
	# {'name': "Koizumi Hanayo", 'description': descriptors[3], 'cardPhoto': cardPhotos[3], 'avatar': avatars[], 'voice': voices[3]},
	# {'name': "Nishikino Maki", 'description': descriptors[4], 'cardPhoto': cardPhotos[4], 'avatar': avatars[4], 'voice': voices[4]},
	# {'name': "Hoshizora Rin", 'description': descriptors[5], 'cardPhoto': cardPhotos[5], 'avatar': avatars[5], 'voice': voices[5]},
	# {'name': "Yazawa Nico", 'description': descriptors[6], 'cardPhoto': cardPhotos[6], 'avatar': avatars[6], 'voice': voices[6]},
	# {'name': "Ayase Eli", 'description': descriptors[7], 'cardPhoto': cardPhotos[7], 'avatar': avatars[7], 'voice': voices[7]},
	# {'name': "Tojo Nozomi", 'description': descriptors[8], 'cardPhoto': cardPhotos[8], 'avatar': avatars[8], 'voice': voices[8]}
	# ]
	#
	# #Aqours sample payload
	# aqours = [
	# {'name': "Takami Chika", 'description': descriptors[9], 'cardPhoto': cardPhotos[9], 'avatar': avatars[9], 'voice': voices[9]},
	# {'name': "Riko Sakurauchi", 'description': descriptors[10], 'cardPhoto': cardPhotos[10], 'avatar': avatars[10], 'voice': voices[10]},
	# {'name': "You Watanabe", 'description': descriptors[11], 'cardPhoto': cardPhotos[11], 'avatar': avatars[11], 'voice': voices[11]},
	# {'name': "Ruby Kurosawa", 'description': descriptors[12], 'cardPhoto': cardPhotos[12], 'avatar': avatars[12], 'voice': voices[12]},
	# {'name': "Yoshiko Tsushima", 'description': descriptors[13], 'cardPhoto': cardPhotos[13], 'avatar': avatars[13], 'voice': voices[13]},
	# {'name': "Hanamaru Kunikida", 'description': descriptors[14], 'cardPhoto': cardPhotos[14], 'avatar': avatars[14], 'voice': voices[14]},
	# {'name': "Kanan Matsura", 'description': descriptors[15], 'cardPhoto': cardPhotos[15], 'avatar': avatars[15], 'voice': voices[15]},
	# {'name': "Mari Ohara", 'description': descriptors[16], 'cardPhoto': cardPhotos[16], 'avatar': avatars[16], 'voice': voices[16]},
	# {'name': "Kurosawa Dia", 'description': descriptors[17], 'cardPhoto': cardPhotos[17], 'avatar': avatars[17], 'voice': voices[17]}
	# ]

	avatars = [
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	''
	]

	voices = [
	'Nitta Emi',
	'Uchida Aya',
	'Mimori Suzuko',
	'Kubo Yurika',
	'Pile',
	'Iida Riho',
	'Tokui Sora',
	'Nanjou Yoshino',
	'Kusuda Aina',
	'Inami Anju',
	'Aida Rikako',
	'Saitou Shuka',
	'Furihata Ai',
	'Kobayashi Aika',
	'Takatsuki Kanako',
	'Suwa Nanaka',
	'Suzuki Aina',
	'Komiya Arisa'
	]

	#Muse sample payload
	muse = [
	{'name': "Kosaka Honoka", 'description': descriptors[0], 'cardPhoto': cardPhotos[0], 'avatar': avatars[0], 'voice': voices[0]},
	{'name': "Minami Kotori", 'description': descriptors[1], 'cardPhoto': cardPhotos[1], 'avatar': avatars[1], 'voice': voices[1]},
	{'name': "Sonoda Umi", 'description': descriptors[2], 'cardPhoto': cardPhotos[2], 'avatar': avatars[2], 'voice': voices[2]},
	{'name': "Koizumi Hanayo", 'description': descriptors[3], 'cardPhoto': cardPhotos[3], 'avatar': avatars[], 'voice': voices[3]},
	{'name': "Nishikino Maki", 'description': descriptors[4], 'cardPhoto': cardPhotos[4], 'avatar': avatars[4], 'voice': voices[4]},
	{'name': "Hoshizora Rin", 'description': descriptors[5], 'cardPhoto': cardPhotos[5], 'avatar': avatars[5], 'voice': voices[5]},
	{'name': "Yazawa Nico", 'description': descriptors[6], 'cardPhoto': cardPhotos[6], 'avatar': avatars[6], 'voice': voices[6]},
	{'name': "Ayase Eli", 'description': descriptors[7], 'cardPhoto': cardPhotos[7], 'avatar': avatars[7], 'voice': voices[7]},
	{'name': "Toujou Nozomi", 'description': descriptors[8], 'cardPhoto': cardPhotos[8], 'avatar': avatars[8], 'voice': voices[8]}
	]

	#Aqours sample payload
	aqours = [
	{'name': "Takami Chika", 'description': descriptors[9], 'cardPhoto': cardPhotos[9], 'avatar': avatars[9], 'voice': voices[9]},
	{'name': "Riko Sakurauchi", 'description': descriptors[10], 'cardPhoto': cardPhotos[10], 'avatar': avatars[10], 'voice': voices[10]},
	{'name': "You Watanabe", 'description': descriptors[11], 'cardPhoto': cardPhotos[11], 'avatar': avatars[11], 'voice': voices[11]},
	{'name': "Ruby Kurosawa", 'description': descriptors[12], 'cardPhoto': cardPhotos[12], 'avatar': avatars[12], 'voice': voices[12]},
	{'name': "Yoshiko Tsushima", 'description': descriptors[13], 'cardPhoto': cardPhotos[13], 'avatar': avatars[13], 'voice': voices[13]},
	{'name': "Hanamaru Kunikida", 'description': descriptors[14], 'cardPhoto': cardPhotos[14], 'avatar': avatars[14], 'voice': voices[14]},
	{'name': "Kanan Matsura", 'description': descriptors[15], 'cardPhoto': cardPhotos[15], 'avatar': avatars[15], 'voice': voices[15]},
	{'name': "Mari Ohara", 'description': descriptors[16], 'cardPhoto': cardPhotos[16], 'avatar': avatars[16], 'voice': voices[16]},
	{'name': "Kurosawa Dia", 'description': descriptors[17], 'cardPhoto': cardPhotos[17], 'avatar': avatars[17], 'voice': voices[17]}
	]
	payload = {'Muse': muse, 'Aqours': aqours}
	return payload
