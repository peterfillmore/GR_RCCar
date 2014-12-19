GR_RCCar
========

Gnuradio implementation for cheap remote control cars
This contains the source code for the gr-rccar2 gnuradio blocks that can control 27MHz RC cars

Idea behind this is to show how to transmit using the hackRF and other SDRs that can transmit.

Feel free to hack around with this - it probably needs a lot of work.

Compiling
=========
normal building of out of tree modules for gnuradio
http://gnuradio.org/redmine/projects/gnuradio/wiki/OutOfTreeModules

cd ./gr-rccar2/build
cmake ../
make
make install

Installing
==========
Copy the xml blocks into your chosen gnuradio-companion folder i.e:
on my mac this is:
cp ./gr-rccar2/examples/*.xml ~/.grc_gnuradio/

Issues
======
Probably many - key one is that signals generated are not "clean" - as in the car shudders due to commands being switched on and off.
Untested on other platforms - since i can't be bothered - test it your self.
Any problems you spot - send a pull request! - happy to accept changes.:w


