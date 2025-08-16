// create axios instance with default settings
import axios from 'axios';

const VITE_API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: VITE_API_URL,
  withCredentials: true,
});

export default axiosInstance;
