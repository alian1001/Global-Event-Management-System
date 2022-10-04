const canvas = document.getElementById("badge_result");
const preview = document.getElementById("submit");
preview.addEventListener("click", preview_badge);

canvas.height = canvas.width / 1.616;
const ctx = canvas.getContext("2d");
ctx.font = "20px Helvetica";

// const image = document.getElementById("file_image");
const logo = document.getElementById("logo");

function preview_badge(){
    let inFirstname = document.getElementById("firstname").value;
    let inLastname = document.getElementById("lastname").value;
    let inEmail = document.getElementById("email").value;

    const firstname_badge = document.getElementById("firstname");
    const lastname_badge = document.getElementById("lastname");
    const email_badge = document.getElementById("email");
    const image = document.getElementById("file_image");

    firstname_badge.innerHTML = inFirstname;
    lastname_badge.innerHTML = inLastname;
    email_badge.innerHTML = inEmail;

    ctx.fillStyle = "#159";
    ctx.rect(0, 0, 300, 56);
    ctx.fill();
    ctx.fillStyle = "#fff";
    ctx.fillText("Badge for Event", 10, 25);
    ctx.font = "16px Arial";
    ctx.fillText("Guest", 15, 45);
    ctx.fillStyle = "#000";
    ctx.fillText(firstname_badge.innerHTML, 110, 90);
    ctx.fillText(lastname_badge.innerHTML, 110, 115);
    ctx.fillText(email_badge.innerHTML, 110, 140);
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