import axios from "axios";
import parsedEnv from "../config/env";

const api = axios.create({
  baseURL: `${parsedEnv.VITE_API_BASE}${parsedEnv.VITE_API_PREFIX}`,
  withCredentials: true
});

export default api;