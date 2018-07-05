var entries;

var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function(){
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
        entries = xmlhttp.response;
        console.log(entries);
    }
}
xmlhttp.responseType = 'json';
xmlhttp.open("GET", "http://127.0.0.1:3000/api/v1.0/entries", true);
xmlhttp.send();

