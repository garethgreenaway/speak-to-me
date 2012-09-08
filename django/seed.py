#!/usr/bin/env python

#
# Pull in the django support
#
from django.core.management import setup_environ
import mysite.settings
setup_environ(mysite.settings)

import hashlib

from home.models import User,UserProfile

speakers = dict([
		('jono@jonobacon.org',['Jono','Bacon','Canonical']),
		('stu@actusa.net',['Stu','Sheldon','ActUSA']),
		('akgraner@gmail.com',['Amber','Graner','Linaro']),
		('pgraner@canonical.com',['Pete','Graner','Canonical']),
		('tarus@opennms.org',['Tarus','Balog','OpenNMS']),
		('jenn@wiked.org',['Jenn','Greenaway','Elemental Aardvark']),
		('orv@socallinuxexpo.org',['Orv','Beach','SCALE']),
		('larry@socallinuxexpo.org',['Larry','Caferio','SCALE']),
		('danese@gmail.com',['Danese','Cooper','Wikipedia']),
		('nhaines@ubuntu.com',['Nathan','Haines','Ubuntu']),
		('coreyfields@xbmc.com',['Corey','Fields','XBMC']),
		('lydia@kde.org',['Lydia','Pintscher','KDE']),
		('jono1@jonobacon.org',['Jono','Bacon','Canonical']),
		('stu1@actusa.net',['Stu','Sheldon','ActUSA']),
		('akgraner1@gmail.com',['Amber','Graner','Linaro']),
		('pgraner1@canonical.com',['Pete','Graner','Canonical']),
		('tarus1@opennms.org',['Tarus','Balog','OpenNMS']),
		('jenn1@wiked.org',['Jenn','Greenaway','Elemental Aardvark']),
		('orv@1socallinuxexpo.org',['Orv','Beach','SCALE']),
		('larry1@socallinuxexpo.org',['Larry','Caferio','SCALE']),
		('danese1@gmail.com',['Danese','Cooper','Wikipedia']),
		('nhaines1@ubuntu.com',['Nathan','Haines','Ubuntu']),
		('coreyfields1@xbmc.com',['Corey','Fields','XBMC']),
		('lydia1@kde.org',['Lydia','Pintscher','KDE']),
		('jono2@jonobacon.org',['Jono','Bacon','Canonical']),
		('stu2@actusa.net',['Stu','Sheldon','ActUSA']),
		('akgraner2@gmail.com',['Amber','Graner','Linaro']),
		('pgraner2@canonical.com',['Pete','Graner','Canonical']),
		('tarus2@opennms.org',['Tarus','Balog','OpenNMS']),
		('jenn2@wiked.org',['Jenn','Greenaway','Elemental Aardvark']),
		('orv2@socallinuxexpo.org',['Orv','Beach','SCALE']),
		('larry2@socallinuxexpo.org',['Larry','Caferio','SCALE']),
		('danese2@gmail.com',['Danese','Cooper','Wikipedia']),
		('nhaines2@ubuntu.com',['Nathan','Haines','Ubuntu']),
		('coreyfields2@xbmc.com',['Corey','Fields','XBMC']),
		('lydia2@kde.org',['Lydia','Pintscher','KDE']),
		('jono3@jonobacon.org',['Jono','Bacon','Canonical']),
		('stu3@actusa.net',['Stu','Sheldon','ActUSA']),
		('akgraner3@gmail.com',['Amber','Graner','Linaro']),
		('pgraner3@canonical.com',['Pete','Graner','Canonical']),
		('tarus3@opennms.org',['Tarus','Balog','OpenNMS']),
		('jenn3@wiked.org',['Jenn','Greenaway','Elemental Aardvark']),
		('orv3@socallinuxexpo.org',['Orv','Beach','SCALE']),
		('larry3@socallinuxexpo.org',['Larry','Caferio','SCALE']),
		('danese3@gmail.com',['Danese','Cooper','Wikipedia']),
		('nhaines3@ubuntu.com',['Nathan','Haines','Ubuntu']),
		('coreyfields3@xbmc.com',['Corey','Fields','XBMC']),
		('lydia3@kde.org',['Lydia','Pintscher','KDE']),
	])

for speaker in speakers:
	print speaker
	print speakers[speaker]

	user = User.objects.create_user(hashlib.md5(speaker).hexdigest(), speaker, '!')
	up = user.profile

	up.first_name = speakers[speaker][0]
	up.last_name = speakers[speaker][1]
	up.company = speakers[speaker][2]

	up.save()
