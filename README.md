#Malbim dictionary

**לזכות רפואה שלמה מן השמים רפואת הנפש ורפואת הגוף לרחל יונינה בת לאה רייזל בתוך שאר חולי ישראל**


This is the beginning of a Malbim dictionary/index.  As it was originally conceived, I wanted references to each place the
Malbim defines a word. What's the difference between שמחה and ששון?  Between חכמה, בינה, דעת, and שכל?  The Malbim discusses
all of these things, but it's not always easy to find where he does. Sometimes you can search for the word in a pasuk---but
he sometimes just gives it in short, then says "כמו שכתבתי במקום אחר".  I hoped to create an index to identify just where that
מקום אחר is.

But as soon as I started, I realized that it's possible to do more, to also identify where the Malbim discusses central and
important concepts.  The places where he does are scattered all over the place, and sometimes difficult to find when they're
needed.  An index for those would be even more useful.


My approach to this task is to separate the content from the implementation.  I worked out a basic syntax for recording where
the Malbim talks about different concepts in text files.  Python scripts in the implementation folder compile the text files into a
final LaTeX document.


##Syntax

Each text file will be stored in a directory with a descriptive name.  The directory has a file called info.txt, which 
describes how to report where the file is.  Bereishit/info.txt, looks something like this:

2
בראשית \1 \2

This means that the first 2 words on each line identify where the pasuk is located.  There might be other possibilities.
Something the Malbim says in his Hakdama to Shir Hashirim, for example, might go in a subfolder of Shir Hashirim, with its own
info.txt, which will override the main info.txt in the main Shir Hashirim directory:

0
שיר השירים הקדמה

After the number of words indicated in info.txt, each word on the line (separated by spaces) is interpreted as a word or
phrase that the Malbim defines in that perek and pasuk, or a comparison between words.  For example, Vayeishev/rishon.txt:

לה א [מצרים=כור~הברזל] ישב [ארץ~כנען]
לה ב תולדות רֹעֶה מביא~דבה-מוציא~דבה [מדות] [טבע-שכל]
לה ג בן~זְקֻנִים [אהבה~עצמיית-אהבה~גשמיית] [סגולה] [ברכת~אברהם] [שנאה]
לה ה הגדה-ספור
לה ו הנה קם-נצב-עמד
לה ח מלך-מושל
לה ט הגדה-ספור

###Synonyms, tildes, and brackets

The first "word" for pasuk א is [מצרים=כור~הברזל].  This means that the Malbim discusses Mitzrayim's role as the iron crucible
in this pasuk (which makes sense).  The brackets mean that the Malbim is defining concepts, not words.  The ~ means that כור
הברזל is one phrase, and the = means that both terms are referring to the same thing, so someone searching for מצרים or כור or
הברזל should have this in the result list.  It's also possible that someone would search for ברזל (without the ה).  But this
is a different kind of equality.  It's unlikely that someone would ever search for ברזל and not want results involving הברזל,
so while the words don't mean exactly the same thing, for the purposes of this search they are "global synonyms".  It's very
possible, however, that someone might search for ברזל and be interested in actual physical iron, for example, in the issur to
cut stones of the mizbeyach with iron, not in every place the Malbim talks about the role of Mitzrayim.  מצרים and כור הברזל
are "local synonyms".

Local synonyms do not have to be "synonyms" in the normal sense of the word.  One of the Malbim's major contributions is to
show how two words never mean exactly the same thing.  The purpose of local synonyms is that *for this particular discussion*,
people are equally likely to search for either.

Global synonyms are recorded in synonyms.txt in the main directory.  Any words listed there are essentially equivalent.  The
only words that belong there are something someone might conceivably search for.  For example, הגיד, מגיד, and הגדה are both
"base" forms of the verb, and someone might search for any of them.  It's unlikely that someone would search for something
like וכשתגדנה, so that doesn't belong in synonyms.txt *or* as a local synonym where the Malbim talks about הגדה vs. ספור. 
While it is a global synonym in the sense that it's equivalent for the purposes of a search, it's not something that would
practically be searched for.

There are also one-way synonyms.  What I mean by this is that someone searching for ספר might be looking for הגדה vs. ספור or
for ספירה vs. מניה, but someone searching for ספור is not looking for anything about ספירה or vice versa.  I indicate this by
greater than or less than symbols. For example,

ספור<ספר
ספירה<ספר

One way synonyms have to be global, because there's no point in a local one way synonym.

Each row of synonyms.txt should be in alphabetical order, and the lines should be in alphabetical order by the first word.
That way it's easier to avoid duplicates.  One way synonyms should be on a line by themselves, but two way synonyms can be chained
together.  A line should have exactly one of these in it:
- a single >
- a single <
- any number of =

###Base form

The second word is ישב, which comes from וישב.  I reduce the verb to its "base" form, which in this case is, equivalently, עבר
זכר or the 3 letter shoresh.  That's the most likely thing for someone to search for.  I am not sticking to any particular
grammatical rule for what defines the base form---just what people are likely to search.  If there's more than one, pick
one and put the others in synonyms.txt if they're global synonyms, or connect them with an = if they're local synonyms.

###Nekudot

In pasuk ב, the word רֹעֶה has nekudot.  The search should ignore nekudot, but they should be put in place wherever they're
needed for clarity.  This includes synonyms.txt

###Comparisons

The Malbim comments in pasuk ב in the difference between a מביא~דבה and a מוציא~דבה.  Yosef could not have been making up what
he told Yaakov about his brothers, because (aside from the fact that we know he was a tzadik) in that case he would have been
a מוציא~דבה, but the Torah says ויבא יוסף את דבתם.  I indicate this comparison with a hyphen.

The only exception is in perek or pasuk numbers, or equivalent.  There, hyphen means what it normally does.  In LaTeX output
for proper formatting it's turned into double hyphen, which represents an n dash.

###Grammar

In chamishi of Chayei Sarah:

כד נח (אפעל-אפעלה)

The Malbim comments on the difference between אלך and אלכה.  This is a grammatical comment, so it goes in parentheses.  The
placeholder shoresh פעל is used, while the real words are placed as global, one way synonyms in synonyms.txt.

###Comments

Any line starting with # is ignored.

###Order of Operations

Any words separated by a space are completely separate, and are evaluated individually.  After the first few words on the line
(probably 2 in most cases), the words after that are associated to the location defined by the first two.
It doesn't matter
whether they are on one line or two---for example, בראשית לה ו above is equivalent to

לה ו הנה
לה ו קם-נצב-עמד

Normally there's no reason to use this long form, but it's available.  For example, in shevii of Vayeitzei, I split up

לא נג פחד~יצחק
לא נג אלהי~נחור

The Malbim does not actually define פחד יצחק as a reference to Hashem.  But since Rashi does, it's better not to put it on the
same line as a reference to avodah zarah.

Tildes are higher priority than equals, which are higher priority than hyphens.  For example, in shevii of Vayeishev,

משקה=אופה-משקה~מלך~מצרים=אופה~מלך~מצרים-שר~המשקים=שר~האופים

Using parentheses to indicate the order (not a grammatical comment), this would be split like this:

(משקה=אופה)-[(משקה~מלך~מצרים)=(אופה~מלך~מצרים)]-[(שר~המשקים)=(שר~האופים)]

Overall, the order of operations is:
* folder grouping (used for info.txt)
* newlines or new files---the file divisions are arbitrary, and just for the purpose of seeing what's there and what still
needs to be done
* perek and pasuk numbers, or equivalent, at the beginning of each line (as determined by info.txt)
* space
* hyphen
* equals
* tilde
