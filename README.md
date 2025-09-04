# Installation
### Prerequisites
* miniconda, flask
* npm, midi-player-js
* gunicorn, openssl
    * This command creats an ssl certificate, 
    * -nodes no DES, so without asking password, 
    * certificate.pem.local is the name i chose for the file that holds certificants, and key.pem.local name of file. Days is how many days is valid
    * openssl req -x509 -newkey rsa:4096 -nodes -out certificate.pem.local -keyout key.pem.local -days 10

* then, after installing gunicorn using conda install gunicorn in your conda env, run
*  sudo /home/<your_user>/miniconda3/envs/yourenv/bin/gunicorn  --certfile=./certificate.pem.local --keyfile=./key.pem.local -b 127.0.0.1:443 --log-level debug app:app


*  sudo /home/gaby/miniconda3/envs/musica/bin/gunicorn  --certfile=certificate.pem.local --keyfile=key.pem.local -b 127.0.0.1 --log-level debug app:app





# summer_reu_2022

#### Digital Humanities (Musical Analysis and Visualization of Melodic and Harmonic Content.) <br />
#### Python 3.x is mandatory for this project.

#### Main html reference to repository: <br />
https://github.com/randycone/summer_reu_2022.git

./data/ &emsp; Contains JS Bach Image files

./musicxml/ &emsp;     Contains musicxml data files for analysis

./NoteClass/ &emsp;    Mandatory Class for most programs using this repository.

#### Once you've pulled/cloned this repository, try running the following commands from the console: <br />
cd ./summer_reu_2022 <br />
python wtc1_bach_central_dots_score_visualiser.py <br />

#### This should generate the visualization file: <br />
wtc1_bach_dots_visualisation.svg <br />
Which can be opened in Google Chrome (or GIMP or Inkscape). <br />

#### The latter should also work similarly with: <br />
python wtc2_bach_central_dots_score_visualiser.py

#### NOTE: <br />
#### You can watch this process happen more slowly, with description of musical data via: <br />
python wtc1_bach_central_dots_score_visualiser.py | more

## ScoreParserClass2 is the editted Score parser to be able to use harmony class

Harmony class! things you should know

for each part, it has key_change, which contains  a dictionary of the harmony graph, the chords and 
scales of the key of the voice. If the score has 2 key changes, then key_change will have 2 elements,
one for each key signature. 
Time_change_ is similar to key_change, but the difference is that its for time signatures. 
Both have starting measure ending measure. 

Its repetition of data, but I made it so, so it can be parallelizable with their own datasets

Currently there is no code to manage 2 or more key_changes/time_change

Everything else is commented. 

## This one would generate the harmony detection for SATB
python svg_creation_for_harmony_class.py




