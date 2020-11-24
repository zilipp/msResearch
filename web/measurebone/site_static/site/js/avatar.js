document.getElementById('avatar_form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById("myBtn").disabled = true;
    document.querySelector('#result_label').innerHTML = "Results";
    document.querySelector('#result_span').textContent = "processing...";
    let input = document.getElementById('id_avatar');

    let data = new FormData();
    data.append('file', input.files[0]);
    data.append('enctype', "multipart/form-data");
    data.append('title', "test.txt");
    console.log(data);

    fetch('http://127.0.0.1:8080/analysis/', {
        method: 'POST',
        headers: { },
        body: data
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
        document.querySelector('#result_span').textContent = data.results;
        document.getElementById("myBtn").disabled = false;
    }).catch((error) => {
        console.error('Error:', error);
    });
});