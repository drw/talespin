import os, sys, re, fire

import random


first_lines = ["""Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'""",
"""All children, except one, grow up.""",
"""A BAT who fell upon the ground and was caught by a Weasel pleaded to be spared his life.""",
"""A FATHER had a family of sons who were perpetually quarreling among themselves.""",
"""A HARE one day ridiculed the short feet and slow pace of the Tortoise, who replied, laughing: "Though you be swift as the wind, I will beat you in a race." """,
"""One January day, thirty years ago, the little town of Hanover, anchored on a windy Nebraska tableland, was trying not to be blown away. """,
"""A throng of bearded men, in sad-coloured garments and grey steeple-crowned hats, inter-mixed with women, some wearing hoods, and others bareheaded, was assembled in front of a wooden edifice, the door of which was heavily timbered with oak, and studded with iron spikes.""",
"""The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. """,
"""No one would have believed in the last years of the nineteenth century that this world was being watched keenly and closely by intelligences greater than man's and yet as mortal as his own.""",
"""MARLEY was dead: to begin with. There is no doubt whatever about that.""",
"""In the Country of the Gillikins, which is at the North of the Land of Oz, lived a youth called Tip.""",
"""Some years ago -- never mind how long precisely -- having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. """,
"""In the drowsy heat of the summer afternoon the Red House was taking its siesta. """,

]
first_verses = ["""     "Just the place for a Snark!" the Bellman cried,
          As he landed his crew with care;
     Supporting each man on the top of the tide
          By a finger entwined in his hair""",
]
verses = ["""     The loss of his clothes hardly mattered, because
          He had seven coats on when he came,
     With three pairs of boots--but the worst of it was,
          He had wholly forgotten his name.""" # plot twist: Amnesia!
]
wonderland_lines = ["""'Treacle,' said a sleepy voice behind her.""",
"""So she set to work, and very soon finished off the cake.""",

]
random_lines = ["""He had his position in the city to consider.""",
"""Oh, surely she must have been dreaming.""",
"""'That is all right,' said the Psychologist.""",
"""The Time Traveller smiled.""",
"""'Why not?' said the Time Traveller.""",
"""'To discover a society,' said I, 'erected on a strictly communistic basis.'""",
"""The Psychologist recovered from his stupor, and suddenly looked under the table. """,
"""At that the Time Traveller laughed cheerfully.""",
"""'"Communism," said I to myself.""",
"""The planet Mars, I scarcely need remind the reader, revolves about the sun at a mean distance of 140,000,000 miles, and the light and heat it receives from the sun is barely half of that received by this world.""",
"""All that time the Martians must have been getting ready.""",
"""A boy came running towards me.""",
"""A sudden chill came over me.""",
"""I saw astonishment giving place to horror on the faces of the people about me.""",
"""Two large dark-coloured eyes were regarding me steadfastly.""",
"""I was a battleground of fear and curiosity.""",
"""There were shrieks and shouts, and suddenly a mounted policeman came galloping through the confusion with his hands clasped over his head, screaming.""",
"""Perhaps I am a man of exceptional moods.""",
"""At times I suffer from the strangest sense of detachment from myself and the world about me; I seem to watch it all from the outside, from somewhere inconceivably remote, out of time, out of space, out of the stress and tragedy of it all.""",
"""I saw my neighbour gardening, chatted with him for a time, and then strolled in to breakfast.""",
"""And this Thing I saw!  How can I describe it?""",
"""That night I had come to the fatal cross-roads. """,
"""The Guardian of the Gate at once came out and looked at them curiously, as if a circus had come to town.""",
""""In an emergency," he announced, "it is always a good thing to pause and reflect. Please excuse me while I pause and reflect." """,
"""Very carefully he began sprinkling the Thing with the precious powder.""",
""""That is because you have no brains" answered the girl.""",
""""Who are you and where are you going?" asked the Stork.""",
"""They came from all directions, and there were thousands of them: big mice and little mice and middle-sized mice; and each one brought a piece of string in his mouth.""",
"""The road was smooth and well paved, now, and the country about was beautiful, so that the travelers rejoiced in leaving the forest far behind, and with it the many dangers they had met in its gloomy shades.""",
"""As they walked on, the green glow became brighter and brighter, and it seemed that at last they were nearing the end of their travels.""",
""""Where did you get the mark upon your forehead?" continued the voice.""",
"""After this she stood upon both feet and cried in a loud voice:

"Ziz-zy, zuz-zy, zik!"
""",
"""The sky was darkened, and a low rumbling sound was heard in the air.""",
"""But the wicked creature was very cunning, and she finally thought of a trick that would give her what she wanted. """,

]

ribald_lines = [("The Time Machine", "'What a treat it is to stick a fork into meat again!'"),
        ("The War of the Worlds", "As it bulged up and caught the light, it glistened like wet leather.")
        ]

concluding_lines = ["""Our last glimpse of her shows her at the window, watching them receding into the sky until they were as small as stars.""",
"Whatever we had missed, we possessed together the precious, the incommunicable past.",
"'Excellently observed,' answered Candide; 'but we must cultivate our garden.'",
"""It is a far, far better thing that I do, than I have ever done; it is a far, far better rest that I go to than I have ever known.""",
"""Later on he will understand how some men so loved her, that they did dare much for her sake.""",
"""He was soon borne away by the waves and lost in darkness and distance.""",
"""He now has more patients than the devil himself could handle; the authorities treat him with deference and public opinion supports him. He has just been awarded the Cross of the Legion of Honor.""",
]

def random_story():
    first_line = random.choice(first_lines)
    used = [first_line]
    print(first_line) 

    other_lines = verses + wonderland_lines + random_lines

    while random.random() > 0.2 or len(used) < 2:
        next_line = random.choice(other_lines)
        if next_line not in used:
            print(next_line)
            used.append(next_line)

    conclusion = random.choice(concluding_lines)
    print(conclusion)
    used.append(conclusion)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        random_story()
    else:
        fire.Fire()
