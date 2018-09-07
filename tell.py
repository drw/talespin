import os, sys, re, fire, textwrap

import random
from pprint import pprint

first_lines = [ ("The Time Machine","""The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. """),
("The War of the Worlds","""No one would have believed in the last years of the nineteenth century that this world was being watched keenly and closely by intelligences greater than man's and yet as mortal as his own."""),
("Moby Dick", """Some years ago -- never mind how long precisely -- having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. """),
("The Red House Mystery by A. A. Milne", """In the drowsy heat of the summer afternoon the Red House was taking its siesta. """),
("A Princess of Mars","""I am a very old man; how old I do not know.  Possibly I am a hundred, possibly more; but I cannot tell because I have never aged as other men, nor do I remember any childhood.  So far as I can recollect I have always been a man, a man of about thirty. """),
("A Connecticut Yankee in King Arthur's Court","""It was in Warwick Castle that I came across the curious stranger whom I am going to talk about.  He attracted me by three things: his candid simplicity, his marvelous familiarity with ancient armor, and the restfulness of his company--for he did all the talking."""),
("The Metamorphosis", """As Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his bed into a gigantic insect."""),
("Alice's Adventures in Wonderland", """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'"""),
("Peter Pan", """All children, except one, grow up."""),
("Aesop's Fables", """A BAT who fell upon the ground and was caught by a Weasel pleaded to be spared his life."""),
("Aesop's Fables", """A FATHER had a family of sons who were perpetually quarreling among themselves."""),
("Aesop's Fables", """A HARE one day ridiculed the short feet and slow pace of the Tortoise, who replied, laughing: "Though you be swift as the wind, I will beat you in a race." """),
("O Pioneers", """One January day, thirty years ago, the little town of Hanover, anchored on a windy Nebraska tableland, was trying not to be blown away. """),
("The Scarlet Letter", """A throng of bearded men, in sad-coloured garments and grey steeple-crowned hats, inter-mixed with women, some wearing hoods, and others bareheaded, was assembled in front of a wooden edifice, the door of which was heavily timbered with oak, and studded with iron spikes."""),
("The Marvelous Land of Oz", """In the Country of the Gillikins, which is at the North of the Land of Oz, lived a youth called Tip."""),
]
first_verses = [("The Hunting of the Snark", """     "Just the place for a Snark!" the Bellman cried,
          As he landed his crew with care;
     Supporting each man on the top of the tide
          By a finger entwined in his hair"""),
]
verses = [("The Hunting of the Snark", """     The loss of his clothes hardly mattered, because
          He had seven coats on when he came,
     With three pairs of boots--but the worst of it was,
          He had wholly forgotten his name.""") # plot twist: Amnesia!
]
wonderland_lines = [("Alice's Adventures in Wonderland", """'Treacle,' said a sleepy voice behind her."""),
("Alice's Adventures in Wonderland", """So she set to work, and very soon finished off the cake."""),

]
random_lines = [("Peter Pan","""He had his position in the city to consider."""),
("Peter Pan","""Oh, surely she must have been dreaming."""),
("The Time Machine", """'That is all right,' said the Psychologist."""),
("The Time Machine", """The Time Traveller smiled."""),
("The Time Machine", """'Why not?' said the Time Traveller."""),
("The Time Machine", """'To discover a society,' said I, 'erected on a strictly communistic basis.'"""),
("The Time Machine", """The Psychologist recovered from his stupor, and suddenly looked under the table. """),
("The Time Machine", """At that the Time Traveller laughed cheerfully."""),
("The Time Machine", """'"Communism," said I to myself."""),
("The War of the Worlds","""The planet Mars, I scarcely need remind the reader, revolves about the sun at a mean distance of 140,000,000 miles, and the light and heat it receives from the sun is barely half of that received by this world."""),
("The War of the Worlds","""All that time the Martians must have been getting ready."""),
("The War of the Worlds","""A boy came running towards me."""),
("The War of the Worlds","""A sudden chill came over me."""),
("The War of the Worlds","""I saw astonishment giving place to horror on the faces of the people about me."""),
("The War of the Worlds","""Two large dark-coloured eyes were regarding me steadfastly."""),
("The War of the Worlds","""I was a battleground of fear and curiosity."""),
("The War of the Worlds","""There were shrieks and shouts, and suddenly a mounted policeman came galloping through the confusion with his hands clasped over his head, screaming."""),
("The War of the Worlds","""Perhaps I am a man of exceptional moods."""),
("The War of the Worlds","""At times I suffer from the strangest sense of detachment from myself and the world about me; I seem to watch it all from the outside, from somewhere inconceivably remote, out of time, out of space, out of the stress and tragedy of it all."""),
("The War of the Worlds","""I saw my neighbour gardening, chatted with him for a time, and then strolled in to breakfast."""),
("The War of the Worlds","""And this Thing I saw!  How can I describe it?"""),
("The War of the Worlds","""That night I had come to the fatal cross-roads. """),
("The Marvelous Land of Oz","""The Guardian of the Gate at once came out and looked at them curiously, as if a circus had come to town."""),
("The Marvelous Land of Oz",""""In an emergency," he announced, "it is always a good thing to pause and reflect. Please excuse me while I pause and reflect." """),
("The Marvelous Land of Oz","""Very carefully he began sprinkling the Thing with the precious powder."""),
("The Wizard of Oz",""""That is because you have no brains" answered the girl."""),
("The Wizard of Oz",""""Who are you and where are you going?" asked the Stork."""),
("The Wizard of Oz","""They came from all directions, and there were thousands of them: big mice and little mice and middle-sized mice; and each one brought a piece of string in his mouth."""),
("The Wizard of Oz","""The road was smooth and well paved, now, and the country about was beautiful, so that the travelers rejoiced in leaving the forest far behind, and with it the many dangers they had met in its gloomy shades."""),
("The Wizard of Oz","""As they walked on, the green glow became brighter and brighter, and it seemed that at last they were nearing the end of their travels."""),
("The Wizard of Oz",""""Where did you get the mark upon your forehead?" continued the voice."""),
("The Wizard of Oz","""After this she stood upon both feet and cried in a loud voice:

"Ziz-zy, zuz-zy, zik!"
"""),
("The Wizard of Oz","""The sky was darkened, and a low rumbling sound was heard in the air."""),
("The Wizard of Oz","""But the wicked creature was very cunning, and she finally thought of a trick that would give her what she wanted. """),
("A Connecticut Yankee in King Arthur's Court", """He caught himself nodding, now, and smiled one of those pathetic, obsolete smiles of his, and said: """),
("A Connecticut Yankee in King Arthur's Court", """The moment I got a chance I slipped aside privately and touched an ancient common looking man on the shoulder and said, in an insinuating, confidential way: """),
("A Connecticut Yankee in King Arthur's Court", """I sat down by my fire and examined my treasure. """),
("A Connecticut Yankee in King Arthur's Court", """There were people, too; brawny men, with long, coarse, uncombed hair that hung down over their faces and made them look like animals. """),
("A Christmas Carol", "A smell like an eating-house and a pastrycook's next door to each other, with a laundress's next door to that!"),
("A Christmas Carol", """Quiet and dark, beside him stood the Phantom, with its outstretched hand. """),
("A Connecticut Yankee in King Arthur's Court", """I was not the only prisoner present.  There were twenty or more."""),
("A Connecticut Yankee in King Arthur's Court", """Everybody discussed me; and did it as unconcernedly as if I had been a cabbage."""),
("A Connecticut Yankee in King Arthur's Court", """It was the only compliment I got -- if it was a compliment."""),
("A Connecticut Yankee in King Arthur's Court", """I was shoved into a dark and narrow cell in a dungeon, with some scant remnants for dinner, some moldy straw for a bed, and no end of rats for company."""),
("A Connecticut Yankee in King Arthur's Court", """It was pitiful to see a creature so terrified, so unnerved, so demoralized."""),
("A Connecticut Yankee in King Arthur's Court", """Presently this thought occurred to me: how heedless I have been!"""),
("A Connecticut Yankee in King Arthur's Court", """I worried over that heedless blunder for an hour, and called myself a great many hard names, meantime."""),
("A Connecticut Yankee in King Arthur's Court", """I was in trouble again; in the deepest kind of trouble..."""),
("A Connecticut Yankee in King Arthur's Court", """You see, it was the eclipse.  It came into my mind in the nick of time, how Columbus, or Cortez, or one of those people, played an eclipse as a saving trump once, on some savages, and I saw my chance. """),
("A Connecticut Yankee in King Arthur's Court", """I allowed silence to accumulate while I got my impressiveness together, and then said:"""),
("A Connecticut Yankee in King Arthur's Court", 
"""In the stillness and the darkness, the knowledge that I was in deadly danger took to itself deeper and deeper meaning all the time; a something which was realization crept inch by inch through my veins and turned me cold."""),  
]

dialogue = [("A Connecticut Yankee in King Arthur's Court", """"You know about transmigration of souls; do you know about transposition of epochs -- and bodies?" """),
("A Christmas Carol",""""I want nothing from you; I ask nothing of you; why cannot we be friends?" """),
("A Christmas Carol",""""Are there no prisons?" asked Scrooge."""),
("A Connecticut Yankee in King Arthur's Court", """"Camelot," said he."""),
("A Connecticut Yankee in King Arthur's Court", """"I find I can't go on; but come with me, I've got it all written out, and you can read it if you like." """),
("A Connecticut Yankee in King Arthur's Court", """"I don't seem to remember hearing of it before.  Name of the asylum, likely." """),
("A Christmas Carol",""""Your lip is trembling," said the Ghost. "And what is that upon your cheek?" """),
("A Christmas Carol",""""You have never seen the like of me before!" exclaimed the Spirit."""),
("A Christmas Carol",""""More than eighteen hundred," said the Ghost. """),
("A Connecticut Yankee in King Arthur's Court", """I knew him in Egypt three hundred years ago; I knew him in India five hundred years ago--he is always blethering around in my way, everywhere I go; he makes me tired."""),
("A Connecticut Yankee in King Arthur's Court", """"How long have I been shut up in this hole?" """),
]

metastories = [("A Connecticut Yankee in King Arthur's Court", """This was the old man's tale.  He said:"""),
]

abstractions = [("The Wizard of Oz", "The Protagonist has a happy life on a farm."),
("The Wizard of Oz", "Atmospheric circumstances take the protgaonist away from her happy life to a strange land."),
("The Wizard of Oz", "The Protagonist accidentally kills a powerful villain."),
("The Wizard of Oz", "Through a stroke of good luck, the Protagonist obtains magical footwear."),
("The Wizard of Oz", "The Protagonist begins a quest to return home."),
("The Wizard of Oz", "The Protagonist works with oddball, unlikely heroes to fulfill the quest."),
("The Wizard of Oz", "The Protagonist triumphs over evil and returns home."),
]

ribald_lines = [("The Time Machine", "'What a treat it is to stick a fork into meat again!'"),
("The War of the Worlds", "As it bulged up and caught the light, it glistened like wet leather."),
("A Connecticut Yankee in King Arthur's Court", """It was as sweet an outfit as ever I saw, what there was of it."""),
        ]

concluding_lines = [("Peter Pan","""Our last glimpse of her shows her at the window, watching them receding into the sky until they were as small as stars."""),
("My Antonia", "Whatever we had missed, we possessed together the precious, the incommunicable past."),
("Candide","'Excellently observed,' answered Candide; 'but we must cultivate our garden.'"),
("A Tale of Two Cities","""It is a far, far better thing that I do, than I have ever done; it is a far, far better rest that I go to than I have ever known."""),
("Dracula","""Later on he will understand how some men so loved her, that they did dare much for her sake."""),
("Frankenstein","""He was soon borne away by the waves and lost in darkness and distance."""),
("Madame Bovary","""He now has more patients than the devil himself could handle; the authorities treat him with deference and public opinion supports him. He has just been awarded the Cross of the Legion of Honor."""),
("A Princess of Mars", """I believe that they are waiting there for me, and something tells me that I shall soon know."""),
]

def random_story():
    first_line = random.choice(first_lines)[1]
    used = [first_line]
    print(first_line) 

    other_lines = verses + wonderland_lines + random_lines + dialogue

    while random.random() > 0.2 or len(used) < 2:
        next_line = random.choice(other_lines)[1]
        if next_line not in used:
            print(next_line)
            used.append(next_line)

    conclusion = random.choice(concluding_lines)[1]
    print(conclusion)
    used.append(conclusion)

def interactive():
    used, _ = choose_line([], random.sample(first_lines,4), 'interactive')

    other_lines = verses + wonderland_lines + random_lines + dialogue + abstractions

    while random.random() > 0.3 or len(used) < 2:
        used, chosen_tup = choose_line(used, random.sample(other_lines,5), 'interactive')
        other_lines.remove(chosen_tup)
        next_line = random.choice(other_lines)[1]

    used, _ = choose_line(used, random.sample(concluding_lines,4), 'interactive')

    print("The finished story:\n")
    print(textwrap.fill(used[0],80)+"\n")
    paragraph = ""
    for line in used[1:-1]:
        paragraph += line.strip() + " "
    print(textwrap.fill(paragraph,80)+"\n")
    print(textwrap.fill(used[-1],80)+"\n")

def i():
    interactive()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        random_story()
    else:
        fire.Fire()
