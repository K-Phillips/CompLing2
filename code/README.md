In general, the TNT_tagging.py code is run first, followed by tag_improver.py. 

The tag_dictionary_generator.py is called by the tag_improver, and doesn't run on its own.

These files must be modified, inside the .py file, to run on different files.

tagger_scoring.py and unknown_counter.py evaluate the model.

The other variants are modifications of these core files to test other experiments.
