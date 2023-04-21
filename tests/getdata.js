fetch('http://127.0.0.1:5000/api/search/?q=the+nice+guys')
.then(res => res.json())
.then(data=> console.log(data))