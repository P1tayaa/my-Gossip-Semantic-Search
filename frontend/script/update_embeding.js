async function fetchAndUpdate() {
  const fetchButton = document.getElementById("fetchButton");

  fetchButton.textContent = "Fetching...";
  fetchButton.classList.add("loading");
  fetchButton.classList.remove("completed");

  try {
    const response = await fetch("/api/update_dataset");
    const data = await response.json();

    document.getElementById("searchInput").value = data.title;

    fetchButton.textContent = "Fetch Completed";
    fetchButton.classList.remove("loading");
    fetchButton.classList.add("completed");
  } catch (error) {
    alert("An error occurred while fetching data.");
    fetchButton.textContent = "Fetch Failed";
  }
}
