# PyCh

[![codecov](https://codecov.io/gh/BehindLoader/py2ch/branch/master/graph/badge.svg)](https://codecov.io/gh/BehindLoader/py2ch)
[![Build Status](https://travis-ci.com/BehindLoader/py2ch.svg?branch=master)](https://travis-ci.com/BehindLoader/py2ch)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

## Usage

First import:

```
>>> from py2ch.catalog import Catalog
```

Get threads list:

```
>>> catalog = Catalog('b')
>>> catalog.threads
[<Thread board="b" #200000001 "Тема треда">...]
```

Get thread info:

```
>>> thread = catalog.threads.pop()  # Get last thread
 
>>> thread.subject
'%%Тема треда%%'
```

Get thread post:

```
>>> thread.posts
[<Post #201306703>, <Post #201306882>, <Post #201308883>]

>>> OP = thread.posts[0]
>>> OP.comment
'Даже у него есть тян'
```

Get post files:
```
>>> OP.files
```

## Docs

### `class py2ch.catalog.Catalog(board: str)`

Threads catalog class. Accepts the name of the board.

#### `Catalog.board`

__type__: `str`

The board short name.

#### `Catalog.threads`

__type__: [`Threads[]`](#class-py2chthreadthreadkwargs)

Threads list in specified board. (Lazy property, loads only when called.)

### `class py2ch.file.File(**kwargs)`

Attachment file in post.

#### `File.displayname`

__type__: `str`

Cropped attachment display name.

#### `File.fullname`

__type__: `str`

Full attachment display name.

#### `File.height`

__type__: `int`

Height of attachment in pixels.

#### `File.md5`

__type__: `str`

MD5 hash sum of attachment.

#### `File.name`

__type__: `str`

Server file name.

#### `File.nsfw`

__type__: `int`

...

#### `File.path`

__type__: `str`

Full URL to file.

#### `File.size`

__type__: `int`

Size of attachment in bytes.

#### `File.thumbnail`

__type__: `str`

Full URL to attachment thumbnail.

#### `File.tn_height`

__type__: `int`

The attachment thumbnail height.

#### `File.tn_width`

__type__: `int`

The attachment thumbnail width.

#### `File.type`

__type__: `int`

The attachment type.

1. jpg
2. png
6. webm
10. mp4/mov

#### `File.width`

__type__: `int`

The attachment file width.


### `class py2ch.post.Post(**kwargs)`

#### `Post.board`

__type__: `str`

Post board name.

#### `Post.banned`

__type__: `int`

...

#### `Post.closed`

__type__: `int`

...

#### `Post.comment`

__type__: `str`

Post text with markdown tags.

#### `Post.date`

__type__: `str`

Datetime posted.

#### `Post.email`

__type__: `str`

Post author email.

#### `Post.endless`

__type__: `int`

...

#### `Post.files`

__type__: [`File[]`](#class-py2chfilefilekwargs)

List of File instances.

#### `Post.lasthit`

__type__: `int`

...

#### `Post.name`

__type__: `str`

Post author name.

#### `Post.num`

__type__: `int`

Global post id.

#### `Post.number`

__type__: `int`

Post id regarding thread.

#### `Post.op`

__type__: `int`

Flag OP. 

#### `Post.parent`

__type__: `str`

Parent thread post.

#### `Post.sticky`

__type__: `int`

...

#### `Post.subject`

__type__: `str`

Thread post subject.

#### `Post.timestamp`

__type__: `int`

Timestamp when posted.

#### `Post.trip`

__type__: `str`

...

### `class py2ch.thread.Thread(**kwargs)`

#### `Thread.board`

__type__: `str`

Thread board name.

#### `Thread.comment`

__type__: `str`

Thread OP text with markdown.

#### `Thread.lasthit`

__type__: `int`

...

#### `Thread.num`

__type__: `str`

Thread OP id.

#### `Thread.posts_count`

__type__: `int`

Count of posts inside thread.

#### `Thread.score`

__type__: `float`

Score of the thread.

#### `Thread.subject`

__type__: `str`

Thread subject.

#### `Thread.timestamp`

__type__: `int`

Thread created timestamp.

#### `Thread.views`

__type__: `int`

Count of views of thread.

#### `Thread.url`

__type__: `str`

Thread full URL.

#### `Thread.posts`

__type__: [`Post[]`](#class-py2chpostpostkwargs)

Get thread posts list.
