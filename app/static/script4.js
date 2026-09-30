
// GUMB
function buttonAction() {

    let pressStartTime = 0;
    const button = document.getElementById("action");

    button.addEventListener("mousedown", () => {
        pressStartTime = Date.now();
        button.classList.add("glow");
    });

    button.addEventListener("mouseup", () => {
        button.classList.remove("glow");
        const pressDuration = Date.now() - pressStartTime;
        if (pressDuration >= 2000) {
            createPost();
        } else {
            window.location.href = "/static/add.html";
        }
    });
}

//POST
let posts = [];
let currentIndex = 0;

async function createPost() {
    const postText = document.getElementById('post-input').value;
    const neededCount = document.getElementById('needed-input').value;

    if (!postText || !neededCount) {
        document.getElementById('message').hidden = false;
    }

    const response = await fetch(`/posts/create?post=${encodeURIComponent(postText)}&needed=${encodeURIComponent(neededCount)}`, {
        method: "POST",
        credentials: "include"
    });

    if (response.status === 401) {
        window.location.href = "/static/index.html";
    }

    const data = await response.json();

    if (data.success) {
        window.location.href = "/static/you.html";
    } else {
        document.getElementById('message').hidden = false;
        console.log("Errorefoejfoej");
    }

}

async function loadPosts() {
    const response = await fetch("/posts/your?limit=100&offset=0", {
        credentials: "include"
    });

    if (response.status === 401) {
        window.location.href = "/static/index.html";
        return true;
    }

    posts = await response.json();
    currentIndex = 0;
    showPost();
}

function showPost() {
    if (posts.length === 0) {
        fitPostText();
        return;
    } else {
        document.getElementById("post").textContent = posts[currentIndex].post;
        document.getElementById("info").textContent = `${posts[currentIndex].joined}/${posts[currentIndex].needed}`;
        fitPostText();
    }
}

function nextPost() {
    currentIndex++;
    if (posts.length === 0){
        document.getElementById("post").textContent = "No your posts.";
    }
    if (currentIndex>=posts.length) {
        currentIndex = 0;
    }
    showPost();
}

async function joinPost() {
    const postId = posts[currentIndex].post_id;
    const response = await fetch(`/leave/${postId}`, {
        method: "POST",
        credentials: "include"
    });
    const data = await response.json();
    if (data.success) {
        posts[currentIndex].joined = data.joined;
        showPost();
    }
}


//SVE AI GENERIRANO, POTREBNA PROVJERA

function fitPostText() {
    const post = document.getElementById('post');
    if (!post) return;

    const row = post.parentElement;
    const container = document.querySelector('.container');

    // Red se ne rasteže na visinu grid trake (align-items: center ga
    // centrira i skuplja prema sadržaju), pa row.clientHeight nije
    // pouzdan. Umjesto toga računamo stvarnu visinu 50%-tne trake
    // izravno iz visine containera.
    const rowHeight = container.clientHeight * 0.5;

    // Prije mjerenja resetiramo line-height na 'normal' kako bi svaka
    // veličina fonta koristila svoj prirodni razmak redaka.
    post.style.lineHeight = 'normal';

    // FAZA 1: binarna pretraga najveće veličine fonta pri kojoj sadržaj
    // retka (bold tekst + brojač), uz normalan line-height, još uvijek
    // stane u dostupnu visinu retka. Ovime se fiksira broj redaka teksta.
    let fMin = 6;
    let fMax = 200;
    let bestFont = fMin;

    for (let i = 0; i < 25; i++) {
        const mid = (fMin + fMax) / 2;
        post.style.fontSize = mid + 'px';

        if (row.scrollHeight <= rowHeight) {
            bestFont = mid;
            fMin = mid;
        } else {
            fMax = mid;
        }
    }

    post.style.fontSize = bestFont + 'px';
    post.style.lineHeight = 'normal';

    // FAZA 2: budući da promjena veličine fonta može ostaviti neiskorišten
    // prostor (jer prijelom u retke skače diskretno), sada finim
    // podešavanjem line-heighta (koji NE mijenja prijelom redaka) točno
    // popunjavamo preostali prostor do ruba retka.
    let naturalLH = parseFloat(getComputedStyle(post).lineHeight);
    if (isNaN(naturalLH)) {
        naturalLH = bestFont * 1.2;
    }

    let lhMin = naturalLH;
    let lhMax = naturalLH * 4;
    let bestLH = naturalLH;

    for (let i = 0; i < 30; i++) {
        const mid = (lhMin + lhMax) / 2;
        post.style.lineHeight = mid + 'px';

        if (row.scrollHeight <= rowHeight) {
            bestLH = mid;
            lhMin = mid;
        } else {
            lhMax = mid;
        }
    }

    post.style.lineHeight = bestLH + 'px';
}


///
function fitInputText() {
    const textarea = document.getElementById('post-input');
    if (!textarea) return;

    const container = document.querySelector('.container');
    const maxHeight = container.clientHeight * 0.50;

    const computedStyle = getComputedStyle(textarea);

    const measurer = document.createElement('div');
    measurer.style.position = 'absolute';
    measurer.style.visibility = 'hidden';
    measurer.style.width = (textarea.clientWidth) + 'px';
    measurer.style.whiteSpace = 'pre-wrap';
    measurer.style.wordWrap = 'break-word';
    measurer.style.boxSizing = computedStyle.boxSizing;
    measurer.style.paddingTop = computedStyle.paddingTop;
    measurer.style.paddingBottom = computedStyle.paddingBottom;
    measurer.style.paddingLeft = computedStyle.paddingLeft;
    measurer.style.paddingRight = computedStyle.paddingRight;
    measurer.style.borderWidth = computedStyle.borderWidth;
    measurer.style.borderStyle = 'solid';
    measurer.style.fontFamily = computedStyle.fontFamily;
    measurer.style.fontWeight = computedStyle.fontWeight;
    document.body.appendChild(measurer);

    measurer.textContent = textarea.value || textarea.placeholder;

    let fMin = 6;
    let fMax = 200;
    let bestFont = fMin;

    for (let i = 0; i < 25; i++) {
        const mid = (fMin + fMax) / 2;
        measurer.style.fontSize = mid + 'px';
        measurer.style.lineHeight = 'normal';

        if (measurer.scrollHeight <= maxHeight) {
            bestFont = mid;
            fMin = mid;
        } else {
            fMax = mid;
        }
    }

    document.body.removeChild(measurer);

    textarea.style.fontSize = (bestFont * 0.88) + 'px';
    textarea.style.lineHeight = 'normal';
}

function initInputText() {
    const textarea = document.getElementById('post-input');
    if (!textarea) return;
    
    const placeholderText = textarea.placeholder;
    textarea.value = placeholderText;
    fitInputText();
    textarea.value = '';
}

///


window.addEventListener('load', loadPosts);

window.addEventListener('resize', fitPostText);

buttonAction();

window.addEventListener('load', initInputText);
document.getElementById('post-input').addEventListener('input', fitInputText);
window.addEventListener('resize', fitInputText);

///how to register pressing enter so text resizes