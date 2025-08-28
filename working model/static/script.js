function checkClickbait() {
  const headline = document.getElementById("headline").value;
  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ headline: headline })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("result").innerText = "Result: " + data.result;
  });
}
