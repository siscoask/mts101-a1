# MTS 101 — A1

A question-first MTS 101 practice app. Plain HTML, CSS and JavaScript: no build step, no dependencies, no accounts.

## Run
Open `index.html` in a browser. For install-to-home-screen and offline caching, serve the folder over http(s) once (`python3 -m http.server`, then open http://localhost:8000); the service worker (`sw.js`) caches all files on first visit.

## Structure
- `index.html`, `css/style.css`: interface and styles.
- `js/app.js`: question selection, answer evaluation, progress tracking, localStorage persistence.
- `js/math.js`: small LaTeX-subset to MathML renderer (fractions, roots, powers, subscripts, sums, Greek, sets). Needs a browser with MathML (current Chrome, Edge, Firefox, Safari).
- `data/questions.js` (loaded by the app) and `data/questions.json` (same data): the question bank, kept separate from code.
- `tools/build_questions.py`: regenerates the bank. Answers are computed, then re-checked independently with asserts. Also checks duplicate IDs, duplicate questions, distinct options and answer/explanation consistency.
- `tools/test.js`: `node tools/test.js` checks that every question, option and explanation converts to well-formed MathML.

## Question bank
See `data/REPORT.md` for the actual count per topic. All questions are original practice questions, not past papers. Most are parameterised from templates (different numbers, same pattern), so they are distinct but not all conceptually different.
Mathematical Induction (23) and Trigonometric Functions (45) are below the 100-per-topic goal.
To grow the bank: add or extend templates in `tools/build_questions.py`, run it, then `node tools/test.js`.

## Progress
Stored in your browser (`localStorage`, key `mat101a1.v1`) on that device only. Reset is under the progress summary at the top, with confirmation.

## v2 pages
Practise (topic, 5/10/20/until-I-stop, mistakes), Topics (readiness per topic), Mock (standard: 30 questions in 20 minutes across all nine topics; or 10 from one topic in 7 minutes; submit at any time; resumes after a refresh; results kept in Progress), Progress (stats, flagged list, backup/restore, reset). Dark mode follows the device.

## Not built yet
Written-answer mode, flashcards, unit-circle and Venn tools, smart (spaced) review, question of the day, formula pages, more questions for Induction and Trigonometry.

## Tests performed
- Build-time: 734 questions, unique IDs, unique question text, 4 distinct options each, correct answer matches the explanation. Numeric re-checks for AP/GP, binomial coefficients (by polynomial expansion), quadratics (by substitution), base conversion, complex arithmetic (Python complex), and trig values (math.sin/cos/tan). Passed.
- `node tools/test.js`: all math in all questions renders to well-formed MathML (0 problems). Passed.
- `node --check js/app.js`: syntax OK.
- v2: `node --check` on app.js and sw.js, and the math test, passed.
- NOT done: service worker caching, installability, no browser was available in the build environment, so click-through behaviour, mobile layout, MathML appearance and reload persistence have not been run. Please try those first.
