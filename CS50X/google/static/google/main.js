function play_audio(a) {
    let audio = document.createElement('AUDIO');
    audio.src = "./" + a.textContent + ".mp3";
    audio.load();
    audio.play();
}
document.addEventListener('keyup', (event) => {
    const kbd = document.querySelectorAll('kbd');
    for (let i = 0; i < 12; i++) {
        if (kbd[i].textContent === event.key.toUpperCase()) {
            play_audio(kbd[i]); break;
        }
    }
});