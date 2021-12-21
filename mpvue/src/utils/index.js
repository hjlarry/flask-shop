import Fly from 'flyio/dist/npm/wx';
import store from '../store'

var fly = new Fly();
fly.config.timeout = 10000;
fly.config.baseURL = "http://127.0.0.1:5000/api/v1/"

fly.interceptors.request.use((request) => {
    request.headers["Authorization"] = store.getters.token;
    return request;
})


function formatNumber(n) {
    const str = n.toString()
    return str[1] ? str : `0${str}`
}

export function formatTime(date) {
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()

    const hour = date.getHours()
    const minute = date.getMinutes()
    const second = date.getSeconds()

    const t1 = [year, month, day].map(formatNumber).join('/')
    const t2 = [hour, minute, second].map(formatNumber).join(':')

    return `${t1} ${t2}`
}

export function setTabBarBadge() {
    if (store.getters.cart_num > 0) {
        wx.setTabBarBadge({
            index: 2,
            text: store.getters.cart_num.toString()
        })
    }
}

export default fly
