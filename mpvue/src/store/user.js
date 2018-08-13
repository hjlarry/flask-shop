const user = {
    state: {
        token: '',
        name: '',
        avatar: '',
        auth_type: '',
        cart_num: 0
    },

    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
        },
        SET_CART_NUM: (state, num) => {
            state.cart_num = num
        }
    },

    actions: {
        SetToken({commit}, token) {
            return new Promise(resolve => {
                commit('SET_TOKEN', token)
                resolve()
            })
        },
        SetCartNum({commit}, num) {
            return new Promise(resolve => {
                commit('SET_CART_NUM', num)
                resolve()
            })
        }
    }
}

export default user
