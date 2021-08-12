"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self):
        self._all_playlists = {}

    def get_all_playlists(self):
        """Returns all playlist names."""
        return self._all_playlists.keys()

    def get_videos_in_playlist(self, playlist_name):
        result = None
        for name, video_dict in self._all_playlists.items():
            if name.lower() == playlist_name.lower():
                result = video_dict
                break
        return result

    def add_playlist(self, playlist_name):
        self._all_playlists[playlist_name] = {}

    def add_video_to_playlist(self, playlist_name, video):
        result = None
        videos_in_playlist = self.get_videos_in_playlist(playlist_name)

        """ If video does not exist, add into playlist """
        if videos_in_playlist.get(video.video_id, None) == None:
            videos_in_playlist[video.video_id] = video
            result = video.title
        return result

    def remove_video_from_playlist(self, playlist_name, video_id):
        videos_in_playlist = self.get_videos_in_playlist(playlist_name)
        return videos_in_playlist.pop(video_id, None)

    def clear_playlist(self, playlist_name):
        videos_in_playlist = self.get_videos_in_playlist(playlist_name)
        videos_in_playlist.clear()

    def delete_playlist(self, playlist_name):
        return self._all_playlists.pop(playlist_name, None)
