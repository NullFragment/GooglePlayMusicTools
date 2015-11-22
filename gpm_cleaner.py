#!/usr/bin/env python

# created by shuichinet https://gist.github.com/shuichinet
# forked from https://gist.github.com/shuichinet/8159878 21 Nov 2015
# using minor edits by fcrimins https://www.reddit.com/user/fcrimins from https://www.reddit.com/r/google/comments/2xzgyv/remove_duplicate_songs_from_google_play_music/csh6mrh
# compiled by John M. Kuchta https://medium.com/@sebvance
# thanks to shuichinet and fcrimins for their work

from gmusicapi import Mobileclient
from getpass import getpass

client = Mobileclient()
client.login( raw_input( "Username: " ), getpass(), Mobileclient.FROM_MAC_ADDRESS )

print "Getting all songs ..."
all_songs = client.get_all_songs()
new_songs = {}
old_songs = {}

for song in all_songs:
    song_id = song.get('id')
    timestamp = song.get('recentTimestamp')
    
    key = "%s: %d-%02d %s" % ( song.get('album'), song.get('discNumber'), song.get('trackNumber'), song.get('title') )
    
    if key in new_songs:
        if new_songs[key]['timestamp'] < timestamp:
            old_songs[key] = new_songs[key]
            new_songs[key] = { 'id': song_id, 'timestamp': timestamp }
        else:
            old_songs[key] = { 'id': song_id, 'timestamp': timestamp }
    
    new_songs[key] = { 'id': song_id, 'timestamp': timestamp }

if len( old_songs ):
    print "Duplicate songs"
    
    old_song_ids = []
    
    for key in sorted( old_songs.keys() ):
        old_song_ids.append( old_songs[key]['id'] )
        print "    " + key.encode('utf-8')
    
    if raw_input( "Delete duplicate songs? (y, n): ") is 'y':
        print "Deleting songs ..."
        client.delete_songs( old_song_ids )
else:
    print "No duplicate songs"