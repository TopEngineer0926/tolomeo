import axios from 'axios';
import authHeader from './authHeader';
const API_URL = process.env.REACT_APP_API_URL;
class AdminService {

  //Login
  login(data) {
    return axios.post(API_URL + 'login', data, {});
  }

  getEvidences(limit, page, only_keywords_found, query) {
    return axios.get(API_URL + 'evidences?limit=' + limit + '&page=' + page + '&only_keywords_found=' + only_keywords_found + '&query=' + query, { headers: authHeader() });
  }

  getCharts(limit, page) {
    return axios.get(API_URL + 'map?limit=' + limit + '&page=' + page, { headers: authHeader() });
  }

  getCrawl(data) {
    return axios.post(API_URL + 'crawl', data, { headers: authHeader() });
  }
}

export default new AdminService();