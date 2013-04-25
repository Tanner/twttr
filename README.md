# twttr
An [esoteric programming language](en.wikipedia.org/wiki/Esoteric_programming_language) based on [Twitter](https://twitter.com/).

# Specification
## Variables
Twitter users are variables. They store and hold signed integers.

### Creation
Twitter users are created by making a first tweet. Initially all users have a value of zero.

First tweets must contain the words `first` describing the words `tweet`, `status`, or `post`.

```
tanner: First tweet!
ryan: Making my first post on Twitter.
```

## Status
Regular status updates perform either addition or multiplication depending on the number of words in the tweets.

If the number of words is odd, then addition is performed. Otherwise, multiplication is performed.

The other term involved in the calculation is number of letters in the first word. Negative numbers are denoted by the status ending in a bang "!".

```
tannerld: My cat should be clean.
ryan: Not cool!
```

Turns into:

```
tannerld = tannerld + 2
ryan = ryan * -3
```

## Mentions

## At-Replies

## Hashtags
Hashtags are used to indicate instructions related to a branch.

```
tanner: Heading over to the hotel #wwdc
```

A branch is a status that contains a question and a hashtag. The branch will be taken if the value of the author is not zero.

The target of the branch is the first use of the hashtag. The next instruction executed following that instruction is any status update containing the hashtag. The branch is reevaluated when the original branch statement is reached.

Any further uses of the hashtag after the branch are ignored.

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

## Over Heard
Input is taken in and set to a variable via a status starting with "OH: " aka "overheard".

Any text after the colon is the prompt.

```
tanner: OH: What is the name of the cat?
```