const canvas = document.getElementById("badgegen");
const preview = document.getElementById("submit");
preview.addEventListener("click", preview_badge);

canvas.height = canvas.width / 1.616;
const ctx = canvas.getContext("2d");
ctx.font = "20px Helvetica";

const image = document.getElementById("file_image");
const logo = document.getElementById("logo");

function preview_badge(){

    let fullname = document.getElementById("firstname").value + " " + document.getElementById("lastname").value;
    let email = document.getElementById("email").value;
    let diet = "Dietary Req: " + document.getElementById("diet").value;
    let phone = document.getElementById("phone").value
    let file_image = document.getElementById("file_image").value;

    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = "#159";
    ctx.rect(0, 0, 300, 56);
    ctx.fill();
    ctx.fillStyle = "white";
    ctx.font = "bold 16px Arial";
    ctx.fillText("Badge for Event", 10, 25);
    ctx.fillText("G.E.M.S", 230, 35);
    ctx.fillText("Guest", 15, 45);
    ctx.font = "16px Arial";


    ctx.fillStyle = "black";
    ctx.fillText(fullname, 110, 90);
    ctx.fillText(email, 110, 115);
    ctx.fillText(diet, 110, 140);
    ctx.fillText(phone, 110, 165)
    ctx.drawImage(image, 10, 65, 80, 110);
}

function loadImage(event) {
  const image = document.getElementById("file_image");
  image.src = URL.createObjectURL(event.target.files[0]);
}

const download = document.getElementById("submit");
download.addEventListener("click", function(){

  if(window.navigator.msSaveBlob) {

    window.navigator.msSaveBlob(canvas.msToBlob(), "badge.png");
  } else {

    const a = document.createElement("a");
    document.body.appendChild(a);
    a.href = canvas.toDataURL();
    a.download = "badge.png";
    a.click();
    document.body.removeChild(a);
  }
});