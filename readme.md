[![McMUN logo](http://www.mcmun.org/static/img/logo.png)](http://www.mcmun.org)

McMUN 2013
==========

This is the source for [the McMUN 2013 website](http://www.mcmun.org). I was planning to use the same phpBB-based codebase as that for [the SSUNS website](https://github.com/dellsystem/ssuns-2011), but it turns out the McMUN webhost is capable of running more than just PHP (!!) so I built the McMUN site using Django instead.

If you're wondering how everything works, just take a look at the code: the main content management stuff is handled by the `cms` app, the `committees` app takes care of displaying information for all the committees, and the `signups` app handles one-off signups. All the static files are under mcmun/static, the templates are under the templates/ folder in each app directory, and some fixtures containing page content can be found under committees/fixtures and cms/fixtures. (`mcmun` is listed as an installed app but it's really just the project folder that is created automatically by Django; this is so that I can put static files and templates under this directory and have them be loaded automatically.)

The production site uses PostgreSQL for its database and Passenger WSGI for deployment. The admin site is located at a different URL than /admin/ just to prevent anyone from wasting their life away by trying to guess my password.

Licensing information
---------------------

This repository isn't licensed under any of the standard OSI-approved licenses because I couldn't really find one that fit. In non-legal terms: feel free to use any Python/JS/LESS snippets you see. Attribution is not required. Please don't use the content, however (not that anyone is likely to). Please also refrain from copying the design wholesale. That would make me sad.

Source information for the images:

* The background image (of Montreal) is a modified (cropped and darkened) version of a photo taken by [Anirudh Koul](http://www.flickr.com/photos/anirudhkoul/). The original is available under [CC-BY-NC](http://creativecommons.org/licenses/by-nc/2.0/ "I mean, I'm not making any money from this, so that counts as non-commercial usage, right?") and I guess I'll release the derivative under the same license because why not.
* The bridge photo on the homepage, the photo of Montreal on the "About Montreal" page and the photo of McGill on the "About McGill" page are all public domain. The originals can be found on the Wikimedia Commons page for Montreal/McGill.
* The photos and logo on the "Venue" page are from the [Sheraton Centre website](http://www.sheratoncentremontreal.com). Should be fair use, or whatever.
* The Tourisme Montreal and Star Alliance logos came from somewhere. Same as above.
* The image on the "Sponsoring McMUN" page is just a preview of the first page of the sponsorship package, which was created by Jad El Houssami.
* The photos on the "Contact us" and "Meet the secretariat" pages are, pretty obviously, photos of secretariat members.
* The photos in the Registration/Welcome/Committees block on the home page were taken by either a secretariat member or someone related to McMUN in some way.
* The rest of the images - the dove, the logo, the contact icons in the header - I created in Inkscape. They're not available under any sort of copyleft license, unfortunately. Using the logo for illustration purposes in the context of McMUN is, of course, totally fine.
