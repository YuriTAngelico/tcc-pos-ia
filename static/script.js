const video = document.getElementById('video')
const canvas = document.getElementById('canvas')
const canvas_post = document.getElementById('canvas_post')

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/models')
]).then(startVideo)

function startVideo() {
  navigator.getUserMedia(
    { video: {} },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

// video.addEventListener('play', async () => {

//   const displaySize = { width: video.width, height: video.height }
//   faceapi.matchDimensions(canvas, displaySize)

//   $("#info").html("Iniciando detecção de face da pessoa...")

//   setInterval(async () => {

//     const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks()

//     if (detections.length > 0 && detections[0].detection._classScore > 0.9) {

//       console.log(detections[0].detection._classScore)

//       $("#percentual_of_detection").html(parseFloat(detections[0].detection._classScore.toFixed(2)))

//       $("#card").removeClass("border-primary");
//       $("#card").addClass("border-success");

//       $("#info").html("Autenticando pessoa...")

//       //pega o canvas e transforma em imagem para mandar via POST
//       canvas_post.getContext('2d').drawImage(video, 0, 0, 640, 480);
//       let data_pixel = canvas_post.getContext('2d').getImageData(0, 0, 640, 480).data;

//       //chama o ajax para fazer a requisição POST
//       await $.ajax({
//         url: "http://localhost:8000/face_recognition/tests/receive-post",
//         type: 'post',
//         data: {
//           nome: "Yuri",
//           image: JSON.stringify(data_pixel)
//         },
//         beforeSend: function () {
//           $("#info").html("Face detectada, enviando requisição de entrada!")
//         },
//       })
//         .done(function (data, textStatus, jqXHR) {
//           console.log(data, textStatus);
//         })
//         .fail(function (jqXHR, textStatus, errorThrown) {
//           console.log("Erro -->", errorThrown);
//         });
//     }

//     else {
//       $("#card").removeClass("border-success");
//       $("#card").addClass("border-primary");
//     }
//     const resizedDetections = faceapi.resizeResults(detections, displaySize)
//     canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
//     faceapi.draw.drawDetections(canvas, resizedDetections)
//   }, 250);
// });

function liberar_pessoa() {
  "use strict";

  const displaySize = { width: video.width, height: video.height };
  faceapi.matchDimensions(canvas, displaySize);

  $("#info").html("Iniciando detecção de face da pessoa...")

  let detected = false;

  const intervalId = setInterval(async () => {

    let detections;

    if (!detected){
      detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks()
      const resizedDetections = faceapi.resizeResults(detections, displaySize)
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
      faceapi.draw.drawDetections(canvas, resizedDetections)
    }

    if (detections.length > 0 && detections[0].detection._classScore > 0.85) {

      $("#percentual_of_detection").html(parseFloat(detections[0].detection._classScore.toFixed(2)))
      $("#card").removeClass("border-primary");
      $("#card").addClass("border-success");

      //pega o canvas e transforma em imagem para mandar via POST
      canvas_post.getContext('2d').drawImage(video, 0, 0, 640, 480);
      let data_pixel = canvas_post.getContext('2d').getImageData(0, 0, 640, 480).data;

      //chama o ajax para fazer a requisição POST
      await $.ajax({
        url: "/face_recognition/tests/receive-post",
        type: 'post',
        data: {
          nome: "Yuri",
          image: JSON.stringify(data_pixel)
        },
        beforeSend: function () {
          $("#info").html("Face detectada, enviando requisição de entrada!");
          detected = true;
        },
      })
        .done(function (data, textStatus, jqXHR) {
          clearInterval(intervalId);
          canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
          console.log(data, textStatus);
          $("#info").html(data);
        })
        .fail(function (jqXHR, textStatus, errorThrown) {
          console.log("Erro -->", errorThrown);
        });

    } else {
      $("#card").removeClass("border-success");
      $("#card").addClass("border-primary");
    }
  }, 250);

  console.log("Sai do set interval...")
}