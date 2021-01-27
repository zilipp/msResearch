document.getElementById('avatar_form').addEventListener('submit', function(event) {
    event.preventDefault();
    document.getElementById("myBtn").disabled = true;
    // document.querySelector('#result_h1').innerHTML = "Results";
    // document.querySelector('#result_span').textContent = "processing...";
    let input_obj = document.getElementById('id_obj');
    let input_type = document.getElementById('id_type');

    let data = new FormData();
    data.append('file', input_obj.files[0]);
    data.append('bone_type', input_type.value);
    data.append('enctype', "multipart/form-data");
    data.append('title', "test.txt");
    console.log(data);

    // show on window
    // fetch('http://127.0.0.1:8080/analysis/', {
    //     method: 'POST',
    //     headers: { },
    //     body: data
    // }).then(response => {
    //     return response.text();
    // }).then(data => {
    //     console.log(data);
    //     document.querySelector('#result_span').textContent = data.results;
    //     // document.getElementById("myBtn").disabled = false;
    // }).catch((error) => {
    //     console.error('Error:', error);
    // });

    let url = window.location.href + 'analysis/'
    // let url = 'http://127.0.0.1:8000/analysis/'
    fetch(url, {
        method: 'POST',
        headers: { },
        body: data,
        responseType: 'blob'
    }).then(response => response.blob())
    .then(blob => {
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = input_type.value + ".csv";
        document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        a.click();
        a.remove();  //afterwards we remove the element again
        document.getElementById("myBtn").disabled = false;
    });
});