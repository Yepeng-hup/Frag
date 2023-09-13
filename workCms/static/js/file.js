window.onload = function () {
    var fileInput = document.getElementById('files');
    var info = document.getElementById('files-info');

    fileInput.addEventListener('change', function () {
        if (!fileInput.value) {
            info.innerHTML = '没有选择文件!';
            return;
        }
        var file = fileInput.files;
        if (file.length > 3) {
            window.location = '/push';
            alert('上传文件数量过大！')
        }
        for (var i = 0; i <= file.length; i++) {
            info.innerHTML += '<div>' + '文件: ' + file[i].name + '<br>' +
                '大小: ' + formatSize(file[i].size) + '<br>' +
                '修改: ' + file[i].lastModifiedDate + '</div>' + '<hr>';
        }
    });
};

function formatSize(size) {
    if (size > 1024 && size <= 1048576) {
        return Math.floor(size / 1024) + 'KB';
    } else if (size > 1048576) {
        return Math.floor(size / 1024 / 1024) + 'MB';
    }
};