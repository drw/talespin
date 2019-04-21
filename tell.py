import os, sys, re, fire, textwrap, dataset
from collections import defaultdict
import random, statistics
from pprint import pprint
from datetime import datetime

db_file = "/Users/drw/code/talespin/lines.sqlite"
table_name = 'talespin_lines'

first_lines = [ ("The Time Machine","""The Time Traveller (for so it will be convenient to speak of him) was expounding a recondite matter to us. """),
("The War of the Worlds","""No one would have believed in the last years of the nineteenth century that this world was being watched keenly and closely by intelligences greater than man's and yet as mortal as his own."""),
("Moby Dick", """Some years ago -- never mind how long precisely -- having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. """),
("The Red House Mystery by A. A. Milne", """In the drowsy heat of the summer afternoon the Red House was taking its siesta. """),
("A Princess of Mars","""I am a very old man; how old I do not know.  Possibly I am a hundred, possibly more; but I cannot tell because I have never aged as other men, nor do I remember any childhood.  So far as I can recollect I have always been a man, a man of about thirty. """),
("A Connecticut Yankee in King Arthur's Court","""It was in Warwick Castle that I came across the curious stranger whom I am going to talk about.  He attracted me by three things: his candid simplicity, his marvelous familiarity with ancient armor, and the restfulness of his company -- for he did all the talking."""),
("The Metamorphosis", """As Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his bed into a gigantic insect."""),
("Alice's Adventures in Wonderland", """Alice was beginning to get very tired of sitting by her sister on the bank, and of having nothing to do: once or twice she had peeped into the book her sister was reading, but it had no pictures or conversations in it, 'and what is the use of a book,' thought Alice 'without pictures or conversations?'"""),
("Peter Pan", """All children, except one, grow up."""),
#("Aesop's Fables", """A BAT who fell upon the ground and was caught by a Weasel pleaded to be spared his life."""),
#("Aesop's Fables", """A FATHER had a family of sons who were perpetually quarreling among themselves."""),
("Aesop's Fables", """A HARE one day ridiculed the short feet and slow pace of the Tortoise, who replied, laughing: "Though you be swift as the wind, I will beat you in a race." """),
#("O Pioneers", """One January day, thirty years ago, the little town of Hanover, anchored on a windy Nebraska tableland, was trying not to be blown away. """),
("The Scarlet Letter", """A throng of bearded men, in sad-coloured garments and grey steeple-crowned hats, inter-mixed with women, some wearing hoods, and others bareheaded, was assembled in front of a wooden edifice, the door of which was heavily timbered with oak, and studded with iron spikes."""),
#("The Marvelous Land of Oz", """In the Country of the Gillikins, which is at the North of the Land of Oz, lived a youth called Tip."""), # Too boring a start.
("A Cure for the Blues", "Brightening clouds seemed to rise from the mist of the fair Chattahoochee, to spread their beauty over the thick forest, to guide the hero whose bosom beats with aspirations to conquer the enemy that would tarnish his name, and to win back the admiration of his long-tried friend."),
("Just So Stories", "Once upon a most early time was a Neolithic man. "),
]
first_verses = [("The Hunting of the Snark", """     "Just the place for a Snark!" the Bellman cried,
          As he landed his crew with care;
     Supporting each man on the top of the tide
          By a finger entwined in his hair"""),
]
verses = [("The Hunting of the Snark", """     The loss of his clothes hardly mattered, because
          He had seven coats on when he came,
     With three pairs of boots -- but the worst of it was,
          He had wholly forgotten his name.""") # plot twist: Amnesia!
]
random_lines = [ ("Alice's Adventures in Wonderland", """So she set to work, and very soon finished off the cake."""),
("Peter Pan","""He had his position in the city to consider."""),
("Peter Pan","""Oh, surely she must have been dreaming."""),
("The Time Machine", """The Psychologist recovered from his stupor, and suddenly looked under the table. """),
("The Time Machine", """At that the Time Traveller laughed cheerfully."""),
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
("The Marvelous Land of Oz","""Very carefully he began sprinkling the Thing with the precious powder."""),
("The Wizard of Oz","""They came from all directions, and there were thousands of them: big mice and little mice and middle-sized mice; and each one brought a piece of string in his mouth."""),
("The Wizard of Oz","""The road was smooth and well paved, now, and the country about was beautiful, so that the travelers rejoiced in leaving the forest far behind, and with it the many dangers they had met in its gloomy shades."""),
("The Wizard of Oz","""As they walked on, the green glow became brighter and brighter, and it seemed that at last they were nearing the end of their travels."""),
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
("Around the World in 80 Days" "The way in which he got admission to this exclusive club was simple enough."),
("Just So Stories", "This is the way Bi-Coloured-Python-Rock-Snakes always talk."),
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
("A Connecticut Yankee in King Arthur's Court", """I knew him in Egypt three hundred years ago; I knew him in India five hundred years ago -- he is always blethering around in my way, everywhere I go; he makes me tired."""),
("A Connecticut Yankee in King Arthur's Court", """"How long have I been shut up in this hole?" """),
("The Time Machine", """'"Communism," said I to myself."""),
("The Time Machine", """'That is all right,' said the Psychologist."""),
("The Time Machine", """The Time Traveller smiled."""),
("The Time Machine", """'Why not?' said the Time Traveller."""),
("The Time Machine", """'To discover a society,' said I, 'erected on a strictly communistic basis.'"""),
("The Marvelous Land of Oz",""""In an emergency," he announced, "it is always a good thing to pause and reflect. Please excuse me while I pause and reflect." """),
("The Wizard of Oz",""""That is because you have no brains" answered the girl."""),
("The Wizard of Oz",""""Who are you and where are you going?" asked the Stork."""),
("The Wizard of Oz",""""Where did you get the mark upon your forehead?" continued the voice."""),
("The Wizard of Oz","""After this she stood upon both feet and cried in a loud voice:

"Ziz-zy, zuz-zy, zik!"
"""),
("Alice's Adventures in Wonderland", """'Treacle,' said a sleepy voice behind her."""),
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

def load_table(filename):
    import os.path
    db_exists = os.path.isfile(filename)
    if not db_exists:
        raise ValueError("No such database exists.")
    db = dataset.connect('sqlite:///{}'.format(filename))
    table = db[table_name]
    return table

def get_table(filename):
    try:
        table = load_table(filename)
        return table
    except ValueError as e:
        for line in first_lines:
            table.insert(dict(source = line[0], line = line[1], position = 'first', category = None, uses = 0, views = 0, usage = 0.0))

        for line in random_lines:
            table.insert(dict(source = line[0], line = line[1], position = 'middle', category = None, uses = 0, views = 0, usage = 0.0))

        for line in dialogue:
            table.insert(dict(source = line[0], line = line[1], position = 'middle', category = 'dialogue', uses = 0, views = 0, usage = 0.0))

        for line in ribald_lines:
            table.insert(dict(source = line[0], line = line[1], position = 'middle', tag = 'ribald', uses = 0, views = 0, usage = 0.0))

        for line in abstractions:
            table.insert(dict(source = line[0], line = line[1], position = 'middle', tag = 'abstract', uses = 0, views = 0, usage = 0.0)) 
            # Note that some abstractions are not middle-of-the-story stuff.

        for line in concluding_lines:
            table.insert(dict(source = line[0], line = line[1], position = 'last', category = None, uses = 0, views = 0, usage = 0.0))
        
        return table

def view_usage_by(filename,group):
    """Print usage by a user-specified grouping field, aggregated over all of that group's lines."""
    db = dataset.connect('sqlite:///{}'.format(filename))
    result = db.query('SELECT SUM(uses) all_uses, SUM(views) all_views, {} FROM talespin_lines GROUP BY {}'.format(group,group))
    usage_by_group = {}
    views_by_group = {}
    for row in result:
        usage_by_group[row[group]] = row['all_uses']/(row['all_views'] + 1)
        views_by_group[row[group]] = row['all_views']
    import operator
    sorted_usage = sorted(usage_by_group.items(), key=operator.itemgetter(1))
    for group,usage in sorted_usage:
        print("{:<20.20} {:<4.3f} ({})".format(group, usage,views_by_group[group]))

def view_table(filename):
    table = load_table(filename)
    all_lines = table.find(order_by=['position', '-usage', '-uses', 'views'])
    position = ''
    position_count = defaultdict(int)
    line_count = 0
    genre_count = defaultdict(int)
    for line in all_lines:
        line_count += 1
        position_count[line['position']] += 1
        if 'genre' in line:
            genre_count[line['genre']] += 1
        if line['position'] != position:
            print("\n     ^ {} ^          v {} v\n".format(position,line['position']))
            position = line['position']
        print("{:<50.50} {}/{} = {:1.3}  ({})".format(line['line'], line['uses'], line['views'], line['usage'], line['source']))

    print("---------------\nThere are a total of {} lines in {}, with a first/middle/last/any breakdown of {}/{}/{}/{}.".format(line_count,filename,position_count['first'],position_count['middle'],position_count['last'],position_count['any']))
    pprint(dict(genre_count))

def median_view(lines):
    return statistics.median([x['views'] for x in lines])

def stats(table):
    first_lines = list(table.find(position=['first']) )
    first_median = median_view(first_lines)

    middle_lines = list(table.find(position=['middle']) )
    middle_median = median_view(middle_lines)

    last_lines = list(table.find(position=['last']) )
    last_median = median_view(last_lines)

    any_lines = list(table.find(position=['any']) )
    any_median = median_view(any_lines)
    return first_median, middle_median, last_median, any_median

def add_line(filename, source, author, line, position, category=None, genre=None):
    """The tricky thing about using this function from the command line is that 
        > python tell.py add_line lines.sqlite "Title" "Author" "'I think, therefore I think.'" middle dialgoue
    gets misinterpreted since bash seems to eat the outer quotes, and the fire module eats the
    inner quotes.
    
    A correct way to do this is to escape a third level of quotes.
        > python tell.py add_line lines.sqlite "Title" "Author" "'\"I think, therefore I think.\"'" middle dialgoue
    """
    table = load_table(filename)
    assert position in ['first','middle','last','any']
    assert category in ['narration', 'description', 'action', 'dialogue', 'set-up', 'aphorism', 'abstract', 'meta', 'meta-introduction', None]
    #assert genre in
    #assert tag in ['ribald', 'abstract', ]
    today = datetime.now().strftime("%Y-%m-%d")
    table.insert(dict(source = source, author = author, line = line, position = position, category = category, genre = genre, uses = 0, views = 0, usage = 0.0, added = today))
    print('Added "{}" from "{}" (by {}) with position "{}" and category "{}" and genre "{}".'.format(line, source, author, position, category, genre))

def prompt_for(input_field):
    try:
        text = raw_input(input_field+": ")  # Python 2
    except:
        text = input(input_field+": ")  # Python 3
    if text == "":
        return None
    return text

def multiline_prompt_for(input_field):
    text = " "
    lines = []
    while text not in ["", None]:
        text = prompt_for("Next line of {}".format(input_field))
        if text not in ["", None]:
            lines.append(text)
    return lines

def add_line_i(filename=None, source=None, author=None, line=None, position=None, category=None, genre=None):
    """Provides an interactive mode for adding lines, basically so that lines with characters that can
    not easily be escaped may be handled by Python's input function."""
    if filename is None:
        filename = prompt_for('filename')
    if source is None:
        source = prompt_for('source')
    if author is None:
        author = prompt_for('author')
    if line is None:
        lines = multiline_prompt_for('lines')
        line = '\n'.join(lines)
    if position is None:
        position = prompt_for('position')
    if category is None:
        category = prompt_for('category')
    if genre is None:
        genre = prompt_for('genre')
    add_line(filename=filename,source=source,author=author,line=line,position=position,category=category,genre=genre)

def edit_line(filename=None, line=None):
    if filename is None:
        filename = prompt_for('filename')
    if line is None:
        lines = multiline_prompt_for('lines')
        line = '\n'.join(lines)
    # Now the line has been specified; look it up and let the user edit any parameter.



def delete_line(filename, line):
    table = load_table(filename)
    if table.delete(line=line):
        print("found and deleted line={}".format(line))
    else:
        print("unable to find line={}".format(line))

def unadd_line(filename, source, author, line, position=None, category=None, genre=None):
    """Since lines are still sometimes corrupted by shell interpretation, this
    convenience function has been written to allow an add_line call to be 
    easily undone."""
    delete_line(filename, line)

def unadd_line_i(filename, source, author, line, position=None, category=None, genre=None):
    """Convenience function aliasing to unadd_line."""
    unadd_line(filename, source, author, line, position, category, genre)

def delete_by_source(filename, source):
    table = load_table(filename)
    first = table.find_one(source=source)
    if first is not None:
    #    print("Here, we would be attempting to delete {} which is the first line with source = {}".format(first['line'], source))
        if table.delete(source=source):
            print("Found and deleted line={} for source={}".format(first['line'], source))
            return
    print("Unable to find line for source = {}".format(source))

def extract_numbers(s):
    candidates = s.split(',')
    return [int(c) for c in candidates]

def choose(table,used,options,mode='random',counting=True,controlled=False,full_display=False):
    """Choose among dicts from the database and update
    the view/use counts appropriately for interactive choosing, 
    unless counting = False."""
    if mode == 'random':
        ds = [random.choice(options)]
    elif mode == 'interactive':
        prompt = "Choose an option:\n"
        for k,option in enumerate(options):
            prompt += "{}) {}\n".format(k+1,option['line'])
            if counting:
                option['views'] += 1
            table.update(option, ['line'])
        k_max = len(options)
        numbers = []
        while len(numbers) == 0 or not all(number in range(1,k_max+1) for number in numbers):
            try:
                keyed_in = input(prompt)
                numbers = extract_numbers(keyed_in)
                command = None
            except:
                if controlled:
                    command = keyed_in[0]
                    if command in ['a','x','q']: # For "(a)dd one more line" or "e(x)tend"
                        return used, None, command
                    elif command in ['b']: # meaning to take this beginning line but also
                        # come (b)ack for another
                        command = 'b' # This elif is not really necessary, actually.
                    try:
                        numbers = extract_numbers(keyed_in[1:])
                    except:
                        print("{} is not a series of numbers between 1 and {}".format(keyed_in[1:],k_max))
                else:
                    command = None
                    print("{} is not a series of numbers between 1 and {}".format(keyed_in,k_max))

        ds = []
        for number in numbers:
            d = options[number-1]
            ds.append(d)
            if counting:
                d['uses'] += 1
                table.update(d, ['line'])
                for option in options:
                    option['usage'] = (option['uses']+0.0)/option['views']
                    table.update(option, ['line'])
    else:
        raise ValueError("choose has not been programmed to handle mode {} yet.".format(mode))

    lines = [d['line'] for d in ds]
    used += lines
    if full_display:
        print_story(used)
    else:
        print(textwrap.fill('\n'.join(lines), width = 60, initial_indent="  > ", subsequent_indent="  > "))
    return used, ds, command

def build_paragraph(sentences):
    paragraph = ""
    k = 0
    while len(paragraph) == 0 or (k < len(sentences) and sentences[k][0] not in['"',"'"] ):
        line = sentences[k]
        paragraph += line.strip() + " "
        sentences.remove(line)
    return paragraph, sentences

def print_story(used):
    print(textwrap.fill(used[0], 60, initial_indent = "    ") +"\n")

    sentences = used[1:-1] 
    while len(sentences) > 0:
        paragraph, sentences = build_paragraph(sentences)
        print(textwrap.fill(paragraph, 60, initial_indent = "    ")+"\n")

    print(textwrap.fill(used[-1], 60, initial_indent = "    ")+"\n")

def random_story():
    table = load_table(db_file)
    initial_lines = list(table.find(position=['first','any']) )
    first_line = random.choice(initial_lines)['line']
    used = [first_line]

    middle_lines = list(table.find(position=['middle','any']) )
    while random.random() > 0.3 or len(used) < 2:
        next_line = random.choice(middle_lines)['line']
        if next_line not in used:
            used.append(next_line)

    final_lines = list(table.find(position=['last','any']) )
    conclusion = random.choice(final_lines)['line']
    used.append(conclusion)
    print_story(used)

def extend_story(table,used,view_limit,counting,new,controlled):
    if new:
        middle_lines = [d for d in list(table.find(position=['middle','any'],views=[0,1,2,3,4,5,6,7]) ) if d['line'] not in used]
    else:
        middle_lines = [d for d in list(table.find(position=['middle','any']) ) if d['line'] not in used and d['views'] <= view_limit]
    used, chosen_dicts, command = choose(table, used, random.sample(middle_lines,10), 'interactive', counting, controlled, full_display = True)
    return used, command

    # [ ] Where is chosen_dict used and can it be deleted?

def extend_story_hand(table,persistent_hand,hand,used,view_limit,counting,new,controlled):
    """This is a version of the extend_story function for adding lines to the story, which supports persistent-hand mode."""
    if persistent_hand:
        options = hand
    elif new:
        options = random.sample([d for d in list(table.find(position=['middle','any'],views=[0,1,2,3,4,5,6,7]) ) if d['line'] not in used], 10)
    else:
        options = random.sample([d for d in list(table.find(position=['middle','any']) ) if d['line'] not in used and d['views'] <= view_limit], 10)
    used, chosen_dicts, command = choose(table, used, options, 'interactive', counting, controlled, full_display = True)
    return used, chosen_dicts, command

def fetch_lines(table,positions,used,new=False):
    if new:
        initial_lines = list(table.find(position=positions,views=[0,1,2,3,4,5,6,7]) )
    else:
        initial_lines = list(table.find(position=positions) )
    filtered = [l for l in initial_lines if l not in used]
    return filtered

def remove_from_hand(x,hand):
    hand.remove(x)
    return hand

def draw_hand(table, draw_count=None, persistent_hand=False, positions=[], hand=None, just_used=[], used=[], new=False):
    lines = fetch_lines(table, positions, used, new)
    if persistent_hand:
        for x in just_used:
            hand = remove_from_hand(x,hand)
        hand += random.sample(lines, len(just_used))
        return hand

    if draw_count is None:
        if 'first' in positions and 'middle' in positions and 'last' in positions:
            draw_count = 12
        elif 'first' in positions:
            draw_count = 9
        elif 'last' in positions:
            draw_count = 7
    return random.sample(lines,draw_count)

def combine_hands(hand_1, hand_2):
    return hand_1 + hand_2

def interactive_hand(counting=True,new=False,controlled=True,persistent_hand=True):
    command = None
    table = load_table(db_file)
    first_median, middle_median, last_median, any_median = stats(table)
    if persistent_hand:
        hand_1 = draw_hand(table, 9, False, ['first', 'middle', 'last', 'any'])
        hand_2 = draw_hand(table, 3, False, ['first'])
        hand = combine_hands(hand_1, hand_2)
    else:
        hand = draw_hand(table, None, False, ['first','any'])
    used, chosen_ones, command = choose(table, [], hand, 'interactive', counting, controlled)
    if command == 'q':
        print("Terminating...")
        return
    if command == 'b':
        hand = draw_hand(table, None, persistent_hand, ['first', 'any'], hand, chosen_ones, used, new)
        used, chosen_ones, _ = choose(table, used, hand, 'interactive', counting)

    while command != 'q' and (random.random() > 0.3 or len(used) < 3):
        hand = draw_hand(table, None, persistent_hand, ['middle','any'], hand, chosen_ones, used, new)
        used, chosen_ones, command = extend_story_hand(table,persistent_hand,hand,used,middle_median,counting,new,controlled)

    terminate = (command == 'q')
    while not terminate:
        hand = draw_hand(table, None, persistent_hand, ['last','any'], hand, chosen_ones, used, new)
        used, chosen_ones, command = choose(table, used, hand, 'interactive', counting, controlled)
        if command in ['a','x']: # Add another middle line rather than one of the offered ending lines.
            hand = draw_hand(table, None, persistent_hand, ['last','any'], hand, [], used, new)
            used, chosen_ones, command = extend_story_hand(table,persistent_hand,hand,used,middle_median,counting,new,controlled)
        else:
            terminate = True

    print("The finished story:\n")
    print_story(used)

def interactive(counting=True,new=False,controlled=True):
    command = None
    table = load_table(db_file)
    first_median, middle_median, last_median, any_median = stats(table)
    initial_lines = fetch_lines(table, ['first','any'], [], new)
    used, _, command = choose(table, [], random.sample(initial_lines,9), 'interactive', counting, controlled)
    if command == 'b':
        initial_lines = fetch_lines(table, ['first','any'], used, new)
        used, _, _ = choose(table, used, random.sample(initial_lines,9), 'interactive', counting)

    while command != 'q' and (random.random() > 0.3 or len(used) < 3):
        used, command = extend_story(table,used,middle_median,counting,new,controlled)

    final_lines = fetch_lines(table, ['last','any'], used, new)
    terminate = False
    while not terminate:
        used, _, command = choose(table, used, random.sample(final_lines,7), 'interactive', counting, controlled)
        if command in ['a','x']: # Add another middle line rather than one of the offered ending lines.
            used, command = extend_story(table,used,middle_median,counting,new,controlled)
            final_lines = fetch_lines(table, ['last','any'], used, new)
        else:
            terminate = True

    print("The finished story:\n")
    print_story(used)

def i(counting=True,new=False,controlled=True):
    interactive(counting,new,controlled)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        random_story()
    else:
        fire.Fire()
