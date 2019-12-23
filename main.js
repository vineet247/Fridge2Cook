var t;
async function fun1()
{
  var apigClient = apigClientFactory.newClient();
  var time=document.getElementById('time').value;

  var r_choice=document.getElementById('r_choice').value;
 
  console.log("t = > " + t);
  var latit=t[0];
  var longi=t[1];
  console.log(latit + " " + longi);
  var params = { };
  var body = {time: time,r_choice:r_choice,lat:latit,lon:longi};
  var additionalParams = {headers: {
    'Content-Type':"application/json"
  }};
  apigClient.choicesPost(params, body, additionalParams).then(function(res){
    console.log(params);
    console.log(res);
  });
  

}

async function  getLocation()
{
  navigator.geolocation.getCurrentPosition(showPosition);
}
function showPosition(position) {
  t = [position.coords.latitude,position.coords.longitude];
}


function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    // reader.onload = () => resolve(reader.result)
    reader.onload = () => {
      let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });
}
function uploadPhoto()
{
  var file_data;
   // var file = document.querySelector('#file_path > input[type="file"]').files[0];
   var file = document.getElementById('fileToUpload').files[0];
   const reader = new FileReader();
   var file_data;
  //  var encoded_image = getBase64(file).then(
  //    data => {
  //    //console.log(data)
  //    var apigClient = apigClientFactory.newClient();

  //    // var data = document.getElementById('file_path').value;
  //    // var x = data.split("\\")
  //    // var filename = x[x.length-1]
  //    var file_type = file.type + ";base64"

  //    var body = file
  //    var params = {"key" : file.name, "bucket" : "test-photo-storage", "Content-Type" : file.type};
  //    var additionalParams = {
  //     // If there are any unmodeled query parameters or headers that must be
  //     //   sent with the request, add them here.
  //     headers: {
  //       "Content-Type" : file.type, 
  //       "ContentEncoding": "base64"
  //     }
  //   };
  //    apigClient.uploadBucketKeyPut(params, body , additionalParams).then(function(res){
  //      if (res.status == 200)
  //      {
  //        document.getElementById("uploadText").innerHTML = "Image Uploaded  !!!"
  //        document.getElementById("uploadText").style.display = "block";
  //      }
  //    })
  //  });

  let config = {
      headers: { 'Content-Type': file.type }
  };
  url = 'https://cors-anywhere.herokuapp.com/https://qka4q5sg75.execute-api.us-east-1.amazonaws.com/first/upload/cloud-project-fridge/' + file.name
  axios.put(url, file, config).then(response => {
      // console.log(response.data)
      alert("Image uploaded successfully!");
  });
}





 
  