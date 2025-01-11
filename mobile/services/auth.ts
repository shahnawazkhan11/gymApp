const BASE_URL = 'http://10.0.2.2:8000/api';

export const authApi = {
  async login(email: string, password: string) {
    try {
      const response = await fetch(`${BASE_URL}/signin/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      // Log the response for debugging
      console.log('Login response:', response);

      if (!response.ok) {
        const text = await response.text(); // Get the response as text
        try {
          const data = JSON.parse(text); // Attempt to parse as JSON
          throw new Error(data.message || 'Login failed');
        } catch (jsonError) {
          throw new Error(text || 'Login failed'); // Fallback to text if JSON parsing fails
        }
      }

      return await response.json();
    } catch (error) {
      // Log the error for debugging
      console.error('Login error:', error);
      throw error;
    }
  },

  async signup(email: string, password: string, name: string) {
    try {
      const response = await fetch(`${BASE_URL}/signup/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Signup failed');
      }

      return await response.json();
    } catch (error) {
      throw error;
    }
  },
}; 