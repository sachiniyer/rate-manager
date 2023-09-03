# rate-manager

This is a quick and dirty python package to help you manage rate limits for an api.

## Example

If you have some rate limits such as

1. <10 queries per minute
2. <100 queries per hour
3. <9000 queries per day

Then you can use this package to figure out if you can send a request right now (or if you have to wait)

## Design

Basically, it is just a bunch of queues that are comprised of nodes representing times when queries were sent.

Each queue represents one interval, and has all the nodes between now through now - interval (e.g. minute, hour...). If the time is 9:00 and you have a rate of $x$ per hour, the queue will have everything between 8:00-9:00.

If all the queues are below their limits (e.g. for the rate of 100 queries per hour, the hour queue has less than 100 nodes), then you can send a queries. If not, you get the time that you have to wait (the time to get all queues under length)

It will also sync with local files.

### Chain of events

For all queues:

1. pop until all times are within their respective intervals
2. take difference of last node with current time and remove that from interval $interval - (current time - last node time)$
3. get max of differences and return 0 if negative.
