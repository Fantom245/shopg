function copyToClipboard() {
    // Получаем чистый текст из элемента span
    const copyText = document.getElementById('copyText').textContent.trim(); // Убираем лишние пробелы

    navigator.clipboard.writeText(copyText)
        .then(() => {
            alert('Текст успішно скопійовано: ' + copyText);
        })
        .catch(err => {
            alert('Не вдалося скопіювати текст: ' + err);
        });
}
