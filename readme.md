***NOTE:* This was the original version of UTurn; since, it has been ported to a [MediaWiki extension](https://github.com/berkmancenter/wiki-uturn). Please use that version instead.**

# UTurn

## Version

0.1

*Still in beta, use at your own risk*

## About

There are many MediaWiki installs which are created and then forgotten: wiki's made for classes, a project that is later abandoned, etc. If that wiki has open registration, it is very likely that spam bots may register and start spanning the wiki. Due to the lack of moderators, spam accumulates degrades the quality of the wiki.

Right now, a lot of MediaWiki extensions and functionaility are focused on preventing this: you can lock pages, close registration and make database backups to restore to. But there doesn't seem to be a whole lot to try and cure the problem once a spammed wiki is uncovered. Granted, you can [nuke](http://www.mediawiki.org/wiki/Extension:Nuke) users, but even nuke isn't well equipped to mitigate the effect of an army of spam bots. 

UTurn tries to help those forgotten wikis by adding a way to turn back a wiki to a previous point in time.

## Implementation Details

When designing UTurn, one of the first problems that came up was restoring an entire wiki could take a while; especially when considering large wikis, it is not that difficult to imagine the script taking longer than 30 seconds, PHP's default maximum execution time. Rather than try to modify the PHP max execution time, or split up the task into multiple requests - I decided to use a language which I considered more apt for the task: Python.

Currently, UTurn is implemented as a Python script that queries the MediaWiki API.

When you run UTurn it will ask for 3 seperate values:

1. The URL to the wiki API, for example if you installed MediaWiki on example.com, the API is typically at example.com/api.php. It should be noted that this changes, for example, at the time of this writing, Wikipedia's API was loacated at `wikipedia.org/w/api.php`.

2. A Username/Password for a sysop account

3. The time in UTC to return to (UTurn will ask you for the year, month, day, hour, minute, second - if the hour, minute, second don't matter to you, simply fill in 0 for each one of them).

At that point it will proceed to revert all the pages, printing the title of each page as it completes restoring that page. (Note: the pages are done in alphabetical order)

Once it finished the program closes rather unceremoniously, however in every affected page you should see the newest revision is made by the sysop account and has the summary `UTurn to XYZ`, where `XYZ` is the timestamp it reverted to.

*Note: UTurn only affects pages in the main namespace (e.g. no special pages or talk pages).*

*Also Note: UTurn does modify user accounts nor does it delete pages which didn't exist before the date (rather it removes all their content).*

*Lastly Note: Because UTurn does not delete pages or edit revision history, UTurns can be UTurned. I.E. If you UTurn to a date, and then realize you actually didn't want to do that UTurn, simply UTurn to the hour before you UTurned.*

## Installation

1. Get [python](http://www.python.org) (2.7).

2. Download UTurn to YOUR local machine.

3. Add the following to the wiki's `LocalSettings.php`:

```
# Enable the write api (so we can make edits through the API)
$wgEnableAPI = true;
$wgEnableWriteAPI = true;

# Disable writeapi rights for everyone (so no one can use the write API)
$wgGroupPermissions['*']['writeapi'] = false;

# Re-enable writeapi for sysops, so that only their accounts can use the write API
$wgGroupPermissions['sysop']['writeapi'] = true;
$wgGroupPermissions['sysop']['noratelimit'] = true;
$wgGroupPermissions['sysop']['apihighlimits'] = true;
```

## Use

1. Navigate to the folder in which you downloaded UTurn. 

2. Run `UTurn.py`.

*N.B. It will ask for a username/password, that user MUST be a sysop.*

## Use of 3rd-party software

UTurn wouldn't be possible if it weren't for the following libraries:

* simplemediawiki.py: critical in connecting to the mediawiki API - LGPLv2.1+ Licensed
* kitchen: used by simplemediawiki - LGPLv2+

## License

Copyright President and Fellows of Harvard College, 2012

Licensed under an MIT License (included)