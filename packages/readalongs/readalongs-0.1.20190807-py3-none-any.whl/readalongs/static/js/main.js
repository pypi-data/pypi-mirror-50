var file_socket = io.connect('http://' + document.domain + ':' + location.port + '/file');

function removeFile(path) {
    let host_path = path[0]['path'];
    file_socket.emit('remove event', { data: { 'path_to_remove': host_path } })
}

file_socket.on('remove response', function (msg) {
    let element = document.getElementById(msg['data']['removed_file'])
    element.parentNode.removeChild(element)
})

