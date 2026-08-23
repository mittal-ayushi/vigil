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

function renderEntry(entry) {
  const tbody = document.getElementById("feedBody");
  const row = document.createElement("tr");

  const timeCell = document.createElement("td");
  timeCell.textContent = fmtTime(entry.time);
  row.appendChild(timeCell);

  const typeCell = document.createElement("td");
  typeCell.textContent =
    entry.type === "burst" ? "BURST" : "ALERT";
  row.appendChild(typeCell);

  const ruleCell = document.createElement("td");
  ruleCell.textContent = entry.rule;
  row.appendChild(ruleCell);

  const detailCell = document.createElement("td");

  if (entry.type === "burst") {
    detailCell.textContent =
      entry.count + " hits in " + entry.window + "s";
    burst++;
  } else {
    detailCell.textContent =
      entry.syscall + "(" + entry.args + ") = " + entry.retval;
    alert++;
  }

  row.appendChild(detailCell);

  tbody.insertBefore(row, tbody.firstChild);

  document.getElementById("alert").textContent = alert;
  document.getElementById("burst").textContent = burst;
}