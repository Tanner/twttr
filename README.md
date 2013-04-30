# twttr
An [esoteric programming language](en.wikipedia.org/wiki/Esoteric_programming_language) based on [Twitter](https://twitter.com/).

# Hello World Example
```
john: Hating!
bob: Heh. I wonder if this means we get a refund!
bob: Well. We have not found the kid yet!
bob: Nurses don't know!
bob: Trying other rooms. Still no luck!
sally: Found them!
sally: They might be in the other lot.
sally: I still cannot find my keys.
john: Hate this!
bob: Definitely not a cat. Rats!
bob: Nope. Cat!
bob: I think we might've found him inside!
bob: We lost the kid. Atleast I think!
sally: Is this right... No!
tannerld: Oh bugger. I'm lost again. #lost
clara: Ah. #lost
john: Looking for cat. #lost #bored
bob: My new boy is on the home from the hospital. #lost
sally: Someone in the lot needs some help. #lost #keys
tannerld: I have never had a sandwich as good as Joe's.
```
Adapted from [Brainfuck Hello World](http://en.wikipedia.org/wiki/Brainfuck#Hello_World.21).

# Specification
## Variables
Twitter users are variables. They store and hold signed integers.

### Creation
Twitter users are created by making a first tweet. Initially all users have a value of zero.

## Status
Regular status updates perform addition given the two fragments in the status update. The result is added to the user's value and stored in the user.

A fragment is defined as words before puncuation marks, e.g. `.,!;?:-`.

The number added is determined by the number of words in either the two fragments. The first fragment is indiciated as positive numbers and the second fragment is negative numbers.

```
tannerld: This is my cat. I love it.
ryan: I hate my job. Someone please find me a new.

tanner = 1
ryan = -2
```

### Input
Input is received from the user when a status ends in a question mark (excluding branches). The resulting ASCII value is stored in the author.

The prompt is the status text.

```
tannerld: Do you like coffee?
```

### Printing
Printing the user's value is done by ending the last sentence in the status with a exclamation point.

```
tannerld: I love coffee!
```

## Mentions
Mentions subtracts the value of the user mentioned from the author.

```
tanner: Having a great time with @ryan at WWDC.

tanner = tanner - ryan
```

## @replies
@replies adds the value of the user mentioned to the author.

```
tanner: @ryan I'm heading over to the food court.

tanner = tanner + ryan
```

## Hashtags
Hashtags are used to indicate instructions related to a branch.

```
tanner: Heading over to the hotel #wwdc
```

A branch is a status that contains the last instance of a hashtag. The branch will be taken if the value of the author is not zero.

The target of the branch is the first use of the hashtag. The next instruction executed following that instruction is any status update containing the hashtag. The branch is reevaluated when the original branch statement is reached.

```
tanner: Who is at the hotel? #wwdc
```

## Retweets
Retweets assign the value of the user who was retweeted to the user who retweeted the status.

Note: The value assigned is whatever value the user was assigned at the time of the status update.

The below example stores the value from `ryan` into `tanner`.

```
tanner: RT @ryan "Baking a cake"
```