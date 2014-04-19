nba_reddit
==========

This is a comment stream that I built for myself to learn Reddit's api.


Disclaimer: ###This is not a scalable app at the moment.

Due to the limitations of use Reddit puts on their api, it is very difficult to build a comment stream that fits within
Reddit's rules. Reddit only allows 30 hits per minute, which when it comes to scalability, it really makes building
a comment stream difficult. If I were to publish this app, I would probably rebuild it in socket.io, so that the
server is calling the shots and the client is listening. With several users using ajax long-polling, which is what I
am doing now, you are going to go way above 30 requests.

Since this is only an NBA comment streaming app, I could build a recursive module that hits each of the threads on a
timer and populates the results to Redis. The consuming side of the api could then grab the results when requested from the client.
It is very unlikely that more than 5 to 7 nba games are happening at one time, so comment streams would not take that huge
of a hit in performance.