const imgBoxEl = document.getElementById("imgBox")
imgBoxEl.style.width = imgBoxEl.children.length * 400 + 'px'
PetiteVue.createApp({
    index: 0,
    left: 0,
    timer: null,
    count: imgBoxEl.children.length,
    $delimiters: ['[[', ']]'],
    prev() {
        this.index--;
        if (this.index < 0) {
            this.index = this.count - 1;
            this.left = -400 * this.count;
        }
        this.left += 400;
    },
    next() {
        this.index++;
        if (this.index > this.count - 1) {
            this.index = 0;
            this.left = 0;
        } else {
            this.left -= 400;
        }

    },
    autoPlay() {
        this.timer = setInterval(() => {
            this.next();
        }, 3000);
    },
    stopPlay() {
        clearInterval(this.timer);
    }
}).mount('#banner')