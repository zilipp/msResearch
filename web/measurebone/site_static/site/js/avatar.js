document.getElementById('avatar_form').addEventListener('submit', function(event) {
    event.preventDefault();
    // document.getElementById("myBtn").disabled = true;
    document.querySelector('#result_h1').innerHTML = "Results";
    document.querySelector('#result_span').textContent = "processing...";
    let input_obj = document.getElementById('id_obj');
    let input_mtl = document.getElementById('id_mtl');
    let input_type = document.getElementById('id_type');

    let data = new FormData();
    data.append('file', input_obj.files[0]);
    data.append('mtl', input_mtl.files[0]);
    data.append('bone_type', input_type.value);
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
        // document.getElementById("myBtn").disabled = false;
    }).catch((error) => {
        console.error('Error:', error);
    });
});