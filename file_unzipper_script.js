let dropBox = document.getElementById('dropBox');
let output = document.getElementById('output');
let button1 = document.getElementById('button1');
let button2 = document.getElementById('button2');
let button3 = document.getElementById('button3');

let uploadedFilesContent = new Map();

let fileNameForDownload = ''
let fileTypeForDownload = ''
let fileContentForDownload = ''

function base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}

document.addEventListener('dragover', function(e) {
    e.preventDefault()
});

document.addEventListener('drop', function(e) {
    e.preventDefault();
    if (!dropBox.contains(e.target))
        window.alert('Please drop files only inside the designated area.');
});

dropBox.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropBox.classList.add("over")
    output.classList.add("over")
});

dropBox.addEventListener('dragleave', function(e) {
    dropBox.classList.remove("over")
});

dropBox.addEventListener('drop', function(e) {
    e.preventDefault();
    dropBox.classList.remove("over")

    let files = e.dataTransfer.files;

    if (files.length > 0) {
        let output = document.getElementById(`output`)

        if (output.innerHTML == "No files uploaded")
            output.innerHTML = ""
        else if (output.innerHTML == "Files Uploaded!")
            output.innerHTML = ""
        else 
            output.innerHTML += "<br>"

        for (let i = 0; i < files.length; i++) {
            let file = files[i]
            uploadedFilesContent.set(file.name, file)
            output.innerHTML += `${file.name} (${(file.size / 1048576).toFixed(12)} MB)`
            if (i !== files.length - 1)
                output.innerHTML += "<br>"
        }
    }
})

button1.addEventListener('click', function(e) {
    e.preventDefault();
    let formData = new FormData();
    uploadedFilesContent.forEach((content, name) => {
        formData.append('files', content, name);
    });

    fetch('http://127.0.0.1:5000/upload&unzip', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok')
        }
        return response.json()
    })
    .then(data => {
        if (data.status === "success" && data.files) {
            data.files.forEach(file => {
                fileNameForDownload = file.name
                fileTypeForDownload = file.type
                fileContentForDownload = base64ToArrayBuffer(file.content)
            })
        }
        else {
            console.error("Failed to process files or no files returned:", data)
        }
    })
    .catch(error => console.error('Error:', error))

    let output = document.getElementById('output')

    if (output.innerHTML !== "No files uploaded") {
        output.innerHTML = "Files Uploaded!"
    }
})

button2.addEventListener('click', function(e) {
    e.preventDefault();
    fileNameForDownload = ''
    fileTypeForDownload = ''
    fileContentForDownload = ''
    uploadedFilesContent.clear()
    output.innerHTML = "No files uploaded"
})

button3.addEventListener('click', function(e) {
    const blob = new Blob([fileContentForDownload], {type: fileTypeForDownload});

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = fileNameForDownload;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();

    fileNameForDownload = ''
    fileTypeForDownload = ''
    fileContentForDownload = ''
    uploadedFilesContent.clear()
    
    let output = document.getElementById(`output`)
    if (output.innerHTML == "Files Uploaded!") {
        output.innerHTML = "No files uploaded"
        alert("Zipped data downloaded!")
    }
})
