const copyButton = document.getElementById("copyTextButton");
const extractedText = document.getElementById("extractedText");

if (copyButton && extractedText) {
    const originalButtonText = copyButton.textContent.trim();

    copyButton.addEventListener("click", async function () {
        try {
            await navigator.clipboard.writeText(extractedText.textContent);
            copyButton.textContent = "已复制";
        } catch {
            copyButton.textContent = "复制失败";
        }

        window.setTimeout(() => {
            copyButton.textContent = originalButtonText;
        }, 2000);
    });
}
