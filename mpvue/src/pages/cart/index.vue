<template>
    <div class="page">
        <div class="page__bd">
            <div class="weui-panel weui-panel_access">
                <div class="weui-panel__bd">
                    <navigator v-for="(item,index) in contentList" :key="index"
                               class="weui-media-box weui-media-box_appmsg" hover-class="weui-cell_active"
                               :url=" '/pages/product-detail/main?id='+item.product_id">
                        <div class="weui-media-box__hd weui-media-box__hd_in-appmsg">
                            <image class="weui-media-box__thumb" :src="item.first_img"/>
                        </div>
                        <div class="weui-media-box__bd weui-media-box__bd_in-appmsg">
                            <div class="weui-media-box__title">{{item.title}}
                                <div class="right">x{{item.quantity}}</div>
                            </div>
                            <div class="weui-media-box__desc" v-if="item.variant">{{item.variant}}</div>
                            <div class="weui-media-box__desc">${{item.price}}</div>

                        </div>
                    </navigator>
                </div>


            </div>
        </div>
        <div class="page__operation">
                    <button class="weui-btn" type="primary" @click="">Checkout ${{totalAmount}}</button>
                </div>
    </div>
</template>

<script>
    import fly from '@/utils/index'

    export default {
        data() {
            return {
                contentList: []
            }
        },
        computed: {
            totalAmount: function () {
                let sum = 0
                for (let x of this.contentList) {
                    sum += x.price * x.quantity
                }
                return sum
            }
        },
        methods: {
            getCartData() {
                wx.showLoading({
                    title: 'Loading Data',
                    mask: true
                })
                fly.get('checkout/cart').then(res => {
                    wx.hideLoading()
                    this.contentList = res.data;
                })
            }
        },
        mounted() {
            this.getCartData()
        }
    }
</script>

<style>
</style>
