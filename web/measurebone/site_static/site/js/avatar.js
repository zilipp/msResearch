let userToken;

document.getElementById('avatar_form').addEventListener('submit', function(event) {
    event.preventDefault();
    let input = document.getElementById('id_avatar');

    let data = new FormData();
    data.append('avatar', input.files[0]);

    fetch('http://127.0.0.1:8080/analysis/', {
        method: 'POST',
        headers: {
            // 'Authorization': `Token ${userToken}`
        },
        body: data
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
    }).catch((error) => {
        console.error('Error:', error);
    });
});