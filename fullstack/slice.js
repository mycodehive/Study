// 각 슬라이드의 제목 (head 태그의 <title>에서 직접 불러오도록 구현 가능)
const slideCount = 8;
let currentSlide = 1;

// 슬라이드 HTML 파일 경로
function getSlideFile(slideNum) {
    return `${slideNum}.html`;
}

// slideNum의 <title> 추출
async function extractTitle(html) {
    const match = html.match(/<title>(.*?)<\/title>/i);
    return match ? match[1] : `슬라이드 ${currentSlide}`;
}

// <body> 내용만 추출
function extractBody(html) {
    const match = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    return match ? match[1] : html;
}

async function loadSlide(slideNum) {
    const response = await fetch(getSlideFile(slideNum));
    const html = await response.text();

    // 제목 표시 (head > title에서 추출)
    extractTitle(html).then(title => {
        document.getElementById('slide-title').textContent = title;
    });

    // body 내용 표시
    document.getElementById('slide-container').innerHTML = extractBody(html);

    // 페이지 인디케이터
    document.getElementById('slide-indicator').textContent = `${slideNum} / ${slideCount}`;

    // 버튼 활성/비활성
    document.getElementById('prev-btn').disabled = slideNum === 1;
    document.getElementById('next-btn').disabled = slideNum === slideCount;
}

document.getElementById('prev-btn').addEventListener('click', () => {
    if (currentSlide > 1) {
        currentSlide--;
        loadSlide(currentSlide);
    }
});
document.getElementById('next-btn').addEventListener('click', () => {
    if (currentSlide < slideCount) {
        currentSlide++;
        loadSlide(currentSlide);
    }
});

// 키보드 방향키로 넘기기
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' && currentSlide > 1) {
        currentSlide--;
        loadSlide(currentSlide);
    } else if (e.key === 'ArrowRight' && currentSlide < slideCount) {
        currentSlide++;
        loadSlide(currentSlide);
    }
});

// 첫 슬라이드 로드
window.onload = () => loadSlide(currentSlide);
