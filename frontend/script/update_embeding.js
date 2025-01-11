async function fetchAndUpdate() {
  const fetchButton = document.getElementById("fetchButton");

  // Change button to "loading" state
  fetchButton.textContent = "Fetching...";
  fetchButton.classList.add("loading");
  fetchButton.classList.remove("completed");

  try {
    // Simulating a GET request with a placeholder API
    const response = await fetch("/api/update_dataset");
    const data = await response.json();

    // Update the search input field with fetched value
    document.getElementById("searchInput").value = data.title;

    // Change button to "completed" state
    fetchButton.textContent = "Fetch Completed";
    fetchButton.classList.remove("loading");
    fetchButton.classList.add("completed");
  } catch (error) {
    alert("An error occurred while fetching data.");
    fetchButton.textContent = "Fetch Failed";
  }
}
