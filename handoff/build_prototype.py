import re, random, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + os.sep
SITE = 'https://www.jidearowolo.com/'
YT = 'https://www.youtube.com/channel/UCyCuoStgyosDfWW4lr-FT1A'

def eq(n, cls=''):
    random.seed(n * 7 + 3)
    bars = ''
    for i in range(n):
        bars += '<i style="--s:%.2fs;--d:-%.2fs;--m:%.2f"></i>' % (random.uniform(.9, 1.9), random.uniform(0, 2), random.uniform(.45, 1))
    return '<div class="eq %s" aria-hidden="true">%s</div>' % (cls, bars)

def slug(t):
    t = t.lower().replace("'", '').replace('"', '')
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')

ALBUMS = [
    ('dreams', 'Dreams', '2011', 'jide-dreams.jpg',
     "The first of a twin release with Roots, after five years spent producing other artistes. Highly inspirational, written to uplift whoever is listening.",
     ['Lift Him', 'I Need You', 'Dreams', 'King of Glory', 'You Are My Reason', 'Gbagbo', 'Celebration Song', 'Love of My Life', 'Gbe Mi', 'Take Me There', 'I Got a Treasure']),
    ('roots', 'Roots', '2011', 'jide-roots.jpg',
     "Released with Dreams as a twin CD. A sense of belonging for listeners of any origin, in Jide's native African language and English, with his voice and live instruments throughout.",
     ['Mo Gbinla', 'Ire Ayo', 'Epo Mbe', 'Iya', 'Ogo Ola', 'Alabaro', 'Eleyinjuege', 'Mo Ti Dele']),
    ('love-connection', 'Love Connection', '2006', 'jide-love-connection.jpg',
     "Recorded at Con Dios Studio, London. A contemporary album on the message of God's love, in funk, R&amp;B and ballad-worship, closing with an easy-listening folk medley.",
     ['My Destiny', 'Come on Everybody', "I Won't Cry", "I'll Fix My Eyes on You", 'Love Connection', 'Much in Love', 'Knowing You (Instrumental)', 'All of My Heart', 'Helping Hand', 'God of Mercy', 'Folk Medley']),
    ('so-so-wonder', 'So So Wonder', '2003', 'jide-so-so-wonder.jpg',
     "Warm, relaxing and encouraging. Recorded at Yellowgate Studio in Gambia, with Senegambian Ndaga percussion, afro-beat and a Yoruba medley.",
     ['So So Wonder', 'Aye Mi', 'God Will Make a Way', 'Be Exalted', 'Liar', 'Evermore', 'Yoruba Medley', 'E Se / Thank You', 'Sing Out Now', 'Love Found a Way', 'Where Is the Love', 'All I Hope For', 'Holy Is the Lord']),
    ('treasures', 'Treasures', '2001', 'jide-treasures.jpg',
     "Jide's first personal album, recorded at Yellowgate Studio, Gambia. Afro-beat, reggae, salsa and contemporary jazz. Hits include Ololufe, Nibo and Kakhi No Be Leather.",
     ['Kakhi No Be Leather', 'Nibo', 'Arise and Shine', 'Ololufe', 'Only You', 'I Give My Praise', 'Come Unto Me', 'Return to the Lord', 'Baba O Se', 'You Are My Treasure', 'Ki Lo Se Fun Mi']),
]

PAGES = [('index.html', 'Home'), ('music.html', 'Music'), ('story.html', 'Story'), ('watch.html', 'Watch')]

HEAD = '''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="theme-color" content="#0e0a07">
<link rel="canonical" href="@@URL@@">
<meta property="og:type" content="website">
<meta property="og:title" content="@@TITLE@@">
<meta property="og:description" content="@@DESC@@">
<meta property="og:url" content="@@URL@@">
<meta property="og:image" content="https://www.jidearowolo.com/images/share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="logo/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,500;0,6..96,700;1,6..96,500&family=Figtree:wght@400;500;600&family=Great+Vibes&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
<noscript><style>.welcome{display:none}.reveal{opacity:1!important;transform:none!important}</style></noscript>
<script type="application/ld+json">@@LD@@</script>
</head>
<body class="@@BODY@@">
<a class="skip" href="#main">Skip to content</a>
'''

def mark(uid, cls):
    """Inline JA monogram (ring turns via CSS). uid keeps gradient ids unique per page."""
    svg = open(OUT + 'logo/ja-monogram-nav.svg', encoding='utf-8').read()
    svg = svg.replace('xmlns="http://www.w3.org/2000/svg" ', '').replace('id="gn"', 'id="g%s"' % uid).replace('url(#gn)', 'url(#g%s)' % uid)
    svg = svg.replace('role="img" aria-label="Jide Arowolo"', 'class="%s" aria-hidden="true" focusable="false"' % cls)
    return svg

def nav(active):
    links = ''
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == active else ''
        links += '<a href="%s"%s>%s</a>\n    ' % (href, cur, label)
    cur = ' aria-current="page"' if active == 'book.html' else ''
    return '''<header class="nav" id="nav">
  <a class="nav__brand" href="index.html" aria-label="Jide Arowolo, home">''' + mark("nav", "logo-mark") + '''</a>
  <button class="nav__toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks"><span class="sr">Menu</span><i></i><i></i></button>
  <nav class="nav__links" id="navLinks" aria-label="Main">
    %s<a class="btn btn--small" href="book.html"%s>Book Jide</a>
  </nav>
  <span class="nav__progress" id="progress" aria-hidden="true"></span>
</header>
''' % (links, cur)

FOOT = '''<footer class="footer">
  <a class="footer__logo" href="index.html" aria-label="Jide Arowolo, home"><img src="logo/jide-arowolo-wordmark.svg" alt="Jide Arowolo" width="360" height="94"></a>
  <p>Afro pop, gospel and worship music. London.</p>
  <p class="footer__links"><a href="index.html">Home</a> <a href="music.html">Music</a> <a href="story.html">Story</a> <a href="watch.html">Watch</a> <a href="book.html">Book Jide</a> <a href="%s" target="_blank" rel="noopener">YouTube</a></p>
  <p class="footer__small">&copy; <span id="year"></span> Jide Arowolo. All rights reserved.</p>
</footer>
''' % YT

PLAYER = '''<div class="player" id="player" hidden>
  <button class="player__btn" id="playBtn" type="button" aria-label="Pause">
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path id="playIcon" fill="currentColor" d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>
  </button>
  <div class="player__meta"><strong id="pTitle"></strong><span id="pMsg"></span></div>
  %s
  <button class="player__close" id="pClose" type="button" aria-label="Close player">&times;</button>
  <audio id="audio" preload="none"></audio>
</div>
''' % eq(7, 'eq--mini')

MOBILEBAR = '''<div class="bookbar" id="bookbar">
  <a class="bookbar__btn" href="@@HREF@@"><span class="bookbar__eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><span class="bookbar__label">Book Jide</span><span class="bookbar__arrow" aria-hidden="true">&rarr;</span></a>
</div>
'''

WELCOME = '''<div class="welcome" id="welcome" role="dialog" aria-modal="true" aria-label="Welcome">
  <div class="welcome__photo"><img src="images/jide-portrait.webp" alt="Jide Arowolo" width="794" height="976"></div>
  <div class="welcome__inner">
    @@MARK@@
    <p class="welcome__greet">E kaabo &middot; Welcome</p>
    <p class="welcome__name"><span>Jide</span> <span>Arowolo</span></p>
    <p class="welcome__line">It is such a joy to welcome you. Be my guest. <span>Peace, Jide</span></p>
    <button class="btn btn--gold" id="enter" type="button">Enter the site</button>
  </div>
</div>
'''
WELCOME = WELCOME.replace('@@MARK@@', mark('wel', 'welcome__mark'))

def ld(obj):
    import json
    return json.dumps(obj, ensure_ascii=False)

PERSON = {"@type": "Person", "@id": SITE + "#jide", "name": "Jide Arowolo", "jobTitle": "Musician, songwriter and producer", "url": SITE, "birthPlace": "South Western Nigeria", "workLocation": "London, United Kingdom", "sameAs": [YT]}
GROUP = {"@type": "MusicGroup", "name": "Jide Arowolo", "genre": ["Afro pop", "Afro-beat", "Gospel", "Reggae", "R&B", "Jazz"], "url": SITE, "sameAs": [YT]}

def page(fname, title, desc, ldobj, main, body='', welcome='', player=''):
    html = HEAD.replace('@@TITLE@@', title).replace('@@DESC@@', desc).replace('@@URL@@', SITE + ('' if fname == 'index.html' else fname)).replace('@@LD@@', ld({"@context": "https://schema.org", "@graph": ldobj})).replace('@@BODY@@', 'page-' + body if body else '')
    html += welcome + nav(fname) + '<main id="main">\n' + main + '\n</main>\n' + FOOT + MOBILEBAR.replace('@@HREF@@', '#bookForm' if fname == 'book.html' else 'book.html') + player + '<script src="script.js"></script>\n</body>\n</html>\n'
    open(OUT + fname, 'w', encoding='utf-8').write(html)

def head(h1, lede, bg, extra=''):
    return '''<section class="page-head" style="--bg:url(images/%s)">
  <div class="wrap">
    <h1>%s</h1>
    <p>%s</p>
    %s
  </div>
</section>''' % (bg, h1, lede, extra)

def cover(img, title, w=500, lazy=True):
    return '<div class="cover" data-title="%s"><img src="images/%s" alt="%s album cover" width="%d" height="%d"%s onerror="this.remove()"></div>' % (title, img, title, w, w, ' loading="lazy"' if lazy else '')

# ---------------- HOME ----------------
minis = ''.join('<a class="mini" href="music.html#%s">%s<span class="mini__name">%s</span><span class="mini__year">%s</span></a>' % (a[0], cover(a[3], a[1], 400), a[1], a[2]) for a in ALBUMS)
home = '''<div class="hero-wrap">
  <section class="hero hero--photo" id="top">
    <div class="hero__text">
      <p class="kicker">Afro pop, gospel and worship</p>
      <h1 class="hero__name">
        <span class="sr-only">Jide Arowolo</span>
        <svg viewBox="0 0 1000 720" aria-hidden="true" focusable="false">
          <defs><linearGradient id="gjide" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3dfa6"/><stop offset=".55" stop-color="#c9a24b"/><stop offset="1" stop-color="#8a6a22"/></linearGradient></defs>
          <text class="hero__jide" x="40" y="340" font-size="400" textLength="940" lengthAdjust="spacingAndGlyphs" fill="url(#gjide)">Jide</text>
          <text class="hero__arowolo" x="40" y="665" font-size="235" textLength="940" lengthAdjust="spacingAndGlyphs" fill="#f3e9d6">Arowolo</text>
        </svg>
      </h1>
      <p class="hero__tagline">Music with roots, <em>made to lift.</em></p>
      <p class="hero__lede">Self-taught musician, songwriter and producer. Five albums blending afro-beat, reggae, R&amp;B, jazz and Yoruba folk, recorded in Gambia and London.</p>
      <div class="hero__cta">
        <a class="btn btn--gold" href="music.html">Listen now</a>
        <a class="btn btn--ghost" href="book.html">Book Jide</a>
      </div>
    </div>
    <div class="hero__portrait">
      <picture>
        <source media="(min-width:820px)" srcset="images/jide-hero-half.webp" width="760" height="530">
        <img src="images/jide-hero-close.webp" alt="Jide Arowolo seated with his hands clasped, smiling" width="900" height="1200" fetchpriority="high">
      </picture>
    </div>
  </section>
  %s
</div>

<section class="section" aria-labelledby="soundH">
  <div class="wrap">
    <h2 id="soundH" class="h2">The sound</h2>
    <p class="sub">Afro-beat, reggae, R&amp;B, jazz and worship, recorded in London and The Gambia.</p>
    <div class="sound">
      <article class="sound__card" data-reveal><img src="images/bg-piano.jpg" alt="A grand piano in a dim room" width="1600" height="900" loading="lazy"><div class="sound__text"><h3>Written in the studio</h3><p>Songs are written and produced at his Con Dios Studio in London, where all his productions are made.</p></div></article>
      <article class="sound__card" data-reveal><img src="images/bg-drum.jpg" alt="A hand drum with gold bands" width="1600" height="900" loading="lazy"><div class="sound__text"><h3>Rhythm from the Gambia</h3><p>Senegambian Ndaga percussion drives Be Exalted and All I Hope For on So So Wonder.</p></div></article>
      <article class="sound__card" data-reveal><img src="images/bg-sax.jpg" alt="A brass saxophone in low light" width="1600" height="900" loading="lazy"><div class="sound__text"><h3>Afro-beat and jazz</h3><p>Treasures moves through afro-beat, reggae, salsa and contemporary jazz.</p></div></article>
      <article class="sound__card" data-reveal><img src="images/bg-violin.jpg" alt="A violin on a dark stage" width="1600" height="900" loading="lazy"><div class="sound__text"><h3>Ballad and worship</h3><p>Love Connection sits in funk, R&amp;B and ballad-worship, closing with an easy-listening folk medley.</p></div></article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="albH">
  <div class="wrap">
    <h2 id="albH" class="h2">Five albums, 2001 to 2011</h2>
    <p class="sub">Pick one to see the tracks and listen on YouTube.</p>
    <div class="minis">%s</div>
  </div>
</section>

<section class="cta" aria-labelledby="ctaH">
  <h2 id="ctaH" class="h2">Bring Jide to your event</h2>
  <p>Concerts, worship nights, conferences and workshops. Tell us about your event and get a reply with availability.</p>
  <a class="btn btn--gold" href="book.html">Book Jide</a>
</section>''' % (eq(48, 'eq--wide'), minis)

page('index.html', 'Jide Arowolo | Afro Pop, Gospel and Worship Music',
     'Jide Arowolo is a self-taught Nigerian-born musician, songwriter and producer based in London. Listen to five albums and book him for concerts, worship and workshops.',
     [PERSON, GROUP, {"@type": "WebSite", "name": "Jide Arowolo", "url": SITE}], home, 'home', WELCOME)

# ---------------- MUSIC ----------------
tabs = ''.join('<a href="#%s">%s</a>' % (a[0], a[1]) for a in ALBUMS)
panels = ''
# Album playlists on YouTube (sold by the CD distributor). Albums not listed here link to the channel.
# Song videos on YouTube (from the distributor's Dreams playlist), keyed by track slug.
VIDEOS = {'mo-gbinla': 'xnCuodYA28Q', 'ire-ayo': 'TkCzW8bB9YY', 'epo-mbe': '7VQLbfC2pkQ', 'iya': 'MD5NbyyuEAQ', 'ogo-ola': 'a4h3Xag11c0', 'alabaro': 'uWNDs3hSbu8', 'eleyinjuege': 'jXAB7faaf_o', 'mo-ti-dele': 'gyWxQC6--2s', 'lift-him': 'Jw1CwFnheUQ', 'i-need-you': 'JcY2KsXzGFM', 'dreams': 'GqAIA9XUMyQ', 'king-of-glory': 'e6fpl588MYc', 'you-are-my-reason': 'SuC2udU8j3U', 'gbagbo': 'qebhN-ufRzM', 'celebration-song': '2uLoS9Qq-M8', 'love-of-my-life': '1glqafXTHgI', 'gbe-mi': 'Nj1tdvdyQ1g', 'take-me-there': 'ryCc4dBAOl8', 'i-got-a-treasure': 'CU7X9s-aw9I'}
PLAYLISTS = {k: 'https://www.youtube.com/playlist?list=' + v for k, v in {'dreams': 'OLAK5uy_mFhrmDyC8Euh-rTAOAwUa5mGVT4G667p4', 'roots': 'OLAK5uy_nTKFN2yFvqarAM1RcJZDDLPsIj1pdcJ3w'}.items()}
for sl, name, yr, img, desc, tracks in ALBUMS:
    tl = ''.join('<li><button type="button" data-track="%s">%s</button>%s</li>' % (slug(t), t, ('<a class="tracks__yt" href="https://www.youtube.com/watch?v=%s" target="_blank" rel="noopener" aria-label="Watch %s on YouTube">YouTube</a>' % (VIDEOS[slug(t)], t)) if slug(t) in VIDEOS else '') for t in tracks)
    panels += '''<article class="panel" id="%s" data-reveal>
  %s
  <div class="panel__body">
    <h2 class="h2">%s <small>%s</small></h2>
    <p>%s</p>
    <p><a class="btn btn--gold" href="%s" target="_blank" rel="noopener">Listen on YouTube</a></p>
    <ol class="tracks" aria-label="%s tracks">%s</ol>
  </div>
</article>
''' % (sl, cover(img, name), name, yr, desc, PLAYLISTS.get(sl, YT), name, tl)
music = head('Music', 'Five albums in afro-beat, reggae, R&amp;B, jazz and worship. Listen on YouTube, or play a sample where one is available.', 'bg-drum.jpg', eq(40, 'eq--head')) + '''
<nav class="tabs" aria-label="Albums"><div class="tabs__in">%s</div></nav>
<div class="wrap panels">
%s</div>''' % (tabs, panels)
page('music.html', 'Music | Jide Arowolo',
     'Jide Arowolo albums: Dreams, Roots, Love Connection, So So Wonder and Treasures. Full track lists, with links to listen on YouTube.',
     [GROUP | {"album": [{"@type": "MusicAlbum", "name": a[1], "datePublished": a[2], "numTracks": len(a[5])} for a in ALBUMS]}] if False else
     [dict(GROUP, album=[{"@type": "MusicAlbum", "name": a[1], "datePublished": a[2]} for a in ALBUMS])],
     music, 'music', '', PLAYER)

# ---------------- STORY ----------------
ERAS = [
    ("Nigeria: the early years", "1984 to 1998", [
        ("1984 to 1990", "Played guitar for the Liberators at CCC Central, Oshogbo. From 1984 to 1986 he also played for CAC Agbala Itura."),
        ("1985 to 1989", "Played guitar for the Jesus Revolution Voices at the University of Ibadan, and for many groups at the Livingspring Christian Music Festival, University of Ife."),
        ("Late 1980s", "Featured at the Maranatha Music Festivals alongside prominent Christian artistes. Shared the stage with Margurite Ingram, Leon Patillo and Kenny Smith at the University of Lagos, in collaboration with Ebenezer Obey."),
        ("1989 to 1993", "Played guitar and bass for Emerald, a Christian contemporary instrumental jazz quartet in Ibadan. Notable performances included Emerald in Concert, Segi's Restaurant, Broking House Ibadan, Spectrum Books, the National Arts Theatre Lagos and RCCG Model Parish, Lagos."),
        ("1990", "Supported Marcel McArthur's concert in Nigeria."),
        ("1990 to 1998", "National Music Director for New Covenant Church (NCC) Nigeria, headed at NCC Samonda, where he organised three major concerts with the NCC Samonda music team at Trenchard Hall, University of Ibadan. The team was invited to perform at the Broadcasting Corporation of Oyo State, Radio Nigeria, NTA and other broadcasters, and the concerts became regulars on Sunday television."),
        ("1996", "Gained a Diploma in Music Technology."),
        ("1997 and 1998", "Rejoice '97 and He Is Risen '98, concerts with the Samonda music team. The recordings became favourites on television stations in and beyond Oyo State."),
    ]),
    ("The Gambia and the wider world", "1995 to 2005", [
        ("1995 and 1996", "Guest music minister at the Abiding Word Ministries concerts in The Gambia."),
        ("1998", "Delivered a command performance with the Emerald Jazz Quartet for the Diplomatic Corps in The Gambia, and at the Kololi Beach Resort."),
        ("1999", "Invited to the State House in The Gambia to meet President Yahya Jammeh one-on-one."),
        ("Early 2000s", "Headed Abiding Word Ministries in The Gambia, and the Evangelical Mass Choir."),
        ("2000 to 2001", "Produced signature tunes and radio adverts for Sabena Airlines (now Air Brussels), Maersk Sealand and GNIC."),
        ("2001", "Recorded Treasures at Yellowgate Studio in The Gambia, his first personal album, which included Ololufe. Wrote, performed and produced the official International Roots Homecoming Festival theme song CD, Welcome Home, for the Department of State for Tourism and Culture, The Gambia. Commissioned to write 2 songs by the United Nations, representing The Gambia, featured on the International Year of Volunteers 2001 album, which was mastered in Germany."),
        ("2002", "Wrote music lyrics for Marcel McArthur in The Gambia."),
        ("2003", "Released So So Wonder, recorded at Yellowgate Studio with Senegambian Ndaga percussion and a Yoruba medley. Guest music minister at a concert in Sierra Leone."),
        ("2005", "Guest UK music minister at the Nigeria Turning Point Prayer Rally in Abuja Stadium, organised by Bishop Wale Oke."),
    ]),
    ("London and abroad", "2006 to 2014", [
        ("2006", "Released Love Connection, recorded at his Con Dios Studio in London. Delivered seminars for the choirs of the Sword of the Spirit Ministries Churches in Nigeria."),
        ("2006", "Commissioned to perform in Brasov, Romania, with Hospice of Hope fully funding his performance at Bistro de l'arte. Performed in Bucharest with Debbie Perolls."),
        ("2011", "Released the twin albums Dreams and Roots, after five years producing other artistes."),
        ("2013 to 2014", "Guest music minister at NCC Hungary and in Stuttgart, Germany."),
    ]),
]
tl = ''.join('<div class="era" data-reveal><h3>%s</h3><span>%s</span></div><ol class="timeline">%s</ol>' % (n, r, ''.join('<li data-reveal><time>%s</time><p>%s</p></li>' % t for t in items)) for n, r, items in ERAS)
PLACES = [("Nigeria", "Ibadan, Lagos, Abuja, Oshogbo and Ife"), ("The Gambia", "Concerts, hotels and festivals"), ("Sierra Leone", "Concert, 2003"), ("United Kingdom", "London studio and guest ministry"), ("Romania", "Brasov and Bucharest"), ("Hungary", "Guest music minister"), ("Germany", "Stuttgart and Hanover"), ("Canada", "Toronto"), ("United States", "Maryland")]
places = ''.join('<li data-reveal><strong>%s</strong><span>%s</span></li>' % p for p in PLACES)
BEYOND = [
    ("The Gambia and the Roots Festival", "Wrote, performed and produced the official International Roots Homecoming Festival theme song CD, Welcome Home, for the Department of State for Tourism and Culture, The Gambia, in 2001. In 1999 he was invited to the State House to meet President Yahya Jammeh one-on-one. He also handled sound production for the World Expo in Hanover, Germany.", "roots-theme-song-front.webp", "Cover of the International Roots Homecoming Festival theme song CD, Welcome Home"),
    ("United Nations", "Two of his songs, \"Join hands together\" and \"It's our year. It's our time\", represent The Gambia on the 2-CD International Year of Volunteers 2001 album, a collection of songs donated by artists around the world. Sponsored by the Government of Japan and mastered in Germany.", "iyv-2001-front.webp", "Cover of the International Year of Volunteers 2001 album, Songs celebrating volunteerism"),
    ("Commissioned recordings", "Signature tunes and radio adverts for Sabena Airlines (now Air Brussels), Maersk Sealand and GNIC in 2000 and 2001, and music productions for Ogun State Broadcasting Corporation, the Riding on the Rails radio series and Eko FM."),
    ("Producer", "Has produced many artistes and groups, including Precious (UK), Yemisi (Toronto), Mary Tade, Femi Adedoyin (God Is Good), Tinuola (UK), Kola Olotu, Kola Olawuyi, Standard Chartered Bank and the NCC Samonda debut album. He also produces downloadable tracks for UK artistes and critiques productions before release."),
    ("Teaching and training", "Has taught many students formal piano, all of whom passed their ABRSM piano examinations with good grades, some up to Grade 8. He has led seminars and training on praise and worship and sound management in universities, churches and conferences around the world."),
    ("Universal Recording Studio", "Established and managed the Universal Recording Studio in Nigeria, funded by NCC Nigeria and set up at the direction of Pastor E. Aladiran."),
    ("On the hotel stage", "Appointed pianist and singer at Shikra, Kairaba Beach Hotel, The Gambia, where visiting Lords from the UK and many foreign guests recommended him. His style cut across cultural barriers and tastes, and guests and management loved it."),
    ("Concerts and giving back", "Concerts across the UK, Canada, Romania, Hungary and Germany, including the Prayer Centre Concert in Toronto and NCC Maryland in the USA, and fundraising for Hospice of Hope, which cares for the terminally ill. He has also been featured in magazines and on radio programmes in the UK and Europe."),
]
def card(b):
    img = ('<img class="beyond__img" src="images/archive/%s" alt="%s" width="%d" height="%d" loading="lazy">' % ((b[2], b[3]) + {'roots-theme-song-front.webp': (900, 826), 'iyv-2001-front.webp': (804, 711)}[b[2]])) if len(b) > 2 else ''
    return '<article data-reveal>%s<h3>%s</h3><p>%s</p></article>' % (img, b[0], b[1])
beyond = ''.join(card(b) for b in BEYOND)
ARCHIVE = [
    ("International Roots Homecoming Festival theme song CD, 2001", [
        ("roots-theme-song-front.webp", "Front cover: International Roots Homecoming Festival Theme Song, Welcome Home."),
        ("roots-theme-song-back.webp", "Back cover: \"Produced by Jide Arowolo, Con Dios Music, for the Department of State for Tourism and Culture, The Gambia.\""),
        ("roots-theme-song-dedication.webp", "The dedication from the Secretary of State for Tourism and Culture and the National Organising Committee."),
    ]),
    ("International Year of Volunteers 2001 album", [
        ("iyv-2001-front.webp", "Front cover: International Year of Volunteers 2001, Songs celebrating volunteerism."),
        ("iyv-2001-tracklist.webp", "Track listing. Jide Arowolo represents The Gambia with \"Join hands together\" (CD 1, track 9) and \"It's our year. It's our time\" (CD 2, track 6)."),
    ]),
]
archive = ''.join('<h3 class="archive__title" data-reveal>%s</h3><div class="archive">%s</div>' % (t, ''.join('<figure data-reveal><a class="zoom" href="images/archive/%s" data-caption="%s"><img src="images/archive/%s" alt="%s" loading="lazy"></a><figcaption>%s</figcaption></figure>' % (f, c.replace('"', '&quot;'), f, c.replace('"', '&quot;'), c) for f, c in items)) for t, items in ARCHIVE)
story = head('Story', 'Self-taught, and always in the room where the music happens.', 'bg-violin.jpg') + '''
<section class="section">
  <div class="wrap story">
    <figure class="story__photo" data-reveal>
      <div class="cover cover--portrait" data-title="Jide Arowolo"><img src="images/jide-portrait.webp" alt="Portrait of Jide Arowolo" width="794" height="976" onerror="this.remove()"></div>
    </figure>
    <div class="story__text" data-reveal>
      <p>Born in South Western Nigeria, Jide recognised his musicianship in his late teens. He taught himself, and has spent more than two decades in mainstage music, songwriting and public worship leading, gaining recognition especially in gospel music.</p>
      <p>He is a highly prolific songwriter, with a large catalogue of original songs in ballad, pop, reggae, R&amp;B and contemporary afro-rhythms. One of them is the popular Ololufe.</p>
      <p>He has taught many musicians, some now well-known producers around the world, and has been technical adviser and producer to Christian bands and artistes. He has led seminars and training on praise and worship and sound management in universities, churches and conferences across the world.</p>
      <ul class="facts" aria-label="Career highlights">
        <li><strong>5</strong> albums</li>
        <li><strong>20+</strong> years in mainstage music</li>
        <li><strong>1</strong> London studio</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="plH">
  <div class="wrap">
    <h2 id="plH" class="h2">Stages around the world</h2>
    <p class="lede">Concerts, festivals, hotels, churches and conferences across Africa, Europe and North America.</p>
    <ul class="places">@@PLACES@@</ul>
  </div>
</section>

<section class="section section--story" aria-labelledby="tlH">
  <div class="wrap">
    <h2 id="tlH" class="h2">The story so far</h2>
    @@TL@@
  </div>
</section>

<section class="section" aria-labelledby="bsH">
  <div class="wrap">
    <h2 id="bsH" class="h2">Beyond the stage</h2>
    <div class="beyond">@@BEYOND@@</div>
  </div>
</section>

<section class="section section--story" aria-labelledby="arH">
  <div class="wrap">
    <h2 id="arH" class="h2">From the archive</h2>
    <p class="lede">Scans of two projects from The Gambia. Select an image to enlarge it.</p>
    @@ARCHIVE@@
  </div>
</section>

<section class="cta" aria-labelledby="ctaH">
  <h2 id="ctaH" class="h2">Work with Jide</h2>
  <p>Concerts, worship leading, music direction, sound consultancy and workshops.</p>
  <a class="btn btn--gold" href="book.html">Book Jide</a>
</section>
<dialog class="lightbox" id="lightbox" aria-label="Enlarged image"><button class="lightbox__close" type="button" id="lbClose" aria-label="Close">&times;</button><img id="lbImg" alt=""><p id="lbCap"></p></dialog>'''
story = story.replace('@@PLACES@@', places).replace('@@TL@@', tl).replace('@@BEYOND@@', beyond).replace('@@ARCHIVE@@', archive)
page('story.html', 'Story | Jide Arowolo',
     'The story of Jide Arowolo: self-taught Nigerian-born musician, songwriter and producer, from Ibadan and The Gambia to London, with concerts across Africa, Europe and North America.',
     [PERSON], story, 'story')

# ---------------- WATCH ----------------
watch = head('Watch', 'Live performances and music from Jide\'s YouTube channel, with photos from the stage and studio.', 'bg-sax.jpg') + '''
<section class="section">
  <div class="wrap">
    <div class="videos" id="videos"></div>
    <p class="yt-note"><a class="btn btn--ghost" href="%s" target="_blank" rel="noopener">Open the channel on YouTube</a></p>
  </div>
</section>
<section class="section section--live" aria-labelledby="galH">
  <div class="wrap">
    <h2 id="galH" class="h2">Gallery</h2>
    <div class="gallery">
      <figure class="cover" data-title="On stage"><img src="images/jide-stage.jpg" alt="Jide Arowolo singing on stage under red lights" width="800" height="520" loading="lazy" onerror="this.remove()"></figure>
      <figure class="cover" data-title="Guitar"><img src="images/jide-guitar.jpg" alt="Jide Arowolo playing electric guitar on stage" width="800" height="520" loading="lazy" onerror="this.remove()"></figure>
      <figure class="cover" data-title="Studio"><img src="images/jide-studio.jpg" alt="Jide Arowolo with an acoustic guitar in his London studio" width="800" height="520" loading="lazy" onerror="this.remove()"></figure>
    </div>
  </div>
</section>''' % YT
page('watch.html', 'Watch | Jide Arowolo',
     'Watch and listen to Jide Arowolo on YouTube, and see photos from the stage and from his London studio.',
     [PERSON], watch, 'watch')

# ---------------- BOOK ----------------
book = head('Book Jide', 'Tell us about your event and you will get a reply with availability and next steps. The more detail you share, the faster we can say yes, or suggest what would work better.', 'bg-piano.jpg') + '''
<section class="section">
  <div class="wrap book">
    <div class="book__intro" data-reveal>
      <h2 class="h2">Booking enquiry</h2>
      <ul class="list">
        <li>Concerts and festivals</li>
        <li>Worship leading and conferences</li>
        <li>Music direction and sound consultancy</li>
        <li>Workshops on praise, worship and sound management</li>
        <li>Studio production</li>
      </ul>
    </div>
    <form class="form" id="bookForm" novalidate data-reveal>
      <div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      <div class="field"><label for="type">What are you booking for?</label>
        <select id="type" name="type" required>
          <option value="">Choose one</option>
          <option>Concert or festival</option>
          <option>Worship leading</option>
          <option>Conference or church event</option>
          <option>Workshop or training</option>
          <option>Studio production</option>
          <option>Something else</option>
        </select></div>
      <div class="row">
        <div class="field"><label for="date">Event date</label><input id="date" name="date" type="date"></div>
        <div class="field"><label for="place">Location</label><input id="place" name="place" placeholder="City and venue"></div>
      </div>
      <div class="row">
        <div class="field"><label for="size">Expected audience</label>
          <select id="size" name="size"><option value="">Not sure yet</option><option>Under 100</option><option>100 to 500</option><option>500 to 2,000</option><option>Over 2,000</option></select></div>
        <div class="field"><label for="budget">Budget range</label>
          <select id="budget" name="budget"><option value="">Prefer to discuss</option><option>Under &pound;1,000</option><option>&pound;1,000 to &pound;3,000</option><option>&pound;3,000 to &pound;7,500</option><option>Over &pound;7,500</option></select></div>
      </div>
      <div class="field"><label for="msg">About your event</label><textarea id="msg" name="msg" rows="5" required placeholder="Who is it for, what is the occasion, and what would you like Jide to do?"></textarea></div>
      <button class="btn btn--gold" type="submit">Send booking enquiry</button>
      <p class="form__status" id="formStatus" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>

<section class="section section--story" id="guestbook" aria-labelledby="gbH">
  <div class="wrap book">
    <div class="book__intro" data-reveal>
      <h2 id="gbH" class="h2">Guest book</h2>
      <p>Jide's old welcome said: &ldquo;Please do your best to sign my guest book before leaving, I'd love to hear from you.&rdquo; Leave a message. New messages appear after review.</p>
      <div class="guests" id="guestList"><p class="empty"><strong>No messages yet.</strong> Be the first to sign.</p></div>
    </div>
    <form class="form" id="guestForm" novalidate data-reveal>
      <div class="field"><label for="gname">Your name</label><input id="gname" name="name" autocomplete="name" required></div>
      <div class="field"><label for="gplace">Where are you writing from?</label><input id="gplace" name="place" placeholder="City or country"></div>
      <div class="field"><label for="gmsg">Your message</label><textarea id="gmsg" name="msg" rows="4" required></textarea></div>
      <input type="hidden" name="form_type" value="guestbook">
      <button class="btn btn--gold" type="submit">Sign the guest book</button>
      <p class="form__status" id="guestStatus" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''
page('book.html', 'Book Jide Arowolo | Concerts, Worship and Workshops',
     'Book Jide Arowolo for concerts, worship leading, conferences, workshops, music direction and studio production. Tell us about your event.',
     [{"@type": "ContactPage", "name": "Book Jide Arowolo", "url": SITE + "book.html"}], book, 'book')

# sitemap + robots
urls = ['', 'music.html', 'story.html', 'watch.html', 'book.html']
open(OUT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>%s%s</loc></url>\n' % (SITE, u) for u in urls) + '</urlset>\n')
open(OUT + 'robots.txt', 'w').write('User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n' % SITE)
print('built', os.listdir(OUT))
