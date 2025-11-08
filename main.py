"""
===================================================================================
VIRTUAL PIANO PROJECT - TEMPLATE
===================================================================================
This is a simplified template for a virtual piano program. Your job is to
implement the missing functions to make the piano interactive!

WHAT THIS PROGRAM DOES:
- Displays a virtual piano keyboard on screen (ALREADY DONE)
- Shows hand position indicators for left and right hands (ALREADY DONE)
- Displays a title bar with instructions (ALREADY DONE)
- You will make it respond to mouse clicks, keyboard input, and MIDI playback!

FUNCTIONS YOU NEED TO IMPLEMENT:
1. midi_to_note_name() - Converts MIDI numbers to note names
2. load_midi_file() - Loads a MIDI file for playback
3. find_first_note_after() - Finds notes at specific times
4. play_note_with_limiter() - Plays sounds with volume control

===================================================================================
"""

"""
# ===================================================================================
# SUMMARY OF VARIABLES FOR YOUR IMPLEMENTATION
# ===================================================================================

KEY VARIABLES YOU NEED TO USE:

For midi_to_note_name():
    - NOTE_NAMES: List of 12 note names ["C", "C#", "D", ...]
    - midi_num parameter: The MIDI note number (0-127)

For load_midi_file():
    - playback_messages: Global list to store (time, index, type, velocity) tuples
    - current_msg_index: Global int for current position in playback
    - playback_active: Global bool for whether MIDI is playing
    - black_note_map: Dict mapping note names to black key indices
    - white_note_map: Dict mapping note names to white key indices
    - filepath parameter: Path to MIDI file

For find_first_note_after():
    - playback_messages: Global list of note tuples
    - time_ms parameter: Time in milliseconds to search for

For play_note_with_limiter():
    - g_active_channels: Global list of active pygame mixer channels
    - LIMITER_THRESHOLD: Constant = 16 (max notes before limiting)
    - BASE_NOTE_VOLUME: Constant = 0.6 (base volume level)
    - sound_to_play parameter: pygame.mixer.Sound object
    - velocity parameter: Note velocity (0-127)

PYGAME/MIXER FUNCTIONS YOU'LL NEED:
    - pygame.mixer.find_channel(): Returns available channel or None
    - channel.set_volume(volume): Sets volume (0.0 to 1.0)
    - channel.play(sound): Plays sound on channel
    - channel.get_busy(): Returns True if channel is playing

MIDO (MIDI LIBRARY) USAGE:
    - mido.MidiFile(filepath): Loads MIDI file
    - for msg in mid: Iterate through messages
    - msg.time: Time delta for this message
    - msg.type: Message type (e.g., "note_on")
    - msg.note: MIDI note number
    - msg.velocity: How hard key was pressed (0-127)

MATH FUNCTIONS:
    - sqrt(x): Square root (already imported from math module)

TIPS:
1. Use 'global' keyword when modifying global variables in functions
2. Remember integer division (//) vs regular division (/)
3. Remember modulo operator (%) for getting remainder
4. Check for None/empty lists before processing
5. Use try-except for file operations to handle errors gracefully
"""

from math import sqrt

import mido
import pygame
from pygame import mixer

import piano_lists as pl

# ===================================================================================
# PYGAME INITIALIZATION - This sets up the audio and graphics
# ===================================================================================
pygame.mixer.pre_init(
    frequency=44100,  # Standard sample rate (CD quality)
    size=-16,  # 16-bit audio (standard quality)
    channels=2,  # Stereo sound (left and right speakers)
    buffer=2048,  # Buffer size for audio processing
)

pygame.init()  # Initialize all pygame modules

# Set up 512 audio channels so many notes can play simultaneously
pygame.mixer.set_num_channels(512)

# ===================================================================================
# FONTS - Different sized fonts for different text elements
# ===================================================================================
font = pygame.font.Font("assets/Terserah.ttf", 48)  # Large font for title
medium_font = pygame.font.Font(
    "assets/Terserah.ttf", 28
)  # Medium font for instructions
small_font = pygame.font.Font("assets/Terserah.ttf", 16)  # Small font for key labels
real_small_font = pygame.font.Font(
    "assets/Terserah.ttf", 10
)  # Tiny font for black key labels

# ===================================================================================
# DISPLAY SETTINGS
# ===================================================================================
fps = 60  # Frames per second (how smooth the animation is)
timer = pygame.time.Clock()  # Clock to control frame rate
WIDTH = 52 * 35  # Window width (52 white keys × 35 pixels each = 1820 pixels)
HEIGHT = 400  # Window height in pixels
screen = pygame.display.set_mode([WIDTH, HEIGHT])  # Create the game window

# ===================================================================================
# SOUND LOADING - Load all piano note sound files
# ===================================================================================
white_sounds = []  # List to store white key sounds
black_sounds = []  # List to store black key sounds

# ===================================================================================
# ACTIVE KEY TRACKING - These lists track which keys are currently pressed/highlighted
# ===================================================================================
# Each entry is [key_index, frames_remaining]
# frames_remaining counts down each frame to create a visual flash effect
active_whites = []  # List of white keys currently active (being pressed)
active_blacks = []  # List of black keys currently active (being pressed)

# ===================================================================================
# OCTAVE SETTINGS - Control which octave each hand is playing
# ===================================================================================
# An octave is a set of 12 notes (7 white, 5 black). Piano has multiple octaves.
# Octaves are numbered 0-8. Middle C is in octave 4.
left_oct = 4  # Left hand starts at octave 4
right_oct = 5  # Right hand starts at octave 5 (one octave higher)

# ===================================================================================
# AUDIO CHANNEL MANAGEMENT
# ===================================================================================
g_active_channels = []  # Tracks which audio channels are currently playing sounds

# ===================================================================================
# MIDI PLAYBACK VARIABLES (For playing pre-recorded piano music)
# ===================================================================================
playback_messages = []  # List of notes to play from MIDI file
playback_start_time = 1000 * 60 * 2 + 15 * 1000  # Start time: 2 minutes 15 seconds
current_msg_index = 0  # Current position in the MIDI playback
playback_active = False  # Is MIDI playback currently playing?
midi_loaded = False  # Has a MIDI file been loaded?
midi_file_path = "assets/MIDI/Thomas_Bergersen_-_Made_of_Air_(2_Pianos).mid"

# ===================================================================================
# NOTE NAME CONSTANTS
# ===================================================================================
# Standard music notation: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
# The # symbol means "sharp" (the black key above)
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ===================================================================================
# PIANO NOTE LISTS (imported from piano_lists.py)
# ===================================================================================
left_hand = pl.left_hand  # Keyboard letters for left hand (Z, X, C, V, B, N, M, etc.)
right_hand = (
    pl.right_hand
)  # Keyboard letters for right hand (R, T, Y, U, I, O, P, etc.)
piano_notes = pl.piano_notes  # All piano notes in order
white_notes = pl.white_notes  # List of all white key notes (C0, D0, E0, F0, etc.)
black_notes = pl.black_notes  # List of all black key notes (C#0, D#0, F#0, etc.)
black_labels = pl.black_labels  # Labels for black keys

# ===================================================================================
# AUDIO LIMITER SETTINGS - Prevents sound from being too loud
# ===================================================================================
LIMITER_THRESHOLD = 16  # Maximum number of notes before volume reduction kicks in
BASE_NOTE_VOLUME = 0.6  # Base volume for each note (0.0 to 1.0)

# ===================================================================================
# LOAD SOUND FILES - Load .wav files for each piano key
# ===================================================================================
# White keys: Load sound files for all 52 white keys
for i in range(len(white_notes)):
    sound = mixer.Sound(f"assets/notes/{white_notes[i]}.wav")
    white_sounds.append(sound)

# Black keys: Load sound files for all 36 black keys
for i in range(len(black_notes)):
    sound = mixer.Sound(f"assets/notes/{black_notes[i]}.wav")
    black_sounds.append(sound)

# Set window title
pygame.display.set_caption("Arpeggio")

# ===================================================================================
# NOTE MAPPING DICTIONARIES
# ===================================================================================
# These create a quick lookup: given a note name, find its index in the list
white_note_map = {note_name: index for index, note_name in enumerate(white_notes)}
black_note_map = {note_name: index for index, note_name in enumerate(black_labels)}


# ===================================================================================
# FUNCTIONS TO IMPLEMENT - YOUR ASSIGNMENT!
# ===================================================================================


def midi_to_note_name(midi_num):
    """
    *** YOU NEED TO IMPLEMENT THIS FUNCTION! ***

    Converts a MIDI note number (0-127) to a note name like "C4" or "A#5"

    PARAMETERS:
        midi_num: Integer from 0-127 representing a MIDI note
                  (Middle C = 60, which is C4)

    WHAT YOU NEED TO DO:
        1. Check if midi_num is valid (between 0 and 127)
           - If not valid, return None

        2. Calculate the octave number
           - Formula: octave = (midi_num // 12) - 1
           - The // operator does integer division (no decimals)
           - We subtract 1 because MIDI octave -1 starts at note 0

        3. Calculate which note in the octave (0-11)
           - Formula: note_index = midi_num % 12
           - The % operator gives the remainder after division
           - This tells us which of the 12 notes it is

        4. Get the note name from NOTE_NAMES list
           - Use note_index to look up the name
           - NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        5. Return a string combining note_name and octave
           - Format: "C4", "D#5", etc.
           - Use f-string: f"{note_name}{octave}"

    EXAMPLE:
        midi_to_note_name(60) should return "C4" (Middle C)
        midi_to_note_name(61) should return "C#4"
        midi_to_note_name(72) should return "C5"

    VARIABLES TO USE:
        - NOTE_NAMES: List of 12 note names in order

    RETURNS:
        String like "C4", "D#5", etc. or None if midi_num is invalid
    """
    # YOUR CODE HERE
    pass


def load_midi_file(filepath):
    """
    *** YOU NEED TO IMPLEMENT THIS FUNCTION! ***

    Loads a MIDI file and converts it to a list of notes with timestamps

    PARAMETERS:
        filepath: String path to the MIDI file (e.g., "assets/song.mid")

    WHAT YOU NEED TO DO:
        1. Use try-except to handle errors when loading the file
           - try: mid = mido.MidiFile(filepath)
           - except: print error message and return False

        2. Initialize an empty list for playback_messages
           - This will store all the notes from the MIDI file

        3. Create a variable current_time_sec = 0.0
           - This tracks the current time as we read through the MIDI file

        4. Loop through all messages in the MIDI file:
           for msg in mid:

        5. For each message:
           a. Add msg.time to current_time_sec (accumulate time)
           b. Check if it's a note_on message with velocity > 0
              - msg.type == "note_on" means a key was pressed
              - msg.velocity > 0 means it's not a note_off
           c. If it is a note_on:
              - Get note_name using midi_to_note_name(msg.note)
              - Get velocity from msg.velocity (how hard key was pressed)
              - Check if note_name is in black_note_map or white_note_map
              - Get the index from the appropriate map
              - Set note_type to "black" or "white"
              - Append to playback_messages: (time_in_ms, index, note_type, velocity)
                * time_in_ms = current_time_sec * 1000

        6. Reset playback variables:
           - current_msg_index = 0
           - playback_active = False

        7. Print how many notes were loaded

        8. Return True if successful

    VARIABLES TO USE:
        - playback_messages: Global list to store notes
        - current_msg_index: Global variable for playback position
        - playback_active: Global flag for whether playback is active
        - black_note_map: Dictionary mapping note names to black key indices
        - white_note_map: Dictionary mapping note names to white key indices

    IMPORTANT:
        - Don't forget to use 'global' keyword for global variables!
        - global playback_messages, current_msg_index, playback_active

    RETURNS:
        True if file loaded successfully, False if there was an error
    """
    # YOUR CODE HERE
    pass


def find_first_note_after(time_ms):
    """
    *** YOU NEED TO IMPLEMENT THIS FUNCTION! ***

    Finds the index of the first note at or after a given time
    Used for seeking to a specific point in MIDI playback

    PARAMETERS:
        time_ms: Time in milliseconds to search for

    WHAT YOU NEED TO DO:
        1. Check if playback_messages is empty
           - If empty, return 0

        2. Loop through playback_messages with enumerate():
           for i, msg in enumerate(playback_messages):
           - enumerate gives you both the index (i) and the message (msg)

        3. Get the timestamp from the message
           - msg_time = msg[0]  (first element is the timestamp)

        4. Check if msg_time is >= time_ms
           - If yes, return i (the index)
           - This is the first note at or after the requested time

        5. If no note is found (loop completes), return len(playback_messages)
           - This means we're past the end of the song

    EXAMPLE:
        If playback_messages has notes at times [1000, 2000, 3000, 4000]
        find_first_note_after(2500) should return 2 (the note at 3000ms)
        find_first_note_after(5000) should return 4 (past the end)

    VARIABLES TO USE:
        - playback_messages: Global list of notes with timestamps

    RETURNS:
        Integer index of the first note found, or length of playback_messages if none found
    """
    # YOUR CODE HERE
    pass


def play_note_with_limiter(sound_to_play, velocity):
    """
    *** YOU NEED TO IMPLEMENT THIS FUNCTION! ***

    Plays a piano note with dynamic volume limiting
    Prevents distortion when many notes play simultaneously

    PARAMETERS:
        sound_to_play: pygame.mixer.Sound object to play
        velocity: Note velocity (0-127), controls how loud the note is
                  127 = loudest (forte), 64 = medium, 1 = softest (piano)

    WHAT YOU NEED TO DO:
        1. Count how many notes are currently playing
           - num_playing = len(g_active_channels)

        2. Calculate the limiter_factor (volume reduction)
           - Start with limiter_factor = 1.0 (no reduction)
           - If num_playing > LIMITER_THRESHOLD:
             * ratio = LIMITER_THRESHOLD / num_playing
             * limiter_factor = sqrt(ratio)
             * This smoothly reduces volume as more notes play

        3. Calculate velocity_factor (how hard the key was pressed)
           - velocity_factor = velocity / 127.0
           - This converts 0-127 range to 0.0-1.0 range

        4. Calculate final_volume
           - final_volume = (BASE_NOTE_VOLUME * limiter_factor) * velocity_factor
           - Combines all three factors: base volume, limiter, and velocity

        5. Find an available audio channel
           - channel = pygame.mixer.find_channel()
           - Returns None if all channels are busy

        6. If channel is not None:
           - Set the channel's volume: channel.set_volume(final_volume)
           - Play the sound: channel.play(sound_to_play)
           - Add channel to g_active_channels list

        7. If channel is None (all channels busy):
           - Print a warning message
           - The note will be dropped (not played)

    HOW THE LIMITER WORKS:
        - Without limiter: 20 notes at full volume = distortion and clipping
        - With limiter: Volume automatically reduces when many notes play
        - Uses square root (sqrt) for smooth, musical volume reduction

    EXAMPLE:
        If 8 notes are playing (below threshold of 16):
            limiter_factor = 1.0 (no reduction)
        If 32 notes are playing:
            ratio = 16/32 = 0.5
            limiter_factor = sqrt(0.5) ≈ 0.707 (about 30% quieter)

    VARIABLES TO USE:
        - g_active_channels: Global list of active channels
        - LIMITER_THRESHOLD: Maximum notes before volume reduction (16)
        - BASE_NOTE_VOLUME: Base volume level (0.6)

    PYGAME FUNCTIONS:
        - pygame.mixer.find_channel(): Finds an available audio channel
        - channel.set_volume(volume): Sets volume (0.0 to 1.0)
        - channel.play(sound): Plays a sound on the channel

    MATH FUNCTIONS:
        - sqrt(x): Square root function (already imported from math)

    IMPORTANT:
        - Don't forget 'global g_active_channels' at the start!

    RETURNS:
        Nothing (plays sound as a side effect)
    """
    # YOUR CODE HERE
    pass


# ===================================================================================
# DRAWING FUNCTIONS (ALREADY IMPLEMENTED - DON'T MODIFY!)
# ===================================================================================


def draw_piano(whites, blacks):
    """
    Draws the piano keyboard with white and black keys
    Shows visual feedback when keys are pressed
    """
    white_rects = []

    # Draw all 52 white keys
    for i in range(52):
        rect = pygame.draw.rect(screen, "white", [i * 35, HEIGHT - 300, 35, 300], 0, 2)
        white_rects.append(rect)
        pygame.draw.rect(screen, "black", [i * 35, HEIGHT - 300, 35, 300], 2, 2)
        key_label = small_font.render(white_notes[i], True, "black")
        screen.blit(key_label, (i * 35 + 3, HEIGHT - 20))

    # Draw 36 black keys with special spacing pattern
    skip_count = 0
    last_skip = 2
    skip_track = 2
    black_rects = []

    for i in range(36):
        rect = pygame.draw.rect(
            screen,
            "black",
            [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200],
            0,
            2,
        )

        # Check if this black key is active (being pressed)
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(
                        screen,
                        "green",
                        [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200],
                        2,
                        2,
                    )
                    blacks[q][1] -= 1

        key_label = real_small_font.render(black_labels[i], True, "white")
        screen.blit(key_label, (25 + (i * 35) + (skip_count * 35), HEIGHT - 120))
        black_rects.append(rect)

        # Skip pattern: 2 blacks, gap, 3 blacks, gap, repeat
        skip_track += 1
        if last_skip == 2 and skip_track == 3:
            last_skip = 3
            skip_track = 0
            skip_count += 1
        elif last_skip == 3 and skip_track == 2:
            last_skip = 2
            skip_track = 0
            skip_count += 1

    # Highlight active white keys
    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            pygame.draw.rect(screen, "green", [j * 35, HEIGHT - 100, 35, 100], 2, 2)
            whites[i][1] -= 1

    return white_rects, black_rects, whites, blacks


def draw_hands(rightOct, leftOct, rightHand, leftHand):
    """
    Draws hand position indicators showing which keyboard letters play which notes
    """
    # Left hand indicator
    pygame.draw.rect(
        screen, "dark gray", [(leftOct * 245) - 175, HEIGHT - 60, 245, 30], 0, 4
    )
    pygame.draw.rect(
        screen, "black", [(leftOct * 245) - 175, HEIGHT - 60, 245, 30], 4, 4
    )

    # Draw white key letters for left hand
    text = small_font.render(leftHand[0], True, "white")
    screen.blit(text, ((leftOct * 245) - 165, HEIGHT - 55))
    text = small_font.render(leftHand[2], True, "white")
    screen.blit(text, ((leftOct * 245) - 130, HEIGHT - 55))
    text = small_font.render(leftHand[4], True, "white")
    screen.blit(text, ((leftOct * 245) - 95, HEIGHT - 55))
    text = small_font.render(leftHand[5], True, "white")
    screen.blit(text, ((leftOct * 245) - 60, HEIGHT - 55))
    text = small_font.render(leftHand[7], True, "white")
    screen.blit(text, ((leftOct * 245) - 25, HEIGHT - 55))
    text = small_font.render(leftHand[9], True, "white")
    screen.blit(text, ((leftOct * 245) + 10, HEIGHT - 55))
    text = small_font.render(leftHand[11], True, "white")
    screen.blit(text, ((leftOct * 245) + 45, HEIGHT - 55))

    # Draw black key letters for left hand
    text = small_font.render(leftHand[1], True, "black")
    screen.blit(text, ((leftOct * 245) - 148, HEIGHT - 55))
    text = small_font.render(leftHand[3], True, "black")
    screen.blit(text, ((leftOct * 245) - 113, HEIGHT - 55))
    text = small_font.render(leftHand[6], True, "black")
    screen.blit(text, ((leftOct * 245) - 43, HEIGHT - 55))
    text = small_font.render(leftHand[8], True, "black")
    screen.blit(text, ((leftOct * 245) - 8, HEIGHT - 55))
    text = small_font.render(leftHand[10], True, "black")
    screen.blit(text, ((leftOct * 245) + 27, HEIGHT - 55))

    # Right hand indicator
    pygame.draw.rect(
        screen, "dark gray", [(rightOct * 245) - 175, HEIGHT - 60, 245, 30], 0, 4
    )
    pygame.draw.rect(
        screen, "black", [(rightOct * 245) - 175, HEIGHT - 60, 245, 30], 4, 4
    )

    # Draw white key letters for right hand
    text = small_font.render(rightHand[0], True, "white")
    screen.blit(text, ((rightOct * 245) - 165, HEIGHT - 55))
    text = small_font.render(rightHand[2], True, "white")
    screen.blit(text, ((rightOct * 245) - 130, HEIGHT - 55))
    text = small_font.render(rightHand[4], True, "white")
    screen.blit(text, ((rightOct * 245) - 95, HEIGHT - 55))
    text = small_font.render(rightHand[5], True, "white")
    screen.blit(text, ((rightOct * 245) - 60, HEIGHT - 55))
    text = small_font.render(rightHand[7], True, "white")
    screen.blit(text, ((rightOct * 245) - 25, HEIGHT - 55))
    text = small_font.render(rightHand[9], True, "white")
    screen.blit(text, ((rightOct * 245) + 10, HEIGHT - 55))
    text = small_font.render(rightHand[11], True, "white")
    screen.blit(text, ((rightOct * 245) + 45, HEIGHT - 55))

    # Draw black key letters for right hand
    text = small_font.render(rightHand[1], True, "black")
    screen.blit(text, ((rightOct * 245) - 148, HEIGHT - 55))
    text = small_font.render(rightHand[3], True, "black")
    screen.blit(text, ((rightOct * 245) - 113, HEIGHT - 55))
    text = small_font.render(rightHand[6], True, "black")
    screen.blit(text, ((rightOct * 245) - 43, HEIGHT - 55))
    text = small_font.render(rightHand[8], True, "black")
    screen.blit(text, ((rightOct * 245) - 8, HEIGHT - 55))
    text = small_font.render(rightHand[10], True, "black")
    screen.blit(text, ((rightOct * 245) + 27, HEIGHT - 55))


def draw_title_bar():
    """
    Draws the title bar with instructions and logo
    """
    instruction_text = medium_font.render(
        "Up/Down Arrows Change Left Hand", True, "black"
    )
    screen.blit(instruction_text, (WIDTH - 500, 10))

    instruction_text2 = medium_font.render(
        "Left/Right Arrows Change Right Hand", True, "black"
    )
    screen.blit(instruction_text2, (WIDTH - 500, 50))

    img = pygame.transform.scale(pygame.image.load("assets/logo.png"), [150, 150])
    screen.blit(img, (0, -34))

    title_text = font.render("A Project of the Resonance Committee.", True, "white")
    screen.blit(title_text, (298, 18))
    title_text = font.render("A Project of the Resonance Committee.", True, "black")
    screen.blit(title_text, (300, 20))


# ===================================================================================
# MAIN GAME LOOP
# ===================================================================================
run = True
while run:
    # Create keyboard mapping dictionaries for current octaves
    # These map keyboard letters to note names with octave numbers
    left_dict = {
        "Z": f"C{left_oct}",
        "S": f"C#{left_oct}",
        "X": f"D{left_oct}",
        "D": f"D#{left_oct}",
        "C": f"E{left_oct}",
        "V": f"F{left_oct}",
        "G": f"F#{left_oct}",
        "B": f"G{left_oct}",
        "H": f"G#{left_oct}",
        "N": f"A{left_oct}",
        "J": f"A#{left_oct}",
        "M": f"B{left_oct}",
    }
    right_dict = {
        "R": f"C{right_oct}",
        "5": f"C#{right_oct}",
        "T": f"D{right_oct}",
        "6": f"D#{right_oct}",
        "Y": f"E{right_oct}",
        "U": f"F{right_oct}",
        "8": f"F#{right_oct}",
        "I": f"G{right_oct}",
        "9": f"G#{right_oct}",
        "O": f"A{right_oct}",
        "0": f"A#{right_oct}",
        "P": f"B{right_oct}",
    }

    timer.tick(fps)  # Control frame rate
    screen.fill("gray")  # Clear screen with gray background

    # Remove finished audio channels from tracking list
    g_active_channels = [ch for ch in g_active_channels if ch.get_busy()]

    # ===================================================================================
    # MIDI PLAYBACK LOGIC
    # ===================================================================================
    # This section plays notes from a MIDI file automatically
    if playback_active and current_msg_index < len(playback_messages):
        now_ms = pygame.time.get_ticks() - playback_start_time

        while current_msg_index < len(playback_messages):
            msg_time_ms, index, note_type, velocity = playback_messages[
                current_msg_index
            ]
            if now_ms >= msg_time_ms:
                sound_to_play = None
                if note_type == "black":
                    sound_to_play = black_sounds[index]
                    active_blacks.append([index, 30])
                else:
                    sound_to_play = white_sounds[index]
                    active_whites.append([index, 30])

                if sound_to_play:
                    play_note_with_limiter(sound_to_play, velocity)

                current_msg_index += 1
            else:
                # This note is in the future, stop checking for now
                break

        if current_msg_index >= len(playback_messages):
            print("Playback finished.")
            playback_active = False
            playback_start_time = 0

    # ===================================================================================
    # DRAWING - Render everything to screen
    # ===================================================================================
    white_keys, black_keys, active_whites, active_blacks = draw_piano(
        active_whites, active_blacks
    )
    draw_hands(right_oct, left_oct, right_hand, left_hand)
    draw_title_bar()

    # ===================================================================================
    # EVENT HANDLING - Process user input
    # ===================================================================================
    for event in pygame.event.get():
        # Quit if window is closed
        if event.type == pygame.QUIT:
            run = False

        # Handle mouse clicks on piano keys
        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            # Check black keys first (they're on top)
            for i in range(len(black_keys)):
                if black_keys[i].collidepoint(event.pos):
                    play_note_with_limiter(black_sounds[i], 127)
                    black_key = True
                    active_blacks.append([i, 30])
            # Check white keys if no black key was clicked
            for i in range(len(white_keys)):
                if white_keys[i].collidepoint(event.pos) and not black_key:
                    play_note_with_limiter(white_sounds[i], 127)
                    active_whites.append([i, 30])

        # Handle keyboard text input (letter keys)
        if event.type == pygame.TEXTINPUT:
            # Check if left hand key was pressed
            if event.text.upper() in left_dict:
                if left_dict[event.text.upper()][1] == "#":
                    index = black_labels.index(left_dict[event.text.upper()])
                    play_note_with_limiter(black_sounds[index], 127)
                    active_blacks.append([index, 30])
                else:
                    index = white_notes.index(left_dict[event.text.upper()])
                    play_note_with_limiter(white_sounds[index], 127)
                    active_whites.append([index, 30])
            # Check if right hand key was pressed
            if event.text.upper() in right_dict:
                if right_dict[event.text.upper()][1] == "#":
                    index = black_labels.index(right_dict[event.text.upper()])
                    play_note_with_limiter(black_sounds[index], 127)
                    active_blacks.append([index, 30])
                else:
                    index = white_notes.index(right_dict[event.text.upper()])
                    play_note_with_limiter(white_sounds[index], 127)
                    active_whites.append([index, 30])

        # Handle special key presses (arrow keys, spacebar)
        if event.type == pygame.KEYDOWN:
            # SPACEBAR: Load and play/pause MIDI file
            if event.key == pygame.K_SPACE:
                # Load MIDI file on first press
                if not midi_loaded:
                    print(f"Loading {midi_file_path}...")
                    if load_midi_file(midi_file_path):
                        print("MIDI file loaded.")
                        midi_loaded = True
                    else:
                        print(f"Could not load {midi_file_path}")
                        continue

                # Toggle play/pause/restart
                if midi_loaded:
                    if not playback_active:
                        # Start or restart playback
                        playback_active = True

                        if current_msg_index == 0 or current_msg_index >= len(
                            playback_messages
                        ):
                            # Starting fresh or restarting
                            START_MS = playback_start_time
                            print(
                                f"Starting/Restarting playback from {START_MS / 1000.0:.2f}s..."
                            )
                            current_msg_index = find_first_note_after(START_MS)
                            playback_start_time = pygame.time.get_ticks() - START_MS
                        else:
                            # Resuming from pause
                            msg_time_ms_to_resume_at = playback_messages[
                                current_msg_index
                            ][0]
                            playback_start_time = (
                                pygame.time.get_ticks() - msg_time_ms_to_resume_at
                            )
                            print(
                                f"Resuming playback from {msg_time_ms_to_resume_at / 1000.0:.2f}s"
                            )
                    else:
                        # Pause playback
                        print("Pausing playback.")
                        playback_active = False

            # Arrow keys: Change octaves for left and right hands
            if event.key == pygame.K_RIGHT:
                if right_oct < 8:
                    right_oct += 1
            if event.key == pygame.K_LEFT:
                if right_oct > 0:
                    right_oct -= 1
            if event.key == pygame.K_UP:
                if left_oct < 8:
                    left_oct += 1
            if event.key == pygame.K_DOWN:
                if left_oct > 0:
                    left_oct -= 1

    # Update the display
    pygame.display.flip()

# Clean up and exit
pygame.quit()
