Collect
=======

This module provides functionality to scrape the 
[malawi-music.com](http://malawi-music.com) website for information.

## Bundle Download

Included in this module is a tool to allow you to download multiple
songs from the Malawi Music Website "in bulk". Ofcourse, how long
it takes to download given "Bundle" will depend on your internet 
connection and other things.

You might find it useful if you know the ids of the songs you want 
to download in advance.

### Example usage

```sh
$ python -m collect.bundle --bundle MyBundle --dir /home/user/Music 830 7300
```

This will download the songs with id `803` and `7300` and place them
in a directory with the name `MyBundle-<timestamp>`, where the timestamp
is some integer value, in the `/home/user/Music` directory.
