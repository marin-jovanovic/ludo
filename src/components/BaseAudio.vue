<template>
  <div>
    <button @click="playMusic">Play Music</button>
    <button @click="pauseMusic">Pause Music</button>
    <button @click="stopMusic">Stop Music</button>
    <select v-model="selectedSong" @change="playMusic">
      <option v-for="song in songs" :key="song.id" :value="song.url">
        {{ song.title }}
      </option>
    </select>
  </div>
</template>
  
  <script>
export default {
  name: "MusicPlayer",
  data() {
    return {
      selectedSong: null,
      audioElement: null,
      songs: [
        { id: 1, title: "Song Corruption", url: "mp3/Corruption.mp3" },
        { id: 2, title: "Song 2", url: ".mp3" },
        { id: 3, title: "Song 3", url: ".mp3" },
      ],
    };
  },
  methods: {
    playMusic() {
      if (!this.audioElement) {
        this.audioElement = new Audio(this.selectedSong || this.songs[0].url);
      }
      this.audioElement.play();
    },
    pauseMusic() {
      if (this.audioElement) {
        this.audioElement.pause();
      }
    },
    stopMusic() {
      if (this.audioElement) {
        this.audioElement.pause();
        this.audioElement.currentTime = 0;
      }
    },
  },
};
</script>
  