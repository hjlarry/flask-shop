<template>
    <div class="container" @click="clickHandle('test click', $event)">

        <div class="userinfo" @click="bindViewTap">
            <div class="userinfo-avatar">
                <open-data type="userAvatarUrl"></open-data>
            </div>

            <div class="userinfo-nickname">
                <open-data type="userNickName"></open-data>
            </div>
        </div>

        <div class="usermotto">
            <div class="user-motto">
                <card :text="motto"></card>
            </div>
        </div>

        <form class="form-container">
            <input type="text" class="form-control" v-model="motto" placeholder="v-model"/>
            <input type="text" class="form-control" v-model.lazy="motto" placeholder="v-model.lazy"/>
        </form>
        <button :if="canIUse" open-type="getUserInfo" @click="bindGetUserInfo">授权登录</button>
    </div>
</template>

<script>
    import card from '@/components/card'
    import {mapMutations} from 'vuex'

    export default {
        data() {
            return {
                motto: 'Hello World',
                userInfo: {},
                token: '',
                canIUse: wx.canIUse('button.open-type.getUserInfo')
            }
        },

        components: {
            card
        },

        methods: {
            // ...mapMutations({
            //     setTokenVuex: 'SET_TOKEN'
            // }),
            bindViewTap() {
                const url = '../logs/main'
                wx.navigateTo({url})
            },
            getUserInfo() {
                wx.getSetting({
                    // withCredentials: true,
                    success: function (res) {
                        if (res.authSetting['scope.userInfo']) {
                            // 已经授权，可以直接调用 getUserInfo 获取头像昵称
                            wx.getUserInfo({
                                success: function (res) {
                                    console.log(res)
                                }
                            })
                        }
                    }
                })
            },
            clickHandle(msg, ev) {
                console.log('clickHandle:', msg, ev)
            },
            bindGetUserInfo: function (e) {
                console.log(e.detail.userInfo)
            },
            commitMpvueInfo() {
                let token = 'test token...'
                this.setTokenVuex(token);
            }
        },
        created() {
            // 调用应用实例的方法获取全局数据
            // this.getUserInfo()
        }
    }
</script>

<style scoped>
    .userinfo {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .userinfo-avatar {
        width: 128 rpx;
        height: 128 rpx;
        margin: 20 rpx;
        border-radius: 50%;
    }

    .userinfo-nickname {
        color: #aaa;
    }

    .usermotto {
        margin-top: 150px;
    }

    .form-control {
        display: block;
        padding: 0 12px;
        margin-bottom: 5px;
        border: 1px solid #ccc;
    }

    .counter {
        display: inline-block;
        margin: 10px auto;
        padding: 5px 10px;
        color: blue;
        border: 1px solid blue;
    }
</style>
