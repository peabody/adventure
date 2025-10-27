#!/usr/bin/env python3

# type: ignore
from adventurelib import * 


class InvRoom(Room):
    """Room type which gives rooms inventories"""
    def __init__(self, description: str):
        super().__init__(description)
        self.things = Bag()


class Readable(Item):
    """Object which can be read."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parts = []
    
    def add_part(self, data: str):
        """Add something to the journal"""
        self.parts.append(data)
    
    def read(self):
        if self.parts:
            for i in range(len(self.parts) - 1):
                say(self.parts[i])
                input("Enter to keep reading...")
            say(self.parts[-1])
        else:
            say("It appears to be blank")


JOURNAL = Readable('an ornate journal', 'journal')
JOURNAL.add_part("""Sept 1st, 1871

Word has spread of virulent flu accosting the local townships. Characteristics
are a long incubation (approximately 2 weeks), finally followed by flu like
symptoms which progress startlingly quickly. Death occurs within two days.""")

JOURNAL.add_part("""Sept 20th, 1871
            
It won't be long now. The disease is clearly airborne and heading east.
Strict quarantine measures have failed. A checkpoint blocking all entry
past Heart's Basin has been erected to try and stem the spread, but
there are already cases reported in the closest town past it.

We will be locking down access to the grounds, effective immediately. No
members of the house including servants are to enter or exit the
premises.""")

JOURNAL.add_part("""Sept 30th, 1871

It's happened. One of the grounds servants have shown symptoms. They've been
isolated to quarters, but I know all too well it's too late. One case means
there are many.""")

Study = InvRoom("""
You find yourself in a quaint, cozy study. A desk sits along
the western wall, while the remaining walls are covered in book shelves.

There are exits to the east and north.
""")

Paperweight = Item('a spherical glass paperweight', 'paperweight')
Paperweight.description = """There are cracks and scratching on one edge, as if it were used to strike something."""

Study.things.add(JOURNAL)
Study.things.add(Paperweight)

Study.shelves = """There are countless books among the shelves.
You wager it would take a lifetime to read them all. Subjects vary from microbiology, to anatomy."""

Red_Hallway = InvRoom("""You find yourself in a brightly painted red hallway.
                  
There are exits to the south and north.""")

Second_Floor_Landing = InvRoom("""You find yourself on a large 2nd floor landing.
Ornate red carpetting covers the flooring.
                               
Over the banister you can see the main staircase to a large entryway below.
                               
A hallway extends to the east.
A bright painted hallway extends to the south.
""")

Study.north = Red_Hallway
Red_Hallway.south = Study

# starting room and inventory
CR = Study
INV = Bag()


def current_room(new_room=None):
    """Get or set the current room."""
    global CR
    if new_room:
        CR = new_room
    return CR


@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
@when('n', direction='north')
@when('s', direction='south')
@when('e', direction='east')
@when('w', direction='west')
def move(direction):
    """Provide directional commands."""
    new_room = current_room().exit(direction)
    if new_room:
        current_room(new_room)
        look()
    else:
        say("You see no exit in that direction.")


@when("look THING")
@when("l THING")
@when("look", thing=None)
@when("l", thing=None)
def look(thing=None):
    cr = current_room()
    # show room description when no thing is given
    if not thing:
        say(cr.description)
        if len(cr.things):
            say("You see here: ")
            for item in cr.things:
                say(f'- {item.name}') 
        return

    # if attribute on room matching thing is found
    # read that
    obj = hasattr(cr, thing) and getattr(cr, thing)
    if obj:
        say(obj)
        return
    
    # Otherwise if room has an inventory
    # read the description of the item found
    obj = cr.things.find(thing) 
    if obj:
        if hasattr(obj, 'description'):
            say(obj.description)
        else:
            say(f"You see nothing special. It's just {obj.name}")
    else:
        say(f"You see no '{thing}' here.")


@when("take THING")
@when("get THING")
def take(thing):
    cr = current_room()
    obj = cr.things.take(thing)
    if hasattr(obj, 'fixed') and obj.fixed:
        say("You can't pick that up")
        return
    if obj:
        say(f"You take {obj.name}") # type: ignore
        INV.add(obj)
    else:
        say(f"You see no '{thing}' here.")


@when("drop THING")
def drop(thing):
    obj = INV.take(thing)
    if obj:
        cr = current_room()
        cr.things.add(obj)
    else:
        say(f"You don't have {thing}.")


@when("read THING")
def read_thing(thing):
    obj = INV.find(thing) or current_room().things.find(thing)
    if obj and hasattr(obj, 'read'):
        obj.read()
    else:
        say("That isn't readable.")


@when("inventory")
@when("i")
def show_inventory():
    if len(INV):
        say("You are currently holding:")
        for item in INV:
            say(f'- {item.name}')
    else:
        say("You are currently holding nothing.")


@when("say PHRASE")
def say_hello(phrase):
    say(f"You bellow the words '{phrase}!' ")


@when("help")
def game_help():
    print("""Try commands such as:
        - n,s,e,w - go in that direction
        - inventory or i - show current inventory
        - take ITEM - pickup an item
        - read ITEM - read something
        - look or l - look at current surroundings
        - look ITEM - examine an item
        - use ITEM [with THING] - use an item)
        - throw ITEM [at THING] - attempt to throw an item
        - open THING - open a door or container
        - close THING - close a door or container
        - say THING - speak""")


say("""You wake with a dull pain in your right temple.
 
    "How did I get here?" you wonder.
 
    You search your memories, but they fail you. The last distant vision in your
    mind is that of a face, one of a kindly looking old man.

    Try as you might, you've no memory of who you are, or where you currently might be.

    Slowly you pick yourself up from the floor, and glance around your surroundings...
    """)
print()   
look()
start(False)