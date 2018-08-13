import Vue from 'vue'
import App from './App'
import store from './store'
import './css/app.css'
import '../static/weui.css'
import 'animate.css'

Vue.config.productionTip = false
App.mpType = 'app'
Vue.prototype.$store = store

const app = new Vue(App)
app.$mount()

export default {
    // 这个字段走 app.json
    config: {
        // 页面前带有 ^ 符号的，会被编译成首页，其他页面可以选填，我们会自动把 webpack entry 里面的入口页面加进去
        pages: ['pages/logs/main', '^pages/index/main',
            'pages/product-list/main', 'pages/cart/main', 'pages/account/main', 'pages/product-detail/main'],
        window: {
            backgroundTextStyle: 'light',
            navigationBarBackgroundColor: '#fff',
            navigationBarTitleText: 'WeChat',
            navigationBarTextStyle: 'black'
        },
        tabBar: {
            color: '#999999',
            selectedColor: '#1AAD16',
            backgroundColor: '#ffffff',
            borderStyle: 'white',
            /* eslint-disable */
            list: [{
                pagePath: 'pages/index/main',
                text: 'Home',
                iconPath: 'static/images/nav_home.png',
                selectedIconPath: 'static/images/nav_home_sel.png'
            },
                {
                    pagePath: 'pages/product-list/main',
                    text: 'Product',
                    iconPath: 'static/images/nav_type.png',
                    selectedIconPath: 'static/images/nav_type_sel.png'
                },
                {
                    pagePath: 'pages/cart/main',
                    text: 'Cart',
                    iconPath: 'static/images/nav_cart.png',
                    selectedIconPath: 'static/images/nav_cart_sel.png'
                },
                {
                    pagePath: 'pages/account/main',
                    text: 'Me',
                    iconPath: 'static/images/nav_me.png',
                    selectedIconPath: 'static/images/nav_me_sel.png'
                }
            ]
            /* eslint-enable */
        }
    }
}
