// 각 슬라이드의 제목 (head 태그의 <title>에서 직접 불러오도록 구현 가능)
const slideCount = 8;
let currentSlide = 1;

// 슬라이드 HTML 파일 경로
function getSlideFile(slideNum) {
    return `slide/${slideNum}.html`;
}

async function extractTitle(html) {
    const match = html.match(/<title>(.*?)<\/title>/i);
    return match ? match[1] : `슬라이드 ${currentSlide}`;
}

function extractBody(html) {
    const match = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
    return match ? match[1] : html;
}

async function loadSlide(slideNum) {
    try {
        const response = await fetch(getSlideFile(slideNum));
        if (!response.ok) throw new Error("슬라이드 파일을 불러올 수 없습니다.");
        const html = await response.text();
        extractTitle(html).then(title => {
            document.getElementById('slide-title').textContent = title;
        });
        document.getElementById('slide-container').innerHTML = extractBody(html);
        document.getElementById('slide-indicator').textContent = `${slideNum} / ${slideCount}`;
        document.getElementById('prev-btn').disabled = slideNum === 1;
        document.getElementById('next-btn').disabled = slideNum === slideCount;
    } catch (e) {
        document.getElementById('slide-container').innerHTML =
            `<div class="text-red-400 text-2xl text-center py-20">
            [${slideNum}.html] 파일을 불러올 수 없습니다.<br>
            <span style="font-size:1.2rem;">에러: ${e.message}</span><br>
            <span style="font-size:1rem;">경로/파일명/네트워크 오류를 확인하세요.</span>
            </div>`;
        document.getElementById('slide-title').textContent = "에러";
    }
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
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' && currentSlide > 1) {
        currentSlide--;
        loadSlide(currentSlide);
    } else if (e.key === 'ArrowRight' && currentSlide < slideCount) {
        currentSlide++;
        loadSlide(currentSlide);
    }
});
window.onload = () => loadSlide(currentSlide);
