const API_URL = "https://reverse-imaging-similiarity-search.onrender.com";

export const searchImage = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  console.log("Sending request to:", API_URL);
  const response = await fetch(API_URL, {
    method: "POST",
    body: formData,
  });

  console.log("Response status:", response.status);
  const data = await response.json();
  console.log("Response data:", data);

  if (!response.ok) {
    throw new Error(`Search failed: ${data.detail || response.statusText}`);
  }
  return data;};