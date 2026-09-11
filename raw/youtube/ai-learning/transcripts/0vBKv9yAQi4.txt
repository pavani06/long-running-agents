[Music]
hey everyone uh my name is Zach Reno
Adine uh I'm going to be telling a few
stories and hopefully we'll leave you
all entertained and with an idea of how
we build agents and improve them at
Sierra so in a nutshell Sierra is the
conversational AI platform for
businesses and just poll of the room out
of curiosity how many people have heard
of
Sierra so most of the room but not all
if you've heard of us you probably
associate us with uh chat experiences
and perhaps with customer service and
that's a lot of what we do uh but I
would say that we're kind of broadening
out in both cases uh probably by the end
of this year most of our interactions
will be over the phone um so that's
already a big area for us and we'll also
have a lot more touch points we have a
lot of customers uh which I'll show
today who are using us for um sales for
subscription management for product
recommendations kind of all pieces of
the customer
experience I noticed yesterday were a
lot of people here yesterday some people
so it was funny to watch people were
reflecting on you know how much has
happened in Ai and they had these
timelines and they went way back in time
and so Colin from augment code went all
the way back to
2023 uh Wasim from writer was talking
about purpose-built models and went all
the way back to
2020 and Grace from Lux Capital went
even further she went back to 2019
although if you zoom in you can see
actually the first thing here is still
from 2020 so everyone was reflecting on
ancient history in Ai and it was all
this decade so I'm going to zoom back
even further
2016 in the AI
caves and I know uh what you're thinking
you know AI goes back to the 70s and all
that but it definitely felt like the
caves in 2016 I know because if you zoom
in on the bottom right you can see I'm
actually down there I was working at
Google uh with a bunch of amazing
computer vision engineers and uh what
that meant in 2016 is we were really
trying to help computers understand the
difference between Chihuahua and
blueberry
muffins and you know it's not actually
that simple uh it's not just Chihuahua
and blueberry muffins you know it's dog
dogs and bagels dogs and mops and of
course dogs and fried
chicken and so in other words what we
were doing is we were building the first
version of Google Lens um and at this
time I lived in New York City I was in
the East Village and I had about a 30
minute walk to work and on my walk I
would see a bunch of stuff New York's
one of the greatest walking cities in
the world and I would say what's going
on there what are they even doing or oh
I wonder if that bookstore is nice or I
wonder if this restaurant is tasty or oh
my goodness look at that dog uh and so
there were also a bunch of flowers on
the walk at this time Google Lens was in
its infancy and one of the very few
things that computer vision models were
actually good at that had some consumer
application was identifying plants you
might still know this today it's kind of
in the you know is that bug poisonous
category and so I'd ask questions on the
walk like you know can it tell the color
of the plant in addition to the species
or what's that what type of fern or or
Palm is that and there's a bunch of
shops on this walk so I'd even walk in
these are all actually photos from 2016
from my walks to work and I would go in
and test them all out and as you can
imagine you know sometimes it was
accurate and sometimes you know it
wasn't necessarily wrong but it wasn't
really on the nose either and so it felt
like a slot machine and I think everyone
here who's building with AI can probably
understand that feeling of uh it worked
five times in a row Why didn't it work
the sixth time whether it's the
non-determinism of the inputs or the
non-determinism of the outputs that's
just part of what it means to be
building with
AI so let's fast forward a bit to
present day Google Lens you can not only
search what you see you can also shop
what you see you can do this on Google
Images on YouTube you can do it with
your camera you can translate non-latin
character sets into English so you can
read the washing machine in Tokyo and
actually figure out what settings in
your Airbnb you should use you can do
your math homework I'm a little bit too
old to have benefited from this but
apparently it's a Brave New World out
there for the kids and of course this is
from the Google enss homepage you can
still identify
flowers so this is all very mind-blowing
but in my opinion it comes down to
consistent step-by-step iteration over a
decade and when we think about what
drives this we're all engineers in the
room we understand that you need a
process to iteratively improve to get
better without also getting worse and
this over time has kind of been
considered software development life
cycle how do you continuously improve
how do you implement test maintain
analyze design and go through this as
many times as you
can let's rewind a bit more
2012 the AI caves you know the drawings
are a little bit less sophisticated I'm
not there yet uh I've been oblad and I
pulled some headlines from around this
time you can see this is uh around when
Google brain was watching cat videos and
identifying them on YouTube and it was a
big breakthrough I don't know if anyone
remembers how big this model was it was
about a billion parameters and this was
a huge breakthrough if you think today
the frontier models are about a trillion
parameters so it was one 1,000th it was
as if this whole room had like a quarter
of a person in
it and so uh it was still very
impressive at the time there was also a
theory you know everyone thought
computers would be limited in terms of
what they can achieve I think this is a
less popular Theory today what I'm
trying to say is it was a long time ago
this is also around the time that Mark
andri published his famous essay that
said soft worries eating the world and
that took a lot of people by storm if
you looked at Stanford University on
campus you would have seen some early
stage startups forming on the lawn does
anyone know which startups I'm talking
about you can call it
out okay you might be thinking Snapchat
uh not that one I did actually hear door
Dash in the back very good guess not
that one either of course I'm talk you
look like stylish people so I I think
you'll know what I'm talking about I'm
talking about
Chubbies Chubbies had a contrarian idea
that was also right which was not only a
software eating the world but teeny
shorts for men are also going to take
over and uh as I mentioned they were
correct which you can see here and you
can also see here
fast forward to
2024 uh kit Garten SVP of commercial at
cheles we were fortunate enough to host
her in Sierra's office and Chubbies has
had an amazing brand since they were
founded and they've always been on the
Forefront of customer experience they've
always been thinking about how to level
up and how to make the experience more
fun and better for their customers and
so it clicked immediately for kit that
the same way you needed a website in
1995 the same way your business needed a
Social profile and a mobile app this
Millennium in 2025 you need an AI agent
to represent your business and to help
your
customers so kit and Chubbies partnered
with
Sierra we came up with an AI agent which
is affectionately called Duncan Smothers
first and foremost he's incredibly
capable but almost as importantly he's
always down to clown Duncan mothers is
on the Chubby's website and can help you
with a variety of cases
I got permission from kit to show some
of these conversations to you today so
you can see what some of the Sierra
interactions look like under the hood
and some of the things that these agents
are capable of so on the left here you
have a customer asking a question about
sizing and fit Duncan is able to
empathetically help them while asking
questions like what's your waist size
and offer product recommendations at the
end it gets a thumbs up from the
customer another example another thumbs
up this is inventory track in Duncan can
tell what's in stock and help customers
choose new
items and then finally package tracking
and refunds so more customer love uh in
this case the Duncan is able to inform
the customer actually there's a couple
different tracking numbers for your
order and in the second case issue a
refund and so when we talk about
autonomous agents agents actually taking
action not just answering questions this
is what we're talking about and the
results for Chubbies have been they're
able to help more customers more quickly
and with higher
satisfaction the way that we get to this
is because we believe at Sierra that
every agent is a product that means that
you can't just drag and drop a bunch of
boxes you need a fully featured
developer platform you need a fully
featured customer experience operations
platform in order to work on this the
same way you would work on your mobile
app the same way that you would work on
your website if you want the best
results and so when Chubbies is
partnering with Sierra it's not just
using the product it's is actually
partnering with our team and so we have
dedicated agent engineering and agent
product management functions that you
can think of sort of as forward deployed
with our customers working closely with
kit and her team on a daily
basis by the way remember that face that
you just saw on the last slide were any
was anyone here at the AI engineering
World's Fair uh back in
June nice got some whoops from the
audience uh so I know Ben was there he's
up there on stage introducing everyone
and the energy was electric you can see
the crowd is packed when I got there the
first thing I did was I sat down at the
Deep gram Workshop this was the uh about
three months into me building voice
agents at Sierra and I was very
interested in what deep gram had to say
what did they think of the latest
multimodal models how are they handling
latency how are they handling tone and
phrasing all of these problems that were
new at the time and I sat down next to a
man named Shawn and Shawn and I were
nerding out about how to increase the
speed of our developer Loop by using the
say command on Mac and then using a
program called loop back in order to
pipe that into the browser so that we
didn't have to wear headphones and talk
and look awkward in the office Sean gave
me his contact info he was interested in
Sierra and a few months later uh there
we are working together in the office so
when I told our company and our Founders
hey I'm going to the AI Summit uh you
know I hope it's as productive as the
last one I'm excited to learn they said
go find more
Shan so I'm hopeful that people in the
audience will say hi after this uh
whether or not you're interested in
working at Sierra I'm interested in
meeting you and so uh I'm I hope to meet
you later today anyway back to Duncan
mothers the point of the software
development life cycle the point of our
agent engineering team is that even if
Duncan is not perfect today he should be
getting better every single day and so
what we did is we sought out to build
something like the software development
cycle borrowing as many Concept as we
could and inventing new ones where we
needed
to the issue is that large language
models are like building on top of a
foundation of jello and so you can't
just take everything out of the box and
have it just work while traditional
software is deterministic fast cheap
rigid and and governed by if statements
that always follow logic large language
models can be non-deterministic they can
be slow they can be expensive to run
they're very flexible though they are
creative they can reason through through
problems and so we wanted to create a
methodology that takes advantage of all
the strengths of large language models
and then also is able to invoke
traditional software where it's
helpful and that brings me to slide
78 the agent development life cycle so
at Sierra this is the process by which
we build and improve AI
agents you might be thinking about it
like oh that looks kind of like the
software development life cycle and I
think the devil is in the detail so I'm
going to dive in a little bit it's not
that these are revolutionary or
Innovative Concepts it's that each one
of them involves iterative refinement
with customers in production to make it
as productive and as bulletproof as
possible so if we dig into quality
assurance for example if you work at one
of your customer one of our customer
companies you have access to Sierra's
experience manager what that means is
that you can dive in and look at every
conversation and you can look at high
level reports of how is the agent
forming in real time you can provide
feedback so for example if Duncan
Smothers has incorrect inventory maybe
it made one API call to one warehouse
but it didn't make all the API calls
that it needed to or one of them timed
out whatever it may be you can report
this issue it then will lead to an issue
being filed which leads to a test being
created and then once that test is
passing we can make a new release and
over the course of time a Sierra agent
will go from having a hand handful of
tests at launch to hundreds and then
thousands of tests as it
improves another example here is it's
not always that the agent is making a
mistake sometimes there's an opportunity
to go above and beyond uh Chubbies
actually has each of its agents have a
budget in order to Delight customers and
so in this case Duncan mothers could
actually you know door Dash the shorts
from a retail location if they're not
available
online so this is the agent development
life cycle at work but the thing is a
year ago we were doing this all manually
this was kind of early on in in in the
history of Sierra and we were learning
what works at each of these stages and
with the uh improvements to AI we're
actually able to add AI to each part of
this life cycle and speed up the
improvements in the present
day but it's bigger than just Duncan the
agent development life cycle is more
effective the larger the customer is and
while Duncan hand hundreds of thousands
of requests we have customers that are
doing tens of
millions so the more valuable the
velocity and change management are when
you're that
big and the change also comes from
everywhere it's not just that oh there's
an issue with the agent and we need to
improve it there's tons of stuff going
on outside there's all those graphs at
the beginning of this presentation
showing how fast our space is moving you
have models being upgraded you have new
paradigms like reasoning models you have
of multimodality and more and more when
we think about how these impact the
agent development life cycle reasoning
models are a force multiplier toward
each step we're actually able to be more
effective applying AI to development to
testing to QA and every step in
between now another one that's near and
dear to my heart I mentioned the Deep
gram Workshop eight months ago which was
an accelerant uh in my understanding of
the voice landscape is building for
voice and I started working on this
about a year ago uh and in October we
were able to launch Voice generally
available at Sierra one of our large
customers that has benefited from the
agent development life cycle that has
you know tens of millions of customers
in the United States is Serius XM and
with Sierra's voice capabilities they're
able to pick up the phone right away
every time to answer their
customers the way that we think about
voice I think is similar to the way that
we think about web development today if
you remember 10 15 years ago a lot of
websites were you know m. website.com
you had two separate websites for mobile
phones and for desktops and then we
graduated to responsive design and this
is how we think about our AI agents at
Sierra to under the hood it's the same
platform it's the same agent code but
it's able to be responsive to whatever
Channel someone reaches out in and
whatever modality you're operating in of
course you can still customize the the
same way you might have a different
layout you can still have different
phrasing you can still parallelize
requests to achieve lower latency but it
basically just works out of the
box I'll close with a few thoughts this
is something I've been thinking about a
lot lately one of the most fascinating
and fun Parts about building with AI is
that large language models remind us of
ourselves in short they're unpredictable
they're
slow and they're not that great at math
but also it allows us to be great
designers by having empathy in a way
that we probably couldn't ever before
with
computers and so you can actually put
yourself in the shoes of the robot you
can put yourself in the I don't know
primordial soup of the Jell-O and you
can think about what it would mean to
actually build a good experience and as
someone who's building voice agents and
a bunch of you I bet in the audience are
I know there's kind of this thought on
are these multimodal agents the real
deal you know should I just kind of wire
everything together and hope it works
and the question I've been asking myself
a lot lately and what our results have
kind of shown us is you know how would
you do if someone just passed you
transcribed text of your conversation
partner with a few hundred milliseconds
of delay and then you had to respond on
the spot and so what we're building at
Sierra is much more robust and very
exciting to me and I hope to talk to you
all about it I think on my badge it says
voice too models is the thing that I'm
excited about uh and so here is kind of
a sense of the robustness and the
richness of what you can create when you
let large language models have the same
inputs and same experiences that humans
have um and so uh thank you for your
time today I look forward to a lot of
engaging discussions and uh it's great
to talk to you all
[Music]