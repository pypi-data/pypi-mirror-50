defang
======

Defangs and refangs malicious URLs

Usage
-----

- As a script: use the `defang` command to defang or "refang"
  content, supporting
  both stdin/stdout streams as well as to/from files on disk::

        $ echo http://evil.example.com/malicious.php | defang
        hXXp://evil.example[.]com/malicious.php

- As a library::

        >>> from defang import defang
        >>> url = "http://evil.example.com/malicious.php"
        >>> defang(url)
        'hXXp://evil.example[.]com/malicious.php'

- We've added a few new keyword argument options::

        >>> defang(url, colon=True)
        'hXXp[:]//evil.example[.]com/malicious.php'
        >>> defang(url, all_dots=True)
        'hXXp://evil[.]example[.]com/malicious.php'
        >>> defang(url, zero_width_replace=True)
        'h\u200bt\u200bt\u200bp\u200b:\u200b/\u200b/\u200be\u200bv\u200bi\u200bl\u200b.\u200be\u200bx\u200ba\u200bm\u200bp\u200bl\u200be\u200b.\u200bc\u200bo\u200bm\u200b/\u200bm\u200ba\u200bl\u200bi\u200bc\u200bi\u200bo\u200bu\u200bs\u200b.\u200bp\u200bh\u200bp'
        # printed as 'h​t​t​p​:​/​/​e​v​i​l​.​e​x​a​m​p​l​e​.​c​o​m​/​m​a​l​i​c​i​o​u​s​.​p​h​p'

Releases
--------

0.5.3:
  - Merged in optional feature to split characters with the zero-width character.
0.5.2:
  - left in a debug print message in my last patch... removed it.
0.5.1:
  - refangs boxed in colons [:]
0.5.0:
  - added new options to defang
  - `all_dots=True` will turn all dots into [.] and not just the one before the TLD
  - `colon=True` will translate http:// into http[:]// as well as other protocols
0.4.0:
  - added support for URIs with IPv4
0.3.0:
  - added some regex fixes and arbitrary protocol defanging
