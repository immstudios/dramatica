# Dramatica

Dramatica is a [Nebula 5](https://github.com/nebulabroadcast/nebula) plugin for automated rundown creation.

Usage
-----

As a `solver` plugin, Dramatica replaces rundown placeholders with assets according to
given rules.
Solving can be triggered manually (hybrid micro-scheduling mode) using [Firefly](https://github.com/nebulabroadcast/firefly)
or automatically using CRON or worker services (autonomous channels).


### Current features

Dramatica currently takes in account following features:

 - Run count
 - Distance from last run
 - Genre
 - Editorial format
 - Song performer and album
 - Music tempo (BPM)
 - Asset validity (QC State)
 - Content alert scheme (Parental guidance rating)

### Limitations

Following features are not supported yet (but they are planned)

 - Per block feature preference
 - Taking `intention` in account
 - Taking `atmosphere` in account
 - Taking `intended_audience` in account
 - Taking automatically extracted metadata (overal color tone, edit rate...) in account
 - Subclips
 - Series planning
 - Commercials
 - Scheduling placeholders (for trailers)
 - Scheduling according broadcast time instad of scheduled time
   (current limitation of Nebula solver architecture.

Installation
------------

1. Clone this repository to `.nx/scripts/v5/solver` directory
2. Copy `examples/dramatica.json` to `.nx/dramatica.json` and tweak the rules to match your needs.
3. Add `dramatica` to the `solvers` list of your playout channel configuration

### Requirements

Dramatica uses default Nebula metadata types extensively.
It assumes [EBUCore](https://tech.ebu.ch/MetadataEbuCore) classification schemes are used (Nebula default),
but similar structure should also work.

Following configuration is required

 - `genre` and `editorial_format` types must be of `SELECT` class. `LIST` will not work.
 - `content_alert/scheme` is supported to disallow scheduling inappropriate content
    during the day. Currently only a few stadards are implemented (czech, danish,...)
