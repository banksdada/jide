/* ---------- Settings you can edit ---------- */
// YouTube channel address
var YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/UCyCuoStgyosDfWW4lr-FT1A";
// Embedded player showing the channel's uploads (the channel ID with UC changed to UU).
// If it shows "video unavailable", replace with an album playlist ID from YouTube (starts with OLAK5uy_ or PL).
var YOUTUBE_PLAYLIST_ID = "UUyCuoStgyosDfWW4lr-FT1A";
// Or list individual video IDs (the part after v= in a YouTube link). Used when no playlist ID is set.
var YOUTUBE_VIDEO_IDS = [];
// Welcome screen: seconds before the site opens by itself (0 turns this off). Visitors can also swipe, scroll, press a key or tap the button.
var WELCOME_AUTO_SECONDS = 8;
// Form service address (Formspree, Basin, Getform and similar). Leave empty for a preview-only form.
var FORM_ENDPOINT = "";
// Until a form service address is set above, the booking form opens the visitor's email app addressed here.
var BOOKINGS_EMAIL = "bookings@jidearowolo.com";
// Sample tracks: put MP3 files in the audio folder, named after each track, e.g. audio/ololufe.mp3
var AUDIO_FOLDER = "audio/";
/* ------------------------------------------- */

(function () {
  "use strict";
  var doc = document;
  doc.documentElement.classList.add("js");
  function $(s, c) { return (c || doc).querySelector(s); }
  function $all(s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); }
  function store(get, key, val) {
    try { return get ? sessionStorage.getItem(key) : sessionStorage.setItem(key, val); } catch (e) { return null; }
  }

  /* Welcome screen (home page only) */
  var welcome = $("#welcome"), enter = $("#enter");
  if (welcome) {
    var autoTimer = null, touchY = null;
    var stopAuto = function () { if (autoTimer) { clearTimeout(autoTimer); autoTimer = null; } };
    var onWheel = function (e) { if (e.deltaY > 8) openSite(); };
    var onTouchStart = function (e) { touchY = e.touches && e.touches[0] ? e.touches[0].clientY : null; };
    var onTouchMove = function (e) {
      if (touchY === null || !e.touches || !e.touches[0]) return;
      if (touchY - e.touches[0].clientY > 40) openSite();
    };
    var onKey = function (e) {
      if (welcome.classList.contains("is-open")) return;
      var k = e.key;
      if (k === "Escape" || k === "ArrowDown" || k === "PageDown" || k === " " || k === "Spacebar") {
        if (k === " " && doc.activeElement === enter) return; /* the button handles its own space press */
        if (k !== "Escape") e.preventDefault();
        openSite();
      }
    };
    var openSite = function () {
      if (welcome.classList.contains("is-open")) return;
      stopAuto();
      welcome.classList.add("is-open");
      doc.body.classList.remove("locked");
      welcome.setAttribute("aria-hidden", "true");
      store(false, "ja-welcomed", "1");
      welcome.removeEventListener("wheel", onWheel);
      welcome.removeEventListener("touchstart", onTouchStart);
      welcome.removeEventListener("touchmove", onTouchMove);
      doc.removeEventListener("keydown", onKey);
    };
    if (store(true, "ja-welcomed")) {
      welcome.classList.add("is-open");
      welcome.setAttribute("aria-hidden", "true");
    } else {
      doc.body.classList.add("locked");
      enter.focus();
      doc.addEventListener("keydown", onKey);
      welcome.addEventListener("wheel", onWheel, { passive: true });
      welcome.addEventListener("touchstart", onTouchStart, { passive: true });
      welcome.addEventListener("touchmove", onTouchMove, { passive: true });
      if (WELCOME_AUTO_SECONDS > 0) {
        var ms = WELCOME_AUTO_SECONDS * 1000;
        enter.style.setProperty("--auto", WELCOME_AUTO_SECONDS + "s");
        welcome.classList.add("is-timing");
        autoTimer = setTimeout(openSite, ms);
        /* hovering over the button pauses the countdown so nobody is rushed */
        enter.addEventListener("mouseenter", function () { stopAuto(); welcome.classList.remove("is-timing"); });
      }
    }
    enter.addEventListener("click", openSite);
  }

  /* Nav */
  var toggle = $("#navToggle"), links = $("#navLinks");
  function setNav(open) {
    links.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  toggle.addEventListener("click", function () { setNav(!links.classList.contains("is-open")); });
  $all("a", links).forEach(function (a) { a.addEventListener("click", function () { setNav(false); }); });

  /* Scroll progress */
  var bar = $("#progress"), ticking = false;
  function update() {
    var h = doc.documentElement.scrollHeight - innerHeight;
    bar.style.transform = "scaleX(" + (h > 0 ? Math.min(scrollY / h, 1) : 0) + ")";
    ticking = false;
  }
  addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();

  /* Reveal blocks when they scroll into view */
  var revealEls = $all("[data-reveal]");
  revealEls.forEach(function (el) { el.classList.add("reveal"); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* Sample player (music page) */
  var player = $("#player");
  if (player) {
    var audio = $("#audio"), playBtn = $("#playBtn"), icon = $("#playIcon");
    var pTitle = $("#pTitle"), pMsg = $("#pMsg"), current = null;
    var PAUSE = "M6 5h4v14H6zM14 5h4v14h-4z", PLAY = "M8 5v14l11-7z";
    var setIcon = function (playing) {
      icon.setAttribute("d", playing ? PAUSE : PLAY);
      playBtn.setAttribute("aria-label", playing ? "Pause" : "Play");
      doc.body.classList.toggle("playing", playing);
    };
    var clearPlaying = function () { $all(".tracks button.is-playing").forEach(function (b) { b.classList.remove("is-playing"); }); };
    $all(".tracks button").forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (current === btn) { if (audio.paused) audio.play(); else audio.pause(); return; }
        current = btn; clearPlaying(); btn.classList.add("is-playing");
        var album = btn.closest(".panel");
        pTitle.textContent = btn.textContent;
        pMsg.textContent = $("h2", album).childNodes[0].textContent.trim();
        player.hidden = false; setIcon(true);
        audio.src = AUDIO_FOLDER + btn.getAttribute("data-track") + ".mp3";
        var p = audio.play();
        if (p && p.catch) p.catch(function () {});
      });
    });
    audio.addEventListener("play", function () { setIcon(true); });
    audio.addEventListener("pause", function () { setIcon(false); });
    audio.addEventListener("ended", function () { setIcon(false); clearPlaying(); });
    audio.addEventListener("error", function () { setIcon(false); pMsg.textContent = "Sample not added yet. Listen on YouTube."; });
    playBtn.addEventListener("click", function () {
      if (!audio.src) return;
      if (audio.paused) audio.play(); else audio.pause();
    });
    $("#pClose").addEventListener("click", function () {
      audio.pause(); player.hidden = true; clearPlaying(); current = null;
    });
  }

  /* YouTube (watch page) */
  var videos = $("#videos");
  if (videos) {
    if (YOUTUBE_PLAYLIST_ID) {
      var pw = doc.createElement("div"); pw.className = "video video--wide";
      var pf = doc.createElement("iframe");
      pf.src = "https://www.youtube-nocookie.com/embed/videoseries?list=" + encodeURIComponent(YOUTUBE_PLAYLIST_ID);
      pf.title = "Jide Arowolo on YouTube"; pf.loading = "lazy";
      pf.allow = "encrypted-media; picture-in-picture"; pf.allowFullscreen = true;
      pw.appendChild(pf); videos.appendChild(pw);
    } else if (YOUTUBE_VIDEO_IDS.length) {
      YOUTUBE_VIDEO_IDS.forEach(function (id) {
        var wrap = doc.createElement("div"); wrap.className = "video";
        var b = doc.createElement("button");
        b.type = "button"; b.setAttribute("aria-label", "Play video");
        b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + encodeURIComponent(id) + "/hqdefault.jpg)";
        b.addEventListener("click", function () {
          var f = doc.createElement("iframe");
          f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(id) + "?autoplay=1&rel=0";
          f.title = "Jide Arowolo on YouTube"; f.allow = "autoplay; encrypted-media; picture-in-picture"; f.allowFullscreen = true;
          wrap.replaceChild(f, b);
        });
        wrap.appendChild(b); videos.appendChild(wrap);
      });
    } else {
      var e = doc.createElement("p"); e.className = "empty";
      e.innerHTML = "<strong>Videos are on the way.</strong> Live performances and music videos will appear here.";
      videos.appendChild(e);
    }
  }

  /* Latest videos grid (watch page). videos.json is refreshed automatically by tools/update_videos.py */
  var vgrid = $("#vgrid");
  if (vgrid && window.fetch) {
    fetch("videos.json", { cache: "no-cache" })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (list) {
        if (!Array.isArray(list)) return;
        var shown = 0;
        list.forEach(function (v) {
          if (!v || typeof v.id !== "string" || !/^[\w-]{11}$/.test(v.id)) return;
          var title = (typeof v.title === "string" && v.title) ? v.title : "Video";
          var card = doc.createElement("div"); card.className = "vcard";
          var wrap = doc.createElement("div"); wrap.className = "video";
          var b = doc.createElement("button");
          b.type = "button"; b.setAttribute("aria-label", "Play: " + title);
          b.style.backgroundImage = "url(https://i.ytimg.com/vi/" + encodeURIComponent(v.id) + "/hqdefault.jpg)";
          b.addEventListener("click", function () {
            var f = doc.createElement("iframe");
            f.src = "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(v.id) + "?autoplay=1&rel=0";
            f.title = title; f.allow = "autoplay; encrypted-media; picture-in-picture"; f.allowFullscreen = true;
            wrap.replaceChild(f, b);
          });
          wrap.appendChild(b);
          var t = doc.createElement("p"); t.className = "vcard__title"; t.textContent = title;
          card.appendChild(wrap); card.appendChild(t); vgrid.appendChild(card); shown++;
        });
        if (shown) { vgrid.hidden = false; var h = $("#vgridH"); if (h) h.hidden = false; }
      })
      .catch(function () {});
  }

  /* Booking form */
  function wireForm(form, status, rules, okMsg) {
    if (!form) return;
    function fail(msg, field) {
      status.textContent = msg; status.classList.add("is-error");
      if (field) { field.classList.add("err"); field.focus(); }
    }
    var honey = form.querySelector('[name="_gotcha"]');
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      status.classList.remove("is-error"); status.textContent = "";
      $all(".err", form).forEach(function (f) { f.classList.remove("err"); });
      for (var i = 0; i < rules.length; i++) {
        var r = rules[i], el = $(r.sel, form);
        if (!r.ok(el.value)) return fail(r.msg, el);
      }
      if (honey && honey.value) return;
      if (!FORM_ENDPOINT) {
        var lines = [];
        $all("input[name],select[name],textarea[name]", form).forEach(function (f) {
          if (f.type === "hidden" || f.name === "_gotcha" || !f.value) return;
          var lab = form.querySelector('label[for="' + f.id + '"]');
          lines.push((lab ? lab.textContent : f.name) + ": " + f.value);
        });
        window.location.href = "mailto:" + BOOKINGS_EMAIL + "?subject=" + encodeURIComponent("Booking enquiry from jidearowolo.com") + "&body=" + encodeURIComponent(lines.join("\n"));
        status.textContent = "Opening your email app with your details filled in. Press send there to finish.";
        return;
      }
      status.textContent = "Sending...";
      fetch(FORM_ENDPOINT, { method: "POST", headers: { "Accept": "application/json" }, body: new FormData(form) })
        .then(function (r) { if (!r.ok) throw new Error(); form.reset(); status.textContent = okMsg; })
        .catch(function () { fail("Could not send. Check your connection and try again."); });
    });
  }
  wireForm($("#bookForm"), $("#formStatus"), [
    { sel: "#name", ok: function (v) { return v.trim().length > 0; }, msg: "Enter your name." },
    { sel: "#email", ok: function (v) { return /^\S+@\S+\.\S+$/.test(v); }, msg: "Enter an email address like name@example.com." },
    { sel: "#type", ok: function (v) { return !!v; }, msg: "Choose what you are booking for." },
    { sel: "#msg", ok: function (v) { return v.trim().length >= 15; }, msg: "Add a few details about your event (at least a sentence)." }
  ], "Sent. You will get a reply by email.");

  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
})();

/* Archive lightbox: enlarge a scan in a dialog; without JS the link opens the image itself */
(function () {
  var box = document.getElementById("lightbox");
  if (!box || typeof box.showModal !== "function") return;
  var img = document.getElementById("lbImg"), cap = document.getElementById("lbCap");
  document.querySelectorAll("a.zoom").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      img.src = a.getAttribute("href");
      img.alt = a.getAttribute("data-caption") || "";
      cap.textContent = a.getAttribute("data-caption") || "";
      box.showModal();
    });
  });
  document.getElementById("lbClose").addEventListener("click", function () { box.close(); });
  box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
})();
