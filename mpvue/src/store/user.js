const user = {
    state: {
        token: '',
        name: '',
        avatar: '',
        auth_type: ''
    },

    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
        }
    },

    actions: {
        SetToken({commit}, token) {
            return new Promise(resolve => {
                commit('SET_TOKEN', token)
                resolve()
            })
        }
    }
}

export default user
