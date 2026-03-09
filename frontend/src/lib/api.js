// Get the API base URL from Vite environment variables (set in render.yaml during build)
// Fallback to empty string for local development (which uses Vite's proxy)
export const API_BASE_URL = import.meta.env.VITE_API_URL || '';

export const apiFetch = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API call failed: ${response.statusText}`);
  }

  return response.json();
};
