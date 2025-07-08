# COLORS
# ebe5ce
# 3f2653
# fd4589
# a14675

# --- Variable Declarations ---
default cigs = 20
default seen_scenes = []
default available_scenes = ["Jay1", "Jay2", "Jay3", "Jay4", "alcPoison", "ahmed1", "ahmed2", "marwaCar", "sadiki", "ryan", "oldLady", "ray1", "martin1", "martin3", "lois", "fran", "tre", "philly", "reyan", "knala", "ale"]
default roomies = ["fran", "lois", "tre", "reyan", "knala", "philly", "ale", "talia", "vitor", "elio"]
default current_roomie = ""
default strangerCount = 0

# Scene dependencies
define scene_dependencies = {
    "Jay2": "Jay1",  # Jay2 only available if Jay1 has played
    "Jay3": "Jay2",  # Jay3 only available if Jay2 has played
    "Jay4": "Jay3",  # Jay4 only available if Jay3 has played
    "ahmed2": "ahmed1",  # ahmed2 only available if ahmed1 has played
    "martin3": "martin1",  # martin3 only available if martin1 has played
}

# transfrom for box
transform top_left:
    xalign 0.98
    yalign 0.08
    zoom 0.7

# The script of the game goes in this file.

# Declare characters used by this game.
define m = Character('Me', color="#fd4589")

define j = Character('Johnny', color="#3f2653")
define ja = Character('Jay', color="#3f2653")
define ahmed = Character('Ahmed', color="#3f2653")

define ry = Character('Ryan', color="#a14675")
define ra = Character('Ray', color="#a14675")
define marwa = Character('Amo', color="#a14675")
define mart = Character('Martin', color="#a14675")
define sad = Character('Sadiki', color="#a14675")

define fran = Character('Fran', color="#a14675")
define lois = Character('Lois', color="#a14675")
define tre = Character('Tre', color="#a14675")

define ale = Character('Ale', color="#a14675")
define rey = Character('Reyan', color="#a14675")
define kna = Character('Knala', color="#a14675")
define philly = Character('Phillip', color="#a14675")
define el = Character('Elio', color="#a14675")
define vi = Character('Vitor', color="#a14675")
define ta = Character('Talia', color="#a14675")

screen cig_display():
    zorder 1
    frame:
        xalign 0.95
        yalign 0.02
        background "#0008"
        xpadding 10
        ypadding 10
        text "Cigs: [cigs]" color "#ebe5ce" size 32

transform flip:
    xzoom -1

screen burnAnimation():
    zorder 0

    # Initially: show the video
    frame:
        xpos 1525
        ypos 520
        background None
        add Movie(size=(336, 112), play="images/Burning_Animation.webm", loop=False) at flip

    # After 20 seconds, hide video and show text instead
    timer 20 action [Hide("burnAnimation"), Show("click_prompt")]

screen click_prompt():

    text "click anything to go next!":
        xpos 1535
        ypos 550
        size 40
        color "#3f2653"
        xmaximum 400

    # Detect user input and hide this screen on click
    key "dismiss" action Hide("click_prompt")


# --- Function Definitions ---
init python:
    import random

# --- Script ---
# The game starts here.
label start:
    $ _preferences.music_volume = 0.8

    scene bg house
    with fade

    play music "Nostalgia Normal.mp3" fadeout .2

    "welcome to 528! \n\n\nClick or press any button to continue."
    "we're so glad you're here \n\n\nClick or press any button to continue."
    "come sit down, relax, and have a smoke"
    "lots of crazy things happen out here"
    "you can see it all from here"

    scene bg cig
    with fade

    m "i need to start cutting down..."
    m "just one pack..."
    m "a day"
    "each day starts off with a fresh pack (20 cigs)"
    "as you experience the day, you will smoke cigs"

    scene bg house
    with fade
    
    show box 20 at top_left
    show screen cig_display

    m "they say each day {i}is{/i} every day "
    m "each day {i}is{/i} every day "
    m "not each day is {i}like{/i} every day"
    m "each day {i}is{/i} every day "

    jump play_random_scene


# if renpy.has_label(current_scene):
#     renpy.jump(current_scene)
# else:
#     renpy.jump("invalid_scene")

# label invalid_scene:
#     "Oops. An error occurred."
#     jump play_random_scene


label play_random_scene:

    scene bg house
    
    if cigs <= 0:
        jump final_scene

    # call screen interlude
    play movie "images/interlude.webm"
    play audio "audio/Lighter.mp3"
    show movie
    # show movie onlayer movie

    # wait for movie duration
    $ renpy.pause(2.0, hard=True)
    

    stop movie
    hide movie

    # Filter scenes that haven’t been played & whose dependencies are met
    python: 
        valid_scenes = []
        for s in available_scenes:
            if s not in seen_scenes:
                if s in scene_dependencies:
                    if scene_dependencies[s] in seen_scenes:
                        valid_scenes.append(s)
                else:
                    valid_scenes.append(s)

        if not valid_scenes:
            renpy.jump("final_scene")
        else:
        # Pick a random valid scene
            current_scene = renpy.random.choice(valid_scenes)
            renpy.store.seen_scenes.append(current_scene)


    # Check if the chosen scene is a Roomie scene
        def is_roomie_scene(scene):
            for prefix in roomies:
                if scene.startswith(prefix):
                    return True
            return False

    if is_roomie_scene(current_scene):
        $ current_roomie = None
        python:
            for prefix in roomies:
                if current_scene.startswith(prefix):
                    current_roomie = prefix
                    break
        jump roomie_event
    else:
        jump expression current_scene


label roomie_event:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display
    "You see someone walking by. You think it might be [current_roomie!c]."

    menu:
        "What do you do?"
        
        "Look at them and say hi":
            jump expression current_roomie
        
        "Just say hi":
            $ chance = random.random()
            if chance < 0.8:
                jump expression current_roomie
            else:
                jump stranger
        
        "Ignore them":
            jump stranger

    $ cigs = max(cigs - 1, 0)

label stranger:
    $ strangerCount = strangerCount + 1
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    m "FUCKKKKKKKK"
    m "Fuck"
    m "fuckkkkkkk"
    m "i let a stranger into our home"


    if strangerCount == 1:
        m "a whole ass stranger ... "
        m "i guess i didn't really look to see who was coming in, but they walked in and opened that door without hesitation?"
        m "the roomies are in and out of this house all the time, but i always always look up and say hi"
        m "that comes with the job of being a gargoyle"
        m "ugh and i really fucked up this time"
        m "at least he just wanted to use the bathroom ?"
        m "he did take the bathroom window pane tho... and left a metal 24/7 surveillance sign... he seemed just as confused as us?"
    elif strangerCount == 2:
        m "i'm the worst gargoyle ever :/"
        m "i know he was confused as hell when he saw the human-sized exercise pen"
        m "he defintely doesn't know that's for the baby bunny boy Opal"
    elif strangerCount == 3: 
        m "i can't believe his ass took a whole ass tour this time"
        m "and just chilled on the couch for a while before anyone in the house got the vibe he shouldn't be there"
    else:
        m "what is wrong with me...."
        m "why does this keep happening..."
        m "i need to go see a doctor or something"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label reyan:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    rey "heyyy"
    m "hey!"
    m "where are you coming back from?"
    rey "played some pickup soccer at the complex and now i have no thoughts."
    m "is that a good thing?"
    rey "i think it is. usually, it sounds like a battle of the bands in my head."
    rey "i like the quiet when i can get it."
    m "okay but why are you so sweaty? like you're literally soaked..."
    rey "don't act like i'm the weird one when you just don't sweat"
    m "girl go take a shower"
    rey "on it"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label knala:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    kna "heyyy"
    m "hey!"
    m "where are you coming back from?"
    kna "it was a good day outside. i just sat in the grass and played with my rubiks cube."
    m "see you later!"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label ale:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    ale "heyyy"
    m "hey!"
    m "where are you coming back from?"
    ale "thrifting! and i got some really cute things!"
    m "that's awesome!"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label philly:
    scene bg house
    show expression "box [cigs]" at top_left
    show screen cig_display
    $ _preferences.music_volume = 0.8
    $ renpy.music.set_pause(True, channel='music')  # Pauses current music
    stop music fadeout 0.05
    play audio "audio/HustleThatCat.mp3" volume 0.7
    queue music "Nostalgia Normal.mp3" fadein 0.1
    show screen burnAnimation


    philly "heyyy"
    m "heyyy"
    m "where are you coming back from?"
    philly "i'm just coming back from lab! but i'm gonna have a snack and some pre-workout and then go to a spin class"
    m "what kind of music is it gonna be?"
    philly "it's actually only gonna be ru paul music"
    m "WERKKK you better hustle that cat"
    philly "oh don't worry, you're gonna see me sweat, put my whole kitty in it"
    philly "HUSTLE THAT THING FOR MEEE"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label lois:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    lois "heyyy"
    m "heyy"
    m "where are you coming back from?"
    lois "just a stop cop city meeting downtown, that jawn was looooong"
    m "oh really? how was it?"
    lois "not too bad... but actually kind of floppy. it's a mess, but we gon figure it out"
    m "word, lemme know if i can help out"
    lois "bet, for sure. our next meeting is this weekend, i'll  hit you up"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label fran:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    fran "heyyy"
    m "heyyy"
    m "where are you coming back from?"
    fran "From Berkeley. Went to Mo's and got a new book!"
    m "book haul book haul book haul"
    fran "Girl, you know I love me some Duke University Press! Don't play!"
    fran "I found the book that inspired the exhibit that inspired the MET Gala... "
    fran "Let's see why the girls flopped."

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene


label tre:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    tre "hi"
    m "heyyyy"
    m "where are you coming back from?"
    tre "from the rave"
    m "what was the theme this time?"
    tre "The theme was Hatsune Miku they had somebody cosplay as her"
    m "did the crowd also dress up?"
    tre "no, everybody wore black lol"
    m "haha glad you had fun, goodnight"
    tre "nightttt"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label elio:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    el "heyyy"
    m "hey!"
    m "where are you coming back from?"
    el "just finished working out! Catch ya later!"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label vitor:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    vi "heyyy"
    m "hey!"
    m "where are you coming back from?"
    vi "LA! Did you forget about my one day trip to see Beyonce?"
    m "girl, i didn't forget. i didn't believe you!"
    vi "I'll tell you all about it later, I have to sit down"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene

label talia:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    ta "i'm home!"
    m "hey!"
    m "where are you coming back from?"
    ta "ughhh up north. I need to quit soon, it's killing my lungs"
    m ":( yea take care of yourself! Let me know if you need anything, I have some extra inhalers and stuff"

    $ cigs = max(cigs - 1, 0)
    jump play_random_scene


label Jay1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "I see Jay coming out... she's been letting her dogs shit all over the driveway and isn't picking it up. Makes it hard to take out the trash."

    "She always says hi to me, but those who have lived here longer have warned me about her explosive temper and retaliating when they ask her about the poop or blocking their car in..."

    ja "heyyyy girlie"

    menu:
        "What should I do?"

        "ignore her. it's not your weekly job to take out the trash, and you don't need to be encouraging crazy ppl.":
            jump dogPoopMean

        "calmly bring it up":
            $ drank_tea = True
            jump dogPoopNice

        "match her attitude and tell her she needs to take care of her shit. literally and figuratively.":
            jump dogPoopMean
        
        "call the landlord.":
            jump dogPoopMean

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label dogPoopMean:
    scene bg house
    show expression "box [cigs]" at top_left
    "My roommates have asked her so many times to pick up after her dogs. They say it always goes poorly, so it's time for her to just face the consequences"
    "or so i thought"
    "that just really pissed her off and destroyed the budding nice neighbor relationship we were building, and she keeps scowling or yelling at me"
    "i don't blame her though"
    "i choose to be scared and do the easy thing for me, the selfish option of invoking an authority figure on her when i should\'ve just spoken to her myself"
    "she told me I really hurt her feelings and am jeoparidizing her housing"
    "she yelled for a while and i deeply apologized"
    "she told me how she is only 19 and has always been alone due to growing up in foster care"
    "she only has her tiny place due to finally getting approved for Section 8 housing, and the landlord is looking to kick her out and raise the rent"
    "she told me how much she appreciated seeing me on the porch everyday and having friendly chats. Before me, my previous roommates would judge her for her appearance and were combatative right off the bat because of her face tattoos, blackccent (she\'s white), and her fights with her boyfriend"
    "i don't blame her. if i was her i would also let my dog shit everywhere to piss off the judgy weird neighbors who spoke to me with obvious disdain."
    "i apologized for being rash"
    "she apologized for the dog poop"
    "we shared a smoke and watched her two puppies run as we bonded over our mutual dislike of the previous roomies."
    $ cigs -= 3
    pause
    jump play_random_scene

label dogPoopNice:
    scene bg house
    show expression "box [cigs]" at top_left
    "I asked her to pick up the poop. I explained how it's like a maze trying to get the two bins in and out of the backyard for garbage day and how we end up getting poop all over the wheels and smearing it everywhere."
    "at first she got mad"
    "real mad"
    "she started screaming stuff like:" 
    ja "boujee bitches come to oakland not expecting to find some dog poop"
    ja "BITCH its OAKLANd"
    "i just smiled and wished her well. She came back later apologizing and explaining that she got scared I was going to be mean and jeopardize her housing."
    "she told me how she is only 19 and has always been alone due to growing up in foster care"
    "she only has her tiny place due to finally getting approved for Section 8 housing, and the landlord is looking to kick her out and raise the rent"
    "she told me how much she appreciated seeing me on the porch everyday and having friendly chats. Before me, my previous roommates would judge her for her appearance and were combatative right off the bat because of her face tattoos, blackccent (she is white), and her fights with her boyfriend"
    "i dont blame her. if i was her i would also let my dog shit everywhere to piss off the judgy weird neighbors who spoke to me with obvious disdain."
    "i apologized for being rash"
    "we shared a smoke and watched her two puppies run as we bonded over our mutual dislike of the previous roomies. "
    $ cigs -= 2
    pause
    jump play_random_scene

label Jay2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "that was really scary..."
    "Jay says she can handle herself but i'm glad she came to us for help"
    "i'm glad we were out here... i know we always are but i think i\'m starting to understand what it means to be visible"
    "we hear stories of people suffering alone, wishing they had anyone to support them, and we tell ourselves that we are the kinds of people who would step up for their neighbor or stop a child from running into the street but"
    "but are we really if we are not visible? present?"
    "if we are uncomfortable bearing witness to our own neighbor, how can we be the welcoming neighbor?"
    "she ran out crying from her building, clutching her throat"
    "her boyfriend was close behind"
    "it happened so fast. she got onto our porch, and her abusive shit boyfriend is too scared to do anything with witnesses"

    $ cigs -= 2
    pause
    jump play_random_scene


label Jay3:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "last night there was a shooting"
    "a shooting is a bit dramatic"
    "there was a shot"
    "Jay and her gbf (gay best friend) came home drunk together, and he was too drunk to understand what was going on"
    "he started getting violent, and she ran into her home"
    "he tried coming into her apartment through her window"
    "she warned him and begged him to leave"
    "so i don't blame her for firing the shot"
    "apparently everything went silent after the shot"
    "i hope she's okay"
    "it's hard to keep losing people when you already have no one"
    "fuck our roomie for using that as an excuse to move out"
    "that's fucked up"
    "everyone has a right to defend themselves until they actually have to"
    "then that makes you \"uncomfortable\""
    "right......."
    "ugh... i need to find a new roomie"

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label Jay4:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "She said she was going to move to San Jose and get into pharmacy school. She got a new kind boyfriend who talks things out with her and isn't a broke ass bum forcing her to sell pussy to fund his lifestyle while simultaneously slut-shaming her."
    "She seemed happier. Kinder to her dogs. No loud arguements. Waking up earlier."
    "She said she was going to leave before. A million times over. "
    "This time she really did it."
    "She didn\'t say bye. I hope she knows I consider her a friend."

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene


label ahmed1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "suddenly, it's pouring rain and a man appears at the steps of your porch"

    m "hello?"

    ahmed "Hi! My name is Ahmed and I am your neighborhood council representative."

    menu:
        "neighborhood council rep?":
            ahmed "Yup! I live at the end of the block. That house with a bunch of garbage and recycle bins."
        "hi?":
            ahmed "If you ever need anything, I live in that house end of the block with all those garbage and recycle bins."
    
    menu:
        "why do you have so many bins?":
            ahmed "If you ever need anything, don't be shy!"
        "oh okay... (how can we stop talking to this person???)":
            ahmed "Don't be a stranger!"

    m "do you want to step underneath our awning? you're getting soaked"
    "You take a better look at him and see that he is a bald man, just a few inches taller than you, wearing a plastic rain coat and..."
    "no shoes?"

    ahmed "I saw that you had some issues with Sadiki"
    m "who?"
    ahmed "Sadiki! The unhoused man who was shoving socks into your mail slot and yelling at your house that he will protect you."
    m "right.. he's harmless, but thanks for offering to help. stay dry out there!"
    "I hope he takes the hint."
    ahmed "Okay well, when you do need help — when NOT if — I am available. He is pretty harmless, but I have been keeping my distance since he punched me in the throat."
    m "bye!"

    "Sadiki punched him in the throat??? Probably deserved it. Why is he walking around barefoot?"
    
    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label ahmed2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "Neighborhood Council Rep? Ahemd is walking by with his family"
    ahmed "Salaam! This is my wife, my kids, and our puppy"

    menu:
        "should I say ..."

        "salaam":
            jump ahmed2_1
        
        "hello!":
            jump ahmed2_1

        "marhaba":
            jump ahmed2_1

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label ahmed2_1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display
    ahmed "Oh! I should've known by your necklaces that you're also Lebanese and Muslim. I thought you were a white-washed Christian"
    m "thanks?"

    jump ahmed3

label sadiki:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display
    
    "here comes Sadiki. he's been around our block recently and has been in the general area ever since he lost his housing a few months ago"
    "it has only been a few months, but the glimpse you get into his wellbeing everytime you see him is enough to know it has been unbearable"
    sad "Hey, hey - do you know what Sadiki means?"
    m "it's Arabic for my friend?"
    sad "Yes, so when I pass you will all have to say 'my friend passed away'"
    $ msg = renpy.input("What do you even say to that? (psttt - type something!)", length=64)
    
    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label ahmed3:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    m "he's so interesting... there's dog shit, broken glass, needles, and crack pipes everywheree, and he parades his whole family around barefoot"
    m "not to being a haterrrr - just sayin"
    m "he also must be the one painting those beautiful murals with arabic calligraphy on the side of their house facing the highway"    
    
    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label alcPoison:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "A man comes up to the porch..."
    "hi umm.. i got my friend over there across the street at the church, and he got alcohol poisoning and my phone is dead. can you call 911? I'm going to the store real quick, and I'll call 911 there too"
    m "Oh- yes of course"
    m "but why are you going to the store? andd he is gone"
    "You call 911, and they arrive in 4 minutes which is unusual because normal response time is at least 20 minutes. Good because the man was starting to slump over, and his friend is no where to be seen"
    "You can't see much anymore; the firetruck is blocking your view"
    "The paramedics leave pretty quickly, giddy, laughing, and you see the alleged alc poisoned man up and walking fine."
    "The friend never came back. hmph"
    
    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene


label ryan:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "You see Ryan walking her silly pitbull."
    menu:
        "should I..."

        "say hi?":
            jump ryan2
        
        "ignore her?":
            jump ryan2

label ryan2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display
    "You lock eyes and awkwardly look away." 
    "You both laugh, and they come by the porch steps for a chat."
    "Ryan tells you how Dexter has been catching an attitude ever since she found out he's allergic to chicken and she changed his diet."
    "As she walks away, you chastise yourself for even considering ignoring her."
    
    "{i}You shouldn't ignore people for the convenience of not using your voice. You're missing out on the little moments that help make us all feel grounded and welcome here. {/i}"

    "{i}Remember we are all visitors.{/i}"
    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label marwaCar:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    m "hmmm it's around that time of day, where is he?"
    m "and just like clockwork there he is"
    "Every weekday, at the same time, the owner of the Marwa's Grill (shop right around the corner) parks his car here and brings down supplies"
    "This time though, it looks like he's making his way over here"

    marwa "Marhaba!"

    menu: 
        "Marhaba":
            jump marwaCar2
        "Salaam":
            jump marwaCar2
        "Hello!":
            jump marwaCar2

label marwaCar2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    marwa "Do you know who owns that car?"
    "He points to a neighbor's recently crashed Mustang. What does he care?"
    m "Not really, I know it belongs to one of my neighbors. What's up?"
    marwa "I want to buy it. Do you think they'd sell?"
    m "honestly, no... it's a pretty complicated situation"
    marwa "Why not?"

    menu: 
        "Should I give him the..."

        "end this convo non-answer": 
            "They love that car, they're not going to sell."
        "short and sweet answer": 
            "It was hit by the police and is part of a lawsuit. Even if they wanted to sell it, they can't anytime soon until they're done taking the evidence."
        "full story answer": 
            "Her dumbass, broke, on-parole boyfriend used her car with a suspended license, and he got hit by a cop at an intersection and zoomed home. It's part of a lawsuit now, so even if she wanted to, they can't sell it anytime soon."

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label oldLady:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "You hear the sound of metal scraping the sidewalk. "
    "You look up and see an old woman with a walker slowly walking down the sidewalk. "
    "The scraping stops. There is a car parked behind yours in the driveway. It's blocking the sidewalk. "
    "You let out a sigh. The neighbors in the apartment building next door always block your car in no matter how many times you've asked, so you started leaving no extra room in the driveway for another car. But those fuckers don't care and just block the whole sidewalk instead. "
    "A shakey, frail voice interrupts you cursing out your neighbors. The woman is asking if you can move the car."

    menu:
        "What should you do?"

        "I could look for the car\’s owner but that's going to take awhile...":
            jump oldLady1
        "I don't know whose car it is, and I've never really knocked on their doors like that before. Maybe I could just tell her it's not my car?" :
            jump oldLady2
        "or maybe I just help her get around the car?":
            jump oldLady3

label oldLady1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "You tell her that you\'ll go look for the car owner. "
    "You go to the apartment building and knock on the doors of all 5 units. Some answered. Some didn't. No one claimed the car. Good thing you didn't have to go to work..."
    "You have to go back and tell the woman something."

    menu:
        "Should I..." 
        "tell her it's not my car and sit back down":
            jump oldLady2
        "help her get around the car?":
            jump oldLady3

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label oldLady2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display
    
    "{i}NO! you can't just ignore her.... what the fuck.. you can't say you care about the elderly and only mean your grandparent or kindergarten teacher... everyone wants a community but no one wants to be a community member{/i}" 
    "{i}stupid ass bitch {/i}"
    "GO HELP HER!1!1!!1!11!!!!1!"

    $ cigs = max(cigs - 1, 0)
    pause
    jump oldLady3

label oldLady3:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "You tell her that you don't know where the car owner is but can help her get around."
    "She lets out a sigh.. of relief maybe? And she thanks me."
    "Her walker is full of groceries. The sidewalk is really cut up and jagged. You help her lift the walker over the big cracks and the curve of the driveway."

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label ray1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "An unhoused man walks up to the house and opens the water faucet"

    menu:
        "What will you do?"

        "Sit quietly and observe": 
            jump ray2
        "Say hi":
            jump ray2
        "Shoo him away":
            ra "you and your jokes :)"
            jump ray2
        "Call the cops": 
            jump weirdo

transform flashing_text:
    xpos 0.5
    ypos 0.5
    xanchor 0.5
    yanchor 0.5
    alpha 1.0
    linear 0.2 alpha 0.0
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.0
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.0
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.0
    linear 0.2 alpha 1.0
    linear 0.2 alpha 0.0
    linear 0.2 alpha 1.0

label weirdo:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    menu:
        "were you scared?"

        "Yes": 
            "did that fear steal your voice?"
        "No": 
            "then why"

    "you didn't even give anyone a chance"
    "you were selfish and chose yourself even in a simulation"
    
    scene black
    show text "{size=100}{color=#fd4589}WEIRDOOOOOOOOOOO{/size}" at flashing_text

    pause 5.0
    hide text

    $ cigs = max(cigs - 2, 0)
    jump ray1

label ray2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    ra "Well hey there lil lady!"
    m "how are you today, Ray?"
    ra "every day is a good day when I get to see you"
    m "aww thanks Ray, it makes me happy to see you still walking around"
    ra "I know I know, it's a blessing these legs have carried me for over 70 years, and I just hope they can keep going a lil more"
    m "I always say this, but you look amazing for 70"
    ra "It's my job keeping me young"
    m "what's your job?"
    ra "Picking up around the neighborhood, the church, your house, you know, the rounds"
    m "ahh yes, and I always appreciate it Ray. Would you like some water? I also got more of those fruit pouches you like."
    ra "Yes Ma'am, thank you. Those are great cuz you know I ain't got teeth"
    m "*chuckles* yes I do, I'll be right back."

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene


label martin1:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    mart "OBAMA!" 
    mart "*snap*"
    mart "*clap*"
    mart "OBAMA!"
    mart "fourty-four"
    mart "fourty-fourr"
    mart "FOURTY-FOUR PRESIDENTTTTTTTTTTTTTTT"
    mart "OBAMA!"

    m "mhmm sounds like Martin is up and about to start drinking and DJing on his stoop"
    m "i wonder how that old man makes enough to afford alc and rent... its tough out here"

    mart "HEY NEIGHBOR!"

    m "anddd hes coming over here now"

    jump martin2

label martin2:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    mart "hehehe you got your PJs on"
    m "*sigh* yes I do"
    mart "Are you with the devil?"
    m "what.. ? no?"
    mart "What's that on your shirt then? 0-o"
    "He leans over cartoonishly with one eye open real wide"
    m "it says Evil but it's just some PJs"
    mart "DEVIL! reghehghgrghrhhe"
    m "Martin please chill out or leave. We've talked about this. No more cackling."
    mart "oook ook ooooook i'll be right back"

    menu:
        "okay...i wonder what he's up to now":
            jump martinYes
        "i know he's lonely... but should i tell him not to come back?":
            jump martinNo

label martinYes:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    mart "I got this book here full of memories. Flip to a random page, and write something down for me."
    m "Oookay, sure!"
    "You grab the heavy, thick book. Bits and pieces of paper and scraps poking out from the edges. 4 glittery markers."
    "He means business."
    "You begin to open the book and-"
    mart "NOOOOOOOOO not in front of me. I can't know I can't know I can't know."
    m "Martin"
    m "just turn around."
    "You open the book and let out a gasp."
    "It's a memory book. Pages full of news clippings, photos, ticket stubs."
    "I am holding the memory of his life"

    $ msg = renpy.input("What should I write? (psttt - type something and hit enter!)", length=64)
    $ msg = msg.strip()

    if not msg:
        $ msg = "Hang in there!"

    m "okay, here you go Martin"
    mart "DON'T TELL ME what you wrote. I want to find it later after we have forgotten each other."
    m "okay?"

    scene bg scrapbook1
    pause 1.0
    scene bg scrapbook2 with dissolve

    show expression Text(msg, size=53, color="#a14675", xpos=350, ypos=900, xmaximum=400)
    pause 1.0

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene

label martinNo:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "he be doing too much..."
    "I can't keep encouraging him to come over here..."
    "I know he's lonely, but he randomly freaks out on me 0-o"
    
    $ cigs -= 2
    pause
    jump play_random_scene   

label martin3:
    scene bg house
    show screen burnAnimation
    show expression "box [cigs]" at top_left
    show screen cig_display

    "oh Martin..."
    "a for sale sign is up"
    "we never got to say bye..."
    "I wonder what happened to him?"

    $ cigs = max(cigs - 1, 0)
    pause
    jump play_random_scene 


transform slidein:
    xpos -100
    yalign 0.4
    linear 1.0 xpos 1300

label final_scene:
    hide screen burnAnimation  # or any custom screens
    hide screen click_prompt
    scene bg end
  
    "huh..."
    "guess that was the last one"
    "time to go to bed"

    scene bg house end with fade
    show text Text("guess each day is every day", size=80, font="fonts/Jersey10.ttf", color="#FFFFFF") at slidein
    pause 8
    hide text Text("guess each day is every day", size=80, font="fonts/Jersey10.ttf") with dissolve
    pause 2

    # This ends the game.
    return

