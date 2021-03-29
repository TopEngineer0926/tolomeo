import axios from 'axios';
import authHeader from './authHeader';
const API_URL = process.env.REACT_APP_API_URL;
class AdminService {

  //Login
  login(data) {
    return axios.post(API_URL + 'login', data, {});
  }

  getEvidences(data) {
    return axios.get(API_URL + 'evidences?limit=' + data.limit + '&page=' + data.page + '&only_keywords_found=' + data.only_keywords_found + '&query=' + data.query, { headers: authHeader() });
  }

  getCharts(limit, page) {
    return axios.get(API_URL + 'map?limit=' + limit + '&page=' + page, { headers: authHeader() });
  }

  getCrawl(data) {
    return axios.post(API_URL + 'crawl', data, { headers: authHeader() });
  }
}

export default new AdminService();