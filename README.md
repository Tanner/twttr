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

Other examples can be found in [EXAMPLES.md](EXAMPLES.md).

# Specification
## Variables
Twitter users are variables. They store and hold signed integers.

For simplicity, usernames can only contain alphanumeric characters.

### Creation
Twitter users are created by making a first tweet. Initially all users have a value of zero.

## Status
All status updates perform addition given the two fragments in the status update. The result is added to the user's value and stored in the user.

A fragment is defined as words before puncuation marks, e.g. `.,!;\?:-`.

The number added to the user is determined by the number of words in the two fragments. The first fragment is indiciated as positive numbers and the second fragment is negative numbers.

```
tannerld: This is my cat. I love it.
ryan: I hate my job. Someone please find me a new.
```

Results in:
```
tannerld = 1
ryan = -2
```

### Input
Input is received from the user when a status ends in a question mark (excluding hashtags). The resulting ASCII value is added to the author.

The prompt for the input is the status text.

```
tannerld: Do you like coffee?
```

Results in:
```
Do you like coffee? A

tannerld = 65
```

### Printing
Printing the user's value is done when a status ends in a exclamation mark (excluding hashtags).

```
tannerld: I love coffee!
```

## Mentions
Mentions subtracts the value of the user mentioned from the author.

```
tannerld: Having a great time with @ryan at this concert.
```

Results in:
```
tannerld = tannerld - ryan
```

## @replies
@replies adds the value of the user mentioned to the author.

```
tannerld: @ryan I'm heading over to the food court.
```

Results in:
```
tannerld = tannerld + ryan
```

## Hashtags
Hashtags are used to indicate instructions related to a branch.

For simplicity, hashtags can only contain alphabetic characters.

```
tannerld: Heading over to the hotel #foofighters
```

A branch is a status that contains the last instance of a hashtag. The branch will be taken if the value of the author is not zero. The target of the branch is the first use of the hashtag.

If the branch has been taken, the only instructions that will be executed must contain the hashtag that caused the branch.

The branch is reevaluated when the original branch instruction statement is reached.

```
tannerld: My cat hates me. It knows something about me. #cat
ryan: Plus two. Maybe. #cat
tannerld: I love my kitty cat.
```

Results in:
```
tannerld = 0
ryan = 5
```

## Retweets
Retweets assign the value of the user who was retweeted to the user who retweeted the status.

Note: The value assigned is whatever value the user was assigned at the time of the status update.

```
tannerld: RT @ryan Dancing is not cool. That is definitely not cool.
ryan: Ok maybe this is cool.
ryan: Dancing is not cool. That is definitely not cool.
ryan: Not sure if I'm ready for this.
```

Results in:
```
tannerld = 6
ryan = 11
```