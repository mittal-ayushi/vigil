let alert = 0;
let burst = 0;

function fmtTime(unixSeconds) {
  return new Date(unixSeconds * 1000).toLocaleTimeString();
}

function resetFeed() {
  document.getElementById("feedBody").innerHTML = "";
  alert = 0;
  burst = 0;

  document.getElementById("alert").textContent = 0;
  document.getElementById("burst").textContent = 0;
}
