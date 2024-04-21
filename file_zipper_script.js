let dropBox = document.getElementById('dropBox');
let output = document.getElementById('output');
let button1 = document.getElementById('button1');
let button2 = document.getElementById('button2');
let button3 = document.getElementById('button3');

let uploadedFilesContent = new Map();

function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
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
            let fileName = files[i].name
            let fileType = files[i].type
            let fileSize = files[i].size

            let reader = new FileReader()

            reader.onload = function(e) {
                let base64String = arrayBufferToBase64(reader.result);
                let fileInfo = {
                    name: fileName,
                    type: fileType,
                    content: base64String,
                }
                uploadedFilesContent.set(fileName, fileInfo)
            }

            reader.onerror = function(e) {
                console.error("File could not be read: " + e.target.error)
            }

            reader.readAsArrayBuffer(files[i]);

            output.innerHTML += `${fileName} (${(fileSize / 1048576).toFixed(12)} MB)`
            if (i != files.length - 1)
                output.innerHTML += "<br>"
        }
    }
})

button1.addEventListener('click', function(e) {
    e.preventDefault();
    const filesArray = Array.from(uploadedFilesContent.values())
    fetch('http://127.0.0.1:5000/upload&zip', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filesArray),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

    let output = document.getElementById(`output`)

    if (output.innerHTML != "No files uploaded")
        output.innerHTML = "Files Uploaded!"
})

button2.addEventListener('click', function(e) {
    e.preventDefault();
    uploadedFilesContent.clear()
    output.innerHTML = "No files uploaded"
})

button3.addEventListener('click', function(e) {
    fetch('http://127.0.0.1:5000/download', {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const fileName = 'zipped_data.gz';
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    })
    .catch(error => console.error('Error:', error));

    let output = document.getElementById(`output`)

    if (output.innerHTML == "Files Uploaded!") {
        output.innerHTML = "No files uploaded"
        alert("Zipped data downloaded!")
    }
})
