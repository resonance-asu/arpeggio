# 🎹 Arpeggio - Virtual Piano Project

**A Project of the Resonance Committee**

An educational programming assignment where you'll implement core functionality for a virtual piano application using Python and Pygame.

---

## 📋 Overview

This is a freshman-level programming project where you'll complete a partially-implemented virtual piano application. The visual interface is already built for you - your job is to implement the core logic functions that make the piano interactive and capable of playing MIDI files.

**Estimated Time:** 4-6 hours  
**Difficulty:** Intermediate  
**Topics Covered:** Functions, File I/O, Audio Processing, Algorithm Implementation

---

## 🎯 Learning Objectives

By completing this project, you will:
- ✅ Practice implementing functions from detailed specifications
- ✅ Work with audio libraries (pygame.mixer)
- ✅ Parse and process MIDI files using the mido library
- ✅ Implement search algorithms (binary search concepts)
- ✅ Apply mathematical concepts (square root for audio limiting)
- ✅ Handle file I/O with proper error handling
- ✅ Work with global variables and understand scope

---

## 📦 What's Already Done For You

The following components are **fully implemented** - you don't need to modify these:

- ✅ **Complete Visual Interface** - All drawing functions (`draw_piano`, `draw_hands`, `draw_title_bar`)
- ✅ **Event Handling** - Mouse clicks, keyboard input, arrow keys
- ✅ **Main Game Loop** - Display updates, frame rate control
- ✅ **Audio File Loading** - All 88 piano note sound files are loaded
- ✅ **User Interface** - Instructions, logo, hand position indicators
- ✅ **MIDI Playback Logic** - The playback system in the main loop

---

## 🔨 Your Assignment: Implement 4 Functions

You need to implement the following functions in the template file:

### 1. `midi_to_note_name(midi_num)` 
**Purpose:** Convert MIDI note numbers (0-127) to musical note names like "C4" or "A#5"

**What You'll Learn:**
- Integer division and modulo operations
- List indexing
- String formatting with f-strings

**Difficulty:** ⭐ Easy

---

### 2. `load_midi_file(filepath)`
**Purpose:** Load a MIDI file and convert it to a list of playable notes with timestamps

**What You'll Learn:**
- File I/O with error handling (try-except)
- Working with external libraries (mido)
- Parsing file formats
- Building data structures (lists of tuples)
- Dictionary lookups

**Difficulty:** ⭐⭐⭐ Medium

---

### 3. `find_first_note_after(time_ms)`
**Purpose:** Search through notes to find the first note at or after a given timestamp

**What You'll Learn:**
- Linear search algorithms
- Working with sorted data
- Loop control (break statements)
- Edge case handling

**Difficulty:** ⭐⭐ Easy-Medium

---

### 4. `play_note_with_limiter(sound_to_play, velocity)`
**Purpose:** Play piano notes with intelligent volume control to prevent audio distortion

**What You'll Learn:**
- Audio channel management
- Dynamic volume calculations
- Using mathematical functions (square root)
- Conditional logic
- Working with pygame.mixer

**Difficulty:** ⭐⭐ Medium

---

## 🚀 Getting Started

### Step 1: Set Up Your Environment

1. **Install Python 3.7+** if you haven't already
2. **Install required packages:**
   ```bash
   pip install pygame mido
   ```

### Step 2: Download the Project Files

Your project should have this structure:
```
arpeggio-piano/
├── main.py                  # Your template file (implement functions here)
├── piano_lists.py           # Note mappings (already complete)
├── pyproject.toml           # Package dependencies
└── assets/
    ├── Terserah.ttf        # Font file
    ├── logo.png            # Logo image
    ├── notes/              # Piano sound files (88 .wav files)
    │   ├── C0.wav
    │   ├── C#0.wav
    │   └── ... (88 total)
    └── MIDI/               # MIDI files for playback
        └── Thomas_Bergersen_-_Made_of_Air_(2_Pianos).mid
```

### Step 3: Read the Documentation

Open `main.py` and read through:
- The extensive comments explaining each variable
- The detailed function specifications
- The examples provided for each function

### Step 4: Implement the Functions

Work on the functions in this recommended order:

1. **Start with `midi_to_note_name()`** - It's the easiest and will help you understand the note naming system
2. **Then do `find_first_note_after()`** - Practice with list searching
3. **Next tackle `play_note_with_limiter()`** - Learn audio management
4. **Finally implement `load_midi_file()`** - The most complex function that ties everything together

### Step 5: Test Your Implementation

After implementing each function, test it:

```python
# Test midi_to_note_name
print(midi_to_note_name(60))  # Should print "C4" (Middle C)
print(midi_to_note_name(61))  # Should print "C#4"

# Test the piano by running the program
python main.py
```

---

## 🎮 Controls (Once Implemented)

### Keyboard Controls:
**Left Hand (Octave 4 by default):**
- `Z` = C
- `S` = C#
- `X` = D
- `D` = D#
- `C` = E
- `V` = F
- `G` = F#
- `B` = G
- `H` = G#
- `N` = A
- `J` = A#
- `M` = B

**Right Hand (Octave 5 by default):**
- `R` = C
- `5` = C#
- `T` = D
- `6` = D#
- `Y` = E
- `U` = F
- `8` = F#
- `I` = G
- `9` = G#
- `O` = A
- `0` = A#
- `P` = B

### Special Keys:
- **↑/↓ Arrow Keys** - Change left hand octave
- **←/→ Arrow Keys** - Change right hand octave
- **Spacebar** - Play/Pause/Resume MIDI playback
- **Mouse Click** - Click any piano key to play it

---

## 📝 Function Implementation Tips

### For `midi_to_note_name()`:
```python
# Remember: There are 12 notes per octave
# MIDI note 0 = C-1, note 12 = C0, note 24 = C1, etc.
# Use // for integer division and % for remainder
```

### For `load_midi_file()`:
```python
# Don't forget the global keyword!
global playback_messages, current_msg_index, playback_active

# Use try-except to catch file errors
try:
    mid = mido.MidiFile(filepath)
except Exception as e:
    print(f"Error: {e}")
    return False
```

### For `find_first_note_after()`:
```python
# Remember: msg[0] is the timestamp
# Use enumerate() to get both index and message
for i, msg in enumerate(playback_messages):
    if msg[0] >= time_ms:
        return i
```

### For `play_note_with_limiter()`:
```python
# The limiter prevents audio clipping when many notes play
# Volume formula: (BASE_VOLUME * limiter_factor) * velocity_factor
# Use sqrt() from math module for smooth volume reduction
```

---

## ✅ Testing Checklist

Once you've implemented all functions, verify:

- [ ] Program runs without errors
- [ ] Clicking piano keys with mouse produces sound
- [ ] Typing keyboard letters plays notes
- [ ] Arrow keys change octaves (indicators move)
- [ ] Keys light up green when pressed
- [ ] Spacebar loads MIDI file (check console output)
- [ ] Spacebar starts/pauses MIDI playback
- [ ] MIDI notes play automatically during playback
- [ ] Multiple notes can play simultaneously without distortion

---

## 🐛 Common Issues & Solutions

### "No module named 'pygame'" or "No module named 'mido'"
**Solution:** Install the packages:
```bash
pip install pygame mido
```

### "FileNotFoundError: assets/notes/C0.wav"
**Solution:** Make sure the `assets/` folder is in the same directory as `main.py`

### "NameError: name 'playback_messages' is not defined"
**Solution:** Add `global playback_messages` at the start of your function

### No sound when clicking keys
**Solution:** 
- Check that `play_note_with_limiter()` is fully implemented
- Verify you're calling `channel.play(sound_to_play)`
- Make sure your system volume is up

### MIDI file won't load
**Solution:**
- Check that `load_midi_file()` is fully implemented
- Verify the MIDI file exists in `assets/MIDI/`
- Check the console for error messages

---

## 📚 Resources

### Python Documentation:
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [List Comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Exception Handling](https://docs.python.org/3/tutorial/errors.html)

### Library Documentation:
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame Mixer](https://www.pygame.org/docs/ref/mixer.html)
- [Mido MIDI Library](https://mido.readthedocs.io/)

### Music Theory:
- [MIDI Note Numbers](https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies)
- [Musical Note Names](https://en.wikipedia.org/wiki/Musical_note)

---

## 🎓 Grading Rubric (Example)

| Component | Points | Criteria |
|-----------|--------|----------|
| `midi_to_note_name()` | 15 | Correctly converts MIDI numbers to note names |
| `find_first_note_after()` | 15 | Properly searches and returns correct index |
| `play_note_with_limiter()` | 30 | Plays sounds with proper volume limiting |
| `load_midi_file()` | 30 | Successfully loads and parses MIDI files |
| Code Quality | 10 | Clean code, proper comments, follows style |
| **Total** | **100** | |

---

## 💡 Extension Ideas (Extra Credit)

Once you've completed the basic assignment, try these challenges:

1. **Add Recording Feature** - Record what the user plays and save it as a MIDI file
2. **Volume Control** - Add slider to adjust overall volume
3. **More MIDI Files** - Load different songs from a menu
4. **Visual Note Display** - Show falling notes like Guitar Hero
5. **Pedal Simulation** - Implement sustain pedal (hold notes longer)
6. **Metronome** - Add a visual/audio beat counter
7. **Chord Detection** - Display what chord is being played

---

## 👥 Getting Help

If you're stuck:

1. **Read the documentation** in the template file carefully
2. **Check the variable summary** at the bottom of the file
3. **Use print statements** to debug your code
4. **Test functions individually** before running the whole program
5. **Ask your instructor or TA** during office hours
6. **Search the error message** on Google or Stack Overflow

---

## 📄 Submission Guidelines

When you're ready to submit:

1. **Test thoroughly** - Run through the testing checklist above
2. **Comment your code** - Explain your logic
3. **Submit only `main.py`** - Don't modify other files
4. **Include a brief writeup** (optional):
   - Which function was hardest?
   - What did you learn?
   - How long did it take?

---

## 🏆 Success Criteria

You'll know you're successful when:
- ✅ All 4 functions are implemented
- ✅ The program runs without errors
- ✅ You can play notes with mouse and keyboard
- ✅ MIDI playback works correctly
- ✅ Audio doesn't distort with many simultaneous notes
- ✅ You understand how each function works

---

## 📞 Contact

**Phase:** Introduction to Programming
**Instructors:** 
- Seif Zakaria
- Ahmed Khalid
- Bishoy Ehab
- Mohamed Nasser

**A Project of the Resonance Committee**

---

Good luck, and happy coding! 🎹🎵
