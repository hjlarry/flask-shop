import * as type from './mutation-types';
const mutations = {
  [type.SET_MPVUEINFO](state, mpvueInfo) { // eslint-disable-line
    state.mpvueInfo = mpvueInfo;
  },
  [type.SET_TOKEN](state, token) { // eslint-disable-line
    state.token = token;
  }
}

export default mutations;
