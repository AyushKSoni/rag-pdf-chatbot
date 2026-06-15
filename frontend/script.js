async function ask() {
  let query = document.getElementById("query").value;
  if (!query) {
    alert("Please enter a query");
    return;
  }
  let chatbox = document.getElementById("chatbox");
  // Display user query
  chatbox.innerHTML += `<div class="user-message">${query}</div>`;

  try {
    let res = await fetch(
      "http://127.0.0.1:8000/ask?query=" + encodeURIComponent(query),
    );
    let data = await res.json();

    if (data.answer) {
      chatbox.innerHTML += `<div class="bot-message">${data.answer}</div>`;
    } else {z
      chatbox.innerHTML += `<div class="bot-message">Sorry, I couldn't find an answer. ${data.error}</div>`;
    }
  } catch (err) {
    console.error(err);
    chatbox.innerHTML += `<div class="bot-message">An Server error occurred while fetching the answer.</div>`;
  }
  chatbox.scrollTop = chatbox.scrollHeight;
  document.getElementById("query").value = "";
}

document.getElementById("query").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    ask();
  }
});
