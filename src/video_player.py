"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import random

def sort_title(item):
    return item.title

def filter_flag_video(list):
    new_list = []
    for video in list:
        if not video.flag:
            new_list.append(video)
    return new_list

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist = Playlist()
        self._current_video = None
        self._paused = None

    """ PART 1 """
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        print("Here's a list of all available videos:")

        for video in sorted(self._video_library.get_all_videos(), key=sort_title):
            if video.flag:
                print("  " + video.title + " (" + video.video_id + ") ["
                        + ' '.join(video.tags) + "] - FLAGGED (reason: "
                        + video.flag_reason + ")")
            else:
                print("  " + video.title + " (" + video.video_id + ") ["
                        + ' '.join(video.tags) + "]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        target_video = self._video_library.get_video(video_id)
        if target_video == None:
            print("Cannot play video: Video does not exist")
        elif target_video.flag:
            print("Cannot play video: Video is currently flagged (reason: "
                    + target_video.flag_reason + ")")
        else:
            if self._current_video != None:
                self.stop_video()
            self._current_video = target_video
            self._paused = False
            print("Playing video: " + self._current_video.title)

    def stop_video(self):
        """Stops the current video."""

        if self._current_video == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: " + self._current_video.title)
            self._current_video = None
            self._paused = None

    def play_random_video(self):
        """Plays a random video from the video library."""

        if len(filter_flag_video(self._video_library.get_all_videos())) == 0:
            print("No videos available")
        else:
            if self._current_video != None:
                self.stop_video()
            random_video = random.choice(self._video_library.get_all_videos())
            while random_video.flag:
                random_video = random.choice(self._video_library.get_all_videos())
            self._current_video = self._video_library.get_video(random_video.video_id)
            self._paused = False
            print("Playing video: " + self._current_video.title)

    def pause_video(self):
        """Pauses the current video."""

        if self._current_video == None:
            print("Cannot pause video: No video is currently playing")
        elif self._paused:
            print("Video already paused: " + self._current_video.title)
        else:
            print("Pausing video: " + self._current_video.title)
            self._paused = True

    def continue_video(self):
        """Resumes playing the current video."""

        if self._current_video == None:
            print("Cannot continue video: No video is currently playing")
        elif self._paused:
            self._paused = False
            print("Continuing video: " + self._current_video.title)
        else:
            print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self._current_video == None:
            print("No video is currently playing")
        else:
            print("Currently playing: "
                    + self._current_video.title + " ("
                    + self._current_video.video_id + ") ["
                    + ' '.join(self._current_video.tags) + "]", end="")

            if self._paused:
                print(" - PAUSED")
            else:
                print("")

    """ PART 2 """

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlist.get_videos_in_playlist(playlist_name) != None:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlist.add_playlist(playlist_name)
            print("Successfully created new playlist: " + playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        if self._playlist.get_videos_in_playlist(playlist_name) == None:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot add video to " + playlist_name + ": Video does not exist")
        elif self._video_library.get_video(video_id).flag:
            print("Cannot add video to " + playlist_name
                    + ": Video is currently flagged (reason: "
                    + self._video_library.get_video(video_id).flag_reason + ")")
        else:
            target_video = self._video_library.get_video(video_id)
            video_title = self._playlist.add_video_to_playlist(playlist_name, target_video)
            if video_title == None:
                print("Cannot add video to " + playlist_name + ": Video already added")
            else:
                print("Added video to " + playlist_name + ": " + video_title)

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self._playlist.get_all_playlists()) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for playlist_name in sorted(self._playlist.get_all_playlists()):
                print("  " + playlist_name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlist.get_videos_in_playlist(playlist_name) == None:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Showing playlist: " + playlist_name)
            video_dict = self._playlist.get_videos_in_playlist(playlist_name).values()
            if len(video_dict) == 0:
                print("  No videos here yet")
            else:
                for video in video_dict:
                    if video.flag:
                        print("  " + video.title + " (" + video.video_id + ") ["
                                + ' '.join(video.tags) + "] - FLAGGED (reason: "
                                + video.flag_reason + ")")
                    else:
                        print("  " + video.title + " (" + video.video_id + ") ["
                                + ' '.join(video.tags) + "]")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        if self._playlist.get_videos_in_playlist(playlist_name) == None:
            print("Cannot remove video from " + playlist_name
                    + ": Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot remove video from " + playlist_name
                    + ": Video does not exist")

        else:
            video = self._playlist.remove_video_from_playlist(playlist_name, video_id)
            if video == None:
                print("Cannot remove video from " + playlist_name
                        + ": Video is not in playlist")
            else:
                print("Removed video from " + playlist_name + ": "
                        + video.title)

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlist.get_videos_in_playlist(playlist_name) == None:
            print("Cannot clear playlist " + playlist_name
                    + ": Playlist does not exist")
        else:
            self._playlist.clear_playlist(playlist_name)
            print("Successfully removed all videos from " + playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if self._playlist.delete_playlist(playlist_name) == None:
            print("Cannot delete playlist " + playlist_name
                    + ": Playlist does not exist")
        else:
            print("Deleted playlist: " + playlist_name)

    """ PART 3 """

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        target_videos = []
        for video in self._video_library.get_all_videos():
            if video.title.lower().find(search_term.lower()) != -1:
                if not video.flag:
                    target_videos.append(video)

        if len(target_videos) == 0:
            print("No search results for " + search_term)
        else:
            count = 0
            print("Here are the results for " + search_term + ":")
            for video in sorted(target_videos, key=sort_title):
                count += 1
                print("  " + str(count) + ") " + video.title + " ("
                        + video.video_id + ") [" + ' '.join(video.tags) + "]")

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            selection = input()

            try:
                selection = int(selection)
                if selection < 1 or selection > count:
                    return
                self._current_video = target_videos[selection-1]
                self._paused = False
                print("Playing video: " + self._current_video.title)
            except ValueError:
                return

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        if not video_tag.startswith("#"):
            print("No search results for " + video_tag)
        else:
            target_videos = []
            for video in self._video_library.get_all_videos():
                for tag in video.tags:
                    if tag.lower() == video_tag.lower() and not video.flag:
                        target_videos.append(video)
                        break

            if len(target_videos) == 0:
                print("No search results for " + video_tag)
            else:
                count = 0
                print("Here are the results for " + video_tag + ":")
                for video in sorted(target_videos, key=sort_title):
                    count += 1
                    print("  " + str(count) + ") " + video.title + " ("
                            + video.video_id + ") [" + ' '.join(video.tags) + "]")

                print("Would you like to play any of the above? If yes, specify the number of the video.")
                print("If your answer is not a valid number, we will assume it's a no.")
                selection = input()

                try:
                    selection = int(selection)
                    if selection < 1 or selection > count:
                        return
                    self._current_video = target_videos[selection-1]
                    self._paused = False
                    print("Playing video: " + self._current_video.title)
                except ValueError:
                    return

    """ PART 4 """

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """

        if self._video_library.get_video(video_id) == None:
            print("Cannot flag video: Video does not exist")
        elif self._video_library.get_video(video_id).flag:
            print("Cannot flag video: Video is already flagged")
        else:
            target_video = self._video_library.get_video(video_id)
            if self._current_video != None and self._current_video.title == target_video.title:
                self.stop_video()

            if flag_reason == "":
                flag_reason = "Not supplied"
            else:
                flag_reason = flag_reason.replace(" ", "_")
            target_video.update_flag(True, flag_reason)
            print("Successfully flagged video: " + target_video.title
                    + " (reason: " + flag_reason + ")")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        if self._video_library.get_video(video_id) == None:
            print("Cannot remove flag from video: Video does not exist")
        elif not self._video_library.get_video(video_id).flag:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            self._video_library.get_video(video_id).update_flag(False, "")
            print("Successfully removed flag from video: " + self._video_library.get_video(video_id).title)
